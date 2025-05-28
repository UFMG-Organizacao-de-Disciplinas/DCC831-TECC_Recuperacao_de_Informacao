# 20-neural-reranking.md

## Pretrained Transformers for Text Ranking: BERT and Beyond

- Andrew Yates, Rodrigo Nogueira, and Jimmy Lin
- @andrewyates @rodrigfnogueira @lintool
- UNIVERSITY OF WATERLOO

Based on the survey:
[Pretrained Transformers for Text Ranking: BERT and Beyond](https://arxiv.org/abs/2010.06467)

### Outline

- Part 1: Background (text ranking, IR, ML)
- Part 2: Ranking with relevance classification
- Part 3: Ranking with dense representations
- Part 4: Conclusion & future directions

## Text Ranking

### Definition

- Given: a piece of text (query, question, etc.)
- Rank: other texts by similarity
- Example: Web search (Google, Bing, etc.)

### Focus: Ad hoc Retrieval

- Input: query $q$ and text collection
- Output: ranked list maximizing a metric (e.g., nDCG)

### Other Problems

- **Question Answering**: Rank passages/answer spans
  - Example: "What causes precipitation to fall?" → "gravity"
- **Community QA**: Rank related questions/answers
  - Example: Quora threads
- **Text Recommendation**: Rank relevant articles

## Transformers

### Text Embeddings

- Input: Token sequences with [CLS] and [SEP]
- Output: Contextualized embeddings (e.g., $E\_{[CLS]}, E_1, \dots, E_n$)

### Pretrained Transformers

- Initialized via self-supervised pretraining (e.g., Masked LM)
- Fine-tuned for downstream tasks

## BERT for Relevance Classification (monoBERT)

### Architecture

- Input: Query-document pair
- Output: Relevance probability $P(\text{Relevant}=1|q, d_i)$
- Training loss:
  $$ L = -\sum*{j \in J*{\text{pos}}} \log(s*j) - \sum*{j \in J\_{\text{neg}}} \log(1 - s_j) $$

### Results

- TREC 2019 Passage Ranking:

| Model      | nDCG@10   | MAP       |
| ---------- | --------- | --------- |
| BM25       | 0.506     | 0.377     |
| + monoBERT | **0.738** | **0.506** |

## Handling Long Documents

### Approaches

1. **Score Aggregation** (BERT-MaxP, FirstP, SumP)
   - Split documents into passages → aggregate scores
2. **Representation Aggregation** (CEDR, PARADE)
   - Combine term/passage embeddings
3. **Long-Context Models** (Longformer, QDS-Transformer)
   - Sparse attention for longer sequences

### Results (2)

- Robust04 (nDCG@20):

| Method        | Title | Description |
| ------------- | ----- | ----------- |
| BERT-MaxP     | 0.469 | 0.529       |
| PARADE (Attn) | 0.513 | 0.552       |

## Multi-stage Reranking

### Why Multi-stage?

- Trade-off between effectiveness and efficiency

### duoBERT

- Pairwise document comparison:
  $$ p\_{ij} = p(d_i > d_j | q) $$
- Loss:
  $$ L*{\text{duo}} = -\sum*{i \in J*{\text{pos}}, j \in J*{\text{neg}}} \log(p\_{ij}) $$

### Inference

- Aggregate pairwise probabilities:
  $$ s*i = \sum*{j \neq i} p\_{ij} $$

## Takeaways

- BERT-based rerankers significantly improve IR metrics
- Long documents require aggregation strategies
- Multi-stage pipelines optimize effectiveness/efficiency

## References

- Devlin et al. (2019): BERT paper
- Nogueira et al. (2019): monoBERT/duoBERT
- PARADE (Li et al., 2020)
- [Ranking Survey](https://arxiv.org/abs/2010.06467)
