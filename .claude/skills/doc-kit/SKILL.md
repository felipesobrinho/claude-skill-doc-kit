---
name: doc-kit
description: "Gera a documentação enxuta de um projeto de software — MVP, Histórias de Usuário (INVEST, critérios Dado/Quando/Então, Definição de Pronto) e BPMN as-is/to-be — a partir do contexto do projeto e dos documentos-modelo desta skill. Use quando alguém iniciar um projeto, ou pedir MVP, histórias, backlog, critérios de aceite, Definição de Pronto ou BPMN, mesmo sem citar a skill."
---

# Kit de documentação de projeto

Quem chega de fora a um projeto precisa entender em minutos o que ele resolve e o que vem primeiro. O kit tem só três documentos curtos:

1. **MVP** (até 3 páginas): problema, hipótese, papéis, o que entra e o que fica para depois, métricas (hoje → meta), releases e checklist de homologação.
2. **Histórias de Usuário** (até 5 páginas): papéis, épicos → histórias com critérios Dado/Quando/Então, Definição de Pronto e requisitos não funcionais.
3. **BPMN** (até 4 páginas + dois `.bpmn`): as-is com dores e causa raiz, to-be com ganhos ligados às histórias. Só quando o projeto muda um processo com mais de um papel; numa ferramenta de uma pessoa só, pule.

Regras de negócio viram critérios de aceite, requisitos viram histórias e o plano de homologação vira releases + checklist. Não existe documento extra "para garantir".

## Arquivos desta skill

| Caminho | Para quê |
|---|---|
| `templates/mvp.md`, `templates/historias.md`, `templates/bpmn.md` | Estrutura e nível de detalhe esperados. Reproduza o ritmo, não o conteúdo |
| `templates/bpmn-spec.json` | Formato da spec que vira `.bpmn` |
| `references/escrita.md` | Como escrever hipótese, métricas, histórias INVEST, critérios e DoD |
| `references/revisao.md` | Checklist de revisão antes de entregar |
| `scripts/bpmn_from_spec.py` | Spec JSON → BPMN 2.0 com diagrama (abre no Camunda Modeler, bpmn.io, draw.io) |
| `scripts/check_kit.py` | Avaliação automática da saída: histórias sem critério, critério vago, lacunas sem marcação |

## Fluxo de trabalho

1. **Contexto.** Junte conversa, anexos e documentos existentes. Identifique: produto, setor dono, como funciona hoje, de onde vêm os dados e que números já existem.
2. **Papéis primeiro.** Liste quem interage com a solução (pessoas, não sistemas) antes de escrever histórias, para o backlog não atender só um papel.
3. **Lacunas.** Pergunte no máximo 3 coisas, de uma vez, e só o que muda a hipótese ou o escopo do MVP. O resto vira `[A CONFIRMAR]` (regra) ou `[A MEDIR]` (número), e a dúvida vira spike ou "Conversa" da história.
4. **MVP.** Ordem de pensamento: hipótese → histórias que a validam → o resto (depois) → métricas → releases. Use `templates/mvp.md`.
5. **Histórias.** Épicos → histórias INVEST com 1 a 4 critérios Dado/Quando/Então cada. Use `templates/historias.md` e `references/escrita.md`.
6. **BPMN, se couber.** Escreva as specs as-is e to-be no formato de `templates/bpmn-spec.json`. No to-be, cada tarefa leva `hu` e cada gateway cita a história no rótulo. Gere os arquivos:
   ```bash
   python3 scripts/bpmn_from_spec.py asis.json -o <id>-asis.bpmn
   python3 scripts/bpmn_from_spec.py tobe.json -o <id>-tobe.bpmn
   ```
7. **Avalie antes de entregar.**
   ```bash
   python3 scripts/check_kit.py <pasta-do-kit>
   ```
   Corrija todo `ERRO`. Depois passe pelo `references/revisao.md`.
8. **Entregue** os três markdowns e os `.bpmn`, com um parágrafo dizendo o que ficou `[A CONFIRMAR]` e quem precisa responder.

## Regras que não se negociam

- **Nunca invente número medido, regra de negócio, sistema, endpoint ou nome de pessoa.** Sem fonte, é `[A MEDIR]` ou `[A CONFIRMAR]`.
- **Uma história tem valor para quem usa** ("Como analista, quero…"), nunca "usar React" ou "criar tabela".
- **Critério vago não é critério.** "Rápido", "fácil", "intuitivo" não passam; reescreva como comportamento observável.
- **Requisito não funcional não vira história:** LGPD, acesso, desempenho e licença refinam a Definição de Pronto.
- **Dado pessoal** que a solução trata é citado no MVP (o quê e por quê) e no checklist de homologação.
- **O legado continua no ar** até a última release: escreva qual é o plano de volta.

## Voz

Português do Brasil, frases curtas, voz ativa. Datas `dd/mm/aaaa`. Se uma frase não muda decisão nem teste, ela sai. Termos técnicos em `` ` ``. Nunca apresente suposição como fato.
