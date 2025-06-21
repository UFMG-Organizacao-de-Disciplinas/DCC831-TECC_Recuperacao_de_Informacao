# Anotações

## Slide X - Ele falou muito bem do SIGIR keynote

## Index Retrieval-Ranking: Disadvantages

- Eles acabam sempre tentando melhorar segmentos por um único modelo.

## Opinion paper: A single model for IR

- Assumiremos uma LLM que dado um modelo, retornará um ranking de itens.
- Ainda não está num ponto de conseguir
- A Máquina de Busca, trabalha com um delphic cost, ou seja, ele não dá a resposta, mas sim um caminho pra que o usuário encontre a resposta.
- IR não visava encontrar links, mas encontrar a informação
  - E por que não mudaram antes?
    - Porque o jeito que foi feito era o que haviam conseguido operacionalizar.

## Neural IR models: Discriminative vs. Generative

- Discriminative: prever um label
- Generative
- Prever a próxima palavra é muito mais difícil do que ranquear.
- Então, como precisou aprender muito mais coisa, acabou aprendendo mais coisas do que só o necessário.

## Two families of generative retrieval

- Closed-book
- Open-book

## Why generative retrieval?

- Tende a ser mais rápido e com menos espaço gasto.

## Generative Retrieval: Definition

- Generates docids of relevant

## Autoregressive formulation

- As gerações são usadas pra predizer o próximo
- Treinar um modelo com suas próprias respostas tende a gerar um model collapse em que suas respostas divergem e o tornam pior nos casos mais raros.
- Dúvida: por que o crawler não está dentro do modelo da LLM?
- Dúvida: por que ao invés de retornar os docids, não retornamos justamente as informações?

## Two basic operations in GR

- Indexing: memorize info about documents
  - "Differentiable" search index
  - Se for devidamente memorizado, ele conseguiria retornar o lookup dos conteúdos. Porém usaremos queries arbitrárias.
- Retrieval

## A single docid: number-based

- Number-based docids
  - Un...
  - ...
  - ...
  - ...

### Number-based: Unstructured atomic integers

- Como conseguir superar a limitação de tokens das LLMs?

### Number-based: Naively structured strings

- Particionar um interio em partes menores.
- Dúvida: mas aí seria adequado conseguir identificar quais partes desse id são relevantes para já conseguir mapear o documento para um ponto no espaço mais próximo de documentos similares?

#### Naively structured strings: obvious constraints

- id definido arbitrariamente
- faltam lógica semantica

### Number-based: Semantically structured strings

- [Imagem com beam search]

## Performance comparison

## Number-based docids: Summary

- Apesar dos grupos serem mais relevantes, ainda assim, o que significaria o id "142"? Como poderíamos explicar isso melhor?

## A Single docid: Word-based

### Word-based: Titles

- Funciona bem para ambientes com títulos comportados e únicos, tipo na wikipédia

### Word-based: URLs

- Funciona bem para documentos da web
- Esses até então não são gerais o bastante em caso de excasses de metadados.

### Word-based: Pseudo queries

- Doc2Query: tendem a ser formas de resumir o documento nas informações que podem ser obtidas dele.
- Pode-se acabar repetindo as mesmas queries pra documentos diferentes: como solucionar?

### Word-based: Important Terms

## Multiple docids

### Single type (N-grams)

### Diverse types: Pseudo queries + N-grams + titles (MINDER)

- Esse conjunto tem mais chance de ser único.

### Multiple Docids: Summary

- Gasta mais armazenamento

## Performance comparison (2)

- Ao invés de lidar com docids fixos, permitir a criação de novos tokens.
- Isso tudo aqui é exploratório. Não há uma estrutura definida que bata a clássica, mas tá caminhando.

## Supervised Learning: Basic training method

- Loss function: Indexing.
- Loss function: Retrieval.

  - Um fine tuning supervisionado.
  - Com pares treinados

- Primeiro faz todo o treinamento de indexing, e depois toda retrieval. Ou então, alterna entre ambos

### Limitation (1): Single document granularity

---

---

---

## Generative Information Retrieval

- SIGIR 2024 tutorial - Section 1
- **Yubao Tang$^a$**, Ruqing Zhang$^a$, **Zhaochun Ren$^b$**, Jiafeng Guo$^a$ and **Maarten de Rijke$^c$**
- [https://generative-ir.github.io/](https://generative-ir.github.io/)
- July 14, 2024
- $^a$ Institute of Computing Technology, Chinese Academy of Sciences & UCAS
- $^b$ Leiden University
- $^c$ University of Amsterdam

## Complex architecture design behind search engines

- User Query
  - Search Results
  - Re-ranking Module
  - Retrieval Module
  - Intermediate Results
  - Offline Components
  - Online Components
- Query parser
  - Syntable
  - Modified Query
  - Matching Technique
  - Structured Web-page Repository
  - Web-page Prediction
  - Indexing Module
  - Web-page Repository
- Crawlers
  - Web-page Repository
- Advantages:
  - Pipelined paradigm has withstood the test of time
  - Advanced machine learning and deep learning approaches applied to many components of modern systems

## Index-Retrieval-Ranking: Disadvantages

- Query parser: rewriting, expansion, suggestion, ...
- Search query
- Doc parser: extraction, anti-spamming, ...
- Index
- Retrieval $\to$ Re-ranking
- Search results
- Memory efficient data structure and storage
- Term-based inverted index
- Semantic-based vector index
- Efficient retriever:
  - Term-based retriever: PIV, DIR, BM25 etc.
  - Dense Retriever: dual-encoder, ColBert, ICT...
- Key idea: recall a small set of candidate documents from millions of documents in a coarse-grained way
- Effective re-ranker:
  - LTR models: RankNet, RankerSVM, LambdaMart etc.
  - Neural ranking models: cross-encoder, DRMM, BERT-maxP ...
- Key idea: conduct fine-grained relevance matching between a query and a small set of candidate documents
- Effectiveness: Heterogeneous ranking components are usually difficult to be optimized in an end-to-end way towards the global objective

---

- MS MARCO 300K
- Big storage: GTR (Dense retrieval) - Memory size 1430MB
- Slow inference speed: GTR (Dense retrieval) - Online latency 1.97s
- Efficiency: A large document index is needed to search over the corpus, leading to significant memory consumption and computational overhead

## Opinion paper: A single model for IR

- Query Parser: rewriting, expansion, suggestion, ...
- Search query
- Doc Parser: extraction, anti-spamming, ...
- Index
- Retrieval
- Ranking
- Search results
- A Single Model:
  - Search query
  - Search results

## Neural IR models: Discriminative vs. Generative

- Discriminative:
  - Document Space: d₁, d₂, d₃, ..., d₊
  - Query Space: q₁, q₈ -$p(R = 1|q, d) \approx ... \approx \text{argmax } s(\text{ᵢ}, \text{ᵥ})$$ (probabilistic ranking principle)
- Generative:
  - Query Space: q₁, q₈
  - Meta-identifier Space: l₂, g₀, a₁₀, b₁₀, c₁₀
  - Document Space: d₁₀ "olympic games", d₂ "olympic symbols", d₊ "2022 Winter Olympics opening ceremony"
  - association

## Two families of generative retrieval

- Closed-book: The language model is the only source of knowledge leveraged during generation, e.g.:
  - Capturing document ids in the language models
  - Language models as retrieval agents via prompting
- Open-book: The language model can draw on external memory prior to, during, and after generation, e.g.:
  - Retrieval augmented generation of answers
  - Tool-augmented generation of answers
- Source: [Najork, 2023]

## Why generative retrieval?

- Heterogeneous objectives:
  - Doc Parser: extractors, anti-spamming, ...
  - Index
  - Retrieval
  - Ranking
- A global objective:
  - A Single Model
  - Effectiveness: Knowledge of all documents in corpus is encoded into model parameters, which can be optimized directly in an end-to-end manner
- Query Parser: rewriting, expansion, suggestion, ...
- Search query
- Search results

## Why generative retrieval?

- Memory size (MS MARCO 300K):
  - Dense retrieval: GTR - 1430MB
  - Generative retrieval: GenRet - 860MB
- Online latency:
  - Dense retrieval: GTR - 1.97s
  - Generative retrieval: GenRet - 0.16s
- Efficiency: Main memory computation of GR is the storage of document identifiers and model parameters
- Heavy retrieval process is replaced with a light generative process over the vocabulary of identifiers
- Data source: [Sun et al., 2023]

## Generative retrieval: Definition

- Generative retrieval (GR) aims to directly generate the identifiers of information resources (e.g., docids) that are relevant to an information need (e.g., an input query) in an autoregressive fashion
- "Transformer Memory as a Differentiable Search Index". Tay et al. [2022]; "Autoregressive Entity Retrieval". De Cao et al. [2021]

## Autoregressive formulation (2)

- $P(x_n|x_1, x_2, \ldots, x_{n-1})$
- Output: x₁, x₂, ⋯, xₙ₋₁, xₙ
- Input: [bos]

## Two basic operations in GR (2)

- Indexing: To **memorize information about each document**, a GR model should learn to associate the content of each document with its corresponding docid
- Retrieval: Given an input query, a GR model should **return a ranked list of candidate docids** by autoregressively generating the docid string
- Source: [Tay et al., 2021]

## A single docid: Number-based

- Unstructured atomic integers (Tay et al. 2022)
- Naively structured strings (Tay et al. 2022)
- Product quantization strings (Zhou et al. 2022)
- Semantically structured strings (Tay et al. 2022)

## Number-based: Unstructured atomic integers (2)

- An arbitrary (and possibly random) unique integer identifier
- Corpus: 0, 1, 2, ...
- Docids: Dodds, ...
- Source: [Tay et al., 2021]

## Unstructured atomic integers and subsequent work

- Unstructured atomic integers (Tay et al. 2022)
- Number-based docids:
  - Naively structured strings (Tay et al. 2022)
  - Product quantization strings (Zhou et al. 2022)
- Semantically structured strings (Tay et al. 2022)
- Easy to build: analogous to the output layer in standard language model
- Zhou et al. 2022, Zhou et al. 2023, Nguyen and Yates et al. 2023c, Nadeem et al. 2022, Mehta et al. 2022

## Unstructured atomic integers: obvious constraints

- The need to learn embeddings for each individual docid
- The need for the large softmax output space
- It is challenging to be used on large corpora!

## Number-based: Naively structured strings (2)

- Treat arbitrary unique integers as tokenizable strings
- Corpus: 243168, ...
- Docids: ..., ...
- Tokenized docid strings: 24, 316, 8
- Source: [Tay et al., 2021]

## Naively structured strings and subsequent work

- Unstructured atomic integers (Tay et al. 2022)
- Number-based docids:
  - Naively structured strings (Tay et al. 2022)
  - Product quantization strings (Zhou et al. 2022)
- Semantically structured strings (Tay et al. 2022)
- Such a way frees the limitation for the corpus size that comes with unstructured atomic docid
- Zhou et al. 2022, Zhou et al. 2023, Nguyen and Yates et al. 2023c, Nadeem et al. 2022, Mehta et al. 2022, Zhuang et al. 2023, Nadeem et al. 2022

## Naively structured strings: obvious constraints (2)

- Identifiers are assigned in an arbitrary manner
- The docid space lacks semantic structure

## Number-based: Semantically structured strings (2)

- Properties:
  - The docid should capture some information about the semantics of its associated document
  - The docid should be structured in a way that the search space is effectively reduced after each decoding step
- Semantically similar documents share docid prefixes

## Number-based: Semantically structured strings (2)

- A hierarchical clustering algorithm over document embeddings to induce a decimal tree
- Source: [Tay et al., 2021]
- Document Embeddings
- Beam search decodes "233"

## Semantically structured strings and subsequent work

- Unstructured atomic integers (Tay et al. 2022)
- Number-based docids:
  - Naively structured strings (Tay et al. 2022)
  - Product quantization strings (Zhou et al. 2022)
- Semantically structured strings (Tay et al. 2022)
- The document semantics can be incorporated in the decoding process
- It is not limited by the size of the corpus
- Zhou et al. 2022, Zhou et al. 2023, Nguyen and Yates et al. 2023c., Nadeem et al. 2022, Mehta et al. 2022, Zhuang et al. 2023, Nadeem et al. 2022, Wang et al. 2022, Chen et al. 2023a, Nadeem et al. 2022

## Performance comparisons [Tay et al., 2022]

| Model                                 | Hits@1 |
| ------------------------------------- | ------ |
| DSI (Unstructured atomic integers)    | 27.4   |
| DSI (Naively structured strings)      | ...    |
| DSI (Semantically structured strings) | ...    |

- Backbone: T5-base
- Observations: imbuing the docid space with semantic structure can lead to better retrieval capabilities
- Natural Questions 320K
- Data source: Tay et al. (2022)

## Number-based docids: Summary

- [x] Docids based on integers are easy to build
- [x] Unstructured atomic integers and naively/semantically structured strings can maintain uniqueness
- [x] They are composed of unreadable numbers
- [x] It is challenging to interpret the model’s understanding of the corpus

## A single docid: Word-based

- Unstructured atomic integers (Tay et al. 2022)
- Number-based docids:
  - Naively structured strings (Tay et al. 2022)
  - Product quantization strings (Zhou et al. 2022)
  - Semantically structured strings (Tay et al. 2022)
- Word-based docids:
  - Titles (De Cao et al. 2021)
  - URLs (Zhou et al. 2022)
  - Pseudo queries (Tang et al. 2023a)
  - Important terms (Zhang et al. 2023)

## A single docid: Word-based

- The fundamental inspiration:
  - The query is usually keyword-based natural language, which can be challenging to map into a numeric string, while mapping it to words would be more intuitive

## Word-based: Titles

- Document titles: be able to summarize the main content
- Information retrieval | Decoding target
- Article: Talk From Wikipedia, the free encyclopedia **Information retrieval (IR)** In computing and information science is the process of obtaining information system resources that are relevant to an information need from a collection of those resources. Searches can be based on full-text or other content-based indexing. Information retrieval is the science[1] of searching for information in a document, searching for documents themselves, and also searching for the metadata that describes data, and for databases of texts, images or sounds. Automated information retrieval systems are used to reduce what has been called information overload. An IR system is a software system that provides access to books, journals and other documents; it also stores and manages those documents. Web search engines are the most visible IR applications.
- "Autoregressive Entity Retrieval". De Cao et al. [2021]
- **Chiamaka Nnadozie’s father didn’t want her to play soccer. Nigerian star defied him and rewrote the record books** By Michael Johnston and Amanda Davies, CNN © 5 minute read - Updated 10:06 AM EDIT, Wed November 1, 2023 (CNN) — It wasn’t always plain sailing for Paris FC and Nigerian goalkeeper, Chiamaka Nnadozie, throughout her now-flourishing career. Growing up in a family of boys and men – who had all tried their hand at going professional – Nnadozie’s ambition to follow suit wasn’t greeted with unyielding enthusiasm. Quite the opposite. "It wasn’t very good from my family. They never let me play, especially my dad," the 22-year-old told CNN’s Amanda Davies. "Whenever I went to play soccer, he would always tell me: 'Girls don’t play football. Look at me. I played football, I didn’t make it. Your brother, he played, he didn’t make your cousin played, he didn’t make it. So why do you want to choose this? Why don’t you want to go to school or maybe do some other things?'" Nnadozie recollected.

## Word-based: URLs

- The URL of a document contains certain semantic information and can uniquely correspond to this document
- What is Information Retrieval? Read Discuss Courses Information Retrieval (IR) can be defined as a software program that deals with the organization, storage, retrieval, and evaluation of information from document repositories, particularly textual information. Information Retrieval is the activity of obtaining material that can usually be documented on an unstructured nature i.e. usually text which satisfies an information need from within large collections which is stored on computers. For example, Information Retrieval can be when a user enters a query into the system. Not only librarians, professional searchers, etc engage themselves in the activity of information retrieval but nowadays hundreds of millions of people engage in IR every day when they use web search engines. Information Retrieval is believed to be the dominant form of "TOME: A Two-stage Approach for Model-based Retrieval". Ren et al. [2023]
- [Imagem: Geek5forgeeks example]

## If the special document metadata is not available

- It is necessary to design automatic docid generation techniques

## Word-based: Pseudo queries

- Doc2Query technique: pseudo queries are likely to be representative or related to the contents of documents
- In fiscal 2015, Disney earned $16,162 billion in revenue from ⋯⋯ Documents
- Query Generation Model $\to$ Average cost of Disneyland (Pseudo queries)
- "Semantic-Enhanced Differentiable Search Index Inspired by Learning Strategies". Tang et al. [2023]

## Pseudo queries and subsequent work

- Unstructured atomic integers (Tay et al. 2022)
- Number-based docids: Product quantization strings (Zhou et al. 2022)
- Semantically structured strings (Tay et al. 2022)
- Titles (De Cao et al. 2021)
- URLs (Zhou et al. 2022)
- Word-based docids:
  - Pseudo queries (Zhou et al. 2023)
  - Important terms (Zhang et al. 2023)
- Zhou et al. 2022, Zhou et al. 2023, Nguyen and Yates et al. 2025; Nademir et al. 2022, Mehta et al. 2022, Wong et al. 2021, Chen et al. 2020, Nademir et al. 2022, Ren et al. 2023, Thorne et al. 2022, Chen et al. 2022a, Chun et al. 2022, Liang et al. 2022, Lee et al. 2022, 2023, Zhou et al. 2022

## Word-based docids: Summary

- Semantically related to the content of the document
- Good interpretability
- Rely on metadata or labeled data
- May lead to duplication

## Multiple docids

- A single docid:
  - Number-based docids: Unstructured atomic integers (Tay et al. 2022), Product quantization strings (Zhou et al. 2022), Semantically structured strings (Tay et al. 2022)
  - Word-based docids: Titles (De Cao et al. 2021), URLs (Zhou et al. 2022), Pseudo queries (Tang et al. 2023a), Important terms (Zhang et al. 2023), Ren et al. 2023, Thorne et al. 2022
- Multiple docids:
  - Single type (N-grams) (Bevilacqua et al. 2022)
  - Diverse types (Pseudo queries + N-grams + Titles) (Ii et al. 2023)

## Multiple docids: Single type (N-grams) [Bevilacqua et al., 2022]

- All n-grams (i.e., substrings) in a document are treated as its possible docids
- Part of n-grams as docids during training: Only the terms from the document that have a high overlap with the query are chosen as the target docids
- Carbon footprint Carbon dioxide is released naturally by decomposition, ocean release and respiration. Humans contribute an n-grams increase of carbon dioxide emissions by burning fossil fuels, deforestation, and cement production. Methane (CH4) is largely released by coal, oil, and natural gas industries. Although methane is not mass-produced like carbon dioxide, it is still very prevalent.
- "Autoregressive Search Engines: Generating Substrings as Document Identifiers" . Bevilacqua et al. [2022]

## Multiple docids: Diverse types (MINDER) [Li et al., 2023]

- Query: Who is the singer of does he love you? ↑Relevant Passage \[ https://en.wikipedia.org/wiki/Does_He_Love_You\] "Does He Love You" is a song written by Sandy Knox and Billy Stritch, and recorded as a duet by American country music artists Reba McEntire and Linda Davis. It was released in August 1993 as the first single from Reba's album "Greatest Hits Volume Two". It is one of country music's several songs about a love triangle. "Does He Love You" was written in 1982 by Billy Stritch. .....
- Multiview Identifiers:
  - Title: Does He Love You
  - Substrings: "Does He Love You" is a song ... recorded as a duet by American country music artists Reba McEntire and Linda Davis, ...
  - Pseudo-queries: Who wrote the song does he love you? Who sings does he love you? When was does he love you released by reba? What is the first song in the album "Greatest Hits Volume Two" about?
- Three views of docids:
  - Title: Indicate the subject of a document
  - Substrings (N-grams): Be also semantically related
  - Pseudo-queries: Integrate multiple segments and contextualized information
- _Multiview Identifiers Enhanced Generative Retrieval_. Li et al. [2023]

## Performance comparisons

| Model                           | Recall@100 |
| ------------------------------- | ---------- |
| Semantically structured strings | 0.6        |
| Single type (N-grams)           | 0.655      |
| Multiple (Diverse types)        | 0.863      |
| MINDER                          | 0.867      |

- Natural Questions 320K
- Backbone: BART-large
- Results: Using multiple docids for a document yields better results than using a single docid

## Multiple docids: Summary

- Multiple docids can provide a more comprehensive representation of the document, assisting the model in gaining a multifaceted understanding
- Similar docids across different documents can reflect the similarity between the documents
- GR models with the increased docid numbers demand more memory usage and inference time
- It is challenging to design discriminative multiple docids for a document

## Performance comparisons

| Model                        | Recall@1 |
| ---------------------------- | -------- |
| Product quantization strings | 0.52     |
| Titles                       | 0.552    |
| N-grams                      | 0.599    |
| URLs+titles                  | 0.612    |
| Learnable discrete numbers   | 0.681    |
| NOVO docids                  | 0.693    |

- Backbone: T5-base
- Results: Two learnable docids yields better results than partial pre-defined static docids

## Learnable docids: Summary

- It can be optimized together with the ultimate goal of GR to better adapt to retrieval
- A learnable approach can enable number-based docids like those in GenRet [Sun et al., 2023] to perform well
- It relies on complex task design for learning

## Supervised learning: Basic training method

- Learn the indexing task first, and then learn retrieval tasks:
  - Step 1:$ \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) = -\sum_{d \in D} \log P(id | d; \theta)$
  - Step 2:$ \mathcal{L}_{\text{Retrieval}}(Q, I_Q; \theta) = -\sum_{q \in Q} \sum\_{id^q \in I_Q} \log P(id^q | q; \theta)$
- Learn indexing and retrieval tasks simultaneously in a multitask fashion:
  - $\mathcal{L}_{\text{Global}}(Q, D, I_D, I_Q; \theta) = \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) + \mathcal{L}_{\text{Retrieval}}(Q, I_Q; \theta)$
  - $= -\sum_{d \in D} \log P(id | d; \theta) - \sum_{q \in Q} \sum_{id^q \in I_Q} \log P(id^q | q; \theta)$
- "Transformer Memory as a Differentiable Search Index". Tay et al. [2022]

## Limitation (1): Single document granularity (2)

- $\mathcal{L}_{\text{Global}}(Q, D, I_D, I_Q; \theta) = \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) + \mathcal{L}_{\text{Retrieval}}(Q, I_Q; \theta)$
- $= -\sum_{d \in D} \log P(id \mid d; \theta) - \sum_{q \in Q} \sum_{id^q \in I_Q} \log P(id^q \mid q; \theta)$
- When indexing, memorizing each document at a single granularity, e.g., first $ L $ tokens or the full text, is insufficient, especially for long documents with rich semantics
- "Semantic-Enhanced Differentiable Search Index Inspired by Learning Strategies". Tang et al. [2023a]

### Supervised learning: Multi-granularity enhanced

- Given a document, the important passages $ p $ and sentences $ s $ are selected to augment the indexing data
- $\mathcal{L}_{\text{Indexing}}(D, I_D; \theta) = -(\sum_{d \in D} \log P(id | d; \theta) + \sum_{p \in d} \log P(id | p; \theta) + \sum_{s \in d} \log P(id | s; \theta))$
- "Semantic-Enhanced Differentiable Search Index Inspired by Learning Strategies". Tang et al. [2023a]

- [JV]
  - d: sentenças do documento

## Comparisons

| Model  | Performance |
| ------ | ----------- |
| DSI    | ...         |
| SE-DSI | 0.5         |

- Standard: T5-base
- Multi-granularity representations of documents can comprehensively encode the documents, and further contribute to the retrieval
- Data source: MS MARCO 100K

## Limitation (2): The gap between indexing and retrieval

- $\mathcal{L}_{\text{Global}}(Q, D, I_D, I_Q; \theta) = \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) + \mathcal{L}_{\text{Retrieval}}(Q, I_Q; \theta)$
- $= -\sum_{d \in D} \log P(id \, | \, d; \theta) - \sum_{q \in Q} \sum_{id^q \in I_Q} \log P(id^q \, | \, q; \theta)$
- Long document in indexing vs. Short query in retrieval
- The data distribution mismatch that occurs between the indexing and retrieval
- "Bridging the Gap Between Indexing and Retrieval for Differentiable Search Index with Query Generation". Zhuang et al. [2023]

- [JV]
  - As duas loss functions são meio contraditórias, pois elas fazem geração de texto pra texto.
  - Se um é mais geral e outro mais restrito, isso acaba limitando o aprendizado do modelo.
  - Uma alternativa é então reduzir o textos grandes em outros menores.

## Supervised learning: Pseudo query enhanced

- Documents: d₁, d₂, d₃ (e.g., "Jeffrey Kaplan is an American visual game designer... docid 313")
- Query Generation Model $\to$ Pseudo queries (e.g., "who is Jeffery Kaplan?", "who is the vice president of Blizzard Entertainment? docid 313")
- DSI: Encoder $\to$ Decoder $\to$ docid 313
- Using a set of pseudo queries $pq$ generated from the document as the inputs of the indexing task
- "Bridging the Gap Between Indexing and Retrieval for Differentiable Search Index with Query Generation". Zhuang et al. [2023]

---

- Original:$ \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) = -\sum_{d \in D} \log P(id \mid d; \theta)$
- Enhanced:$ \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) = -\sum_{pq \in D} \log P(id \mid pq; \theta)$
- Retrieval loss unchanged:$ \mathcal{L}_{\text{Retrieval}}(Q, I_Q; \theta) = -\sum_{q \in Q} \sum\_{id^q \in I_Q} \log P(id^q \mid q; \theta)$
- "Bridging the Gap Between Indexing and Retrieval for Differentiable Search Index with Query Generation". Zhuang et al. [2023]

## Comparisons

| Model                                 | Hits@1 (MS MARCO 100K) |
| ------------------------------------- | ---------------------- |
| DSI (Natively structured strings)     | 0.021                  |
| DSI-QG                                | ...                    |
| DSI (Semantically structured strings) | ...                    |
| DSI+PQ                                | ...                    |

- Backbone: T5-base
- Using only pseudo synthetic queries to docid during indexing is an effective training strategy on MS MARCO [Pradeep et al., 2023]

## Limitation (3): Limited labeled data

- $\mathcal{L}_{\text{Global}}(Q, D, I_D, I_Q; \theta) = \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) + \boxed{\mathcal{L}_{\text{Retrieval}}(Q, I_Q; \theta)}$
- What should we do if there is no or few labeled query-docid pairs?

- [JV] Dado rotulado é escasso

## Pre-training methods

- Constructing pseudo query-docid pairs $(PQ, I_Q^P)$ for the pre-training retrieval task
- $\mathcal{L}_{\text{Pre\_train}}(PQ, D, I_D, I_Q^P; \theta) = \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) + \mathcal{L}_{\text{Retrieval}}(PQ, I_Q^P; \theta)$

- [JV] Geraremos dados sintéticos.

## CorpusBrain [Chen et al., 2022]: Performance

| Model                                           | R-precision (FEVER) |
| ----------------------------------------------- | ------------------- |
| TF-IDF (Sparse retrieval)                       | ...                 |
| MT-DPR (Dense retrieval)                        | ...                 |
| GENRE (Generative retrieval)                    | 83.64               |
| CorpusBrain (Generative retrieval Pre-training) | 84.07               |

- In the KILT leaderboard, Corpusbrain achieved first place in 5 of them, second place in 1 task, and third place in 4 tasks, outperforming traditional pipelined approaches
- _CorpusBrain: Pre-train a Generative Retrieval Model for Knowledge-Intensive Language Tasks_. Chen et al. [2022]

## Limitation (4): Pointwise optimization for GR

- $\mathcal{L}_{\text{Global}}(Q, D, I_D, I_Q; \theta) = \mathcal{L}_{\text{Indexing}}(D, I_D; \theta) + \mathcal{L}_{\text{Retrieval}}(Q, I_Q; \theta)$
- $= -\sum_{d \in D} \log P(id | d; \theta) - \sum_{q \in Q} \sum_{id^q \in I_Q} \log P(id^q | q; \theta)$
- It assumes the likelihood for each relevant docid is independent of the other docids in the list for a query
- Ranking is a prediction task on list of objects
- Pairwise and listwise optimization strategies for GR are necessary!

- [JV] point, pair and listwise podem ser usadas aqui.

## Pairwise optimization: LTRGR [Li et al., 2023c]

- Step 1: Initial training with pointwise optimization
- Step 2: Based on the trained initial model, perform pairwise optimization
- Query $\to$ Autoregressive Model $\to$ Predicted Identifiers
  - Predicted titles
  - Predicted body
- Passage rank list: Passage 1, Passage 2 $\to$$ \text{max}(0, s(q, d*-) - s(q, d*+) + m)$ where $ d*- $ and $ d*+ $ are negative and positive documents, and $ m $ is the margin
- "Learning to Rank in Generative Retrieval". Li et al. [2023c]

## LTRGR [Li et al., 2023c]: Performance

| Model                         | Hits@5 (Natural Questions) | MRS@10 (MS MARCO Passage Ranking) |
| ----------------------------- | -------------------------- | --------------------------------- |
| BM25 (Sparse retrieval)       | ...                        | ...                               |
| DPR (Dense retrieval)         | ...                        | ...                               |
| MINDER (Generative retrieval) | ...                        | ...                               |
| LTRGR (Generative retrieval)  | ...                        | ...                               |

- _Learning to Rank in Generative Retrieval_. Li et al. [2023c]

## Roadmap of inference strategies

- A **single identifier** to represent a document:
  - Constrained beam search with a prefix tree
  - Constrained greedy search with the inverted index
- Multiple **identifiers** to represent a document:
  - Constrained beam search with the FM-index
  - Scoring functions to aggregate the contributions of several identifiers

## Single identifier: Constrained beam search with a prefix tree

- [Imagem: Constrained beam search prefix tree example from De Cao et al. [2021]]
- BOS $\to$ English $\to$ literature $\to$ France $\to$ EOS
- Applicable docids: Naively structured strings, semantically structured strings, product quantization strings, titles, n-grams, URLs and pseudo queries
- Prefix tree: Nodes are annotated with tokens from the predefined candidate set. For each node, its children indicate all the allowed continuations from the prefix defined traversing the tree from the root to it
- _Autoregressive Entity Retrieval_. De Cao et al. [2021]

- [JV] Só poderá emitir palavras que existem em alguma estrutura.

## Example

- Beam size = 2
- <80s> (0.3)
- English (0.7) $\to$ Frame (0.3), Image (0.8)
- English language (0.2), English literature (1.0)
- France (0.5), EOS (0.4), EOS (0.6)
- Input: English (0.14), Frame (0.14)

- [JV] "[EOS]" é "End of Sentence"
  - O Algoritmo guloso iria só pro mais provável.
  - O Beam Search analisa algo maior, analisando as probabilidades conjuntas.

## Inference efficiency: Memory footprint

- Memory (MB):
  - Dense retrieval: GTR-Base - 1400MB
  - Generative retrieval: GenRet - 800MB
- The memory footprint of the GR model GenRet is smaller than that of the traditional dense retrieval method GTR, e.g., 1.6 times

## Inference efficiency: Offline latency

- Offline time (Min):
  - Dense retrieval: GTR-Base - ...
  - Generative retrieval: GenRet - 200min
- MS MARCO 300K
- GenRet takes a longer time for offline indexing, as the use of auxiliary models. GTR's offline time consumption comes from document encoding
- Data source: Sun et al. [2023]

- [JV] Qual é o custo para indexação offline?

## Inference efficiency: Online latency

- Online time (s):
  - Dense retrieval: GTR-Base - 1.97s
  - Generative retrieval: GenRet - 0.16s
- MS MARCO 300K
- Compared with the traditional dense retrieval model GTR, the GR model GenRet is faster, e.g., 12 times

- [JV] Custo de consulta.

## Pros of generative retrieval

- Information retrieval in the era of language models:
  - Encode the **global information** in corpus; optimize in an **end-to-end way**
  - The semantic-level **association** extending beyond mere signal-level matching
  - Constraint decoding over **thousand-level vocabulary**
  - Internal index which **eliminates** large-scale external index

## Cons of generative retrieval: Scalability

- **Large-scale real-word corpus:**
  - Current research can generalize from corpora of hundreds of thousands to millions
  - How **to accurately memorize vast amounts of complex data?**
- **Highly dynamic corpora:**
  - Document addition, removal and updates
  - How to keep such GR models up-to-date?
  - How to learn on new data without forgetting old ones?
- **Multi-modal/granularity/language search tasks:**
  - Different search tasks leverage very different indexes
  - How to unify different search tasks into a single generative form?
  - How to capture task specifications while obtaining the shared knowledge?
- **Combining GR with retrieval-augmented generation (RAG):**
  - How to integrate GR with RAG to enhance the effectiveness of both?

## Cons of generative retrieval: Controllability

- For a failure issue, it is often unclear what modeling knobs one should turn to fix the model's behavior
- Interpretability:
  - Black-box neural models
  - How to provide credible explanation for the retrieval process and results?
- Debuggable:
  - Attribution analysis: how to conduct causal traceability analysis on the causes, key links and other factors of specific search results?
  - Model editing: how to accurately and conveniently modify training data or tune hyperparameters in the loss function?
- Robustness:
  - When a new technique enters into the real-world application, it is critical to know not only how it works in average, but also how would it behave in abnormal situations

## Cons of generative retrieval: User-centered

- Searching is a **socially** and **contextually** situated activity with diverse set of goals and needs for support that must not be boiled down to a combination of text matching and text generating algorithms [Shah and Bender, 2022]

  - Human information seeking behavior
  - Transparency
  - Provenance
  - Accountability

- [JV] Até então, os testes são muito "in vitro" (ou "in silico"), sem analisar o fator social.

## Cons of generative retrieval: Performance

- The current performance of GR can only be compared to the index-retrieval stage of traditional methods, and it has not yet achieved the additional improvement provided by re-ranking

## Q & A

- Thank you for joining us today!
- All materials are available at [https://generative-ir.github.io/](https://generative-ir.github.io/)
