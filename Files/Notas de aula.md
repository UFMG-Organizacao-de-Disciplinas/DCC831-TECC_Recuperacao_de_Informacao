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

## Aula 03 - 19/03/2025

### Slide - 03-web-crawling

#### Web Crawling

- Outros nomes: spiders, harversters
- Funciona para fazer caches

---

##### Success measures

- Coverage: quanto da web foi coberto
- Freshness: quão atualizados estão
- Utility: qual fração das páginas úteis foram coletadas?
- Efficiency: bytes baixados por unidade de tempo

#### Crawling overview (2)

WWW -> Fetcher --> Controller -> Frontier -> Fetcher -> WWW

---

Pseudocódigo

Em casos de crawlers, a tendência é que o loop seja infinito. Ele tende a revisitar páginas já vistas. Além disso existe páginas dinâmicas que podem sempre direcionar a páginas seguintes. Talvez algo como a Biblioteca de Alexandria. Isso, desconsiderando a criação contínua de páginas.

No geral, os crawlers são feitos já com a intenção de serem executados continuamente.

```python
def crawler (frontier, corpus):
  while not frontier.empty():
    url = frontier.pop() # Control
    if crawlable(url): # Politeness
      content = fetch(url) # Networking
      corpus.store(url, content) # storage
      for outlink in parse (content): # Processing
        frontier.enqueue(outlink) # Control
```

- Control: definir como priorizar as urls
- Politeness: evitar floodar o site
- Networking:
- Storage: armazenar o conteúdo; Quanto? Quais? O quê?
- Processing: o que fazer com o conteúdo?

---

#### Crawl Seeding

- Quais URLs começar?
  - Que eu comece com HUBs, que são páginas que apontam para muitas outras páginas
  - Sitemaps
  - Seed URLs

#### Traversing

- Separar as filas por descoberta e atualização
  
  - Lista de busca
    - URLs que apontam para páginas baixadas.
    - O objetivo é aumentar a busca
  - Lista de atualização
    - URLs já baixadas.
    - O objetivo é manter a atualização

##### Enqueuing policy

- Deve-se manter um registro das URLs
  - Idealmente, a complexidade deve ser O(1), então um hash é uma boa alternativa.
  - Seria interessante então o uso de um SGBD que use Key-Value pair.
  - Preferencialmente que esteja em memória e não em disco pra não demorar tanto.

###### URL Keying

- Múltiplas URLs mapeiam para a mesma página
  - <http:/www.cnn.com:80/x/../index.html> -> <cnn.com>
    - Nome de domínio é case-insensitive;
    - Porta HTTP padrão pode ser ignorada;
    - WWW é desnecessário?
- A normalização auxilia a ter chaves únicas para uma mesma página
  - Remover fragmentos de foco como "#section"

"Existem mudanças que são mais ou menos perigosas de se alterar." Perigosas no sentido de que podem acabar atrapalhando o busca por páginas.

##### Dequeuing Policy

- O importante é encontrar as páginas importantes rapidamente
  - Tanto por descoberta, quando por revisitação.

[JV: Plus Flags: posso fazer um grafo de como as páginas estão interligadas. posso tentar botar um timestamp de momento em que foi pesquisado.]

- Políticas de descoberta
  - Aleatórias?
  - Em ordem (BFS)
  - Centralidade (indegree; PageRank)
    - Afinal, se eu já sei que uma página já tem um alto nível de indegree, por que ainda não a baixei? Ela já deveria ser baixada
- Políticas de revisitação
  - Aleatória
  - Centralidade (indegree, PageRank)
  - Impacto (clicks, quantidade de visualizações, likes, compartilhamentos)
  - Idade (tempo desde a última vez que foi vasculhada)
  - Longevidade (frequência de atualização)
    - Porém, se a página é atualizada com muita frequência, talvez não seja necessário revisitar com tanta frequência. Seria muito custoso.

##### Page fetching

[(Frontier)] -->|"foo.com/bar; foo.com/baz"| Fetcher -->|foo.com| DNS Server <--> [(DNS Cache)]

[(DNS Cache)] -->|208.77.188.166| Fetcher

Fetcher -->|Connect| WebServer

##### Multi-threading

- Crawling é uma tarefa limitada pela rede
  - Crawlers podem usar múltiplas threads para buscar várias páginas ao mesmo tempo
- Embora um nó possa rodar várias threads de crawling, a CPU por si só também tem suas limitações.
  - Então, isso tende a se tornar gargalo antes de exaurir a banda.

##### Politeness

- Requisições excessivas e não coordenadas podem gerar estresse aos servidores ou sub redes de determinada plataforma.

- Um craler "educado"
  - Mantém apenas uma conexão TCP-IP aberta por servidor
  - Adiciona um delay entre requisições consecutivas.

##### Robots exclusion protocol

- Um padrão da WWW desde os primórdios
  - robots.txt ajuda a guiar os web crawlers por onde sugerem ou não.
  - Esse aquivo não serve como uma regra, mas é um acordo de cavalheiros. É ideal que o coletor leia esse arquivo, processe, e entenda o que pode ou não fazer.
  - Indica quais comportamentos que os bots são aconselhados a ter.
  - A Google informou que não respeitaria mais o crawl-delay do robots.txt porque eles sabe o bastante para considerar que tende a ser mais prejudicial do que benéfico caso ele dê um delay maior.
  - "Ao invés da máquina de busca respeitar o site, o dono do site que reclame de abusos das máquinas de busca".

##### Mirror Sites

- Uma réplica do site, com tráfico reduzido mas com foco em disponibilidade.
- Sites Mirror podem ser detectados com a similaridade da URL, a estrutura de links e as similaridades de coonteúdo.

##### Sitemap protocol

- Sitemap.xml
  - Traz uma forma de índice do site

#### Crawling architecture

- Single node (não escalável)
  - CPU, RAM and disk becomes a bottleneck
- Multi-node (Escalável)
  - Distribuição de carga
  - Paralelismo
  - Redundância
- Distribuída geograficamente (escalável, latência reduzida)
  - Existem registros de geo-localização de IPs, então é possível saber onde estão os servidores.

##### Distributed Web Crawling

- Web partida por URL Hashing
  - Pode causar crawling impolite
- Web partida por host hashing
  - Politeness controlada pelo host
- Nós diferentes podem acabar coletando a mesma URL

[JV: Plus Flags: Uma AVL balanceada pelos pesos das páginas, pesos esses dados pela frequência com que uma certa página já foi visitada antes.]

Dúvida: como manter a rede TCP-IP ligada entre nós distribuídos?

##### Benefícios

- Maior crawling throughput
  - Proximidade geográfica que reduz a latência do crawling
- Aumento da politeness de rede
  - menor demanda nos roteadores
- Resiliência às partições da rede
  - Melhor cobertura e disponilidade alta

#### Parsing

- Texto é armazenado em diversos formatos incompatíveis
  - Raw text, RTF, HTML, XML, MS Word, ODF, PDF, ...
- Tipicamente use uma ferramenta de conversão do conteudo em algum formato de texto marcado
  - HTML, XML
  - Mantendo a informação relevante nessa estrutura

##### Character Encoding

- Conversão entre bits e glifos
  - Converter bits em caracteres na tela
  - Pode ser uma grande fonte de incompatibilidade

Existem técnicas para identificação de encodings.

- ASCII é um esquema de encoding padrão e simples pro Inglês
  - Unicode tenta unir todos os glifos comumentes usados.

##### Removing noise

- Remover textos, links e figuras que podem não estar relacionadas ao conteúdo da página.
  - Esse conteúdo noisy (barulhento), pode impactar negativamente o ranqueamento
- Existem várias técnicas que detectam esses blocos de conteúdos
  - Page content vs ads
  - Material que não é conteudo é ignorado ou flagged.

##### Content storage

- Armazenar o texto do documento
  - Extração eficiente da extração: Snippets
- Requisitos para os documentos do sistemas de armazenamento
  - Acesso randômico por hashed URL
  - Atualizações rápidas (modificações, anchor text)
  - Representação comprimida

##### Compression

- Texto é altamente redundante ou previsível
  - A compressão explora a redundância para fazer arquivos menores sem perder nada do conteúdo.
- Algoritmos populares conseguem comprimir HTML em 80%
  - DEFLATE(zip, gzip) and LZW (Unix Compress, PDF)
  - Comprimir arquivos grandes para tornar o acesso mais rápido

##### Focused Web Crawling

- O objetivo é buscar páginas temáticas
  - Tópico (Energia nuclear)
  - Gênero (music)
  - Type (forums)
  - Demographics (kids)

Ele comentou sobre uma startup que foca em dar notícias importantes para CEO's de empresas direcionadas a eles.

[JV: Dissertation: posso propor algo como um "sitemap" que consiga definir as características dos objetos. Acho que o BIM tem algo assim. RDF?]

##### Deep Web Crawling

- Crawling traditionally focused on the surface Web
  - Web pages accessible by following links
- Conteúdo escondido mas potencialmente útil
  - Páginas não linkadas
  - Sites Privados
  - Conteúdo Scriptado

- Ferramentas de exploração
  - Selenium
  - Microsoft Playride
- Uma máquina de busca conseguiria simular o uso de botões e formulários em páginas? Ele considera que sim.

### Summary - Aula 3

- O Scopus é um cache da Web que viabilida indexação e busca mais rápida
- A Web é um ambiente grande e dinâmico
- Deve-se visar a cobertura e atualização, preferencialmente mantendo o politeness
- Several open Challenges

### Referências

Search Engines: Information Retrieval in Practice, Ch. 3Croft et al., 2009

Scalability Challenges in Web Search Engines, Ch. 2Cambazoglu and Baeza-Yates, 2015

### Próxima aula: Document Understanding

## Aula 04 - 24/03/2025 - Document Understanding

## Aula 05 - 26/03/2025 - Document Indexing

## Aula 06 - 31/03/2025 - Query Understanding

## Aula 07 - 02/04/2025 - Document Matching

## Aula 08 - 07/04/2025 - Efficient Matching

## Aula 09 - 09/04/2025 - Vector Space Models

## Aula 10 - 14/04/2025 - Language Models

## Aula 11 - 16/04/2025 - Experimental Methods

## Aula 12 - 21/04/2025 - Offline Evaluation

## Aula 13 - 23/04/2025 - Exam #1

## Aula 14 - 28/04/2025 - Quality Models

## Aula 15 - 30/04/2025 - Feedback Models

## Aula 16 - 05/05/2025 - Diversification Models

## Aula 17 - 07/05/2025 - Learning to Rank: Fundamentals

## Aula 18 - 12/05/2025 - Learning to Rank: Algorithms

## Aula 19 - 14/05/2025 - Neural Models: Reranking

## Aula 20 - 19/05/2025 - Neural Models: Retrieval

## Aula 21 - 21/05/2025 - Online Evaluation

## Aula 22 - 26/05/2025 - Online Learning to Rank

## Aula 23 - 28/05/2025 - Seminars

## Aula 24 - 02/06/2025 - Seminars

## Aula 25 - 04/06/2025 - Exam #2

## --- - 09/06/2025 - Recess: Corpus Christi

## Aula 26 - 11/06/2025 - RC Development (off-class)

## Aula 27 - 16/06/2025 - RC Presentations

## Aula 28 - 18/06/2025 - RC Presentations

## Aula 29 - 23/06/2025 - Replacement Exam

## Aula 30 - 25/06/2025 - Resit Exam
