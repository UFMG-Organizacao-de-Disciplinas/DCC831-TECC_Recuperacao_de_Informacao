# Pretrained Transformers for Text Ranking: BERT and Beyond

- Andrew Yates, Rodrigo Nogueira, and Jimmy Lin
- @andrewyates @rodrigfnogueira @lintool
- UNIVERSITY OF WATERLOO

## Outline

- Part 1: Background
  - (text ranking, IR, ML)
- Part 2: Ranking with relevance classification
- Part 3: Ranking with dense representations
- Part 4: Conclusion & future directions

## monoBERT: BERT reranker

- We want:
  - $s_i = P(\text{Relevant} = 1|q, d_i)$
- Query $q$
- Text $d_i$
- $D \times 2$ softmax
  - $s_i = \text{softmax}(T_{[CLS]}W + b)_1$
  - Non-relevant
  - Relevant

## Once monoBERT is trained

- $H_0$
- $R_0$
- $H_1$
- $R_1$
- BM25
  - $d_1$
  - $d_2$
  - $d_3$
- Inverted Index
  - $d_4$
  - $d_5$
- $q$
- mono BERT
  - $s_i$
  - $d_1$
  - $d_2$
  - $d_3$
  - $d_4$

## BERT's Limitations

- Cannot input entire documents
  - What do we input?
  - & how do we label it?
- Need separate embedding for every possible position
  - Restricted to indices 0-511
- [Imagem: Token Embeddings, Segment Embeddings, Position Embeddings diagram]

## Multi-stage ranking pipeline

- Identify candidate documents
- Rerank

## From Single to Multiple Rerankers

- Texts
  - Inverted Index
  - Queries
  - Initial Retrieval
  - Candidate Texts
  - Reranker
  - Ranked List
- Texts
  - Inverted Index
  - Queries
  - Initial Retrieval
  - Candidate Texts
  - Reranker
  - Ranked Candidates
  - Reranker
  - Reranker
  - Ranked List

## Why Multi-stage?

- Trade-off between effectiveness (quality of the ranked lists) and efficiency (retrieval latency)
  - Fewer Candidates

## Multi-stage with duoBERT

- $H_0$
- $R_0$
- $H_1$
- $R_1$
- $H_2$
- $R_2$
- $q$
- BM25
  - $d_1$
  - $d_2$
  - $d_3$
- Inverted Index
  - $d_4$
  - $d_5$
- $q$
- mono BERT
  - $d_5$
  - $d_2$
  - $d_3$
- $q$
- duoBERT
  - $d_5$
  - $d_3$
- Doc Pairwise
  - $d_5$
  - $d_1$
  - $d_2$
  - $d_3$
- duo BERT

  - $d_j$
  - $d_i$
  - $d_j$
  - $P_{i,j}$

- **Nogueira, Yang, Cho, Lin. Multi-stage document ranking with bert. 2019.**

## duoBERT's Input Format

- $D > 2$
- $T_{[CLS]}$
- $U_1$
- $U_2$
- $U_3$
- $T_{[SEP1]}$
- $V_1$
- $V_m$
- $T_{[SEP2]}$
- $X_1$
- $X_m$
- $T_{[SEP3]}$
- duoBERT
- $E_{[CLS]}$
- $E_1$
- $E_2$
- $E_3$
- $E_{[SEP1]}$
- $F_1$
- $F_m$
- $E_{[SEP2]}$
- $G_1$
- $G_n$
- $E_{[SEP3]}$
- Token Embeddings
  - [CLS]
  - $q_1$
  - $q_2$
  - $q_3$
  - [SEP]
  - $d_i'$
  - $d_m'$
  - [SEP]
  - $d_i'$
  - $d_i'$
  - [SEP]
- Segment Embeddings
  - $E_A$
  - $E_A$
  - $E_A$
  - $E_A$
  - $E_B$
  - $E_B$
  - $E_B$
  - $E_C$
  - $E_C$
- Position Embeddings
  - $P_0$
  - $P_1$
  - $P_2$
  - $P_3$
  - $P_4$
  - $P_5$
  - $P_{m+4}$
  - $P_{m+5}$
  - $P_{m+6}$
  - $P_{m+7}$
  - $P_{m+8}$
  - $P_{m+9}$
- Query
- Text $d_i$
- Text $d_j$

## Training duoBERT

- **Loss:**
  - $L_{\text{duo}} = - \sum_{i \in J_{\text{pos}}, j \in J_{\text{neg}}} \log(p_{i,j}) - \sum_{i \in J_{\text{neg}}, j \in J_{\text{pos}}} \log(1 - p_{i,j})$
- CLS
  - Query $q$
  - SEP
  - text $d_i$
  - SEP
  - text $d_j$
- duoBERT

## Inference with duoBERT

- $p_{1,2} = p(d_1 > d_2 | q)$
- $d_1$
- $q$
- $d_2$
- duo BERT
- $d_3$
- $d_2$
- $d_1$
- R1 monoBERT
  - $d_1$
  - $d_2$
  - $d_3$
- R2
  - $d_1$
  - $d_2$
  - $d_3$
- Pairwise aggregation:
  - $s_1 = p_{1,2} + p_{1,3}$
  - $s_2 = p_{2,1} + p_{2,3}$
  - $s_3 = p_{3,1} + p_{3,2}$
- Text Pairs

## Sparse Representations

- Task: Estimate the relevance of text $d$ to a query $q$:
  - $q = "fix my air conditioner"$
  - $d = "... AC repair ..."$
  - $BM25(q, d) = \sum_{t \in q \cap d} \log \frac{N - df(t) + 0.5}{df(t) + 0.5} \cdot \frac{tf(t, d) \cdot (k_1 + 1)}{tf(t, d) + k_1 \cdot (1 - b + b \cdot \frac{L_d}{L})}$
- Advantages:
  - Fast to retrieve candidates from an inverted index because $q$ is usually short.
  - Fast to compute because $q \cap d$ is usually small.
- Disadvantage: Terms need to match exactly.

## Dense Representations

- $q = "fix my air conditioner"$
- $d = "... AC repair ..."$
- Encoder
  - $\eta(q)$
  - $\eta(d)$
- $\phi$ is a similarity function (e.g., inner product or cosine similarity)
  - $\phi(\eta(q), \eta(d)) \rightarrow$ ideally measures how relevant $q$ and $d$ are to each other.

## Types of Encoders: Cross-encoder

- [Imagem: Cross-encoder architecture diagram]

## Types of Encoders: Bi-encoder

- [Imagem: Bi-encoder architecture diagram]

## Nearest Neighbor Search

- Task: find the top k most relevant texts to a query
- Query
- Texts
  - $\phi(\eta(q), \eta(d_1))$
  - $\phi(\eta(q), \eta(d_{|C|}))$
- Top k
- Brute-force search:
  - We often need to search many (e.g.: billions) of texts.
  - Brute-force won't scale.

## Approximate Nearest Neighbor Search

- Exchange accuracy for speed
  - E.g.: k-means
- Query $\eta(q)$
- Centroids
  - $\phi(\eta(q), \eta(c_1))$
  - $\phi(\eta(q), \eta(c_2))$
  - $\phi(\eta(q), \eta(c_3))$
- $\phi(\eta(q), \eta(d_1))$
- $\cdots$
- $\phi(\eta(q), \eta(d_m))$
- In practice, ANN implementations are more complicated.
- We assume a fast dense retrieval library is available (e.g.: Faiss, Annoy, ScaNN).

## Distance-based Transformer Representations

- Key characteristic
  - Simple similarity function -> inner (dot) product, cosine similarity, ...
  - $\phi(u,v) = \eta(u) \cdot \eta(v)$
  - Compatible with ANN search.
- **Johnson, Douze, Jégou. Billion-scale similarity search with GPUs. arXiv 2017.**

## Distance-based: SentenceBERT

- Softmax classifier
  - (u, v, |u-v|)
- pooling
  - BERT
  - Sentence A
  - v
  - pooling
  - BERT
  - Sentence B
- -1 ... 1 cosine-sim(u, v)
- pooling
  - BERT
  - Sentence A
  - v
  - pooling
  - BERT
  - Sentence B
- Classification
- **Reimers, Gurevych. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. EMNLP 2019.**

## Comparison-based: ColBERT

- Sum
- M
- U
- MaxSim operator
  - Encoder
  - $V_1$
  - $V_2$
  - ...
  - $V_m$
  - Encoder
- **Khattab, Zaharia. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. SIGIR 2020.**

---

- Sum
- Max Pool
- MaxSim:
  - Sim-mat max pooling (along query dimension)
  - $s_{q,d} = \sum_{i \in \eta(q)} \max_{j \in \eta(d)} \eta(q)_i \cdot \eta(d)^T_j$
- **Khattab, Zaharia. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. SIGIR 2020.**

---

- Compatible with ANN?
  - Unclear
  - Data-dependent
  - 70x faster than BERT-large
- Bag-of-Words (BoW) Model
  - BoW Model with NLU Augmentation
  - Neural Matching Model
  - Deep Language Model
  - ColBERT (ours)
- BERT-large
  - BERT-base
- Outer
  - Duel
  - fT+ConvKNRM
  - ColBERT (full retrieval)
  - BM25
  - KNRM/doc2query
  - DeepCT
  - docTTTTTquery
  - ColBERT (re-rank)
- MRR@10 0.15 0.20 0.25 0.30 0.35 0.40
- **Khattab, Zaharia. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. SIGIR 2020.**

---

- MS MARCO Passage Development
- Latency (ms)
- Method
  - MRR@10
  - Recall@1k
  - (ms)
- BM25 (Anserini, top 1000)
  - 0.187
  - 0.861
  - 62
  - monoBERTLarge
    - 0.374
    - 0.861
    - 32,900
- FastText + ConvKNRM
  - 0.290
  - 90
- doc2query-T5
  - 0.277
  - 0.947
  - 87
- ColBERT (over BERTBase)
  - 0.360
  - 0.968
  - 458

## Document Preprocessing Techniques

- Query vs document expansion
- doc2query
- DeepCT
- DeepImpact

## Query reformulation as a translation task

- Query Language → Query Reformulator → Document Language
  - Hard: Input has little information
- Query Language → Document Translator → Document Language
  - Easier: Input has a lot of information

## doc2query

- Document
- seq2seq Transformer
- Query
- Supervised training:
  - pairs of <query, relevant document>
- **Nogueira, Yang, Lin, Cho. Document expansion by query prediction. 2019.**
- [Imagem: Source: Vaswani et al., 2017]

---

- Input: Document
  - Researchers are finding that cinnamon reduces blood sugar levels naturally when taken daily...
- In practice: 5-40 queries are sampled with top-k or nucleus sampling.
- Output: Predicted Query
  - does cinnamon lower blood sugar?
- Concatenate
  - -
  - Researchers are finding that cinnamon reduces blood sugar levels naturally when taken daily...
  - does cinnamon lower blood sugar?
- User's Query
  - foods and supplements to lower blood sugar
- Search Engine
  - Index
  - Better Retrieved Docs

## Results

| Model       | MARCO Passage (MRR@10) | TREC-DL 19 (nDCG@10) | TREC-COVID (nDCG@20) | Robust04 (nDCG@20) |
| ----------- | ---------------------- | -------------------- | -------------------- | ------------------ |
| BM25        | 0.184                  | 0.506                | **0.659**            | 0.428              |
| + doc2query | **0.277**              | **0.642**            | 0.6375               | **0.446**          |

- zero-shot: doc2query was trained only on MS MARCO

## DeepCT

- $\text{loss} = \sum_{t}(\hat{y}_{t,d} - y_{t,d})^2$
- Target Scores
  - $y_{t,d}$ | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
- Predicted Scores
  - $\hat{y}_{t,d}$ | 0.2 | 0.5 | 0.2 | 0.1 | 0.4 | 0.1 | 0.0 | 0.6 | 0.2 | 0.4 |
  - $\hat{\Delta}$
  - $D \times 1$
- Text d: The Geocentric Theory was proposed by the greeks under the guidance...
- Relevant query $q$: "who proposed the geocentric theory"
- **Dai, Callan. Context-aware sentence/passage term importance estimation for first stage retrieval. 2019.**

## Once DeepCT is trained

- Index
- New document: "Researchers Researchers ... finding finding ... that that ... cinnamon cinnamon ... reduces ..."
- Term Frequencies:
  - 10 | 0 | 20 | 10 | 90 | 80 | 90 | 100 | 40 | 20 | 0 | 10 | 40 |
- Predicted Scores $\hat{y}_{f,d}$
  - 0.1 | 0.0 | 0.2 | 0.1 | 0.9 | 0.8 | 0.9 | 1.0 | 0.4 | 0.2 | 0.0 | 0.1 | 0.4 |
- DeepCT (BERT)
- Text $d$:
  - Researchers are finding that cinnamon reduces blood sugar levels naturally when taken daily...

## Results on MS MARCO Passage Dev Set

| Model       | MRR@10 | R@1000 | BERT Inferences per doc |
| ----------- | ------ | ------ | ----------------------- |
| BM25        | 0.184  | 0.853  | -                       |
| + doc2query | 0.229  | 0.907  | 1                       |
| + doc2query | 0.277  | 0.944  | 40                      |
| DeepCT      | 0.243  | 0.913  | 1                       |

### DeepImpact: combining doc2query with DeepCT

- Input Document
  - Researchers are finding that cinnamon reduces blood sugar levels naturally when taken daily...
  - Researchers are finding that cinnamon reduces blood sugar levels naturally when taken daily...
  - doc2query → Output: Predicted Query
  - does cinnamon lower blood sugar?
- Expanded Document:
  - Researchers are finding that cinnamon reduces blood sugar levels naturally when taken daily...
  - does cinnamon lower blood sugar?
- Term Scorer (~DeepCT)
  - Researchers: 31, are: 0, finding: 4, that: 1, ...
  - Index → Better Retrieved Docs
- User's Query
  - foods and supplements to lower blood sugar
  - Search Engine → Beta → Total
- **Mallia, Khattab, Tonellotto, and Suel. Learning Passage Impacts for Inverted Indexes. 2021**

## Results on MS MARCO Passage Dev Set (2)

| Model           | MRR@10 | R@1000 | Latency (ms/query) |
| --------------- | ------ | ------ | ------------------ |
| BM25            | 0.184  | 0.853  | 13                 |
| DeepCT          | 0.243  | 0.913  | 11                 |
| doc2query       | 0.278  | 0.947  | 12                 |
| DeepImpact      | 0.326  | 0.948  | 58                 |
| BM25 + monoBERT | 0.355  | 0.853  | (GPU) 10,700       |

## Takeaways of Document Expansion

- Advantages:
  - Documents have more context than queries → easy prediction task.
  - Documents can be processed offline and in parallel.
  - Run on CPU at query time.
- Disadvantages:
  - Have to iterate over the entire collection.
  - Not as effective as rerankers (yet).

## Conclusions

- Pretrained Transformers showed significant improvements in various IR benchmarks.
- Reproduced and adopted by many in academia and industry.
- No doubt we are in the age of BERT and Transformers.

## Learn more in survey (& upcoming book)

- Pretrained Transformers for Text Ranking: BERT and Beyond
- by Jimmy Lin, Rodrigo Nogueira, and Andrew Yates
- [https://arxiv.org/abs/2010.06467](https://arxiv.org/abs/2010.06467)
- Thanks!
