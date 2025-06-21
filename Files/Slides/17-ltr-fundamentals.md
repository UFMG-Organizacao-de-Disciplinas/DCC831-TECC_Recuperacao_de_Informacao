# Aula 17 - 19/05/2025 - Learning to Rank: Fundamentals

## The ranking problem

- q
- f(q, d)
- d

## Many solutions

- Topicality models
  - VSM, BM, LM, DFR, MRF, LSI, DESM, ...
- Quality models
  - PageRank, in-links, spam, ...
- No silver bullet
  - Different models excel at different scenarios

## How to combine multiple models?

## Ensembling the cues

- Linear combination?
  - $$f(q, d) = \alpha_1 f_{BM25}(q, d) + \alpha_2 f_{PR}(q, d)$$
- How to fit $\alpha_1$ and $\alpha_2 = (1 - \alpha_1)$?
  - $\{\alpha_1 = 0.3, \alpha_2 = 0.7\} \rightarrow \{MAP = 0.2, nDCG = 0.6\}$
  - $\{\alpha_1 = 0.5, \alpha_2 = 0.5\} \rightarrow \{MAP = 0.1, nDCG = 0.5\}$
  - $\{\alpha_1 = 0.7, \alpha_2 = 0.3\} \rightarrow \{MAP = 0.4, nDCG = 0.7\}$

## What if we have thousands of models?

- Mr. Singhal has developed a far more elaborate system for ranking pages, which involves more than 200 types of information, or what Google calls "signals."
  - [^1] Saul Hansell, New York Times, June 2007

## Learning to rank

- q
- f(x)
- d

---

- Feature-based representation
  - Individual models as ranking "features"
- Discriminative learning
  - Effective models learned from data
  - Aka machine-learned ranking

---

- Actively researched over the last couple of decades
  - Both by academia as well as industry players
- Why didn't it happen earlier?
  - Limited availability of training data
  - Poor machine learning techniques
  - Too few features to show value

## Query processing overview

- query
  - feedback
- Understanding
  - Knowledge Resources
- Query logs
  - Knowledge bases
  - User preferences
- Matching
  - Index
- Scoring
  - Ranking Model

## Discriminative learning framework

[Imagem: Diagram showing training, validation, and test data flow through scoring and learning components]

## Building blocks

- Goal is to learn a ranking model
  - $$f : \mathcal{X} \to \mathcal{Y}$$
- That minimizes some loss function
  - $$L : f(\mathcal{X}) \times \mathcal{Y} \to \mathcal{R}$$
- $\mathcal{X}$: input space
- $\mathcal{Y}$: output space
- $\mathcal{F}$: hypothesis space
- $L$: loss function
- $O$: optimizer

---

[Imagem: Diagram showing input space X, output space Y, hypothesis f(·), and prediction process]

## Input space (X)

- LTR takes as input feature vectors
  - $$x \in X$$
  - $$x = \Phi(q, d)$$
- Example features:
  - $f_{BM25.title}(q, d)$
  - $f_{BM25.body}(q, d)$
  - $f_{BM25.anchor}(q, d)$
  - $f_{PageRank}(q, d)$

## Ranking features

- Query-dependent (depend on $\langle q, d \rangle$)
  - BM25, LM, PL2, ...
- Query-independent (depend on $d$)
  - PageRank, readability, spaminess, ...
- Query features (depend on $q$)
  - Query length, query type, ...

## Output space (y)

- LTR may produce different outputs
  - $$y \in Y$$
- Each scalar $y$ labels a training instance

## Data labeling alternatives

- Labeling of individual documents
  - Binary judgments (non-rel, relevant)
    - $y \in \{0,1\}$
  - Graded judgments (non-rel, ..., perfect)
    - $y \in \{0,1,2,3,4,5\}$

---

- Labeling of pairs of documents
  - Implicit judgments
    - d1 d3 > d1
    - d2 d3 > d2
    - d3 ∨ d3 > d4
    - d4 d3 > d5
    - d5

---

- Creation of list
  - List (or permutation) of items is given
  - Ideal, but difficult to implement

## Hypothesis space ($\mathcal{F}$)

- Goal is to learn a ranking model
  - $$f : x \to y$$
- A hypothesis $f \in \mathcal{F}$ could be any function
  - Linear functions
  - Non-linear functions (trees, networks)

---

- Linear hypotheses
  - $$f(x) = w^T x + b$$
  - $w$ is a weight vector
  - $b$ is a scalar bias

---

- Tree-based hypotheses
  - $$f(x) = \sum_k b_k 1(x \in R_k)$$
  - $k$ is one of the leaves in the tree
  - $b_k$ is the value predicted in region $R_k$
  - $1(\cdot)$ is the indicator function

---

- Neural network hypotheses
  - $$f(x) = \sigma_2(W_2\sigma_1(W_1x + b_1) + b_2)$$
  - $W_k$ is a weight matrix
  - $b_k$ is a bias vector
  - $\sigma_k$ is an activation function

## How to find the best $f(x)$?

- Look for the one with minimum loss

## Loss function (L)

- Loss as a measure of error
  - $$L(\hat{y}, y) = L(f(x), y)$$
- Many options once again
  - 0-1 loss:
    - $$L(\hat{y}, y) = 1(y \neq f(x))$$
  - Absolute loss:
    - $$L(\hat{y}, y) = |y - f(x)|$$
  - Square loss:
    - $$L(\hat{y}, y) = (y - f(x))^2$$

## Example: square loss

[Imagem: Graph showing square loss function]

## Optimizer

- Coordinate methods
  - Line search, one coordinate at a time
- Gradient methods
  - Walk downhill, all coordinates together
- Boosting methods
  - Upweight difficult examples

## Learning algorithms

[Imagem: Timeline of learning to rank algorithms from 1999-2008]

---

- **Pointwise**
  - $X$: single documents
  - $Y$: scores or class labels
- **Pairwise**
  - $X$: document pairs
  - $Y$: partial orders
- **Listwise**
  - $X$: document collections
  - $Y$: ranked document list

## Pointwise approaches

- Reduce ranking to regression or classification
  - Assume relevance is query-independent
- In practice, relevance is query-dependent
  - Utility of a feature may also be query-dependent
  - By putting documents associated with different queries together, the training process may be hurt

## Pairwise approaches

- Reduce ranking to classification on document pairs associated with the same query
  - No longer assume independent relevance
- Unique properties of ranking not fully covered
  - Number of instance pairs varies across queries
  - Importance of errors varies across ranking positions

## Listwise approaches

- Perform learning directly on document list
  - Treats ranked lists as learning instances
- Two major approaches
  - Define listwise loss functions
  - Directly optimize IR evaluation measures (current state-of-the-art)

## Recap

- Goal is to learn a ranking model
  - $$f : \mathcal{X} \to \mathcal{Y}$$
- That minimizes some loss function
  - $$L : f(\mathcal{X}) \times \mathcal{Y} \to \mathcal{R}$$
- $\mathcal{X}$: input space
- $\mathcal{Y}$: output space
- $\mathcal{F}$: hypothesis space
- $L$: loss function
- $O$: optimizer

## Summary

- Learning to rank has been around for a few decades, but has only recently become hot
  - More data, better resources, better algorithms
- Machine learned ranking over many features easily beats traditional hand-designed ranking models
  - Lots of open directions

## Open directions

- Deep learning
  - Feature learning (vs. feature engineering)
- Online learning
  - Incremental, exploration-exploitation models
- Structured learning
  - Diversity, context-awareness

## References

- Learning to rank for information retrieval - Liu, FnTIR 2009
- Learning to rank for information retrieval - Liu, 2011
- Learning to rank for information retrieval and natural language processing - Li, 2014

## Coming next: Learning to Rank: Pointwise
