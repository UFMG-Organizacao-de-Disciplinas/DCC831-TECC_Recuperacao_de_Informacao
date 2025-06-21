# Aula 18 - 21/05/2025 - Learning to Rank: Algorithms; Learning to Rank: Pairwise and Listwise

## The ranking problem

- q -. d
- f(q, d)

## Learning to rank

- q -. d
- $f(x)$

---

- Feature-based representation
  - Individual models as ranking "features"
- Discriminative learning
  - Effective models learned from data
  - Aka machine-learned ranking

## Pointwise approach

- Several approaches
  - Regression-based
  - Classification-based
  - Ordinal regression-based
- [Representation:]
  - $q \to x_1, x_2, x_3, \ldots, x_n$
  - $\{(x_1, y_1), (x_2, y_2), (x_3, y_3), \ldots, (x_n, y_n)\}$

### Limitations of the pointwise approach

- Ranking requires getting relative scores right
  - Pointwise approaches learn absolute scores
- Higher positions should matter more than lower ones
  - Pointwise loss functions are agnostic to positions
- Queries should be equally important
  - Queries with many relevant documents dominate

## Pairwise approach

- Pairwise classification-based
  - RankNet
  - RankBoost
  - Ranking SVM
  - IR-SVM
- [Training data format]
  - $\{(x_1, x_2, 1), (x_2, x_1, 0), (x_1, x_3, 1), (x_3, x_1, 0), \ldots, (x_{n-1}, x_n, 1), (x_n, x_{n-1}, 0)\}$

### Pairwise classification-based [JV]

#### RankNet (Burges et al., ICML 2005)

- Shallow (2-layer) neural network
  - Sigmoid activations
  - Gradient descent optimizer
- Pairwise prediction probability:
  - $\hat{y}_{uv} = \frac{\exp(f(x_u) - f(x_v))}{1 + \exp(f(x_u) - f(x_v))}$
- Cross entropy loss:
  - $L(f; x_u, x_v, y_{uv}) = -\overline{y_{uv}} \log \hat{y}_{uv} - (1 - y_{uv}) \log (1 - \hat{y}_{uv})$

#### Ranking SVM (Herbrich et al., ALMC 2000; Joachims, KDD 2002)

- Hinge loss:
  - $L(f; x_u, x_v, y_{uv}) = \max(0, 1 - y_{uv}(f(x_u) - f(x_v)))$
- Inherits SVM properties:
  - Good generalization via margin maximization
  - Non-linear models via kernel trick

### Limitations of the pairwise approach

- Ignores graded relevance
  - Pairs labeled as binary (1/0) regardless of relevance grades
- Query dominance exacerbated
  - More documents → exponentially more pairs
- Ranking positions still not considered
  - Swaps at top/bottom treated equally

## Can we optimize ranking metrics directly?

### Ranking metrics generally non-differentiable

- Piecewise constant functions
  - Flat regions: zero derivative
  - Discontinuities: undefined derivative

### LambdaRank (Burges, NIPS 2006)

- Extends RankNet
- Uses ranking metrics (e.g., nDCG) to define gradient magnitudes
- Lambda function:
  - $\lambda_{uv} \equiv \frac{2^{y_u} - 2^{y_v}}{1 + \exp(f(x_u) - f(x_v))} |\Delta\text{nDCG}(x_u, x_v)|$

### LambdaMART (Wu et al., Tech. Report 2008)

- Gradient boosted trees (MART) + LambdaRank
- Objective:
  - $h_t^* = \text{argmin}_{h_t} \sum_{(x,y)} (h_t(x) - (-\alpha \nabla L(f_t))^2)$

## Listwise approach

- Two variants:
  - Metric-specific loss (optimize nDCG/MAP directly)
  - Non-metric-specific loss (optimize other listwise functions)

### Challenges in metric-specific ranking

- Evaluation metrics (nDCG, MAP) are non-differentiable
- Solutions:
  - Soften metrics (SoftRank)
  - Genetic programming (RankGP)
  - Boosting (AdaRank)

#### SoftRank (Taylor et al., WSDM 2008)

- Models scores as random variables:
  - $P(s_i) = N(s_i|f(x_i), \sigma_s^2)$
- Computes expected nDCG over all possible permutations

#### AdaRank (Xu and Li, SIGIR 2007)

- Boosting framework
- Updates query distribution based on metric performance:
  - $D_{t+1}(i) = \frac{\exp(-M(\sum_{s=1}^t \alpha_s f_s,x^{(i)},y^{(i)}))}{\sum_{j=1}^n \exp(-M(\sum_{s=1}^t \alpha_s f_s,x^{(j)},y^{(j)}))}$

### Non-metric-specific listwise ranking

- Representative algorithms:
  - ListNet
  - ListMLE
  - BoltzRank

#### ListNet (Cao et al., ICML 2007)

- Permutation probability:
  - $P_f(\pi^k) = \prod_{i=1}^{k-1} \frac{f(\pi_i)}{\sum_{j=i}^k f(\pi_j)}$
- Loss function: KL-divergence between predicted and ground-truth distributions

## Summary

- Listwise approaches better model ranking:
  - Treat all query documents as single instance
  - Explicitly consider ranking positions
- State-of-the-art on benchmarks (e.g., LETOR)

## RankLib tutorial

- Algorithms available:
  - 0: MART
  - 1: RankNet
  - 6: LambdaMART
  - 7: ListNet
- Usage example:

```bash
java -jar RankLib-2.18.jar -train MQ2008/Fold1/train.txt -ranker 6 -metric2t NDCG@10
```

## References

- Learning to rank for information retrieval
  - Liu, 2011
- Learning to rank for information retrieval and natural language processing
  - Li, 2014

## Coming next: Neural Models
