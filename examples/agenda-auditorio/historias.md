# Histórias de Usuário — Agenda do Auditório

**Versão:** 1.0 · **Data:** 28/10/2026 · **Referência:** MVP — Agenda do Auditório

## Papéis
| Papel | O que precisa |
|---|---|
| Solicitante | Pedir sem trocar e-mails e saber a resposta |
| Secretaria de Eventos | Aprovar com critério e ver a agenda |
| Equipe de apoio | Saber o que montar e quando |

## Mapa do backlog
| Épico | MVP | Depois |
|---|---|---|
| EP-01 Reservar | HU-01, HU-02, HU-05 | HU-06 |
| EP-02 Aprovar e avisar | HU-03, HU-04 | — |
| EP-03 Planejar a ocupação | — | HU-07 |

## EP-01 — Reservar
_Como solicitante, quero reservar o auditório sem depender de e-mail para garantir o espaço da minha atividade._

### HU-01 — Ver horários livres · MVP · P
**Como** solicitante, **quero** ver os horários livres do auditório numa semana **para** escolher um horário possível antes de pedir.

- **Dado** uma reserva aprovada das 14h às 16h, **quando** eu abro a semana, **então** esse intervalo aparece ocupado e os demais aparecem livres.

### HU-02 — Solicitar reserva · MVP · M
**Como** solicitante, **quero** pedir o auditório informando data, início, fim e finalidade **para** registrar o pedido num só lugar.

- **Dado** um horário livre, **quando** eu envio o pedido, **então** ele fica com status "solicitada" e a Secretaria é avisada.
- **Dado** uma reserva aprovada que se sobrepõe ao horário, **quando** eu tento enviar, **então** o sistema bloqueia e mostra os horários livres do dia.

_Conversa:_ antecedência mínima para pedir [A CONFIRMAR].

### HU-05 — Cancelar reserva · MVP · P
**Como** solicitante, **quero** cancelar uma reserva minha **para** liberar o horário para outro setor.

- **Dado** uma reserva aprovada, **quando** eu cancelo, **então** o horário volta a aparecer livre e a equipe de apoio é avisada do cancelamento.

## EP-02 — Aprovar e avisar
_Como Secretaria de Eventos, quero decidir cada pedido e garantir que a equipe de apoio saiba a tempo._

### HU-03 — Aprovar ou recusar com motivo · MVP · P
**Como** Secretaria de Eventos, **quero** aprovar ou recusar pedidos informando o motivo **para** manter a agenda organizada e o solicitante informado.

- **Dado** um pedido "solicitada", **quando** eu aprovo, **então** o status muda para "aprovada" e o solicitante recebe a confirmação.
- **Dado** um pedido "solicitada", **quando** eu recuso sem informar motivo, **então** o sistema não permite concluir a recusa.

### HU-04 — Avisar a equipe de apoio · MVP · M
**Como** equipe de apoio, **quero** receber o aviso de cada reserva aprovada com local, horário e finalidade **para** preparar a montagem com antecedência.

- **Dado** uma reserva aprovada, **quando** a aprovação é registrada, **então** a equipe de apoio recebe o aviso e o evento aparece no calendário institucional.
- **Dado** que o calendário está indisponível, **quando** a aprovação é registrada, **então** a reserva é aprovada mesmo assim e o aviso fica pendente para nova tentativa.

## EP-03 — Planejar a ocupação
### HU-07 — Ver relatório de ocupação · Depois · M
**Como** Secretaria de Eventos, **quero** ver a ocupação do auditório por mês **para** planejar eventos e justificar melhorias.

- **Dado** reservas aprovadas no mês, **quando** eu abro o relatório, **então** vejo horas ocupadas por semana e por setor.

## Definição de Pronto
- Critérios Dado/Quando/Então aprovados pela Secretaria de Eventos em ambiente de teste
- Revisão de código por outra pessoa
- Testes automatizados para a regra de conflito de horário e para as transições de status
- Auditoria de quem aprovou, recusou ou cancelou cada reserva
- Versão publicada com nota de versão

## Requisitos não funcionais
- LGPD: só nome e e-mail institucional do solicitante; sem dados de participantes
- Acesso: três perfis (solicitante, Secretaria, equipe de apoio) com login institucional
- Integrações não bloqueiam a aprovação; falhas ficam registradas e são reprocessadas

## Spikes
| Dúvida | Destrava |
|---|---|
| Criação de eventos no calendário institucional por conta de serviço | HU-04 |
