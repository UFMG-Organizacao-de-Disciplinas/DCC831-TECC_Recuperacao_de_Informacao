# Aula 16 - 14/05/2025 - Diversification Models

## The ranking problem

- q
  - ● ● ● ●
  - ● ● ● ●
  - ● ● ● ●
  - ● ● ● ●

---

- q
- r
- e
- o

---

- q
- f(q, d)
- d

## Relevance-oriented ranking

- Probability Ranking Principle (PRP) (Cooper, 1971; Robertson, 1977)
  - Ranking information items by decreasing probability of relevance results in optimal retrieval effectiveness

[Imagem: maximum relevance]

## Ranking optimality

- PRP is optimal under certain assumptions
  - (Gordon & Lenk, 1991, 1992)
- **A1:** The probability of relevance is estimated with certainty, with no measure of risk
- **A2:** The probability of relevance is estimated independently for every document

## Limiting assumption A1

- **Assumption**
  - **A1** The probability of relevance is estimated with certainty, with no measure of risk
  - Limitation: **ambiguity**
    - Information needs and items are ambiguously represented (Turtle & Croft, 1996)

---

[Imagem: Google search results for "glass" showing diverse interpretations (material, smart device, film, etc.)]

## Query ambiguity

- Wikipedia lists over 30 meanings for 'glass'...
  - ... but we can only display '10 blue links'
    - [JV] Esse é um problema pra máquina de busca. Eles têm que tentar decifrar essa ambiguidade.
- Ambiguity is inherent to user queries...
  - ... but not all queries are equally ambiguous

---

- Glass
  - Material, Smart Device, Composer
- Google Glass

  - Features, Enterprise, Price

- **Ambiguous** query: Multiple **interpretations**
- **Underspecified** query: Multiple **aspects**
  - [JV]
    - Quem tá interessado em um, às vezes está também interessado em outro.

---

- **Ambiguous** query: 16% of web search queries (Song, 2009)
- **Underspecified** query: every query to some extent (Cronen-Townsend & Croft, 2002)
  - [JV]
    - Toda pesquisa tem um quê de underspecified.

## Limiting assumption A2

- **Assumption**
  - A2. The probability of relevance is estimated independently for every document
- Limitation: **redundancy**
  - "The relationship between a document and a query is necessary but not sufficient to determine relevance" (Goffman, 1964)

---3

[Imagem: Google search results for "glass" with a prompt asking if users need more results about the material]

- Any need for more results about the material?
  - Users are unlikely to inspect the results any further once they find something relevant (Craswell et al., 2008)
  - [JV] A relevância dos itens mais abaixo serão relevantes se as de cima dela são menos relevantes, visto que, se o usuário já encontrou o que precisa, não chegará a alcançar as que estão em baixo.

## Diversity and novelty (Clarke et al., 2008)

- **Diversity**
  - "the need to resolve ambiguity" [in the retrieval request]
- **Novelty**
  - "the need to avoid redundancy" [in the retrieval response]

## Greedy approximation

- Diversification is NP-hard (Agrawal, 2009)
  - [JV] maior quantidade de documentos que cubram ao máximo o universo
  - No efficient exact solution
- Constant-factor $(1 - 1/e \approx 0.632)$ approximation

  - Iteratively select a document that covers the most aspects yet uncovered by the previous documents

- [JV] Estratégia:
  - Constrói o ranking incrementalmente. Um documento por vez.
  - Será analisado quais áreas de interesse não foram cobertas ainda.

---

- $D \gets \varnothing$
- $\textbf{while } |D| < \tau \textbf{ do}$
  - $d^* \gets \argmax_{d \in R} f(q, d, D)$
  - $R \gets R \setminus \{d^*\}$
  - $D \gets D \cup \{d^*\}$
- $\textbf{end while}$
- $\textbf{return } D$

- [JV] O F buscará encontrar o quão relevante ele é dado os itens já existentes
  - No pior caso ainda tá distante do ótimo.
  - OK, não tá perfeito, mas quando que o pior carro ocorre?
  - Como já é bom o bastante, geralmente nem precisa analisar outros algoritmos.
  - Geralmente o foco está na $f(q, d, D)$.

---

- Approximation effective in practice (Carterette, 2009)
  - Minor deviations from the optimal solution Most approaches focus on producing effective diversification objectives $f(q, d, D)$

## A departure from the PRP

- Relevance no longer certain
  - Query ambiguously convey multiple needs
- Relevance no longer independent
  - Relevance of a document impacts other documents

## The ranking problem (2)

- q .- d
- $f(q, d)$

---

- q .- d
- $f(q, d, D)$

## The diversification problem

- q .- d & d1 & d2
- $f(q, d, D)$

## How to compute $f(q, d, D)$?

### Diversification dimensions

- Aspect representation
  - Implicit aspects
  - Explicit aspects
- Ranking strategy
  - Novelty-based
  - Coverage-based

#### Implicit aspects

- **Raw factors**
  - One-hot term vectors
    - [JV] Indica presença ou ausência de palavras
  - Count-based term vectors
- **Latent factors**

  - Topic models
  - Cluster models
  - Embeddings

- [JV]
  - Começa produzindo um rank
  - Depois analisa quão bem cobrem as possibilidades.

[Imagem]

#### Explicit aspects

[Imagem: Agora cada um dos critérios do documento têm relação com a query; Talvez cada unidade de item desse vetor do documento seriam as suas possíveis interpretações.]

- **Fixed aspects:** Query categories
- **Non-fixed aspects:** Query suggestions

### Ranking strategies

- **Coverage-based strategy:** Cover as many aspects as possible
  - [JV] Seria uma máxima revocação desses aspectos presentes nos documentos.
- **Novelty-based strategy:** Cover aspects as early as possible
- **Hybrid strategy:** Promote coverage and novelty

- [JV]
  - Estamos assumindo que o usuário não vai interagir com a especificação da query.
  - Não consideramos um histórico de pesquisas do usuário.
  - Estamos assumindo que é um usuário novo.
  - A abordagem de solicitar uma desambiguação do usuário é um caminho, e é usado na prática, mas nem todos vão querer usar, sendo assim, precisamos de uma abordagem que melhore a experiência do usuário.

#### Maximal Marginal Relevance (MMR) (Carbonell and Goldstein, 1998)

- Maximal Marginal Relevance

  - $f(q,d,D) = \lambda rel(q, d) - (1 - \lambda) \max_{d_j \in D} sim(d, d_j)$
    - [JV] O segundo é um score de novidade. O primeiro é uma métrica de score usual.
      - Na verdade, o segundo é uma métrica de similaridade entre os documentos, se for muito similar, é negativo.

- [JV]

  - Na prática, um documento pode ser tão distinto que não é relevante, porém acabaria entrando no ranking.

- [Imagem: gatinhos relevantes e novos]
  - **D**
    - Cinco gatinhos
  - **$R \setminus D$**
    - $d_1:$ (relevant, not novel) = (+, -)
    - $d_2:$ (relevant, novel) = (+, +)
    - $d_3:$ (non-relevant, novel) = (-, +)

#### xQuAD (Santos et al., 2010) [JV: doutorado dele]

- Explicit Query Aspect Diversification
  - $f(q,d,D) = (1 - \lambda) P(d|q) + \lambda P(d, \bar{D}|q)$
- [JV] Busca saber do histórico de usuários: de vocês que pesquisaram sobre isso, quantos quiseram isso?
  - $P(d, \bar{D}|q)$
    - Quão relevante é esse documento, considerando que todos os outro documentos não são relevantes?
  - Na época do doutorado dele, ele foi tentar analisar como o Google fazia.
  - E o Google, nas sugestões de pesquisa, ele se baseia no log das pesquisas anteriores.

---

[Imagem: gráfico de coberturas de relevância]

- [JV] Dada uma consulta, como definir os espaços?

---

[Imagem: Pesquisa no google]

---

[Imagem: Sugestões de pesquisa no google]

##### Estimating $P(d, \bar{D}|q)$

- $f(q, d, D) = (1 - \lambda) P(d|q) + \lambda \sum_{s \in S} P(s|q)P(d|q, s) \prod_{d_j \in D}(1 - P(d_j|q, s))$

  - $P(d|q)$: relevance of document $d$ to query $q$
  - $P(s|q)$: Importância de $s$ dada a query $q$
  - $P(d|q, s)$: Cobertura de $d$ para $s$ dado a query $q$
  - $\prod_{d_j \in D}(1 - P(d_j|q, s))$: Novidade de $\bar{d}_j$ dado $s$ e $q$

[Imagem: Grafo com os nós representando os documentos e as arestas representando as relações entre eles]

##### Example application

- $X^{(i)} = (1 - \lambda) R + \lambda D^{(i-1)} = (1 - \lambda) R + \lambda CN^{(i-1)}$
- How to estimate $R, C, N,$ and $\lambda$?
  - Advanced topics (see Santos et al., FnTIR 2015, Ch. 6)

---

- [JV]
  - R: scores dos documentos
    - Estimado usando o BM25
  - C: Matriz de cobertura. 5 documentos, duas interpretações (5x2)
    - Estimado usando o BM25
  - N: Inicialmente a primeira é mais importante que a segunda, assim dando um peso maior para a primeira coluna. Importância relativa dos dois aspectos.
  - $\lambda$: peso entre os dois = $0.5$

---

[Imagem: calculando os valores]

---

[Imagem: ranking final]

---

- $N^{(i)} = \diag(1 - C_r) N^{(i-1)}$
  - Busca reduzir os valores dos itens que estão abaixo dos mais relevantes.

---

---

- Input ranking: $R = (d_1, d_2, d_3, d_4, d_5)$
- Output ranking: $D = (d_2, d_1, d_4, d_3, d_5)$

## Summary

- Query ambiguity can harm search quality
  - Search result diversification can help
- NP-hard problem
  - Efficient greedy approximation
- Several objective functions in the literature

  - Explicit/hybrid approaches are the state-of-the-art

- [JV]
  - A abordagem dele era o estado da arte na época. Ele ganho 4 vezes seguidas na época.

## Open directions

- Aspect representation
  - Exploitation of dependencies between aspects
  - Document-driven aspect identification
- Diversification strategy
  - Personalized diversification
  - Discriminative diversification

## References

- [[1998_SIGIR]][1998_SIGIR] The use of MMR, diversity-based reranking for reordering documents and producing summaries - Carbonell and Goldstein, SIGIR 1998
- [[2010_Santos]][2010_Santos] Exploiting query reformulations for Web search result diversification - Santos et al., WWW 2010

[1998_SIGIR]: https://doi.org/10.1145/290941.291025
[2010_Santos]: http://dx.doi.org/10.1145/1772690.1772780

---

- [[2015_Santos]][2015_Santos] Search result diversification - Santos et al., FnTIR 2015

[2015_Santos]: http://dx.doi.org/10.1145/1772690.1772780

## Coming next: Learning to Rank: Fundamentals
