# Como escrever cada parte do kit

## Hipótese do MVP

> Acreditamos que **[o que o MVP faz]** vai **[resultado para o negócio]**. Saberemos que deu certo quando **[métrica acionável com número ou condição verificável]**.

O MVP é o mínimo que testa a hipótese com usuários reais; o resto vai para as releases seguintes. Feche com **Depois do MVP**: o que fazer se a métrica bater e se não bater (investir, ajustar ou parar).

## Métricas

- Acionáveis, não de vaidade: "% de reservas sem conflito", não "acessos à página".
- O que é contável sai do processo (etapas, campos redigitados, canais).
- Tempo e retrabalho sem medição ficam `[A MEDIR]` com o método de medição ao lado.
- Nunca invente um número medido. "Hoje" sem dado = `[A MEDIR]`.

| Indicador | Hoje | Meta | Como medir |
|---|---|---|---|
| Reservas em conflito por mês | [A MEDIR] | 0 | Relatório de conflitos bloqueados |

## Histórias de usuário (INVEST)

Formato: **Como** [papel], **quero** [ação] **para** [benefício].

| Letra | Pergunta de revisão |
|---|---|
| **I**ndependente | Dá para implementar em qualquer ordem? |
| **N**egociável | O cartão é convite para conversa, não contrato fechado? |
| **V**aliosa | Tem valor para o negócio? ("usar React" não tem) |
| **E**stimável | O time consegue estimar? Se não, falta spike |
| **S**mall (pequena) | Cabe em menos de uma semana (P ou M)? G é épico |
| **T**estável | Os critérios dizem como provar que está pronta? |

### Critérios de aceite

- 1 a 4 por história, cada um em **Dado** [contexto], **quando** [ação], **então** [resultado observável].
- Regra de negócio entra aqui: "Dado um espaço com reserva aprovada no horário, quando alguém tenta reservar, então o sistema bloqueia e mostra os horários livres."
- Verificável por quem é dono do processo, sem precisar ler o código.
- Proibido: "rápido", "fácil", "intuitivo", "amigável", "eficiente" sem número.

### Conversa e spikes

- **Conversa**: o que falta combinar no refinamento, em uma linha.
- **Spike**: dúvida técnica ou de regra que trava uma história. Fica ligado à história que destrava, não vira história.
- Épicos grandes e sem previsão ficam no fundo do backlog, sem histórias.

## Definição de Pronto

3 a 5 itens objetivos, por exemplo:

- Critérios Dado/Quando/Então aprovados pelo dono do processo em ambiente de teste
- Revisão de código por outra pessoa
- Testes automatizados para regra de negócio e cálculo
- Auditoria registrada nas operações que alteram dados
- Versão publicada com nota de versão

Requisitos não funcionais (LGPD, acesso, desempenho, licença) **refinam** a Definição de Pronto.

## Releases e homologação

MVP → Release 2 → Release 3, cada uma com as histórias que entram. O legado continua no ar até a última release (plano de volta).

Checklist de homologação (4 a 6 itens): dono do sistema e conta de serviço, controle de acesso, onde ficam os dados e o que é dado pessoal, licenças, runbook e rollback.

## BPMN

- **As-is**: como é hoje, com as dores numeradas no próprio diagrama e uma frase de causa raiz.
- **To-be**: como fica, com os ganhos numerados e cada tarefa ligada à história que a implementa (`"hu": ["HU-03"]`).
- Tarefa: verbo no presente + objeto, até ~60 caracteres. Gateway: pergunta com a história no rótulo ("Horário livre? (HU-02)").
- Raias são papéis ou sistemas. Até ~14 etapas e 5 raias por diagrama; passou disso, quebre em subprocessos.
- Tabela "O que muda": etapa · as-is · to-be.
