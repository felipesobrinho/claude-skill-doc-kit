# Checklist de revisão (antes de entregar)

Rode `python3 scripts/check_kit.py <pasta>` primeiro. Depois confira à mão:

## MVP
- [ ] A hipótese tem as três partes: o que o MVP faz, resultado esperado e sinal verificável
- [ ] Toda métrica tem "hoje", "meta" e "como medir"; nenhum "hoje" foi inventado
- [ ] "Depois do MVP" diz o que fazer se bater e se não bater
- [ ] O que fica fora do MVP está escrito (e não esquecido)
- [ ] Dado pessoal citado, se houver
- [ ] Plano de volta: o que do legado continua no ar

## Histórias
- [ ] Papéis listados antes das histórias e todos aparecem em pelo menos uma história
- [ ] Toda história do MVP tem tamanho P ou M
- [ ] Todo critério está em Dado/Quando/Então e é observável
- [ ] Nenhuma história técnica ("criar tabela", "configurar servidor")
- [ ] Spikes ligados às histórias que destravam
- [ ] Definição de Pronto com 3 a 5 itens objetivos; requisitos não funcionais refinando-a

## BPMN
- [ ] As-is validado por quem opera o processo (nome do papel, não da pessoa)
- [ ] Cada dor numerada no as-is tem linha na tabela de dores
- [ ] Cada tarefa do to-be aponta para uma história
- [ ] Tabela "O que muda" cobre todas as etapas alteradas

## Geral
- [ ] Nenhuma suposição apresentada como fato: tudo que é dúvida está `[A CONFIRMAR]` ou `[A MEDIR]`
- [ ] Nenhum nome de pessoa, e-mail, CPF ou endpoint interno
- [ ] Cabe nos limites: MVP ≤ 3 páginas, Histórias ≤ 5, BPMN ≤ 4
