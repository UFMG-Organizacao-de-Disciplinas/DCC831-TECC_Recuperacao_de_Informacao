# Aula 05 - 26/03/2025 - Document Indexing | Slide - Indexing

- Trabalho Prático 1: Crawler
- Trabalho Prático 2: Buscador simples
- Research Challenge: Usar o Kaggle, testar várias coisas
- Replacement: Substitutiva, quase que uma segunda chamada, sem precisar de justificativa
- Provas: 2 provas, fechadas ou abertas; Ainda tá decidindo.

## Search Components (Aula 5)

...

---

...

### Key challenges

...

### Success Metrics

- Qualidade
  - Utilidade do conteúdo: pouco spam, bons matches
  - Efetividade
- Performance
  - Compactação: tamanho do índice em bytes
  - Custo do deployment: tempo para construir e atualizar o índice

## Document Prefiltering

- Detectar spams
  - Term spamming $\to$ Text classification
  - Link Spamming $\to$ trust propagation
    - PageRank: as páginas que recebem links
    - Dúvida: determinada página tem registro de quais são as páginas que tem inlinks para si?
      - Resposta: usualmente não. Blogs talvez sim tenham os backlinks
- Detectar documentos com conteúdo duplicado
  - Exact duplicates: compare hash
  - Near duplicates $\to$ compare _shingles_ instead

### Near duplicates via $n$-shingling

- Pega diversos 2-gramas da página
- Efetua os hashes desses bigramas
- Seleciona o n-menores valores de cada um
- E então efetua o cálculo de Jaccard:
  - $J(A, B) = \frac{|A \cap B|}{|A \cup B|}$
  - Se $J(A, B) > \theta$, então são considerados near duplicates
  - $\theta$ é um threshold. No slide foi definido como sendo 0.5

## Document Features

- Features computed offline
  - **Conteúdo:** Spam score, domain quality score
  - **Web Graph:** PageRank, HostRank
  - **Usage:** click count, CTR, dwell time
    - Essas informações estariam disponíveis apenas para os hosts dos sites, ou donos das máquinas de busca e navegadores
- Features computed online
  - **Query-Documento similarity:** TF-IDF, BM25, etc.
    - [JV: Ele falou brevemente mas não me atentei]

## Indexing Overview (Aula 05)

...

---

...

## Document understanding (Aula 05)

- Parsing + tokenization
  - Turn raw text into indexing terms
- Token analysis
  - Discriminative power
  - Equivalence classing
  - Phrasing, scoping

## Document indexing

O objetivo é evitar fazer um grep em todas as páginas.

Dúvida: grep é para fazer a busca exata?

- Indexing makes crawled documents searchable
  - Efficient searching requires appropriate structures
- Abandoned indexing data structures
  - Suffix arrays, signature files
- Currently used data structure
  - Inverted index

### Example "corpus"

#### Incidence Matrix

Problema: esparsidade da estrutura

#### Inverted index: incidence

Basicamente é uma lista de adjacência, onde cada elemento da lista se chama "posting". E o que armazenamos no "posting" é escolha nossa.

#### Inverted index: frequency

Uma das informações que podemos armazenar é a frequência de cada palavra.

Para isso, geralmente armazenamos o índice do documento (que tende a ser na casa dos milhares/milhões) e depois a frequência de ocorrência, que usualmente não passa da casa das centenas.

#### Inverted index: additional info

- Term positions
  - Exact phrases vs. proximity search
- Document structure
  - Field restrictions (e.g., date:, from:)
  - Some fields more important (e.g., title, h1)

### Inverted List Compression

- Observação: a representação usual é custosa [Em relação a quantidade de bytes]

---

- Ideia base:
  - Representação sem perda de informação usando menos bits
  - Diversas abordagens [[Catena et al., ECIR 2014]](https://doi.org/10.1007/978-3-319-06028-6_30)
- Benefícios
  - Reduz o custo de espaço e rede/reduz o tempo de transferência de disco
  - Custo: overhead de descompressão

#### Example: unary encoding

- Algoritmo:
  - represente o número como sendo ele mesmo como esse número de zeros seguido do número 1
- Exemplo:
  - 5 $\to$ 000001
  - 7 $\to$ 00000001

#### Example: gamma encoding

- Algoritmo:
  - Unário primeiro baseado no...
    - binary digits of k minus 1: (conta todos os dígitos a partir do primeiro 1 à esquerda até a direita)
  - Seguindo dos l - 1 dígitos menos relevantes

[JV: explicar melhor depois]

### Inverted List Compression (Round 2)

- Ao invés de armazenar o número do ID, armazene os deltas entre os índices:
  - fish: (1:2), (2:3), (3:2), (4:2)
  - fish: (1:2), (1:3), (1:2), (1:2) [passo 1]

### Document Identifier Reordering

Basicamente faz um tipo de desfragmentações de forma a colocar os documentos similares mais próximos.

---

E como fazer isso? Caixeiro viajante.

E como resolver? Heurísticas

- Key idea: assign similar documents close docids
  - A term in one doc will likely be in similar docs
- Clustering similar documents
  - Assigns nearby IDs to documents in the same cluster
- Sorting URLs alphabetically
  - Pages from same site have high textual overlap

### Index Construction

- function index(corpus)
  - index = map()
  - did = 0 # Doc Id
  - for document in corpus # Essa ordem é importante. Se estiver seguindo ordem alfabética: ótimo
    - did += 1
    - for (term, tf) in tokenize(document) # Term = Token; TF = Term Frequency
      - if term not in index.keys()
        - index[term] = list()
        - index[term].append((did, tf))
  - return index

---

- Equivalent to computing the transpose of a matrix
  - Parse direct (document-term) occurrences
  - Write out inverted (term-document) occurrences
- Trivial in-memory implementation
  - Does not scale even for moderately sized corpora
  - On-disk processing typically needed

#### External Indexing

- Merging addresses limited memory problem
  - Build the inverted list structure until memory runs out
  - Write partial index to disk, start making a new one
- At the end of this process
  - Merge many partial indexes in memory
  - Equivalent to an external mergesort

#### External Merging

#### Internal Merging

#### External Merging (Round 2)

### Index maintenance

- Index merging efficient for large updates
  - Overhead makes it inefficient for small updates
- Instead, create separate index for new documents
  - Merge results from both indexes
- Could be in-memory, fast to update and search
  - Also works for updates and deletions

Basicamente seria utilizado um sistema de armazenamento mais parudo para guardar o grande volume de dados, e um outro, temporário, ou menor, que seria como um buffer, que, quando enchesse, seria jogado no maior.

### Distributed indexing

- Distributed processing driven by need to index and analyze huge amounts of data (i.e., the Web)
  - Large numbers of inexpensive servers used rather than larger, more expensive machines
- MapReduce is a distributed programming tool designed for indexing and analysis tasks

#### The MapReduce framework [[Dean and Ghemawat, USENIX 2004](https://www.usenix.org/legacy/event/osdi04/tech/full_papers/dean/dean.pdf)]

- Key idea: keep data and processing together
  - Bring code to data!
- Map and reduce functions
  - Inspired by functional programming
- Constrained program structure
  - But massive parallelization!

Pode acabar terminando com vários sub índices que precisariam ser posteriormente agrupados.

#### Distributed indexing with MapReduce [[McCreadie et al. IP&M 2012](https://www.sciencedirect.com/science/article/pii/S0306457319304455)]

#### Index sharding and replication

Parece um pouco com o conceito de RAIDS de armazenamento.

- Multiple index shards
  - Reduce query response times
  - Scale with collection size
- Multiple shard replicas
  - Increase query throughput
  - Scale with query volume
  - Provide fault tolerance

##### Index Sharding

- Term-based sharding
  - Disjoint terms in different nodes
  - Single disk access per term
- Good for inter-query parallelism
  - Higher throughput (disjoint queries)
- Bad for load balancing and resilience
  - Nodes with popular terms overloaded
  - Entire inverted lists missed on node failures

---

- Document-based sharding
  - Disjoint documents in different nodes
  - Multiple (parallel) disk accesses per term
- Good for intra-query parallelism
  - Faster response (smaller indexes)
  - Throughput increased via replication
- Also good for load balancing and resilience
  - Some documents missed on node failures

### Summary (Aula 05)

- Indexing makes search feasible at a web-scale
  - Effective search via carefully encoded postings
  - Efficient search via carefully chosen structures
- Several design choices
  - Prefiltering, feature extraction, text understanding
  - Posting design, ordering, compression, and more

---

- Efficient management
  - Memory-efficient, distributed construction
  - Near-real time updates via clever merging
  - Scalability via sharding and replication

### References - Aula 05

- [Search Engines: Information Retrieval in Practice, Ch. 5 Croft et al., 2009](https://www.amazon.com/Search-Engines-Information-Retrieval-Practice/dp/0136072240)
- [Scalability Challenges in Web Search Engines, Ch. 3 Cambazoglu and Baeza-Yates, 2015](https://doi.org/10.2200/S00662ED1V01Y201508ICR045)

### Próxima aula: Query Understanding
