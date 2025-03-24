# Recuperação de Informação

- Professor: Rodrygo Luis Teodoro Santos
- Email: <rodrygo@dcc.ufmg.br>
- [Pre-Course Survey](https://docs.google.com/forms/d/e/1FAIpQLSfJK_YDa9bH8wzg-xKOWxyShF7MLR8DkvcCRyzEM1R5ofNmsQ/formResponse)

## Aula 01 - 12/03/2025

Essa é a área principal de pesquisa dele. Ele também tem foco nos sistemas de recomendação.

A última edição foi dois anos atrás.

A disciplina está passando por grandes mudanças devido as IAs.

> Information retrieval is a field concerned with the structure, analysis, organization, storage, searching, and retrieval of information.
> Gerard Salton, 1968

- Retrieval tasks
  - Search
    - 1 Query
  - Recommendation
    - 0 Query
  - Anticipation
    - -1 Query
  - Conversation
    - n queries

"O problema está longe de ser resolvido"

"O sistema é muito limitado em várias dimensões"

- Our focus: search
  - User's perspective: accessing information
    - Relevance, Speed
  - Advertiser's perspective: publicity
    - More attention, less ad costs.
  - Search Engine's perspective: monetization
    - More users, more ad revenue, less op costs

---

- O que uma máquina de busca faz?
  - Checagem de correção de ortografia
  - Busca mesmo em caso de erro
  - Query autocompletion and suggestion
  - Generated answers (Uso de IA)
  - Knowledge snippets (fragmentos de informação importantes.)
  - Resposta a perguntas frequentes
  - Buscas relacionadas
  - Personalização (respostas baseadas em informações específicas do usuário)

Busca vertical: buscar informações contidas em um subconjunto de itens diferentes. Ex.: Imagens, vídeos, produtos, etc.

O foco da disciplina será em busca textual.

Nosso foco é o dos "10 blue links". Suponho eu que seria conseguir encontrar os 10 links mais relevantes.

---

- The search problem:
  - Given: some ~~evidence of the user's need~~ query
  - Produce: ~~relevant information~~
  - Produce:
    - a list of matching ~~information items~~ documents
    - In decreasing order of relevance

- Pergunta: é preferível uma resposta direta ou uma lista de documentos?
  - Minha resposta: a resposta direta e objetiva
  - Outra resposta: lista de documentos, porque como as pessoas não sabem exatamente o que querem, é melhor ter uma lista de opções para escolher.
  - Outras resposta: lista de documentos para poder haver um fact checking

As IAs são excessivamente autoconfiantes. Idealmente as pessoas razoáveis verificariam as informações "mas o mundo é cheio de pessoas não razoáveis".

---

Apenas definir se é relevante ou não pode gerar uma quantidade excessiva de informações; então, além disso, é preciso ranquear as informações.

E então, é delegado ao usuário de que forma lidar com as informações que lhe foram passadas.

Com isso, é necessário estimar de quão relevantes são os documentos para determinada consulta.

$f(query, document)$

> E esse problema já não está resolvido? Por que ainda estudamos?
> "Google doesn't have all the answers"

<!-- Slides de PAA:
tinyurl.com/3na6t7dk
-->

- Search in numbers
  - A lot of people
  - From a lot of places
  - Using a lot of devices
    - Smartphones, smartwatch, TV, etc.
    - Exemplo de problemas por dispositivo: se eu estiver usando um speaker, não cabe o retorno de 10 links. Estragaria a experiência do usuário. O texto é muito mais informal e indefinido.
  - Looking for a lot of info
    - Problema: com modelos de imagem generativa, e agora é muito mais fácil de gerar conteúdos falsos.
  - Spread all over the internet
    - É um sistema distribuído; Para onde devo enviar essa query?

---

Nosso foco: Eficiência

- Eficiência é sobre fazer algo, seja boa ou ruim, de forma ótima (mais rápido ou com menos recursos)
- Indicadores chave de performance
  - Latência: demora por busca e muitos documentos
  - Throughput: quantos usuários simultaneamente?
  - Document latency: quão antigos são os documentos?

Eficácia/Efetividade

- Conseguir fazer a coisa certa; Conseguir encontrar os documentos que são relevantes ao usuário.
- Essa relevância é influenciada por vários fatores:
  - Por tópico vs por usuário
  - Por tarefa, contexto, novidade, estilo
  - Quem sabe ao certo a relevância, é o usuário. A máquina de busca apenas estima.

"Se não conseguimos ter certeza absoluta, como podemos nos aproximar o bastante disso?"

- Casamento de strings
  - As LLMs ajudaram bastante na área de casamento de strings.
    - Semântica distribucional
  - Casamento exato
  - Casamento fonético
  - Modificação por radicam (stemming)
  - Dicionário de sinônimos

Ranking models define **a view of** relevance.

- **Dúvida:** por que é usado o termo "documento" e não "página" ou "texto"?
  - "Documento" é um termo mais histórico. Em contexto de web "página" é muito usado, "information item" seria um outro termo genérico válido.

What do search engineers do?

---

- Search pipeline
  - Query
  - query representation
  - Matching + Scoring
  - ONLINE PROCESSING /\
  - OFFLINE PROCESSING \/
  - documento representation
  - Document

- "Já houve alguma pesquisa dizendo que metade das pesquisa feitas num dia são inéditas?"
  - Typos
  - Forma de perguntar
  - Fatos ocorridos recentemente
  - Informações pessoais (CPF)

---

(Continuous) offline processing

- Document acquisition
  - A web é enorme
    - Trillions of known URLs, billions fetched
  - The Web is constantly evolving
    - Updates, additions, deletions
    - Uma situação como o Twitter, até dá para manter um constante fluxo das novas informações e novas postagens, mas para a web como um todo acaba se tornando inviável.
  - Efficient crawling is key
    - Must aim for coverage, but also freshness
- Document understanding
  - Document carry meaning
    - Term-based matching as a first approximation
    - Several techniques to leverage semantics
    - É importante conseguir limpar as informações que se coletam, afinal, as informações de boilerplane não são tão relevantes.
  - Documents vary in quality
    - genuinely: accessibility, readability, authority, depth
    - maliciously: content/link farms, misinformation
- Document indexing
  - Efficient retrieval  through indexes
  - Indexes must be updated
    - New documents, updates, deletionsLike the index of book
      - For each word, a list of document it appears on
    - Broken up into shards of millions of documents
      - 1000s of shards for the web index
    - plus per-document metadata
    - Plus document embeddings

"Representações vetoriais de texto" para possibilitar casamento denso.

---

- Query understanding
  - keywords are poor descriptions of the user's need
    - Interaction and context also matter
  - Query understanding...
    - ...
    - Query scoping through semantic annotation
      - [**san jose** convetion center]
    - Query expansion through acronym expansion
      - [**gm** trucks] -> [**general motors** trucks]
      - [**gm** corns] -> [**genetically modified** corns]
      - "Qual é o ponto exato de corte entre ... e ...? Depende do contexto"
  - Matching and scoring
    - Send the query to all the shards
      - Each shard
        - Finds matching documents
        - Scores each query-document pair
        - Sends back the top n documents
      - Combine all the top documents and sort by score

- **Reflexão:** e se as informações fossem armazenada em hardware assim como são as memórias? Tudo ocorreria basicamente na velocidade da luz, não?

---

- Ranking evaluation
  - Relevance is a user's prerogative
    - We can observe changes in user behavior
    - Or directly ask user how we're doing
  - Evaluation is an empirical science
    - It must be scientifically rigorous
    - It must be economically viable

---

- Course Goals
  - Provide an introductory account of methods for building and evaluating search engines
  - ...
- Course Scope
  - System view
    - Crawling, indexing, retrieval
  - Modeling view
    - Ranking models ("Algumas coisas de machine learning")
  - Behavioral view
    - Ranking evaluation
- Out-of-scope
  - Recommender systems
  - Natural Language Processing
  - Data mining
  - ...
- Course grading (tentative)
  - 50% - Exams
  - 40% - Assignments
  - 10% - Seminars (Pro final da disciplina)
- Chamada
- Course Material: textbooks
  - Search engines: information retrieval in practice
  - Introduction to information retrieval
  - Modern information retrieval
  - Foundations and trends in information retrieval
  - Synthesis lectures on information concepts, retrieval, and services
- Other relevant material
  - General background
    - Algorithms and data structures
    - basic Statistics
    - Basic linear algebra
  - Advanced readings
    - Google Scholar
  - References
    - Search Engines: Information Retrieval in Practice - Ch. 1
    - How Google Works...
    - Pre-course survey

Semana que vem ele envia o material no Moodle.

---

Próxima aula: Search Architecture

## Aula 02 - 17/03/2025

### Slide: Search Architecture

#### Search Infrastructure

- Bandwidth: ...
- Storage: ...
- Processing: crawling, indexing...

Must scale from a single computer in one datacenter...
to huge clusters spread across availability zones

#### Financial costs

- Depreciation: old hardware
- maintenance: failure handling
- Operational: Energy cost

#### Search Architecture

A software achitectuer conssits of software components, the interfaces

- Effectuveness: ...
- Efficiency: ...

#### Search components

World Wide Web > Crawling > Indexing > Query Processing > Ranking > User Interface

- Crawler: é o que navega na internet. Ele gera um Corpus
- Corpus: uma cache da coleção original. Ele é importante para que os dados presentes nele sejam representativos, ou seja, ele filtra a massa de informações presentes na WWW e armazena localmente.
- Indexer: com o corpus, é gerado um índice para facilitar a busca. Um índice invertido é o mais comum.
- Index: serve como um proxy para o que está presente no Corpus, embora possa perder nos detalhes, apresenta um grande ganho na eficiência de busca posterior.
- Query Processor: A pesquisa feita pelo usuário e a forma como ele a busca.

Uma ou mais aulas sobre cada uma dessas coisas. Nessa aula de hoje ele deseja passar de forma mais aprofundade, mas ainda geral, sobre cada um delas.

##### Crawling overview

- Aquisição de documentos: o documento serve como uma generalização de todo o tipo de informação que pode ser buscada. Essa disciplina focará mais na parte textual.
  - BUilds a local corpus for searching
  - Many types - Web, enterprise, desktop

- Web crawlers follow links to find documents
  - Must efficiently find huge numbers of web pages (coverage) and keep them up-to-date (freshness)

---

- Controller: uma forma de definir o comportamento esperado
  - Frontier: uma fila de URLs a serem vasculhadas
- Fetcher: É o que vai buscar a informação da WWW e retorna pro Controller
  - DNS Resolver: uma das partes mais caras, que é a resolução de IP.

```mermaid
flowchart LR

[[Controller]] --> [(Frontier)] --> [[Fetcher]] <-> [[DNS Resolver]] & ((WWW))

[[Fetcher]] --> [[Controller]] --> [(Corpus)]
```

###### Key Challegnes: Crawling

- Web is huge and constantly changing
  - Not under the control of search providers

"O conteúdo em si é selvagem. Tem coisa boa, ruim, bem formatada, mal formatada"

- A lot of time is spent waiting for responses
  - Parallel crawling is essential

- Could potentially flood sites with requests
  - To avoid this problem, use politeness policies
    - [JV: o que seria isso?]
    - "As páginas têm interesse de ser coletados, porque máquinas de busca trazem tráfego. Porém requisições massivas reduzem a resposta de outros usuários, o que pode ser desagradável"

Dúvida de outro aluno: "Se o site é uma ilha: ninguém linka para o meu site e ele não tá indexado, como encontrá-lo?"

Professor: uma forma seriam pelos logs do chrome por exemplo. Se não tá indexado, mas pessoas o acessam, o Chrome talvez tenha algum log e pode informar pro seu BD sobre o site ilhado.

---

##### Indexing Overview

- Document representation
  - From raw text to index terms (Formas buscáveis de representar o texto)
    - Ex.: Autor, data de atualização, etc.
  - Annotations (Ex.: Entidades, categorias, embeddings)
  - Off-document evidente
    - Anchor text, link analysis
      - Texto de âncora é o texto presente...
        - `<a href="https://www.google.com">ESSE TEXTO AQUI</a>`
        - Esse tipo de informação é útil caso, por exemplo, se o site da UOL não citasse "notícias", mesmo que seja sobre notícias, porém, se nos anchor texts essa informação estivesse presente, seria possível inferir que o site é sobre notícias.
    - Social Network Signals

---

- Document representation
  - Topical Features: informações textuais presentes no documento
  - Quality Features: Incoming links, days since last update

---

```mermaid
flowchart lr

CP[(Crpus)]
PR[[Parser]]
TK[[Tokenizer]]
AN[[Analyser]]
WR[[Writer]]
ID[(Index)]

CP --> PR --> TK --> AN --> WR --> ID
```

- Corpus
- Parser: filtra de alguma forma o texto
- Tokenizer: separa em blocos de texto úteis [JV: é mais ou menos isso]
- Analyzer: processa mai
- Writer: armazena o que foi analizado de alguma forma
- Index: estoca os dados encontrados

###### Key challenges: Indexing

- Support effective retrieval
  - Extract meaningful document features
  - Both ropical and quality features
- Support efficient retrieval
  - ...

###### Index Structures

Uma das estruturas mais comuns é o índice invertido.

---

Example "Corpus"

Incidence Matrix: geralmente não se armazenam em matrizes por ocupar muito espaço.

O índice invertido é basicamente uma lista de adjacência.

Uma forma de enriquecer o índice é através da adição de frequência de cada uma das palavras.

Outro método poderia ser a informação da posição em que aparece a palavra. A importância disso é que, se o usuário está buscando por duas palavras, é esperado que essas duas palavras, caso encontradas no índice remissivo esteja próximas entre si.

- Inverted index: fields
  - Document structure is useful in search
    - field restrictions (date, from)
    - Some fields are more important than others
  - ...

- Auxiliary Structures
  - Vocabulary, dictionary, or lexicon
    - Lookup table from term to inverted list
      - Pode-se armazenar um mapa de determinada palavra para que se defina a posição na memória em que a informação está guardada
    - Either Hash table in memory or B-tree for disk
  - Additional strucures for document data
    - Basic statistics, static features, metadata
  - Additional strucutre for corpus statistics

##### Query Processing Overview

- Query representation
  - Infers user's need from a keyword query
- Document ranking
  - Matches...
- ...

---

```mermaid
flowchart LR

Person ((Actor))
Und[[Understanding]]
Know[[Knowledge Resources]]

Person -->|Query/Feedback| Und
Und <--> Know
...
```

- Query
  - Understanding
    - Knowledge Resources
      - Query Logs
      - Knowledge bases
      - User Preferences
  - Matching
    - Index
  - Scoring
    - Ranking Model
- Usuário

###### Key Challenges: Query Processing

- Queries are typically short, ill-specified
  - Long queries tend to be difficult
- Finding matching documents can be expensive
  - Particularly for common terms or long queries
- Ranking is a tough business
  - Different Queries, different requirements

---

###### Query Understanding

É basicamente uma mudança da consulta. Onde a máquina de busca muda o que foi pesquisado originalmente para melhorar a pesquisa.

- expand matches
  - Query relaxation: aumentar a chance de encontrar o que o usuário quer
    - [Information about tropical fish]
      - [Tropical Fish]
  - Query expansion: aumentar a chance de encontrar o que o usuário quer
    - [Tropical Fish]
- Narrow results
  - Query Segmentation
    - Tropical Fish captive breeding
      - ["Tropical fish" AND "captive breeding"]
  - Query Scoping
    - [Tropical fish hawaii]
      - [Category: "Tropical fish" place: hawaii]

---

##### Document Matching

- Scan postings lists for all query terms

"A Web é tão grande, que geralmente usa-se o AND, e mesmo assim encontra muita coisa."

- Scoring matching documents
  - $f(q, d) = \sum_{t \in q} f(t, d)$

---

- Many alternatives
  - Lexical models (bag-of-words)
  - Structural models (query + document structure)
  - Semantic models (implicit + explicit semantics)
  - Interactive models (user feedback)
  - Feature-based models (AKA learning to rank)

#### Summary

- Search is a tough business
  - Big data, big usage
- An architecture tailored for efficiency is crucial
  - Crawling, indexing, query processing
- Must also cater for effectiveness
  - Rule of thumb: don't throw anything away
  - "Mantenha tudo o que você puder manter. Só o que você não quiser manter, aí joga fora, caso esteja além do orçamento"

#### References

- Search Engines: Information Retrieval in Practice

#### Coming Next: Web Crawling
