#!/usr/bin/env python3
"""Avaliação automática de um kit (mvp.md, historias.md e, opcional, bpmn.md).

Uso:
    python3 check_kit.py caminho/do/kit [--json]

Sai com código 1 se houver ERRO. Avisos não bloqueiam, mas devem ser lidos.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

VAGUE = re.compile(r"\b(r[áa]pid[oa]s?|f[áa]ceis?|f[áa]cil|intuitiv[oa]s?|amig[áa]vel|eficientes?|simples|adequad[oa]s?)\b", re.I)
TECHNICAL = re.compile(r"\bquero\*{0,2}\s+(criar (a |uma )?tabela|configurar (o )?servidor|usar (react|next|java|python)|migrar o banco|refatorar)", re.I)
PII = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
HU_HEADER = re.compile(r"^###\s+(HU-\d+)\s+[—-]\s+(.+?)(?:\s+·\s+(MVP|Depois))?(?:\s+·\s+(P|M|G))?\s*$", re.M)
CRITERIO = re.compile(r"^\s*-\s+\*{0,2}Dado\*{0,2}\s+.+?,\s+\*{0,2}quando\*{0,2}\s+.+?,\s+\*{0,2}ent[ãa]o\*{0,2}\s+.+", re.I | re.M)


@dataclass
class Report:
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    info: dict = field(default_factory=dict)

    def erro(self, msg: str) -> None:
        self.erros.append(msg)

    def aviso(self, msg: str) -> None:
        self.avisos.append(msg)


def section(text: str, title: str) -> str:
    m = re.search(rf"^##\s+{re.escape(title)}.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def check_common(name: str, text: str, r: Report) -> None:
    if "{{" in text:
        r.erro(f"{name}: placeholder do modelo não preenchido ({{{{…}}}})")
    if PII.search(text):
        r.erro(f"{name}: possível dado pessoal (e-mail ou CPF)")


def check_mvp(text: str, r: Report) -> None:
    check_common("mvp.md", text, r)
    hip = section(text, "Hipótese")
    if not hip:
        r.erro("mvp.md: falta a seção Hipótese")
    elif not (re.search(r"Acreditamos", hip) and re.search(r"Saberemos", hip)):
        r.erro("mvp.md: hipótese sem as partes 'Acreditamos que…' e 'Saberemos que deu certo quando…'")
    if not section(text, "Métricas"):
        r.erro("mvp.md: falta a seção Métricas")
    if "Depois do MVP" not in text:
        r.aviso("mvp.md: falta 'Depois do MVP' (o que fazer se a métrica bater ou não)")
    if not re.search(r"plano de volta", text, re.I):
        r.aviso("mvp.md: falta o plano de volta (o que do legado continua no ar)")


def check_historias(text: str, r: Report) -> set[str]:
    check_common("historias.md", text, r)
    headers = list(HU_HEADER.finditer(text))
    ids = {h.group(1) for h in headers}
    if not headers:
        r.erro("historias.md: nenhuma história no formato '### HU-01 — Título · MVP · P'")
    if len(ids) != len(headers):
        r.erro("historias.md: ids de história duplicados")
    for i, h in enumerate(headers):
        hu, _title, fase, tam = h.group(1), h.group(2), h.group(3), h.group(4)
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[h.end():end].split("\n## ")[0]
        if not re.search(r"\*\*Como\*\*.+\*\*quero\*\*.+\*\*para\*\*", body, re.S):
            r.erro(f"{hu}: falta 'Como …, quero … para …'")
        criterios = CRITERIO.findall(body)
        if not criterios:
            r.erro(f"{hu}: nenhum critério Dado/Quando/Então")
        elif len(criterios) > 4:
            r.aviso(f"{hu}: {len(criterios)} critérios; mais de 4 indica história grande demais")
        for c in criterios:
            if VAGUE.search(c):
                r.erro(f"{hu}: critério vago ('{VAGUE.search(c).group(0)}'): {c.strip()[:90]}")
        if TECHNICAL.search(body):
            r.erro(f"{hu}: história técnica, sem valor direto para quem usa")
        if fase == "MVP" and tam == "G":
            r.erro(f"{hu}: história do MVP com tamanho G; quebre em histórias menores")
        if not tam:
            r.aviso(f"{hu}: sem tamanho (P, M ou G)")
    dod = section(text, "Definição de Pronto")
    itens = re.findall(r"^\s*-\s+\S", dod, re.M)
    if not dod:
        r.erro("historias.md: falta a Definição de Pronto")
    elif not 3 <= len(itens) <= 6:
        r.aviso(f"historias.md: Definição de Pronto com {len(itens)} itens (esperado 3 a 5)")
    r.info["historias"] = len(headers)
    r.info["historias_mvp"] = sum(1 for h in headers if h.group(3) == "MVP")
    r.info["criterios"] = len(CRITERIO.findall(text))
    return ids


def check_bpmn(text: str, ids: set[str], r: Report) -> None:
    check_common("bpmn.md", text, r)
    citadas = set(re.findall(r"HU-\d+", section(text, "To-be")))
    for hu in sorted(citadas - ids):
        r.erro(f"bpmn.md: to-be cita {hu}, que não existe em historias.md")
    if "Causa raiz" not in text:
        r.aviso("bpmn.md: falta a causa raiz do as-is")
    if not section(text, "O que muda"):
        r.aviso("bpmn.md: falta a tabela 'O que muda'")


def check_kit(folder: Path) -> Report:
    r = Report()
    files = {p.name: p.read_text(encoding="utf-8") for p in folder.glob("*.md")}
    if "mvp.md" not in files:
        r.erro("falta mvp.md")
    else:
        check_mvp(files["mvp.md"], r)
    ids: set[str] = set()
    if "historias.md" not in files:
        r.erro("falta historias.md")
    else:
        ids = check_historias(files["historias.md"], r)
    if "bpmn.md" in files:
        check_bpmn(files["bpmn.md"], ids, r)
    todos = "\n".join(t for n, t in files.items() if n in ("mvp.md", "historias.md", "bpmn.md"))
    r.info["a_confirmar"] = todos.count("[A CONFIRMAR]")
    r.info["a_medir"] = todos.count("[A MEDIR]")
    return r


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    r = check_kit(Path(args.pasta))
    if args.json:
        print(json.dumps(asdict(r), ensure_ascii=False, indent=2))
    else:
        for e in r.erros:
            print(f"ERRO   {e}")
        for a in r.avisos:
            print(f"AVISO  {a}")
        i = r.info
        print(
            f"OK     {i.get('historias', 0)} histórias ({i.get('historias_mvp', 0)} no MVP), "
            f"{i.get('criterios', 0)} critérios, {i.get('a_confirmar', 0)} [A CONFIRMAR], {i.get('a_medir', 0)} [A MEDIR]"
            if not r.erros
            else f"{len(r.erros)} erro(s), {len(r.avisos)} aviso(s)"
        )
    return 1 if r.erros else 0


if __name__ == "__main__":
    sys.exit(main())
