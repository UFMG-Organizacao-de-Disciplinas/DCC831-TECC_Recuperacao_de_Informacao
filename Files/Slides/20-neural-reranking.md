# Aula 19 - 26/05/2025 - Neural Models: Reranking

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

---

---

[JV] Só comecei a prestar atenção em torno da página 19.

### Neural Ranking Models (>2016)

- Representation-based
- Interaction-based

### Popular Neural Ranking Models

- Muita coisa é por tentativa e erro. Não tem tanta teoria que justifique essas escolhas.

## Machine Learning Background

### Progress in Information Retrieval - Robust04

- [Imagem]
- Geralmente os modelos são pre-treinados para entender modelos de linguagem
- O BERT generaliza bem o bastante mesmo no caso de "zero-shot"
  - Certamente modela a linguagem muito melhor do que antigamente

### Adoption by Commercial Search Engines

### What is BERT?

- Entrada: algum texto. Saída? O mesmo texto.
- Treinamento autosupervisionado: ele pega uma palavra, pega o contexto em que ela tá, omite a palavra e tenta prevê-la.
- Os modelos pré-treinados podem ser especificados com mais pequenos testes

#### BERT's Pretraining Ingredients

- Transformer
- Muito texto
- Fóruns de pergunta resposta
- Muito poder computacional.
- Geralmente quem treina são as grandes empresas.

### BERT

- Ele não processa símbolos, ele trabalha com números, então inicialmente ele começa tokenizando
- Cada token então vira um embedding. Um vetor de números que representa esses tokens
  - Token Embeddings
    - Vetor que representam o token
  - Segment Embeddings
    - Segmentos são categorias diferentes de entradas (?)
  - Position Embeddings
    - Vetor que representa a posição do token.

---

- Word2Vec não disambiguava por contexto.
- A saída será os encodings iniciais mas enriquecidas.
- Softmax:
  - Converte o embedding em uma distribuição de probabilidades entre as palavras possíveis.
- Entender o BERT dimensionalmente

### monoBERT: BERT reranker

- Agora temos um segmento de query; e um segmento de texto.
- O Softmax agora categoria apenas como relevante ou não relevante.
- O S_i é um número real
- O rótulo y é definido por humanos

#### Training monoBERT

- Os rótulos positivos são gerados pelos humanos.
- Os negativos podem ser usados pelo BM25

#### Once monoBERT is trained

- Usa BM25 para gerar os ranques
- Depois, com os documentos ordenados, usa-se o monoBERT para reranquear em potenciais scores melhores.
- É bom considerar um pouco além dos top-k afinal o bm25 pode ter ranqueado negativamente algo que seria positivo.
- Por que ao invés de apenas considerar o monoBERT, não considerar também com o BM25
- Naquele vetor de features de um documento que eram usados para ranquear, poderíamos usar a mesma ideia num vetor de scores que calculasse um score final ainda melhor?

## Ranking with

### BERT's limitations

- Transformers têm custo quadrático.

### From Passages to Documents

#### Handling length Limitation: Training

- Pode-se passar os labels nos diversos chunks
- Pelo que entendi os chunks são chamados de passages

#### Inference (2)

- agregar scores pros documentos

#### Over Passage Scores

- Diferentes Métricas
- Usualmente pegar o maior score funciona melhor
- Intuitivamente, se algo for relevante no documento, isso significa que ele é relevante.

#### Over Sentence Scores: Birch

#### Over Sentence Scores: Birch - Results

- O melhor resultado foi treinar com MB após treinar com MS MARCO

#### Aggregation

Usar um tipo de BERT para poder agregar os scores.

#### CEDR

Cria matriz de similaridades entre os vetores da query e do documento
Aí usam outro cálculo específico para matrizes, a tal da convolucional

One Term Embeddings:

BERT foi melhor que GloVe no relevante, e deu um ranque pior quando não era relevante.

### Over Passage Representations: PARADE

---

## Aula 20 - 02/06/2025

### Why Multi-stage Reranking? (2)

- Técnicas de ranqueamento mais para as extremidades em que há menos documentos são mais caras.

#### Multi-stage with duoBERT

- DuoBERT é um modelo que compara pares de documentos
- É bem parecido com o monoBERT, mas agora a entrada é um par de documentos e não um único documento.
- Dúvida: Por que usamos o T[CLS] e não o T[SEP]?
  - Entende-se que o T[CLS] represente uma atenção maior ao contexto geral do par de documentos, embora não esteja claro como.

##### Training duoBERT

##### Inference with duoBERT

- Ele avalia todas as probabilidades de pares de documentos
- Depois ele junta as probabilidades de cada um ser melhor que os outros.
- E esse será o novo score de ranqueamento.
