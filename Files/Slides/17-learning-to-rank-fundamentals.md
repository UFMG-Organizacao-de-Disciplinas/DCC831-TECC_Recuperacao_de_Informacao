# Aula 17 - 19/05/2025 - Learning to Rank: Fundamentals

## The Ranking Problem

...

## Many Solutions

- Topicality
  ...
- Quality
  ...
- No silver
  ...

- [JV] Existem casos em que uma solução vai bem em um método, mas vai mal em outro. Existe a possibilidade de tentar combinar as soluções em uma melhor

## How to combine multiple models?

### Ensembling the cues

- Linear combination?
  - [JV]
    - Mas que peso dar?
      - Depende.
      - Possibilidade 1: valor complementar
- MAP; nDCG
  - [JV]
    - Média desses valores para um conjunto de testes

### What if we have thousands of models?

> Mr. Singhal

- [JV] Grande custo computacional

## The Ranking Problem (2)

...

## Leaning to Rank

- $f(x)$
  - [JV]
    - Como condensar esses vários scores em um só?

---

- Feature-based

---

- Active Researched
  - Both by
  - [JV]
    - RI já pesquisa sobre isso há anos. Pelo menos desde a década de 90.
    - Parte do trabalho passou a ser engenharia de features, que acabou sendo mais uma das entradas no vetor de métricas de relevância.
- Why didn't it...
  - Limited...
  - Poor...
  - Too...

## Query Processing Overview

...

- [JV] A pergunta é: como fazer esse modelo de ranqueamento?

## Discriminative Learning Framework

[Diagrama]

- [JV] Tem vários $q_1$ porque cada um deles estaria fazendo referência a um par de consulta e documento.

- [JV]
  - Para determinados scores X, temos um rótulo Y.
  - Esse Rótulo Y seria um nível de relevância de determinado documento para uma determinada consulta.
  - Várias dessas instâncias rotuladas são usadas para treinar o modelo.
  - Outras dessas instâncias são usadas para testar o modelo. (Validação)
  - Esses dados são usados para haver o aprendizado. Após esse aprendizado de padrões, o modelo pode ser usado para dar os scores para novos documentos, onde teremos um label $\hat{y} = f(x)$.
  - Esse processo de aprendizado pode ser caro, mas na hora de aplicar o modelo já treinado, é mais barato.
  - O problema de que esse aprendizado seja feito de modo offline é que, se ele não for re-treinado, ele se torna obsoleto. Faria sentido se houvesse uma evolução contínua do modelo.
  - Outro detalhe é que essa função aprendida é genérica. Uma alternativa seria um aprendizado por reforço especializado para um usuário específico.

### Building Blocks

- Goal is
  - $f: x \to y$
- That...
  - $\mathcal{L}: f(x) \times y \to \mathbb{R}$
    - x: input space
    - y: output space
    - f: hypothesis space
    - $\mathcal{L}$: loss function
    - $\mathcal{O}$: optimizer
    - R: número real
    - [JV]
      - Para cada função e exemplos rotulados, a função de perda avalia a função do ranking.

---

[Diagrama]

- [JV]
  - O Diagrama mostra o conjunto dos inputs que levam ao espaço de outputs;
  - A Loss function calcula a distância entre o predito e o esperado.

#### Input Space ($\mathcal{X}$)

- LTR takes as input feature vectors
  - $x \in \mathcal{X}$
  - $X = \Phi (q, d)$
    - $q$: query
    - $d$: document
    - $\Phi$: feature extraction function
      - $\Phi_1$: BM25.title(q, d)
      - $\Phi_2$: BM25.body(q, d)
      - BM25.anchor(q, d)
      - PageRank(q, d)
    - [JV]
      - A função de extração de features é a função que vai pegar os documentos e as consultas e vai gerar um vetor de valores em
      - Existe uma ideia de que a Google por exemplo pode ter reduzido o tamanho do vetor de features ao substituir algumas features por grupos de LLMs.
      - Ele brincou sobre cobrar uma questão na prova sobre essa mudança dos vetores de features do google.

##### Ranking Features

- Query-dependent...
  - BM25, LM, PL2, ...
- Query-independent...
  - PageRank...
    - [JV]
      - No geral serve como critério de desempate. Um Boost, uma promoção.
- Query feature...

  - Query length...

- [JV]
  - Em qual dos casos poderíamos usar uma LLM?
    - Bom, nas 3. Mas em qual delas seria mais interessante?
    - Nas Query-Independent, podendo processar offline, e os diversos scores dos documentos podem ser armazenados e consultá-los é muito eficiente.
    - Já os Query Features são feitos online em sua maioria, pois depende da informação do usuário

#### Output Space ($\mathcal{Y}$)

##### Data Labeling Alternatives

- Labeling of...
  - Binary...
    - $y \in \{0, 1\}$
  - Graded...
    - $y \in \{0, 1, 2, 3, 4, 5\}$
    - [JV]
      - Esse daqui tende a ter uma semântica que facilida aos humanos que irão verificar esse output. Ex.: "É perfeitamente o que o usuário procurava", "Não é exato, mas atende bem", etc.

---

- Labeling of pairs of documents
  - Implicit judgments
    - $d_1$
    - $d_2$
    - $d_3$ ✔️
    - $d_4$
    - $d_5$
      - [JV] Não necessariamente esse clique significa que o usuário foi bom, mas é um indicativo de que o usuário gostou do resultado e que foi mais relevante que os outros. Principalmente com relação aos anteriores.
    - $d3 \succ d_1$
    - $d3 \succ d_2$
    - ~~$d3 \succ d_4$?~~
    - ~~$d3 \succ d_5$?~~

---

- Creation of list
  - List (or permutation)...
  - Ideal, but difficult...

#### Hypothesis Space ($\mathcal{F}$)

- Goal is...
  - $f: \mathcal{X} \to \mathcal{Y}$
- A hypothesis $f \in \mathcal{F}$...
  ...

---

[Imagem Matemática]

- Linear Hypotheses
  - $f(x) = w^T x + b$
    - $w$ is a weight vector
    - $b$ is a scalar bias
  - $f(x)$ retorna um escalar

---

[Grafo em árvore de decisão (?): Árvore de regressão simples]

- Tree-based Hypotheses

  - $f(x) = \sum_{k} b_k 1 (x \in R_k)$
  - $k$ is one...
  - $b_k$ is...
  - 1($\cdot$)

- [JV]
  - O Random Forest/Ensemble de árvores, seria rodar essa árvore de regressão simples só que várias e ao mesmo tempo e calcular a média dos resultados.

---

- [Grafo de Rede Neural fully connected]

  - Input (3 nós)
  - Hidden (4 nós)
  - Saída (1 nó)
  - [JV]
    - Cada aresta é um peso que é multiplicado ao input. E a junção de todas essas arestas representaria uma matriz.

- Neural Networks
  - $f(x) = \sigma_2 (W_2 \sigma_1 (W_1 x + b_1) + b_2)$
    - Sigma é uma "função de ativação" que ajuda a encontrar "padrões mais sofisticados"
    - W_2 seriam os pesos da segunda camada

## References

## Coming Next
