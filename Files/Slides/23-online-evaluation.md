# Slide 23 - Information Retrieval Online Evaluation

## Ranking evaluation

- Lots of alternative solutions
  - Which one to choose?
  - How to improve upon them?
- Evaluation enables an informed choice
  - Rigor of science
  - Efficiency of practice

## Evaluation methodology

- Feedback
  - Implicit
  - Explicit
  - **implicit**
- Mode
  - Retrospective
  - Prospective
  - **retrospective**
    - counterfactual evaluation
    - offline evaluation
  - **prospective**
    - online evaluation

## Offline evaluation

- Retrospective experiments
  - How well can we predict (hidden) **past preferences**?
  - Benchmarked using static test collections
- High throughput
- High reproducibility

---

[Image: NIST credit logo]

## Offline evaluation limitations

- Scalability
  - Relevance judgments are costly
  - More so if expert judgments are needed
- Realism
  - Hired judges aren't real users
  - Laboratory studies aren't naturalistic

## Offline results often don't hold live

- Features are built because we believe they are useful
  - Most experiments show that features fail to move the metrics they were designed to improve
- Observations based on experiments at Microsoft
  - [Kohavi et al., 2009]
  - 1/3 good, 1/3 bad, 1/3 neutral ideas

## Why do offline and online eval disagree?

## Causality

- Offline data allows for mining correlations
  - But correlation does not imply causation!
- [Image: Diagram showing possible correlations and causations]
  - **possible correlation**
  - **possible causation**

### Example flawed analysis

[JV] Comecei aqui. Cheguei atrasado.

- Observation (highly stat-sig)
  - Palm size negatively correlates with life expectancy
  - The larger your palm, the less you will live
- Gender is the common cause
  - Women have smaller palms and live 6 years longer than men on average

## Online evaluation

- Focus on implicit user feedback
  - [JV] São mais naturais, e não requerem que o usuário faça nada
  - Derived from observable user activity
  - Captured during natural interaction
- Implicit signals with various levels of noise
  - Clicks, dwell-times, purchase decisions
- **Allows for detecting causation**

## Controlled experiments

- > An experiment is a procedure carried out to support, refute, or validate a hypothesis
- > Experiments provide insight into cause-and-effect by demonstrating what outcome occurs when a particular factor is manipulated
- [Wikipedia: Experiment](https://en.wikipedia.org/wiki/Experiment)

---

- When different variants run concurrently, only two things could explain a change in metrics
  - #1: their "feature(s)" (A vs. B)
  - #2: random chance
- Everything else happening affects both the variants
  - For #2, we conduct statistical tests for significance

## Hypotheses and variables

- Example hypothesis
  - H: increasing the weight given to document recency in the ranking will increase user click-through rate
- Variables of interest
  - X: independent variable (recency weight)
  - Y: dependent variable (user click-through rate)

---

- Alternative hypothesis
  - $H_1:$ increasing X will increase Y
- Corresponding null hypothesis
  - $H_0:$ increasing X will **not** increase Y
- How to support $H_1?$
  - Show that $H_0$ is improbable!

## Unit of experimentation

- Defines the granularity of the experiment
  - User (most typical), query, user+day
- Smaller units (e.g., queries)
  - Reduced data requirements
    - [JV] Queries são negativas porque bots podem fazer consultas que não são relevantes pro experimento proposto.
- Larger units (e.g., users)
  - Reduced risk of network effects
  - [JV] Mas e como agrupar os usuários?

### Between-subject experiments

- Each user is exposed to a single variant
- Randomized splitting
  - Control group
  - Treatment group
- [Image: Diagram showing user allocation to control/treatment groups]
  - [JV]
    - Pergunta do professor: "Como confirmamos que os dois grupos são equivalentes?"
      - Resposta: Fazemos um teste A/A para validar a divisão aleatória.
        - Explicação: A/A test é um teste onde aplicamos a mesma abordagem (A) a dois grupos diferentes de usuários e esperamos que não haja diferença significativa entre eles.

#### A/B test

- Randomly split traffic between two (or more) versions
  - A (control, typically the existing system)
  - B (treatment)
- Collect metrics of interest
- Analyze

---

- A/B/n is common in practice
  - Compare A/B/C/D/..., not just two variants
  - Sensitive to small changes (given large samples)
- Equivalent names
  - Flights (Microsoft), 1% tests (Google), bucket tests (Yahoo!), randomized clinical trials (medicine)
  - [JV]
    - Pergunta do professor: "Por que não testa com a base de usuários inteira?"
      - Porque como são testes, os resultados podem ser negativos, e se você fizer com a base inteira, pode prejudicar a experiência de todos os usuários.
    - Talvez um pré-teste offline ajude a remover ideias horríveis.

#### Pre-test validation

- A/A tests used to validate splitting
  - Same approach (A) applied to different user groups
- Ideally, no significant difference should be observed
  - Outliers in either partition may introduce bias
- In practice, A/A test over multiple splittings

  - Significant differences should rarely occur (under 5%)

- [JV] Esse pré-teste é um teste de sanidade, para garantir que a divisão aleatória dos usuários não introduza viés nos resultados do teste A/B.
  - Dúvida JV: Mas e o que me garante que o grupo testado e que era equilibrado para A/A, seguirá sendo equilibrado para B/B?
    - Resposta Professor: Você pode fazer vários testes A/A, B/B, C/C, etc., para garantir esse equilíbrio.

#### Absolute metrics

- Document-level
  - Click rate, click models
- Ranking-level
  - Reciprocal rank, CTR@k, time-to-click, abandonment
- Session-level
  - Queries per session, session length, time to first click
    - [JV] Queries per session: pode ser uma métrica boa ou ruim. Depende de como o usuário se porta. Se ele tá pesquisando várias coisas diferentes, é bom, pois ele ainda se mantém no sistema. Mas se ele tá pesquisando a mesma coisa várias vezes, é ruim, pois ele não encontrou o que queria e sua insatisfação pode continuar crescendo.

#### Relative metrics

- Absolute document-level metrics are biased
  - Position bias: top ranked document favored
  - Presentation bias: highlighted documents favored
- Relative document-level metrics are less affected
  - Click-skip, fair pairs

## Can we compare rankings to each other?

### Within-subject experiments

- Side-by-side experiments are common in lab studies
  - Not naturalistic to run in production systems though
    - [JV] Deixa de ser naturalístico porque o usuário agora sabe que está participando de um experimento, e isso pode afetar o comportamento dele.
- **Solution: interleaving**
  - Mix results from different rankings
  - Observe user feedback (e.g., clicks)
  - Credit feedback to original rankers

#### Interleaved comparisons [Joachims, KDD 2002]

- Blend results from both conditions into a single ranking
- [Image: Diagram showing ranking A vs. B blended into AB (But the provenance is not visible)]

---

- Hide provenance from the user and collect feedback
- [Image: Diagram showing user interacting with blended ranking AB]

---

- Assign credit based on clicks
  - e.g., B wins over A
- [Image: Diagram showing credit assignment to ranking B]

##### Balanced Interleaving [Joachims, KDD 2002]

- **ALGORITHM 1:** Balanced Interleaving, following [Chapelle et al. 2012]

  - **Input:** $l_1, l_2$
  - $l = []; i_1 = 0; i_2 = 0$
  - $first\_1 = random\_bit()$ `// decide who gets priority`
  - **while** $(i_1 < len(l_1)) \land (i_2 < len(l_2))$ **do** `// if not end of` $A$ `or` $B$
    - **if** $(i_1 < i_2) \lor ((i_1 == i_2) \land (first\_1 == 1))$ **then** `// if` $A$ `least explored or` $A$ `has priority`
      - **if** $l_1[i_1] \notin I$ **then**
        - $append(l, l_1[i_1])$ `// append next` $A$ `result`
        - $i_1 = i_1 + 1$
    - **else**
      - **if** $l_2[i_2] \notin I$
        - $append(l, l_2[i_2])$ `// append next` $B$ `result`
      - $i_2 = i_2\ + 1$
      - `// present` $r$ `to user and observe clicks` $c$`, then infer outcome (if at least one click was observed)`
  - $d_{max} =$ lowest-ranked clicked document in $l$
  - $k = min \{j : (d_{max} = l_1[j]) \lor (d_{max} = l_2[j]) \}$ `// earliest rank of` $d_{max} \in A \lor B$
  - $c_1 = len \{i : c[i] = true \land |i| \in l_1[1..k]\}$ `// count clicks in` $A$ `and` $B$ `up to position` $k$
  - $c_2 = len \{i : c[i] = true \land |i| \in l_2[1..k]\}$
  - **return** $-1$ **if** $c_1 > c_2$ **else** $1$ **if** $c_1 < c_2$ **else** $0$

- [JV] Intuição: Seleção de time de futebol. Entre os capitães, os jogadores são escolhidos alternadamente, de forma que cada time tenha um jogador de cada posição. Assim, o time é balanceado.

---

- Each query produces a single comparison result
  - Either A or B wins, or there is a tie
- Degree of preferences computed across queries

  - $\Delta_{AB} = \frac{\text{wins}(A) + 0.5 \text{ties}(A,B)}{\text{wins}(A) + \text{wins}(B) + \text{ties}(A,B)} - 0.5$

- [JV] Como o mesmo item pode estar em dois produtos, o que começa na frente acaba tendo prioridade nos empates posteriores.

##### Interleaving extensions

- Team draft interleaving [Radlinski et al., CIKM 2008]
  - Randomizes provenance of duplicate documents
- Probabilistic interleaving [Hofmann et al., CIKM 2011]
  - Sample over probabilistic input rankings
- (Probabilistic) multileaving [Schuth et al., CIKM 2014, SIGIR 2015]

  - Mix multiple (possibly infinitely many) rankers

- [JV]
  - Professor: qual a diferença entre a comparação insubject vs interleaving? Tem como obter algum ganho com relação ao teste A/B?
    - Resposta: Com o interleaving, a gente reduz a variância, pois os usuários com atitudes de outliers estarão expostos a ambos os rankings simultaneamente, assim sendo mais eficiente.
  - Dúvida JV: Mas e por que o A/B parece ser mais usado se esse interleaving é mais eficiente?
    - Resposta: Porque o A/B é mais fácil de implementar e é mais abstrato e é usado para casos distintos dos de ranking.

### Long-term metrics [Hohnhold et al., KDD 2015]

- Measuring short-term effects is straightforward
  - i.e., just run an A/B or interleaved test
- Search engines are evaluated on market share (distinct queries per month) and revenue as long-term goals
  - How can we measure (and influence) these?

---

- Revenue can be broken down according to:
  - $\frac{Revenue}{Period} = \frac{Users}{Period} \cdot \frac{Sessions}{User} \cdot \frac{Queries}{Session} \cdot \frac{Ads}{Query} \cdot \frac{Clicks}{Ad} \cdot \frac{Cost}{Click}$
  - 1 and 2: harder to influence
  - 4 and 6: easier to influence, but negative impact
  - 3 and 5: easier to influence, with positive impact
  - [JV]
    1. Users/Period: Depende do usuário
    2. Sessions/User: Depende do usuário
    3. Queries/Session: Depende do usuário
    4. Ads/Query: Facilmente alterável pela máquina de busca
    5. Clicks/Ad: Depende do usuário
    6. Cost/Click: Facilmente alterável pela máquina de busca

---

- Are any of these impacts persistent in the long run?

---

- Long-term impact of B

| Group   | $t=0$ | $t=1$ | $t=2$                                                  |
| ------- | ----- | ----- | ------------------------------------------------------ |
| 1       | A     | A     | B                                                      |
| 2       | A     | B     | B                                                      |
| Outcome | A1=A2 | X     | $B1 = B2$: no impact // $B1 \neq B2$: long-term impact |

- [JV] Eu sigo incomodado com a ideia de que o impacto de A e de B podem ser diferentes sobre os grupos. Então, mesmo que B fosse aplicado aos dois grupos em $t=1$, poderia ser igual ou diferente. Como isso pode ser mitigado?
  - Resposta: parte-se do princípio que os dois grupos são grandes o bastante para serem invariantes aos dois casos de teste.

## The cultural challenge [Deng et al., SIGIR 2017, KDD 2017]

- > It is difficult to get a man to understand something when his salary depends upon his not understanding it.
  - Upton Sinclair

---

- Why people/orgs avoid controlled experiments
  - Some believe it threatens their job as decision makers
  - Proposing several alternatives and admitting you don't know which is best is hard
  - Failures of ideas may hurt professional standing
  - "We know what to do. It's in our DNA!"
  - [JV] Um dos papéis do cientista é ter a humildade de reconhecer que não sabe tudo.

---

- Dismissing controlled experiments as a guiding mechanism means following the HiPPO
  - HiPPO = Highest Paid Person's Opinion

## Summary

- Online evaluation via controlled experiments
  - Crucial to measure causal effects on user behavior
- Several methods proposed for ranking evaluation
  - Between-subject, within subject experiments
- Can be leveraged to guide learning to rank
  - Incremental learning from user interactions

## References

- Online evaluation for information retrieval
  - [Hofmann et al., FrTIR 2016](https://doi.org/10.1561/1500000051)
- A/B testing at scale: accelerating software innovation
  - [Deng et al., SIGIR 2017 / KDD 2017](https://doi.org/10.1145/3077136.3082060)

---

- Trustworthy online controlled experiments: five puzzling outcomes explained
  - [Kohavi et al., KDD 2012](https://doi.org/10.1145/2339530.2339653)
- Focusing on the long-term: it's good for users and business
  - [Hohnhold et al., KDD 2015](https://doi.org/10.1145/2783258.2788583)

## Coming next... Online Learning to Rank
