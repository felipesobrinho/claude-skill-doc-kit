#!/usr/bin/env python3
"""Spec JSON -> BPMN 2.0 (com diagrama DI) que abre no Camunda Modeler, bpmn.io e draw.io.

Uso:
    python3 bpmn_from_spec.py spec.json -o processo.bpmn

Formato da spec: veja templates/bpmn-spec.json.
- lanes: raias (papéis ou sistemas), de cima para baixo
- nodes: id, type, lane, row (coluna no fluxo), label, hu (opcional), mark (opcional: "pain:1" ou "gain:2")
- flows: from, to, label (opcional)
"""
from __future__ import annotations

import argparse
import json
import sys
from xml.sax.saxutils import escape

TYPES = {
    "start": ("startEvent", None),
    "start-msg": ("startEvent", "messageEventDefinition"),
    "start-timer": ("startEvent", "timerEventDefinition"),
    "end": ("endEvent", None),
    "end-msg": ("endEvent", "messageEventDefinition"),
    "timer": ("intermediateCatchEvent", "timerEventDefinition"),
    "msgcatch": ("intermediateCatchEvent", "messageEventDefinition"),
    "task": ("task", None),
    "user": ("userTask", None),
    "service": ("serviceTask", None),
    "send": ("sendTask", None),
    "receive": ("receiveTask", None),
    "manual": ("manualTask", None),
    "script": ("scriptTask", None),
    "xor": ("exclusiveGateway", None),
    "and": ("parallelGateway", None),
}

LANE_H, LABEL_W, COL_W, POOL_X, POOL_Y = 150, 30, 170, 160, 80


class SpecError(ValueError):
    pass


def validate(spec: dict) -> list[str]:
    """Erros estruturais da spec (lista vazia = ok)."""
    errors: list[str] = []
    lanes = {l["id"] for l in spec.get("lanes", [])}
    nodes = spec.get("nodes", [])
    ids = [n["id"] for n in nodes]
    if not lanes:
        errors.append("spec sem raias (lanes)")
    if len(ids) != len(set(ids)):
        errors.append("ids de nós duplicados")
    cells = set()
    for n in nodes:
        if n.get("type") not in TYPES:
            errors.append(f"{n['id']}: tipo desconhecido '{n.get('type')}'")
        if n.get("lane") not in lanes:
            errors.append(f"{n['id']}: raia inexistente '{n.get('lane')}'")
        cell = (n.get("lane"), n.get("row"))
        if cell in cells:
            errors.append(f"{n['id']}: célula (raia, linha) {cell} já ocupada")
        cells.add(cell)
        if n.get("mark") and not str(n["mark"]).split(":")[0] in ("pain", "gain"):
            errors.append(f"{n['id']}: mark deve ser 'pain:N' ou 'gain:N'")
    idset = set(ids)
    incoming = {i: 0 for i in ids}
    outgoing = {i: 0 for i in ids}
    for f in spec.get("flows", []):
        if f["from"] not in idset or f["to"] not in idset:
            errors.append(f"fluxo {f['from']} -> {f['to']} aponta para nó inexistente")
            continue
        outgoing[f["from"]] += 1
        incoming[f["to"]] += 1
    for n in nodes:
        kind = TYPES.get(n.get("type"), ("",))[0]
        if kind == "startEvent" and outgoing[n["id"]] == 0:
            errors.append(f"{n['id']}: evento de início sem saída")
        if kind == "endEvent" and incoming[n["id"]] == 0:
            errors.append(f"{n['id']}: evento de fim sem entrada")
        if kind not in ("startEvent", "endEvent") and (incoming[n["id"]] == 0 or outgoing[n["id"]] == 0):
            errors.append(f"{n['id']}: nó solto (precisa de entrada e saída)")
    if not any(TYPES.get(n.get("type"), ("",))[0] == "startEvent" for n in nodes):
        errors.append("processo sem evento de início")
    if not any(TYPES.get(n.get("type"), ("",))[0] == "endEvent" for n in nodes):
        errors.append("processo sem evento de fim")
    return errors


def size(kind: str) -> tuple[int, int]:
    if kind.endswith("Event"):
        return 36, 36
    if kind.endswith("Gateway"):
        return 50, 50
    return 120, 80


def label_of(n: dict) -> str:
    label = n.get("label", "")
    mark = n.get("mark")
    if mark:
        kind, num = str(mark).split(":")
        label += f" ({'D' if kind == 'pain' else 'G'}{num})"
    return label


def build(spec: dict) -> str:
    errors = validate(spec)
    if errors:
        raise SpecError("; ".join(errors))

    pid = spec["id"]
    lanes = spec["lanes"]
    nodes = spec["nodes"]
    flows = [{**f, "id": f"Flow_{i + 1}"} for i, f in enumerate(spec["flows"])]
    lane_index = {l["id"]: i for i, l in enumerate(lanes)}
    max_row = max(n["row"] for n in nodes)
    pool_w = LABEL_W + 60 + (max_row + 1) * COL_W
    pool_h = LANE_H * len(lanes)

    geo = {}
    for n in nodes:
        kind, _ = TYPES[n["type"]]
        w, h = size(kind)
        cx = POOL_X + LABEL_W + 60 + n["row"] * COL_W + 40
        cy = POOL_Y + lane_index[n["lane"]] * LANE_H + LANE_H / 2
        geo[n["id"]] = (cx - w / 2, cy - h / 2, w, h, kind)

    def anchor(nid: str, side: str) -> tuple[float, float]:
        x, y, w, h, _ = geo[nid]
        return {"r": (x + w, y + h / 2), "l": (x, y + h / 2), "t": (x + w / 2, y), "b": (x + w / 2, y + h)}[side]

    def waypoints(f: dict) -> list[tuple[float, float]]:
        s, t = f["from"], f["to"]
        sx, sy, sw, sh, _ = geo[s]
        tx, ty, tw, th, _ = geo[t]
        same_lane = abs((sy + sh / 2) - (ty + th / 2)) < 1
        if same_lane and tx > sx:
            return [anchor(s, "r"), anchor(t, "l")]
        if tx > sx and geo[s][4].endswith("Gateway"):  # gateway: sai por cima/baixo e segue para a direita
            (x1, y1) = anchor(s, "b" if ty > sy else "t")
            (x2, y2) = anchor(t, "l")
            return [(x1, y1), (x1, y2), (x2, y2)]
        if tx > sx:  # tarefa/evento: muda de raia no corredor entre colunas, sem cruzar outras formas
            (x1, y1) = anchor(s, "r")
            (x2, y2) = anchor(t, "l")
            mid = POOL_X + LABEL_W + 60 + (round((x1 - POOL_X - LABEL_W - 60) / COL_W + 0.5)) * COL_W - 25
            mid = max(mid, x1 + 12)
            return [(x1, y1), (mid, y1), (mid, y2), (x2, y2)]
        if abs(tx - sx) < 1:  # mesma coluna, outra raia
            return [anchor(s, "b" if ty > sy else "t"), anchor(t, "t" if ty > sy else "b")]
        # volta (loop): sai por baixo, passa por baixo e entra por baixo
        (x1, y1) = anchor(s, "b")
        (x2, y2) = anchor(t, "b")
        low = max(y1, y2) + 30
        return [(x1, y1), (x1, low), (x2, low), (x2, y2)]

    inc = {n["id"]: [] for n in nodes}
    out = {n["id"]: [] for n in nodes}
    for f in flows:
        out[f["from"]].append(f["id"])
        inc[f["to"]].append(f["id"])

    p = []
    p.append('<?xml version="1.0" encoding="UTF-8"?>')
    p.append(
        '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
        'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
        'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
        f'id="Definitions_{pid}" targetNamespace="http://bpmn.io/schema/bpmn" exporter="doc-kit" exporterVersion="1.0">'
    )
    p.append(f'  <bpmn:collaboration id="Collaboration_{pid}">')
    p.append(f'    <bpmn:participant id="Participant_{pid}" name="{escape(spec.get("pool", spec.get("name", pid)))}" processRef="Process_{pid}" />')
    p.append("  </bpmn:collaboration>")
    p.append(f'  <bpmn:process id="Process_{pid}" name="{escape(spec.get("name", pid))}" isExecutable="false">')
    p.append(f'    <bpmn:laneSet id="LaneSet_{pid}">')
    for l in lanes:
        p.append(f'      <bpmn:lane id="Lane_{l["id"]}" name="{escape(l["name"])}">')
        for n in nodes:
            if n["lane"] == l["id"]:
                p.append(f"        <bpmn:flowNodeRef>{n['id']}</bpmn:flowNodeRef>")
        p.append("      </bpmn:lane>")
    p.append("    </bpmn:laneSet>")
    for n in nodes:
        kind, definition = TYPES[n["type"]]
        p.append(f'    <bpmn:{kind} id="{n["id"]}" name="{escape(label_of(n))}">')
        if n.get("hu"):
            p.append(f"      <bpmn:documentation>Histórias: {escape(', '.join(n['hu']))}</bpmn:documentation>")
        for fid in inc[n["id"]]:
            p.append(f"      <bpmn:incoming>{fid}</bpmn:incoming>")
        for fid in out[n["id"]]:
            p.append(f"      <bpmn:outgoing>{fid}</bpmn:outgoing>")
        if definition:
            p.append(f'      <bpmn:{definition} id="{n["id"]}_def" />')
        p.append(f"    </bpmn:{kind}>")
    for f in flows:
        name = f' name="{escape(f["label"])}"' if f.get("label") else ""
        p.append(f'    <bpmn:sequenceFlow id="{f["id"]}"{name} sourceRef="{f["from"]}" targetRef="{f["to"]}" />')
    p.append("  </bpmn:process>")

    p.append(f'  <bpmndi:BPMNDiagram id="Diagram_{pid}">')
    p.append(f'    <bpmndi:BPMNPlane id="Plane_{pid}" bpmnElement="Collaboration_{pid}">')
    p.append(f'      <bpmndi:BPMNShape id="Participant_{pid}_di" bpmnElement="Participant_{pid}" isHorizontal="true">')
    p.append(f'        <dc:Bounds x="{POOL_X}" y="{POOL_Y}" width="{pool_w}" height="{pool_h}" />')
    p.append("      </bpmndi:BPMNShape>")
    for i, l in enumerate(lanes):
        p.append(f'      <bpmndi:BPMNShape id="Lane_{l["id"]}_di" bpmnElement="Lane_{l["id"]}" isHorizontal="true">')
        p.append(f'        <dc:Bounds x="{POOL_X + LABEL_W}" y="{POOL_Y + i * LANE_H}" width="{pool_w - LABEL_W}" height="{LANE_H}" />')
        p.append("      </bpmndi:BPMNShape>")
    for n in nodes:
        x, y, w, h, kind = geo[n["id"]]
        marker = ' isMarkerVisible="true"' if kind == "exclusiveGateway" else ""
        p.append(f'      <bpmndi:BPMNShape id="{n["id"]}_di" bpmnElement="{n["id"]}"{marker}>')
        p.append(f'        <dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" />')
        if not kind.endswith("Task") and kind != "task":
            p.append(f'        <bpmndi:BPMNLabel><dc:Bounds x="{x + w / 2 - 50:.0f}" y="{y + h + 6:.0f}" width="100" height="27" /></bpmndi:BPMNLabel>')
        p.append("      </bpmndi:BPMNShape>")
    for f in flows:
        p.append(f'      <bpmndi:BPMNEdge id="{f["id"]}_di" bpmnElement="{f["id"]}">')
        for (wx, wy) in waypoints(f):
            p.append(f'        <di:waypoint x="{wx:.0f}" y="{wy:.0f}" />')
        p.append("      </bpmndi:BPMNEdge>")
    p.append("    </bpmndi:BPMNPlane>")
    p.append("  </bpmndi:BPMNDiagram>")
    p.append("</bpmn:definitions>")
    return "\n".join(p) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args(argv)
    with open(args.spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    try:
        xml = build(spec)
    except SpecError as e:
        print(f"ERRO na spec: {e}", file=sys.stderr)
        return 1
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(xml)
    print(f"{args.out}: {len(spec['nodes'])} nós, {len(spec['flows'])} fluxos, {len(spec['lanes'])} raias")
    return 0


if __name__ == "__main__":
    sys.exit(main())
