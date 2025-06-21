# Aula 08 - 09/04/2025 - Efficient Matching

## Search Components - Aula 08

[Fluxograma dos Search Components padrão]

---

[Foco no Query Processor]

### Query Processing Overview - Aula 08

[Fluxograma geral do Query Processing]

---

[Foco no Matchings]

## Document Matching - Aula 08

- Scan postings list for all query terms
  - [aquarium fish]
    - and: 1:1
    - aquarium: 3:1
    - are: 3:1, 4:1
    - ...
    - environment: 1:1
    - fish: 1:2, 2:3, 3:2, 4:2

---

- Scan postings lists for all query terms
  - [aquarium fish]
    - aquarium: 3:1
    - fish: 1:2, 2:3, 3:2, 4:2
- Score matching documents

  - $f(q, d) = \sum_{t \in q} f(t, d)$

- Index access cost
  - Memory paging (I/O)
  - In-memory processing (CPU)
- Scoring cost
  - Decompression + scoring (CPU)

Para os índices em memória, o custo não é tão grande.

Veremos hoje sobre métodos de reduzir esses dois custos.

## Index Access Cost

- Inherent cost of matching documents to queries

  - Query length (number of posting lists)
  - Posting lists length (number of postings per list)

- De cima a baixo: Query Length
- Da esquerda pra direita: Posting list length

## Traversal direction

- TAAT: inverted lists processed in sequence
  - More memory efficient (sequential access)

Malefícios: acumuladores demais por score de documento.

Se eu fosse fazer pesquisas com E eu teria que armazenar numa outra estrutura de dados que contasse a quantidade de termos que apareçam em determinado documento.

Num caso de busca por proximidade, tem outro problema: precisaria informar quais as posições em que determinado termo aparece e seria necessário checar se a outra é posterior.

- DAAT: inverted lists processed in parallel
  - Uses less memory (no accumulators)
  - Handles complex queries (Boolean, proximity)
  - De facto choice for modern search engines

## Naïve DAAT

- Inverted list processed in parallel
  - One document scored at a time

Se é um AND, só processa se tá presente nos 3. Senão, não processa.

Se é um OR, processa todos os marcados no menor índice.

- A: **_[1:3]_**, [2:3], [3:4], [8:4]
- B: **_[1:4]_**, [5:2], [7:2], [8:5], [9:2], [11:5]
- C: **_[1:6]_**, [2:5], [5:3], [6:7], [10:1], [11:7]
- scores: [1:13]

---

[Explicar o que os slides querem dizer]

- A: _[1:3]_, **_[2:3]_**, [3:4], [8:4]
- B: _[1:4]_, **[5:2]**, [7:2], [8:5], [9:2], [11:5]
- C: _[1:6]_, **_[2:5]_**, [5:3], [6:7], [10:1], [11:7]

- scores: [1:13], [2:8d]

---

21

## What if we want only the top $k$ results?

Se eu ordenasse dos documentos com maior e menor score por palavra, poderia facilitar na busca por palavras únicas. Porém o traversal em postings de mesmo documento fica prejudicada.

## Dynamic pruning

- Dynamic pruning strategies aim to make scoring faster
- by only scoring a subset of the documents
  - Assume user is only interested in the top $k$ results
  - Check if a document can make it to the top $k$
  - Early terminate (or even skip) unviable documents

## Effectiveness guarantees

MORE EFFECTIVE

- **Safe:** exhaustive (i.e. no pruning) matching
- **_Score safe:_** top $k$ with correct scores
- **_Rank safe:_** top $k$ with correct order
  - > Não preciso manter o mesmo score desde que a ordem esteja a mesma
- **Set safe:** top $k$ with correct documents
  - Sem garantia de que os documentos corretos estão em ordem
- **Unsafe:** no correctness guarantees whatsoever

LESS EFFECTIVE

## MaxScore [Turtle and Flood, IPM 1995]

- In a multi-term query, not all terms are worth the same
  - Some will be "essential" for scoring documents
  - Others will be "non-essential" terms

Dessa forma, os termos não essenciais não precisariam ser computados.

- Key idea
  - Traverse "essential" terms first (in DAAT mode)
  - Check "non-essential" terms only if promising

### MaxScore $(k = 2)$

- Each list has an upper bound (aka max-score)

  - Top $k$ results have acceptance threshold $\theta$
  - terms sorted by inc. max-score
  - pivot chosen as least term that cumulatively beats threshold $\theta$
  - terms at least as promising as the pivot deemed "essential"
    - others are "non-essential"

- > A: (CumulativeMS: 4) (MaxScore: 4) [1:3], [2:3], [3:4], [8:4]
- B: (CumulativeMS: 9) (MaxScore: 5) [1:4], [5:2], [7:2], [8:5], [9:2], [11:5]
- C: (CumulativeMS: 16) (MaxScore: 7) [1:6], [2:5], [5:3], [6:7], [10:1], [11:7]

Top $k = 2$: [] []

$\theta = 0$

---

- process "essential" lists first
- process "non-essential" lists only if they are promising
- update top $k$ results and $\theta$
- update pivot on $\theta$ changes

- > A: (CumulativeMS: 4) (MaxScore: 4) **[1:3]**, [2:3], [3:4], [8:4]
- B: (CumulativeMS: 9) (MaxScore: 5) **[1:4]**, [5:2], [7:2], [8:5], [9:2], [11:5]
- C: (CumulativeMS: 16) (MaxScore: 7) **[1:6]**, [2:5], [5:3], [6:7], [10:1], [11:7]

Top $k = 2$: [] []

$\theta = 0$

---

Promising seria apenas se o máximo das listas não promissoras for suficiente para fazer com que o documento computado das promissoras seja grande o bastante pra fazer com que ele ultrapasse o $\theta$.

Uma potencial otimização seria fazer um maxscore mais justo que é atualizado assim que todos os items que têm esse maxscore já foram processados, assim reduzindo os MaxScores.

Outra potencial otimização seria atualizar os MaxScores acumulados quando algumas listas já forem exauridas.

Dúvida 1: Se no pivô o posting analisado já superar o threshold, eu ainda somaria com os não essenciais?

Resposta 1: Sim. Porque senão, esse calculado poderia ser indevidamente descartado.

Dúvida 2: Se empatar, substitui?

Resposta 2: Nesse caso não, só substitui se for superior.

---

Se coincidisse dos melhores documentos estarem no topo, logo o Threshold seria atualizado e subiria. Senão, demoraria pra convergir.

---

...

---

30

### MaxScore Limitations

- MaxScore relies on "non-essential" terms for skipping
  - Naïve DAAT performed on "essential" terms
- It may take long for a term to become "non-essential"
  - It may be a poor term (low max-score)
  - It may get hard to make the heap (high threshold)
- Hindered efficiency, particularly for long queries

## WAND [Broder et al., CIKM 2003]

Weak AND

- MaxScore fully evaluates "essential" lists
  - Not all documents in "essential" lists are promising
- Key idea
  - Evaluate documents (not lists) if they are promising (i.e. have a promising cumulative upper bound)

### WAND $(k = 2)$

- Each list has an upper bound (aka max-score)
  - Top $k$ results have acceptance threshold $\theta$
  - terms sorted by inc. docid
  - pivot chosen as least term that cumulatively beats threshold $\theta$
  - terms managed dynamically
    - lists synced to pivot document
    - terms re-sorted on every move

---

...

---

30

5 / 16 postings skipped $\approx$ 31% savings

### In-memory WAND [Fontoura et al., VLDB 2011]

- Substantial reduction in processed postings
  - Particularly efficient for long queries
- But latency only improved for disk-based indexes
  - No memory paging for in-memory indexes!
  - Pivot management offsets gains in skipping
- Solution: align all cursors before a new re-sort

### Block-Max WAND [Ding and Suel, SIGIR 2011]

[Imagem gráfico de docid x score: erro absoluto]

1

---

[Imagem gráfico de docid x score: Erro absoluto médio]

2

---

3

### Variable-sized blocks [Mallia et al., SIGIR 2017]

- max-score of $t$: 17
  - block max-score of $b_1$: 12
  - block max-score of $b_2$: 17
  - block max-score of $b_3$: 11
- mean absolute error: 6.2

### Impact-sorted blocks [Ding and Suel, SIGIR 2011]

- max-score of $t$: 17
  - block max-score of $b_1$: 17
  - block max-score of $b_2$: 11
  - block max-score of $b_3$: 4
- mean absolute error: 2.7

### Docid reassignment [Ding and Suel, SIGIR 2011]

- max-score of $t$: 17
  - block max-score of $b_1$: 17
  - block max-score of $b_2$: 11
  - block max-score of $b_3$: 4
- mean absolute error: 2.7

### Impact-layered blocks [Ding and Suel, SIGIR 2011]

- max-score of $t$: 17
  - block max-score of $b_1$: 17
  - block max-score of $b_2$: 11
  - block max-score of $b_3$: 4
- mean absolute error: 2.7

## Summary - Aula 08

- Efficient matching for subsecond response times
  - Skip postings (or lists) that won't help make the top $k$
- Carefully play with upper bounds and thresholds
  - Can be extended with blocks, layers, list orderings
- Can always trade-off safety for efficiency
  - Anytime ranking for QoS [Lin and Trotman, ICTIR 2015]

## References - Aula 08

- [[Link_2015_Bae]][Link_2015_Bae] Scalability Challenges in Web Search Engines, Ch. 4 Cambazoglu and Baeza-Yates, 2015
- [[Link_2018_Mac]][Link_2018_Mac] Efficient Query Processing Infrastructures Tonellotto and Macdonald, SIGIR 2018
- [[Link_2018_Ton]][Link_2018_Ton] Efficient Query Processing for Scalable Web Search Tonellotto et al., FnTIR 2018

---

- [[Link_1995_Tur]][Link_1995_Tur] Query evaluation: strategies and optimizations Turtle and Flood, IP&M 1995
- [[Link_2003_Bro]][Link_2003_Bro] Efficient query eval. using a two-level retrieval process Broder et al., CIKM 2003
- [[Link_2011_Din]][Link_2011_Din] Faster top-k document retr. using block-max indexes Ding and Suel, SIGIR 2011

[Link_2015_Bae]: https://link.springer.com/book/10.1007/978-3-031-02298-2
[Link_2018_Mac]: https://dl.acm.org/doi/10.1145/3209978.3210191
[Link_2018_Ton]: https://www.nowpublishers.com/article/Details/INR-057
[Link_1995_Tur]: https://www.sciencedirect.com/science/article/pii/030645739500020H?via%3Dihub
[Link_2003_Bro]: https://dl.acm.org/doi/10.1145/956863.956944
[Link_2011_Din]: https://dl.acm.org/doi/10.1145/2009916.2010048

## Coming next: Vector Space Models
