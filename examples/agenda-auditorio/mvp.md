# MVP — Agenda do Auditório

**Setor dono:** Secretaria de Eventos · **Quem decide:** coordenação da Secretaria de Eventos · **Situação:** pré-desenvolvimento · **Versão:** 1.0 · **Data:** 28/10/2026

## Resumo
Agendamento do auditório com aprovação, bloqueio de conflito de horário e aviso automático para a equipe de apoio. Substitui a planilha compartilhada e os pedidos por e-mail.

## Problema
Pedidos chegam por planilha e e-mail, sem padrão. Já houve duas reservas para o mesmo horário, e a equipe de apoio só fica sabendo da montagem quando alguém lembra de encaminhar o pedido.

## Hipótese
> Acreditamos que **um agendamento com aprovação e bloqueio de conflito no próprio sistema** vai **acabar com reservas duplicadas e avisar a equipe de apoio a tempo**. Saberemos que deu certo quando **nenhuma reserva aprovada tiver conflito de horário no primeiro mês e toda montagem tiver aviso registrado com antecedência mínima de [A CONFIRMAR] dias**.

## Papéis
| Papel | O que precisa |
|---|---|
| Solicitante (servidor de setor) | Saber se o horário está livre e pedir sem trocar e-mails |
| Secretaria de Eventos | Aprovar ou recusar com motivo e ver a agenda consolidada |
| Equipe de apoio | Saber o que montar, onde e quando |

## Escopo
| Entra no MVP | Fica para depois |
|---|---|
| HU-01 — Ver horários livres | HU-06 — Reserva recorrente no semestre |
| HU-02 — Solicitar reserva | HU-07 — Relatório de ocupação |
| HU-03 — Aprovar ou recusar com motivo | Reservas de público externo [A CONFIRMAR] |
| HU-04 — Avisar a equipe de apoio | |
| HU-05 — Cancelar reserva | |

## Métricas
| Indicador | Hoje | Meta | Como medir |
|---|---|---|---|
| Reservas aprovadas com conflito de horário por mês | [A MEDIR] | 0 | Consulta de sobreposição no banco |
| Montagens com aviso registrado antes do evento | [A MEDIR] | 100% | Log de avisos por reserva aprovada |
| Pedidos que exigiram troca de e-mail para completar dados | [A MEDIR] | ↓ | Amostra mensal com a Secretaria |

**Depois do MVP:** se bater, levar o mesmo fluxo para salas de reunião; se não bater, revisar o formulário e as regras de aprovação com a Secretaria antes de expandir.

## Releases
| Release | Foco | Entra |
|---|---|---|
| MVP | Fim do conflito e aviso automático | HU-01 a HU-05; planilha em paralelo, só leitura |
| Release 2 | Planejamento | HU-06 e HU-07 |

**Plano de volta:** a planilha atual continua acessível, em modo leitura, até o fim da Release 2.

## Homologação
- [ ] Dono do sistema e conta de serviço definidos
- [ ] Acesso por perfil: solicitante, Secretaria e equipe de apoio
- [ ] Dados pessoais tratados: nome e e-mail institucional do solicitante (necessários para o aviso)
- [ ] Integração com o calendário institucional validada em homologação
- [ ] Runbook e rollback para voltar à planilha

## Spikes
| Dúvida | Destrava |
|---|---|
| O calendário institucional aceita criar eventos por conta de serviço? | HU-04 |
| Reservas de público externo seguem o mesmo fluxo? | Escopo da Release 2 |

<sub>Elaborado a partir do formulário e da conversa de entendimento (fictícios). Itens `[A CONFIRMAR]` e `[A MEDIR]` dependem da Secretaria de Eventos.</sub>
