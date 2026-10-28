import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "doc-kit" / "scripts"))

import bpmn_from_spec  # noqa: E402
import check_kit  # noqa: E402

EXAMPLE = ROOT / "examples" / "agenda-auditorio"
NS = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL", "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI"}


class BpmnFromSpecTest(unittest.TestCase):
    def test_example_specs_generate_valid_xml_with_diagram(self):
        for name in ("asis.json", "tobe.json"):
            spec = json.loads((EXAMPLE / name).read_text(encoding="utf-8"))
            root = ET.fromstring(bpmn_from_spec.build(spec))
            process = root.find("bpmn:process", NS)
            flows = process.findall("bpmn:sequenceFlow", NS)
            self.assertEqual(len(flows), len(spec["flows"]))
            shapes = root.findall(".//bpmndi:BPMNShape", NS)
            # participante + raias + nós
            self.assertEqual(len(shapes), 1 + len(spec["lanes"]) + len(spec["nodes"]))
            self.assertEqual(len(root.findall(".//bpmndi:BPMNEdge", NS)), len(spec["flows"]))

    def test_marks_and_stories_are_kept(self):
        spec = json.loads((EXAMPLE / "tobe.json").read_text(encoding="utf-8"))
        xml = bpmn_from_spec.build(spec)
        self.assertIn("(G1)", xml)
        self.assertIn("Histórias: HU-04", xml)

    def test_invalid_spec_is_rejected(self):
        spec = {
            "id": "x",
            "lanes": [{"id": "a", "name": "A"}],
            "nodes": [
                {"id": "ini", "type": "start", "lane": "a", "row": 0, "label": "Início"},
                {"id": "t", "type": "tarefa", "lane": "b", "row": 0, "label": "?"},
            ],
            "flows": [{"from": "ini", "to": "nada"}],
        }
        errors = bpmn_from_spec.validate(spec)
        self.assertTrue(any("tipo desconhecido" in e for e in errors))
        self.assertTrue(any("raia inexistente" in e for e in errors))
        self.assertTrue(any("nó inexistente" in e for e in errors))
        self.assertTrue(any("sem evento de fim" in e for e in errors))
        with self.assertRaises(bpmn_from_spec.SpecError):
            bpmn_from_spec.build(spec)


class CheckKitTest(unittest.TestCase):
    def test_example_kit_passes(self):
        r = check_kit.check_kit(EXAMPLE)
        self.assertEqual(r.erros, [])
        self.assertEqual(r.info["historias"], 6)
        self.assertGreater(r.info["a_medir"], 0)

    def test_templates_are_flagged_as_unfilled(self):
        r = check_kit.check_kit(ROOT / ".claude" / "skills" / "doc-kit" / "templates")
        self.assertTrue(any("placeholder" in e for e in r.erros))

    def test_bad_stories_are_caught(self):
        historias = """# Histórias
### HU-01 — Tela bonita · MVP · G
**Como** usuário, **quero** criar tabela de reservas **para** ter dados.

- **Dado** a tela, **quando** abro, **então** ela é rápida.

### HU-02 — Sem critério · MVP · P
**Como** usuário, **quero** algo útil **para** um fim.

## Definição de Pronto
- Testado
"""
        mvp = "# MVP\n## Hipótese\nAcreditamos que X. Saberemos que Y.\n## Métricas\n|a|\n Depois do MVP. Plano de volta: planilha."
        with tempfile.TemporaryDirectory() as d:
            Path(d, "historias.md").write_text(historias, encoding="utf-8")
            Path(d, "mvp.md").write_text(mvp + "\ncontato: fulano@exemplo.com", encoding="utf-8")
            r = check_kit.check_kit(Path(d))
        joined = " | ".join(r.erros)
        self.assertIn("critério vago", joined)
        self.assertIn("história técnica", joined)
        self.assertIn("tamanho G", joined)
        self.assertIn("HU-02: nenhum critério", joined)
        self.assertIn("possível dado pessoal", joined)
        self.assertTrue(any("Definição de Pronto com 1 itens" in a for a in r.avisos))


if __name__ == "__main__":
    unittest.main()
