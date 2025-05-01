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
  - Efficient retrieval through indexes
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

## Aula 04 - 24/03/2025 - Document Understanding Slide: 04-???

### Search Components

```mermaid
flowchart LR
WWW --> Crawler
Crawler --> Corpus[(Corpus)]
Corpus[(Corpus)] --> Indexer
Indexer --> Index[(Index)]
Index[(Index)] <--> Query_Processor
Query_Processor <--> Actor
```

### Indexing Overview (2)

```mermaid
flowchart LR
[(Corpus)] --> Document Understanding --> Writer --> Index
```

```mermaid
flowchart LR
subgraph Document Understanding
  Parser --> Tokenizer --> Analyzer
endsubgraph
```

- Por que não escrever diretamente no índice?

#### Document Understanding

- Entender o texto é desafiador
  - Nem sempre está claro o que é
  - Nem sempre está claro o que os termos significam
- ...

#### Documento Parsing

- Assumido previamente]
  - Sabemos o que o documento é
  - Podemos "machine-read" cada documetno

##### What is a document?

- Or, in IR parlance, what is our Retrieval Unit? ("Ou, em jargão de Recuperação de Informação, o que seria uma Unidade de Recuperação?")
  - Um arquivo simples?
  - Um email com 5 anexos?
  - Um livro com 15 capítulos?
- Quais tipos serão aceitos?
  - Text/html? Application/pdf? Word?

##### How to read a document?

- Idealmente deve lidar com estruturas
  - Texto vs binário, texto vs markup
- Nem sempre é bonito...

```html
<div id="foo">
  <div id="bar">
    <span> Test</span>
  </div>
</div>
```

BeautifulSoup é um dos mais conhecidos pra lidar com isso.

---

- Must handle encoding
  - Traduzir entre bits e characteres
- às vezes, múltiplas, e não especificadas

ISO 88591 (?) para caracteres latinos

UTF=8 Tá se tornando mais popular

#### Document Tokenization

Agrupar palavras em grupos. Talvez várias palavras.

Podem ser várias palavras em um token, ou até subpalavras.

Um par de palavras seria um bigrama

##### How to Tokenize

- One simple strategy (early IR Systems)
  - Any sequence of 3+ alphanumeric charactes
  - Terminado em espaço
  - Ignorado lowercase e uppercase

###### What could go wrong

- Ex

  - Bigcorp's 2007 bi-annual report showed profits of 10%
  - Bigcorp s 2007 bi annual report showed profits of 10
  - Bigcorp 2007 annual report showed profits

- Muita informação perdida
  - Pequenas tokenização podem impactar muito à efetividade de algumas buscas

##### Token Length

- Palavras pequenas tendem a ser pouco representativas.
  - a, an, be, of, to
- Porém elas também ajudam a remover a disambiguation
  - ben e king, el paso, master p, world war ii
- Ou até crucial ao matching
  - xp, ma, pm, gm, j lo, c

##### Special Characters

- Apostrophes podem fazer parte da palavra, possessivo ou um erro
  - Rosie o'donnel, can't, don't, 80's, master's degree
- Acentos e diacríticos podem mudar o sentido
  - résumé vs resume, cocô vs coco

Uma solução pra isso seria considerar que algumas palavras cujo significado com acentuação são casos especiais e devem ser tratadas como tal.

---

- Periods podem ocorrer em números, abreviações, URLs, fim de frase, etc.
  - I.B.M.
- Hífens

##### Numbers and lowercasing

- Números podem ser importantes, inclusive os decimais
  - Nokia 3250, top 10 courses, united 93, quicktime 6.5

Com essa abordagem clássica, estamos tomando as rédeas de todo o processo. O que pode não ocorrer se delegarmos à uma LLM por exemplo

- Lowercasing can change meaning
  - Bush vs bush; Apple vs apple

##### Non-delimited tokens

- How to tokenize this?
  - White House aides wrestle with Trump's comments

Mas e tokens sem espaços?

- How about these?
  - whitehouse.gov, #ImpeachTrump
- And this?!
  - [Texto em Japonês]

Como quebrar "Whitehouse"?

9 Pontos possíveis de quebra. Há uma combinação de possibilidades. Algumas estratégias de particionamento são mais prováveis que outras.

Quão provável é "W" "hitehouse"? E "Whit", "ehou", "se"?

Pode-se fazer probabilisticamente com um log de [alguma coisa]

#### Token Analysis

...

##### Discriminative Power

É como definir quão importantes são as palavras pro contexto.

Document Frequency (in millions)

- Saltwater: 46
- Freshwater: 95
- Aquatic: 118
- Species: 377
- And: 25270
- In: 25270
- The: 25270

##### Stopping

- Discard poorly discriminative works (stopwords)
  - a, an, and, are, as, at, be, by, for, from, has, he, in, is, etc.

Mas e como determinar esse corte em uma linguagem arbitrária?

Determinar um limite, um threshold de frequência das palavras encontradas na nossa coleção.

- Pode ser padronizado ou automaticamente definida

  - Pode depender do domínio/contexto: "click" for anchor text

- Pergunta: Como separar as stopwords das entidades?
  - Na pipeline a função de detecção de entidades viria antes da de stopwords

---

- Reduzir espaço no índice e tempo de resposta
  - Pode aumentar a efetividade
- Desencorajado nas máquinas de busca modernas
  - Stopwords podem ser importantes quando combinadas
    - to be, or not to be: that is the question
      - Question

##### Equivalence classing

- Reduzir as palavras à sua forma canônica
  - Equivalência léxica
  - Equivalência fonética
  - Equivalência semântica

Geralmente apenas fazemos a busca de casamento exato das palavras.

###### Lexical Equivalence

- Many morphological variations of words
  - Inflectional: plural, tenses
  - Derivational: making verbs into nouns
- In most cases, these have very similar meanings
  - Swimming, swam -> Swim

---

- **Stemming**
  - Reduz morfologicamente as variáções ao seu stem (tronco)
    - Geralmente remove sufixos
  - ...Lemmatization...
  - **Porter's Stemmer**
    - SSESS -> SS
    - IES -> I
    - SS -> SS
    - S ->
  - **Stemming effectiveness**
    - Usualmente aumenta a quantidade de retornos
      - Porém, pode danificar a precisão da busca: aumenta tanto o retorno por trazer casamentos parecidos, porém pode gerar falsos positivos
    - Falsos positivos
      - Ex: universal, university, universe -> univers
    - Falso negativo
      - Alumnus -> Alumnu; Alumni -> alumni

###### Fonetic and semantic Equivalence

- Fonética
  - Reduz palavras que soam parecido à mesma forma
    - Hermann <-> Herman
- Semântica
  - diferentes paravas a um mesmo conceito

Pergunta do professor: se isso fosse uma API, como poderia funcionar

Resposta professor: basicamente retornaria a forma canônica da palavra, já tendo sido filtrada em todas as formas desejadas.

Minha resposta:

#### Phrasing

- Muitas queries são frases de 2-3 palavras
  - ...

---

- Estratégias:
  - Fraseamento sintático
  - ...

##### Syntactic phrasing

- Part-of-Speech (POS) taggers podem determinar as palavras de acordo com sua função sintática na linguagem natural
  - NN (Singular Noun), NNS (plural nouns), etc.
- ...

---

###### POS Tagging Example

[Texto]

Ele exemplificou casos de padrões frequentes no inglês onde NN seguido de NNS, por exemplo, seria um conceito padrão.

##### Statistical phrasing

- POS tagging é lento demais para coleções grandes
  - Realmente é necessária a análise sintática completa?
- Definição mais simples: frases como n-gramas
  - Unigrama - 1 palavra
  - Bigrama - 2 palavras
  - Trigrama - 3 palavras

---

- As frequências de N-gramas formam uma distribuição Zipf
  - Algumas muito frequentes, outras pouco
  - ...

---

- Google n-grams

#### Scoping

- Documentos geralmente têm uma estrutura
  - HTML tags: h1, h2, p, a
- Nem todas as partes são relevantes
  - Título, URL, metadado, seções do corpo
- ...

#### Summary - Aula 04

- O entendimento dos documentos aumenta na representação, um exemplo disso é casar coisas e não strings.
- Várias decisões importantes: talvez não se saiba o que seria importante durante a indexação.
  - Nesse caso, postergue. Não há necessidade de fazer tudo imediatamente, porém esteja preparado para arcar com o custo
- KISS (Keep It Simple, Stupid), but keep it all

---

- Indexing vs querying
  - Stopping VS Query Relaxation
  - Equivalence Classing VS Query Expansion
  - Phrasing VS Query segmentation
  - Scoping VS Query Scoping

#### Referências - Aula 04

#### Próxima aula

## Aula 05 - 26/03/2025 - Document Indexing | Slide - Indexing

- Trabalho Prático 1: Crawler
- Trabalho Prático 2: Buscador simples
- Research Challenge: Usar o Kaggle, testar várias coisas
- Replacement: Substitutiva, quase que uma segunda chamada, sem precisar de justificativa
- Provas: 2 provas, fechadas ou abertas; Ainda tá decidindo.

### Search Components (Aula 5)

...

---

...

#### Key challenges

...

#### Success Metrics

- Qualidade
  - Utilidade do conteúdo: pouco spam, bons matches
  - Efetividade
- Performance
  - Compactação: tamanho do índice em bytes
  - Custo do deployment: tempo para construir e atualizar o índice

### Document Prefiltering

- Detectar spams
  - Term spamming -> Text classification
  - Link Spamming -> trust propagation
    - PageRank: as páginas que recebem links
    - Dúvida: determinada página tem registro de quais são as páginas que tem inlinks para si?
      - Resposta: usualmente não. Blogs talvez sim tenham os backlinks
- Detectar documentos com conteúdo duplicado
  - Exact duplicates: compare hash
  - Near duplicates -> compare _shingles_ instead

#### Near duplicates via $n$-shingling

- Pega diversos 2-gramas da página
- Efetua os hashes desses bigramas
- Seleciona o n-menores valores de cada um
- E então efetua o cálculo de Jaccard:
  - $J(A, B) = \frac{|A \cap B|}{|A \cup B|}$
  - Se $J(A, B) > \theta$, então são considerados near duplicates
  - $\theta$ é um threshold. No slide foi definido como sendo 0.5

### Document Features

- Features computed offline
  - **Conteúdo:** Spam score, domain quality score
  - **Web Graph:** PAgeRank, HostRank
  - **Usage:** click count, CTR, dwell time
    - Essas informações estariam disponíveis apenas para os hosts dos sites, ou donos das máquinas de busca e navegadores
- Features computed online
  - **Query-Documento similarity:** TF-IDF, BM25, etc.
    - [JV: Ele falou brevemente mas não me atentei]

### Indexing Overview (Aula 05)

...

---

...

### Document understanding (Aula 05)

- Parsing + tokenization
  - Turn raw text into indexing terms
- Token analysis
  - Discriminative power
  - Equivalence classing
  - Phrasing, scoping

### Document indexing

O objetivo é evitar fazer um grep em todas as páginas.

Dúvida: grep é para fazer a busca exata?

- Indexing makes crawled documents searchable
  - Efficient searching requires appropriate structures
- Abandoned indexing data structures
  - Suffix arrays, signature files
- Currently used data structure
  - Inverted index

#### Example "corpus"

##### Incidence Matrix

Problema: esparsidade da estrutura

##### Inverted index: incidence

Basicamente é uma lista de adjacência, onde cada elemento da lista se chama "posting". E o que armazenamos no "posting" é escolha nossa.

##### Inverted index: frequency

Uma das informações que podemos armazenar é a frequência de cada palavra.

Para isso, geralmente armazenamos o índice do documento (que tende a ser na casa dos milhares/milhões) e depois a frequência de ocorrência, que usualmente não passa da casa das centenas.

##### Inverted index: additional info

- Term positions
  - Exact phrases vs. proximity search
- Document structure
  - Field restrictions (e.g., date:, from:)
  - Some fields more important (e.g., title, h1)

#### Inverted List Compression

- Observação: a representação usual é custosa [Em relação a quantidade de bytes]

---

- Ideia base:
  - Representação sem perda de informação usando menos bits
  - Diversas abordagens [[Catena et al., ECIR 2014]](https://doi.org/10.1007/978-3-319-06028-6_30)
- Benefícios
  - Reduz o custo de espaço e rede/reduz o tempo de transferência de disco
  - Custo: overhead de descompressão

##### Example: unary encoding

- Algoritmo:
  - represente o número como sendo ele mesmo como esse número de zeros seguido do número 1
- Exemplo:
  - 5 -> 000001
  - 7 -> 00000001

##### Example: gamma encoding

- Algoritmo:
  - Unário primeiro baseado no...
    - binary digits of k minus 1: (conta todos os dígitos a partir do primeiro 1 à esquerda até a direita)
  - Seguindo dos l - 1 dígitos menos relevantes

[JV: explicar melhor depois]

#### Inverted List Compression (Round 2)

- Ao invés de armazenar o número do ID, armazene os deltas entre os índices:
  - fish: (1:2), (2:3), (3:2), (4:2)
  - fish: (1:2), (1:3), (1:2), (1:2) [passo 1]

#### Document Identifier Reordering

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

#### Index Construction

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

##### External Indexing

- Merging addresses limited memory problem
  - Build the inverted list structure until memory runs out
  - Write partial index to disk, start making a new one
- At the end of this process
  - Merge many partial indexes in memory
  - Equivalent to an external mergesort

---

##### External Merging

---

##### Internal Merging

---

##### External Merging (Round 2)

---

#### Index maintenance

- Index merging efficient for large updates
  - Overhead makes it inefficient for small updates
- Instead, create separate index for new documents
  - Merge results from both indexes
- Could be in-memory, fast to update and search
  - Also works for updates and deletions

Basicamente seria utilizado um sistema de armazenamento mais parudo para guardar o grande volume de dados, e um outro, temporário, ou menor, que seria como um buffer, que, quando enchesse, seria jogado no maior.

#### Distributed indexing

- Distributed processing driven by need to index and analyze huge amounts of data (i.e., the Web)
  - Large numbers of inexpensive servers used rather than larger, more expensive machines
- MapReduce is a distributed programming tool designed for indexing and analysis tasks

##### The MapReduce framework [[Dean and Ghemawat, USENIX 2004](https://www.usenix.org/legacy/event/osdi04/tech/full_papers/dean/dean.pdf)]

- Key idea: keep data and processing together
  - Bring code to data!
- Map and reduce functions
  - Inspired by functional programming
- Constrained program structure
  - But massive parallelization!

Pode acabar terminando com vários sub índices que precisariam ser posteriormente agrupados.

##### Distributed indexing with MapReduce [[McCreadie et al. IP&M 2012](https://www.sciencedirect.com/science/article/pii/S0306457319304455)]

##### Index sharding and replication

Parece um pouco com o conceito de RAIDS de armazenamento.

- Multiple index shards
  - Reduce query response times
  - Scale with collection size
- Multiple shard replicas
  - Increase query throughput
  - Scale with query volume
  - Provide fault tolerance

###### Index Sharding

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

#### Summary (Aula 05)

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

#### References - Aula 05

- [Search Engines: Information Retrieval in Practice, Ch. 5 Croft et al., 2009](https://www.amazon.com/Search-Engines-Information-Retrieval-Practice/dp/0136072240)
- [Scalability Challenges in Web Search Engines, Ch. 3 Cambazoglu and Baeza-Yates, 2015](https://doi.org/10.2200/S00662ED1V01Y201508ICR045)

#### Próxima aula: Query Understanding

## Aula 06 - 31/03/2025 - Query Understanding

### Trabalho Prático

### Search Components (Aula 6)

```mermaid
flowchart LR
  WWW --> Crawler
  Crawler --> Corpus[(Corpus)]
  Corpus[(Corpus)] --> Indexer
  Indexer --> Index[(Index)]
  Index[(Index)] <--> Query_Processor
  Query_Processor <--> Actor
```

---

```mermaid
flowchart LR
Index[(Index)] <--> Query_Processor
Query_Processor <--> Actor
```

### Query Processing Overview (Aula 6)

```mermaid
flowchart LR
Actor -->|"Query|feedback"| Understanding
Index[(Index)] --> Matching
Understanding --> Matching
Understanding <--> KR[("Knowledge Resources: (Query Logs, Knowledge bases, User Preferences)")]
Matching --> Scoring
RM[(Ranking Model)] --> Scoring
Scoring --> Actor
```

A ideia é que a gente, a partir da consulta, consigamos enriquecer a pesquisa com informações adicionais pressupostas.

Depois case com as informações esperadas

Por fim ranqueie as informações encontradas.

### Queries and Information Needs

- A query can represent very different information needs
  - May require different search techniques and ranking algorithms to produce the best rankings
- A query is often a poor representation of a need
  - Users may find it difficult to express what they want
  - Users may assume the search engine will guess

Engenharia de Promps em LLM: como formatar sua query da melhor forma possível para que o modelo consiga entender o que você quer.

Uma máquina de busca muito robusta, consegue processar bem e deduzir o que o usuário quer. Isso desincentiva o usuário a explicar melhor o que deseja, porém, indica que a máquina de busca está cada vez mais inteligente.

#### Complexity Matters

- Head Queries <--> Tail Queries
  - Head Queries: Shorter, More popular, Less complex
    - Navegacional: quero acessar a página X
  - Tail Queries: Longer, Less popular, More complex
    - Informacional: quero informações sobre XYZ

#### Query Length

- Power law distribution:
  - $p(k) = Ck^{-s}$ for $k \geq k_0$
  - $C$ is a normalizing constant, $s$ is a slope, $k_0$ is a lower bound from which power law holds

Entendimento: consultas pequenas são **muito** mais frequentes que consultas grandes.

##### Long Queries

- Yahoo! (2006) claimed 17% queries with 5+ words
  - Current trend toward longer queries

Um exemplo disso são as pesquisa por voz. E também as assistentes pessoais como o Google, Siri e Alexa. Ah, é mencionado logo abaixo.

- Task-oriented search
  - Question answering, literature search, cut-and-paste
- Voice-activated search
  - Microsoft Cortana, Apple Siri, Google Assistant

#### Complex queries

- Long queries are also complex
  - Rarity of verbose queries
  - High degree of query specificity
  - Term redundancy or extraneous terms (lot of noise)
  - Lack of sufficient natural language parsing
  - Hard to distinguish key and complementary concepts

Uma das principais vantagens de uma LLM nos dias de hoje seria nessa parte. A parte de entendimentos de consulta foi um dos que mais avançou.

#### Context matters

- "It's raining"
  - ... says the weatherman, conveying the weather
  - ... writes the poet, conveying sadness in their work
  - ... says your mom, indicating you should put on a coat
  - ... says one bored person to another

"Uma mesma expressão depende do contexto" A máquina de busca pode não saber desse contexto extra.

### Query understanding

- About what happens **before** ranking
  - How users express their queries
  - How we can interpret their needs
- Queries as first-class citizens
  - ~~How to improve ranking regardless of query~~
  - How to improve query regardless of ranking

"Atualmente já se saturou quanto às técnicas de ranqueamento. O que se busca é melhorar a consulta."

### A host of techniques

- Query preprocessing
  - Language detection
  - Character filtering
  - Query tokenization
  - Spelling correction
  - Inflection handling

Identificar o idioma para direcionar mais. Tratar acentos? O que fazer com a pontuação?

- Query rewriting
  - Query relaxation
  - Query expansion
  - Query segmentation
  - Query scoping

Como ser mais acertivo para encontrar aquili que desejo?

### Spelling correction

- 10-15% of all web queries have spelling errors
  - For today's searchers, a search engine without robust spelling correction simply doesn't work

---

- How to (mis)spell "Britney Spears"
  - britney spears
  - brittany spears
  - brittney spears
  - britany spears
  - britny spears
  - briteny spears
  - britteny spears
  - briney spears
  - brittny spears
  - brintey spears
  - britanny spears
  - britiny spears
  - britnet spears
  - britiney spears
  - britaney spears
  - britnay spears
  - brithney spears
  - ...

---

- Identify misspelled query words
  - Those not found in a spelling dictionary

Espera-se que a mais frequentemente pesquisada seja a correta.

- Identify candidate corrections
  - Dictionary words similar to the misspelled word

Usar um vetor denso para representar as palavras e calcular a distância do significado delas pode não ser uma boa ideia pois poderia acabar gerando um problema. Não queremos similaridade semântica, mas a sintática.

Distância de Edição entre strings.

- Display candidate corrections
  - Ideally, the single best one

### Identifying candidate corrections

- Compute edit distance
  - Minimum number of insertions, deletions, substitutions, or transpositions of single characters
- extenssions $\to$ extensions (insertion error)
- poiner $\to$ pointer (deletion error)
- marshmellow $\to$ marshmallow (substitution error)
- brimingham $\to$ birmingham (transposition error)

Como baratear o custo de calcular a distância de edição de uma palavra errada com todas as palavras corretas?

Possibilidade 1: Palavras que tenham a mesma substring

Possibilidade 2: Palavras que tenham o mesmo tamanho ou próximo

Se não estiver encontrando nenhuma solução apropriada, pode-se afrouxar os critérios.

---

- Edit distance calculation can be sped up
  - Restrict to words starting with same character
  - Restrict to words of same or similar length
  - Restrict to words that sound the same

#### Phonetic encoding (Soundex)

1. Keep the 1st letter (in uppercase)
2. Replace with hyphens: a, e, i, o, u, y, h, w $\to$ –
3. Replace with numbers:
   1. b, f, p, v $\to$ 1
   2. c, g, j, k, q, s, x, z $\to$ 2
   3. d, t $\to$ 3
   4. l $\to$ 4
   5. m, n $\to$ 5
   6. r $\to$ 6
4. Delete adjacent repeats of a number
5. Delete hyphens
6. Keep first 3 numbers and pad with zeros

|   # | extenssions | extensions |
| --: | ----------- | ---------- |
|   1 | Extenssions | Extensions |
|   2 | Ext–nss––ns | Ext–ns––ns |
|   3 | E23–522––52 | E23–52––52 |
|   4 | E23–52––52  | E23–52––52 |
|   5 | E235252     | E235252    |
|   6 | E235        | E235       |

---

Contraexemplo: falso negativo

|   # | poiner | pointer |
| --: | ------ | ------- |
|   1 | Poiner | Pointer |
|   2 | P––n–r | P––nt–r |
|   3 | P––5–6 | P––53–6 |
|   4 | P––5–6 | P––53–6 |
|   5 | P56    | P536    |
|   6 | P560   | P536    |

### Displaying the best correction

- There might be several candidate corrections
  - We can display only one ("Did you mean ...")

Isso por questão de custo e também por interface.

- Best correction depends on context
  - lawers $\to$ lowers, lawyers, layers, lasers, lagers
  - trial lawers $\to$ trial lawyers

Ele pode computar a probabilidade de _lawers_ se válido para cada um dos contextos retornados baseado em erros passados de usuários que, quando direcionados para uma das buscas próximas fez com que o usuário entrasse em algum dos sites mostrados.

- Could mine query logs or other corpora for stats

### Handling word inflections

- Option #1
  - Stem both documents and query
    - [rock climbing] $\to$ [rock climb]

Problema: reduzir radicais de palavras bem diferentes: Univesal, universitário, etc.

- Option #2
  - Expand query with inflection variants
    - [rock climbing] $\to$ [rock {climbing climb}]

Busca qualquer uma das duas possibilidades. Poderia haver um thesauro que armazena palavras similares.

Poderia mapear todas as palavras que mapeiam a quais radicais, e depois fazer o reverso, colocando todas as palavras geradas do radical como alternativas na busca.

### Query-based stemming

- Delay stemming until we see a query
  - Improved flexibility, effectiveness
- Leverage context from surrounding words
  - [logistic manager] $\to$ [{logistic logistics} manager]
  - [logistic regression] $\to$ [logistic regression]

#### Stem classes

- Stem classes identified by stemming large corpora
  - bank: { bank banked banking bankings banks }
  - ocean: { ocean oceaneering oceanic oceanics oceanization oceans }
  - polic: { polic polical polically police policeable policed policement policer policers polices policial policically policier policiers ... }
- Often too big and inaccurate
  - Modify using analysis of word co-occurrence

### Query rewriting

- Rewriting for recall
  - Query relaxation
  - Query expansion
- Rewriting for precision
  - Query segmentation
  - Query scoping

#### Query rewriting for recall

- Some queries may return very limited sets of results
  - Some may return nothing (aka null queries)
- Vocabulary mismatch problem
  - Searcher and publisher's vocabularies may differ
- Solution: bridge the gap by tuning query specificity
  - Either remove or add terms as required

##### Query relaxation

- Rather than a verbose query, fire a shorter version!
  - [ideas for breakfast menu for a staff meeting]
    - [breakfast meeting menu ideas]
  - [Provide information on international support provided to either side in the Spanish Civil War]
    - [spanish civil war]

COmo escolher quais palavras deletar para encontrar melhores resultados?

###### Query relaxation approaches

- How to discard useless (or keep useful) terms?
  - Several feature-based machine learning approaches
- (classification, regression, clustering)
- Key considerations
  - How to identify sub-query candidates?
  - What features best describe a sub-query?

###### Identifying sub-query candidates

- Individual words
- Sequences of 2+ words
- Combinations of 2+ words
- Salient phrases (noun phrases, named entities)
- Right part of the query

###### Sub-query features

- Frequency statistics (TF, MI) in multiple corpora
  - Google n-grams, Wiki titles, query logs
- Linguistic features
  - POS tags, entities, acronyms, stopwords
- Sub-query features
  - Length, category, similarity/position wrt query

##### Query expansion

- Bridge vocabulary mismatch with added words
  - Adding alternative words
- [vp marketing] $\to$ [(vp OR vice president) marketing]
- [laptop repair] $\to$ [(laptop OR computer) repair]
  - Adding related words
- [tropical fish] $\to$ [tropical fish aquarium exotic]

Essa notação é por inconsistência. Aquela de {chave chav chaves} com palavras similares tem a mesma ideia.

###### Alternative words expansion

- Acronyms matched in dictionaries
  - VP: Vice President
  - VP: Vice Principal
- Acronyms mined from text
  - > **Business intelligence (BI)** combines a broad set of data analysis applications, including **online analytical processing (OLAP)**, and **data warehousing (DW)**.

---

- Synonyms matched in dictionaries
  - laptop: computer
  - laptop: notebook
- Synonyms mined via similar contexts
  - Cosine of word embeddings

###### Related words expansion

- Relatedness via word co-occurrence
  - Either in the entire document collection, a large collection of queries, or the top-ranked documents
- Several co-occurrence measures
  - Mutual information, Pearson's Chi-squared, Dice

###### Interactive query expansion

- Require user's (explicit, implicit) feedback
  - Rated, clicked, viewed documents

Uma possibilidade é pegar os top documentos ranqueados, minerar as palavras mais frequentes deles, e acrescentar essas palavras à pesquisa e então refazer a pesquisa, assim gerando um novo resultado de pesquisa.

#### Query rewriting for precision

- Query relaxation and expansion improve recall
  - Avoid small or empty result sets
- We also want to improve precision
  - Avoid large and noisy result sets
- Solution: improve the focus of the query
  - Identify key segments and scopes

##### Query segmentation

- Queries often contain multiple semantic units
  - [new battery charger for hp pavilion notebook]
    - [**new** _battery charger_ **hp pavilion** _notebook_]
- Leverage query structure via segmentation
  - Identify multiple segments
  - Process segments separately

---

- A query with $n$ tokens has $n - 1$ split points
  - We can have a total of $2^{n-1}$ possible segmentations
- How to find the best segmentation?
- [**machine learning toolkit**]
- [**machine** learning toolkit]
- [**machine learning** toolkit]
- [**machine** learning _toolkit_]

###### Query segmentation approaches

- Several approaches
  - Dictionary-based approaches
  - Statistical approaches
  - Machine-learned approaches

###### # Dictionary-based segmentation

- Simplest approach
  - A segment is a phrase in a dictionary
- Drawback #1: dictionary coverage
  - e.g., machine learning not found
- Drawback #2: segment overlap
  - e.g., both machine learning and learning toolkit found

###### # Statistical segmentation

- Exploits word collocations
  - A word is in a segment if it co-occurs with the other
- words already in the segment above a threshold
- Drawback: threshold sensitivity
  - Threshold determines a trade-off (precision vs. recall)
  - Threshold is corpus and language specific

###### # Machine-learned segmentation

- A binary classification approach
  - Each token either continues a segment or not
- Tokens represented as feature vectors
  - e.g., token frequency, mutual information, POS tags
- Drawback: data labeling for training
  - Must manually segment lots of queries

##### Query scoping

- Add a tag to each query segment
  - Attributes in structured domains
    - [black michael kors dress]
      - [black:color michael kors:brand dress:category]
  - Semantic annotations in open domains
    - [microsoft ceo]
      - [microsoft:company-3467 ceo:occupation-7234]

###### Tagging query segments

- Segment tagging as non-binary, sequential prediction
  - Classes known in advance (e.g., document fields,
- product attributes, knowledge base entries)
- Several approaches
  - Dictionary-based approaches
  - Graphical modeling approaches

###### Exploiting tagged scopes

- Attribute scoping
  - Match each segment against its tagged attribute
- Semantic scoping
  - Promote semantically related matches (e.g.: documents with entities close to the query entity)

### Summary (Aula 06)

- Users provide limited evidence of their needs
  - And yet expect fantastic search results
- Query understanding helps bridge the gap
  - Better recall through relaxation and expansion
  - Better precision through segmentation and scoping
- Open up possibilities for effective ranking!

### References (Aula 06)

- [Information Retrieval with Verbose Queries Gupta and Bendersky, FnTIR 2015](http://dx.doi.org/10.1561/1500000050)
- [Search Engines: Information Retrieval in Practice, Ch. 6 Croft et al., 2009](https://www.amazon.com/Search-Engines-Information-Retrieval-Practice/dp/0136072240)
- [Introduction to Information Retrieval, Ch. 3 Manning et al., 2008](https://www.amazon.com/Introduction-Information-Retrieval-Christopher-Manning/dp/0521865719)

---

- [Query Understanding Tunkelang, 2017](https://queryunderstanding.com/?gi=c690650eed78)

### Coming Next: Document Matching

## Aula 07 - 02/04/2025 - Document Matching - Slide: 07-documento-matching

### Search Components (Aula 07)

```mermaid
flowchart LR
  WWW --> Crawler
  Crawler --> Corpus[(Corpus)]
  Corpus[(Corpus)] --> Indexer
  Indexer --> Index[(Index)]
  Index[(Index)] <--> Query_Processor
  Query_Processor <--> Actor
```

---

```mermaid
flowchart LR
Index[(Index)] <--> Query_Processor
Query_Processor <--> Actor
```

#### Query Processing Overview (Aula 07)

```mermaid
flowchart LR
  Actor -->|"Query|feedback"| Understanding
  Index[(Index)] --> Matching
  Understanding --> Matching
  Understanding <--> KR[("Knowledge Resources: (Query Logs, Knowledge bases, User Preferences)")]
  Matching --> Scoring
  RM[(Ranking Model)] --> Scoring
  Scoring --> Actor
```

---

```mermaid
flowchart LR
  Index[(Index)] --> Matching
```

Aqui busca-se ser "exato", para que encontremos tudo que possa vir a ser útil na pesquisa.

---

### Document Matching (Aula 07)

- Scan postings lists for all query terms
  - [aquarium fish]

| Terms       | Postings           |
| ----------- | ------------------ |
| and         | 1:1                |
| aquarium    | 3:1                |
| are         | 3:1, 4:1           |
| ...         | ...                |
| environment | 1:1                |
| fish        | 1:2, 2:3, 3:2, 4:2 |

---

- Score matching documents
  - $f(q, d) = \sum_{t \in q} f(t, d)$

### Key Challenge

- Matching must operate under strict time constraints
  - Even a slightly slower search (0.2s-0.4s) can lead to a dramatic drop in the perceived quality of the results
- What makes it so costly?
  - Must score billions (or trillions?) of documents
  - Must answer thousands of concurrent queries

Essa tende a ser a parte mais custosa, visto que é a parte mais computacionalmente custoso

Deve-se considerar que enquanto um usuário tá acessando certa informação, diversos outros usuários podem estar tentando acessar o exato mesmo documento.

#### Solution #1: Bypass Scoring

- Query distributions similar to Zipf
  ◦ Popular queries account for majority of traffic
- Caching can significantly improve efficiency
  ◦ Cache search results, or at least inverted lists
- Problem: cache misses will happen eventually
  ◦ New queries, index updates

As consultas mais repetidas podem ser armazenadas em um cache, e assim, quando um usuário fizer uma consulta que já foi feita antes, o resultado pode ser retornado mais rapidamente.

Talvez, não a pesquisa específica tenha sido feita, mas uma consulta bem similar. Então poderia-se buscar alguma pesquisa parecida e retornar o resultado dela ou uma versão atualizada dela.

Em algum momento precisamos expirar a cache por ela já não ser mais tão relevante.

#### Solution #2: Distribute the Burden

- Indexes are often distributed in a cluster
  ◦ Too large to fit in a single machine
  ◦ Replication helps load balancing

Índices grandes já não são comportados em um único computador, logo já estarão distribuídos. Assim, cada máquina também acaba precisando acessar outras máquinas.

---

```mermaid
flowchart LR
  Actor -->|query| Broker
  Broker --> Matching_1[Matching]
  Broker --> Matching_2[Matching]
  Index_1[(Index)] --> Matching_1
  Index_2[(Index)] --> Matching_2
```

Pode haver então um **broker** que agrupa os resultados dos índices para retornar ao usuário.

---

- Indexes are often distributed in a cluster
  ◦ Too large to fit in one machine
  ◦ Replication helps load balancing
- Problem: cannot scale indefinitely
  ◦ Costly resources (hardware, energy)
  ◦ Intra-node efficiency still crucial

Ainda precisa se preocupar quanto ao nível de eficiência em cada um dos computadores individualmente.

#### Solution #3: Score Parsimoniously

- Some ranking models can be expensive
  ◦ Infeasible to score billions of documents
- Ranking as a multi-stage cascade
  ◦ Stage #1: Boolean matching (billions)
  ◦ Stage #2: Unsupervised scoring (millions)
  ◦ Stage #3: Supervised scoring (thousands)

Podemos trabalhar com apenas parte do índice.

Podemos usar técnicas computacionalmente caras, desde que usemos em volumes pequenos de dados.

### Why is it still so costly?

- Inherent cost of matching documents to queries
  ◦ Query length (number of posting lists)
  ◦ Posting lists length (number of postings per list)

| Term     | Postings           |
| -------- | ------------------ |
| aquarium | 3:1                |
| fish     | 1:2, 2:3, 3:2, 4:2 |

De cima pra baixo reduz-se o comprimento da query.

Da esquerda pra direita aumenta-se o tamanho da lista de postings

Acaba sendo necessário varrer as listas. Então quanto mais frequentes foram as palavras, mais custosa será a pesquisa.

### How to Traverse Postings?

#### Term-at-a-time (TAAT)

- Inverted lists processed in sequence
  ◦ Partial document scores accumulated

| Term     | Postings      |
| -------- | ------------- |
| salt     | 1:1, 4:1      |
| water    | 1:1, 2:1, 4:1 |
| tropical | 1:2, 2:2, 3:1 |

Podemos varrer um item por ver. Varrendo linha e depois coluna, ou coluna e depois linha. Sendo que a linha representa o termo e a coluna representa o documento.

Mas ao varrer sequencialmente ainda não temos um score global, apenas o parcial que vai sendo acumulado a medida que for percorrido.

---

| Term      | Postings      |
| --------- | ------------- |
| salt      | **1:1, 4:1**  |
| water     | 1:1, 2:1, 4:1 |
| tropical  | 1:2, 2:2, 3:1 |
| **SCORE** | **1:1, 4:1**  |

---

| Term      | Postings          |
| --------- | ----------------- |
| salt      | 1:1, 4:1          |
| water     | **1:1, 2:1, 4:1** |
| tropical  | 1:2, 2:2, 3:1     |
| **SCORE** | **1:2, 2:1, 4:2** |

---

| Term      | Postings               |
| --------- | ---------------------- |
| salt      | 1:1, 4:1               |
| water     | 1:1, 2:1, 4:1          |
| tropical  | **1:2, 2:2, 3:1**      |
| **SCORE** | **1:4, 2:3, 3:1, 4:2** |

---

```python
def taat(query, index, k):
  scores = map()
  results = heap(k)
  for term in tokenize(query):
    postings = index[term]
    for (docid, weight) in postings:
      if docid not in scores.keys():
        scores[docid] = 0
      scores[docid] += weight
  for docid in scores.keys():
    results.add(docid, scores[docid])
  return results
```

- Funcionamento

1. Inicialização:
   - Cria um mapa vazio para armazenar os scores dos documentos
   - Cria uma heap de tamanho k para armazenar os k melhores resultados
2. Processamento por termo:
   - Para cada termo na consulta:
     - Obtém a lista de postings (documentos) associada ao termo
     - Para cada documento na lista:
       - Se o documento ainda não está no mapa de scores, inicializa seu score como 0
       - Adiciona o peso do termo naquele documento ao score acumulado
3. Seleção final:
   - Percorre todos os documentos no mapa de scores
   - Adiciona cada documento e seu score final à heap
   - Retorna os k documentos com maiores score

Características
Processa um termo por vez
Mantém scores parciais em memória
Adequado para consultas com poucos termos
Requer mais memória devido ao armazenamento dos scores parciais
O algoritmo é uma alternativa ao DAAT (Document-at-a-Time) e é especialmente eficiente para acesso sequencial às listas invertidas, embora use mais memória para os acumuladores de scores.

#### Document-at-a-time (DAAT)

- Inverted lists processed in parallel.
  - One document scored at a time.

| X    | Y        |
| ---- | -------- |
| salt | 1:1, 4:1 |

...

---

Ao varrer todo um documento, já temos o valor de seu score.

---

```python
function daat(query, index, k):
  results = heap(k)
  targets = {docid for term in tokenize(query)
                   for docid in index[term]}
  lists = [index[term] for term in tokenize(query)]
  for target in targets:
    score = 0
    for postings in lists:
      for (docid, weight) in postings:
        if docid == target:
          score += weight
    results.add(target, score)
  return results
```

Uma das ineficiências dessa implementação é ter que marcar cada um dos índices que estamos percorrendo no momento.

Outra ineficiência é a inexistência de um iterador que marca o último índice que foi lido´.

### Optimization Techniques

- No clear winner between TAAT and DAAT.
  - TAAT is more memory efficient (sequential access).
  - DAAT uses less memory (no accumulators).

Apesar de TAAT ser mais eficiente, num caso onde uma das palavras da cache seja muito recorrente, acaba sendo muito custoso ainda assim.

Geralmente o DAAT é preferível.

- Naïve versions can be improved:
  - Calculate scores for fewer documents (conjunctions).
  - Read less data from inverted lists (skipping).

Poderia-se fazer a pesquisa por conjunção (interseção), ou seja, apenas os documentos que possuem todas as palavras.

#### Matching Semantics

- **Disjunctive Matching**
  - Documents must contain **at least one** query term (lower precision).

...

---

- **Conjunctive Matching**: Documents must contain **all** query terms (higher precision).
  - Preferred for short queries.
  - Combined with relaxation for long queries.

...

Uma flexibilização interessante seria...

$Conj \cup (Disj - Conj)$

Pode-se também definir quais termos são mais importantes que outros, assim flexibilizando apenas as buscas conjuntivas desses termos que sobraram.

---

#### Skipping

- Linear scanning is inefficient.
- **Solution**: Store skip pointers in the index.

Um problema da compressão é o caso de termos armazenado apenas os deltas dos docIds. Então seria realmente necessário varrer todos os deltas anteriores para saber onde estamos.

...

##### Skip Pointers

Pode-se criar algumas informações adicionais para facilitar a busca. Locais onde se têm o valor acumulado de determinado delta em tal posição da lista encadeada.

##### Skipping Example

| Inverted List | 34      | 36     | 37     | 45     | 48  | 51  | 52  | 57  | 80  | 89  |
| ------------- | ------- | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- |
| Delta Gaps    | 9       | 2      | 1      | 8      | 3   | 3   | 1   | 5   | 23  | 9   |
| Skip Pointers | (52,12) | (17,3) | (34,6) | (45,9) |     |     |     |     |     |     |

How to skip to docid 37?

Pergunta de aluno: E porque é armazenado o valor do acumulado do anterior e não do próprio índice?

---

How to skip to docid 54?

### Other Approaches

- Unsafe Early Termination:
  - Ignore high-frequency words in TAAT.
  - Ignore documents at the end of lists in DAAT.

Uma alternativa seria ordenar por relevância do documento, tentando manter aqueles com melhores scores no começo. O problema disso é que a relevância depende muito de termo pra termo.

- Index Tiering
  - Postings ordered by quality (e.g., PageRank).
  - Postings ordered by score (e.g., BM25).

Uma forma interessante de garantir o tempo do processamento é definir um tempo máximo de processamento para cada um dos documentos. Assim, se o tempo acabar, não se processa mais aquele documento.

### Summary (Aula 07)

- Document matching is **challenging** due to long inverted lists.
- Several complementary approaches:
  - **Caching**
  - **Distribution**
  - **Cascading**
- Efficient **index traversal** remains crucial.

### References (Aula 07)

- _Search Engines: Information Retrieval in Practice_, Ch. 5 - Croft et al., 2009
- _Scalability Challenges in Web Search Engines_, Ch. 4 - Cambazoglu and Baeza-Yates, 2015
- _Efficient Query Processing Infrastructures_ - Tonellotto and Macdonald, SIGIR 2018
  - [Amazon Link](https://www.amazon.com/Search-Engines-Information-Retrieval-Practice/dp/0136072240)
  - [DOI Link 1](https://doi.org/10.2200/S00662ED1V01Y201508ICR045)
  - [DOI Link 2](https://doi.org/10.1145/3209978.3210191)

### Coming Next... Efficient Matching

### Perguntas (Aula 07)

- Poderia usar um tipo de busca binária alternativa para buscar entre valores parcialmente desconhecidos?
  - Depois que se tem os limites inferiores e superiores,
  - Poderia-se fazer uma busca binária entre os dois limites, baseado no valor esperado nesse meio do caminho
  - Talvez deduzindo alguma linearidade
- Devo engajar menos na aula para dar brecha pros outros alunos?
  - Resposta: a preocupação é natural, mas não o está incomodando e ele não sente que a turma está incomodada com isso. Posso continuar o quanto achar devido.

### Coisas para pesquisar posteriormente (Aula 07)

- Zipf

## Aula XX - 07/04/2025 - Efficient Matching - Aula cancelada

## Aula 08 - 09/04/2025 - Efficient Matching

### Search Components - Aula 08

[Fluxograma dos Search Components padrão]

---

[Foco no Query Processor]

#### Query Processing Overview - Aula 08

[Fluxograma geral do Query Processing]

---

[Foco no Matchings]

### Document Matching - Aula 08

- Scan postings list for all query terms
  - [aquarium fish]
    - and: 1:1
    - aquarium: 3:1
    - are: 3:1, 4:1
    - ...
    - environment: 1:1
    - fish: 1:2, 2:3, 3:2, 4:2

---

- Scan postings lists for all query terms
  - [aquarium fish]
    - aquarium: 3:1
    - fish: 1:2, 2:3, 3:2, 4:2
- Score matching documents

  - $f(q, d) = \sum_{t \in q} f(t, d)$

- Index access cost
  - Memory paging (I/O)
  - In-memory processing (CPU)
- Scoring cost
  - Decompression + scoring (CPU)

Para os índices em memória, o custo não é tão grande.

Veremos hoje sobre métodos de reduzir esses dois custos.

### Index Access Cost

- Inherent cost of matching documents to queries

  - Query length (number of posting lists)
  - Posting lists length (number of postings per list)

- De cima a baixo: Query Length
- Da esquerda pra direita: Posting list length

### Traversal direction

- TAAT: inverted lists processed in sequence
  - More memory efficient (sequential access)

Malefícios: acumuladores demais por score de documento.

Se eu fosse fazer pesquisas com E eu teria que armazenar numa outra estrutura de dados que contasse a quantidade de termos que apareçam em determinado documento.

Num caso de busca por proximidade, tem outro problema: precisaria informar quais as posições em que determinado termo aparece e seria necessário checar se a outra é posterior.

- DAAT: inverted lists processed in parallel
  - Uses less memory (no accumulators)
  - Handles complex queries (Boolean, proximity)
  - De facto choice for modern search engines

### Naïve DAAT

- Inverted list processed in parallel
  - One document scored at a time

Se é um AND, só processa se tá presente nos 3. Senão, não processa.

Se é um OR, processa todos os marcados no menor índice.

- A: **_[1:3]_**, [2:3], [3:4], [8:4]
- B: **_[1:4]_**, [5:2], [7:2], [8:5], [9:2], [11:5]
- C: **_[1:6]_**, [2:5], [5:3], [6:7], [10:1], [11:7]
- scores: [1:13]

---

[Explicar o que os slides querem dizer]

- A: _[1:3]_, **_[2:3]_**, [3:4], [8:4]
- B: _[1:4]_, **[5:2]**, [7:2], [8:5], [9:2], [11:5]
- C: _[1:6]_, **_[2:5]_**, [5:3], [6:7], [10:1], [11:7]

- scores: [1:13], [2:8d]

---

21

### What if we want only the top $k$ results?

Se eu ordenasse dos documentos com maior e menor score por palavra, poderia facilitar na busca por palavras únicas. Porém o traversal em postings de mesmo documento fica prejudicada.

### Dynamic pruning

- Dynamic pruning strategies aim to make scoring faster
- by only scoring a subset of the documents
  - Assume user is only interested in the top $k$ results
  - Check if a document can make it to the top $k$
  - Early terminate (or even skip) unviable documents

### Effectiveness guarantees

MORE EFFECTIVE

- **Safe:** exhaustive (i.e. no pruning) matching
- **_Score safe:_** top $k$ with correct scores
- **_Rank safe:_** top $k$ with correct order
  - > Não preciso manter o mesmo score desde que a ordem esteja a mesma
- **Set safe:** top $k$ with correct documents
  - Sem garantia de que os documentos corretos estão em ordem
- **Unsafe:** no correctness guarantees whatsoever

LESS EFFECTIVE

### MaxScore [Turtle and Flood, IPM 1995]

- In a multi-term query, not all terms are worth the same
  - Some will be "essential" for scoring documents
  - Others will be "non-essential" terms

Dessa forma, os termos não essenciais não precisariam ser computados.

- Key idea
  - Traverse "essential" terms first (in DAAT mode)
  - Check "non-essential" terms only if promising

#### MaxScore $(k = 2)$

- Each list has an upper bound (aka max-score)

  - Top $k$ results have acceptance threshold $\theta$
  - terms sorted by inc. max-score
  - pivot chosen as least term that cumulatively beats threshold $\theta$
  - terms at least as promising as the pivot deemed "essential"
    - others are "non-essential"

- > A: (CumulativeMS: 4) (MaxScore: 4) [1:3], [2:3], [3:4], [8:4]
- B: (CumulativeMS: 9) (MaxScore: 5) [1:4], [5:2], [7:2], [8:5], [9:2], [11:5]
- C: (CumulativeMS: 16) (MaxScore: 7) [1:6], [2:5], [5:3], [6:7], [10:1], [11:7]

Top $k = 2$: [] []

$\theta = 0$

---

- process "essential" lists first
- process "non-essential" lists only if they are promising
- update top $k$ results and $\theta$
- update pivot on $\theta$ changes

- > A: (CumulativeMS: 4) (MaxScore: 4) **[1:3]**, [2:3], [3:4], [8:4]
- B: (CumulativeMS: 9) (MaxScore: 5) **[1:4]**, [5:2], [7:2], [8:5], [9:2], [11:5]
- C: (CumulativeMS: 16) (MaxScore: 7) **[1:6]**, [2:5], [5:3], [6:7], [10:1], [11:7]

Top $k = 2$: [] []

$\theta = 0$

---

Promising seria apenas se o máximo das listas não promissoras for suficiente para fazer com que o documento computado das promissoras seja grande o bastante pra fazer com que ele ultrapasse o $\theta$.

Uma potencial otimização seria fazer um maxscore mais justo que é atualizado assim que todos os items que têm esse maxscore já foram processados, assim reduzindo os MaxScores.

Outra potencial otimização seria atualizar os MaxScores acumulados quando algumas listas já forem exauridas.

Dúvida 1: Se no pivô o posting analisado já superar o threshold, eu ainda somaria com os não essenciais?

Resposta 1: Sim. Porque senão, esse calculado poderia ser indevidamente descartado.

Dúvida 2: Se empatar, substitui?

Resposta 2: Nesse caso não, só substitui se for superior.

---

Se coincidisse dos melhores documentos estarem no topo, logo o Threshold seria atualizado e subiria. Senão, demoraria pra convergir.

---

...

---

30

#### MaxScore Limitations

- MaxScore relies on "non-essential" terms for skipping
  - Naïve DAAT performed on "essential" terms
- It may take long for a term to become "non-essential"
  - It may be a poor term (low max-score)
  - It may get hard to make the heap (high threshold)
- Hindered efficiency, particularly for long queries

### WAND [Broder et al., CIKM 2003]

Weak AND

- MaxScore fully evaluates "essential" lists
  - Not all documents in "essential" lists are promising
- Key idea
  - Evaluate documents (not lists) if they are promising (i.e. have a promising cumulative upper bound)

#### WAND $(k = 2)$

- Each list has an upper bound (aka max-score)
  - Top $k$ results have acceptance threshold $\theta$
  - terms sorted by inc. docid
  - pivot chosen as least term that cumulatively beats threshold $\theta$
  - terms managed dynamically
    - lists synced to pivot document
    - terms re-sorted on every move

---

...

---

30

5 / 16 postings skipped $\approx$ 31% savings

#### In-memory WAND [Fontoura et al., VLDB 2011]

- Substantial reduction in processed postings
  - Particularly efficient for long queries
- But latency only improved for disk-based indexes
  - No memory paging for in-memory indexes!
  - Pivot management offsets gains in skipping
- Solution: align all cursors before a new re-sort

#### Block-Max WAND [Ding and Suel, SIGIR 2011]

[Imagem gráfico de docid x score: erro absoluto]

1

---

[Imagem gráfico de docid x score: Erro absoluto médio]

2

---

3

#### Variable-sized blocks [Mallia et al., SIGIR 2017]

- max-score of $t$: 17
  - block max-score of $b_1$: 12
  - block max-score of $b_2$: 17
  - block max-score of $b_3$: 11
- mean absolute error: 6.2

#### Impact-sorted blocks [Ding and Suel, SIGIR 2011]

- max-score of $t$: 17
  - block max-score of $b_1$: 17
  - block max-score of $b_2$: 11
  - block max-score of $b_3$: 4
- mean absolute error: 2.7

#### Docid reassignment [Ding and Suel, SIGIR 2011]

- max-score of $t$: 17
  - block max-score of $b_1$: 17
  - block max-score of $b_2$: 11
  - block max-score of $b_3$: 4
- mean absolute error: 2.7

#### Impact-layered blocks [Ding and Suel, SIGIR 2011]

- max-score of $t$: 17
  - block max-score of $b_1$: 17
  - block max-score of $b_2$: 11
  - block max-score of $b_3$: 4
- mean absolute error: 2.7

### Summary - Aula 08

- Efficient matching for subsecond response times
  - Skip postings (or lists) that won't help make the top $k$
- Carefully play with upper bounds and thresholds
  - Can be extended with blocks, layers, list orderings
- Can always trade-off safety for efficiency
  - Anytime ranking for QoS [Lin and Trotman, ICTIR 2015]

### References - Aula 08

- [Link][Link_2015_Bae] Scalability Challenges in Web Search Engines, Ch. 4 Cambazoglu and Baeza-Yates, 2015
- [Link][Link_2018_Mac] Efficient Query Processing Infrastructures Tonellotto and Macdonald, SIGIR 2018
- [Link][Link_2018_Ton] Efficient Query Processing for Scalable Web Search Tonellotto et al., FnTIR 2018

---

- [Link][Link_1995_Tur] Query evaluation: strategies and optimizations Turtle and Flood, IP&M 1995
- [Link][Link_2003_Bro] Efficient query eval. using a two-level retrieval process Broder et al., CIKM 2003
- [Link][Link_2011_Din] Faster top-k document retr. using block-max indexes Ding and Suel, SIGIR 2011

[Link_2015_Bae]: https://link.springer.com/book/10.1007/978-3-031-02298-2
[Link_2018_Mac]: https://dl.acm.org/doi/10.1145/3209978.3210191
[Link_2018_Ton]: https://www.nowpublishers.com/article/Details/INR-057
[Link_1995_Tur]: https://www.sciencedirect.com/science/article/pii/030645739500020H?via%3Dihub
[Link_2003_Bro]: https://dl.acm.org/doi/10.1145/956863.956944
[Link_2011_Din]: https://dl.acm.org/doi/10.1145/2009916.2010048

### Coming next: Vector Space Models

## Aula 09 - 23/04/2025 - Vector Space Models

### The ranking problem

- Given
  - Some evidence of the user's need
- Produce
  - A list of matching information items
  - In decreasing order of relevance

---

- Given
  - Some evidence of the user's need query
- Produce
  - A list of matching information items documents
  - In decreasing order of relevance

---

- $f(q, d)$

```mermaid
flowchart LR
  q((q)) .-> d((d))
```

### Why rank?

- Couldn't $f(q,d)$ be just an indicator function?

### Document selection vs. ranking

[IMAGEM]

- [JV]
  - A seleção é um ranqueamento binário. Ela pode inclusive ter falsos positivos e falsos negativos.
  - No caso do ranqueamento, ele precisa definir um corte.

### Why not select?

- The classifier is unlikely accurate
  - Over-constrained: no relevants returned
  - Under-constrained: too many relevants returned
  - Hard to find an appropriate threshold
- Not all relevant documents are equally relevant!
  - Prioritization is needed

### Probability Ranking Principle (PRP)

- > Ranking documents by decreasing probability of relevance results in optimal effectiveness, provided that probabilities are estimated (1) with certainty and (2) independently.

  - Robertson, 1977

- [JV]
  - Num caso de ranqueamento, onde os mais relevantes estão no topo, às vezes, não necessariamente o segundo colocado é de fato tão relevante. Isso porque, talvez, o primeiro colocado já cobre o conteúdo do segundo.

### Ranking effectiveness

- Effectiveness is about doing the right thing; it's about finding documents that are relevant to the user
- Relevance is influenced by many factors
  - Topical relevance vs. user relevance
  - [JV] Uma pesquisa como "Natal Rio Grande do Norte" pode ter uma variação de relevância devido a localização do usuário (de BH? Do RJ?), ao que ele busca (Passagens? Hotel? História?)
  - Task, context, novelty, style
  - [JV] Atualmente LLMs processam o texto de forma muito poderosa.
- Ranking models define a view of relevance
  - [JV] No final, é sempre o usuário que diz se a função de ranking é boa ou não.

### Ranking models

- Provide a mathematical framework for ranking
  - Each model builds upon different assumptions
- Progress in ranking models has corresponded with improvements in effectiveness

  - An effective model should score relevant documents higher than non-relevant documents

- [JV]
  - Essa é uma das partes mais focadas na pesquisa porque os outros problemas são mais objetivos, já este acaba sendo mais subjetivo porque depende do usuário.

### Fundamental elements

- f(q="**presidential** campaign _news_", d)
  - "Bag of Words"
    - g("**presidential**", d)
    - g("campaign", d)
    - g("_news_", d)
  - How many times does "**presidential**" occur in $d$?
    - **Term Frequency (TF):** $c("**presidential**", d)$
  - How long is $d$?
    - **Document length:** $|d|$
  - How often do we see "**presidential**" in the entire collection?
    - **Document Frequency:** $df("**presidential**")$
    - $P("**presidential**"|collection)$

### Many classical models

- Similarity-based models: $f(q, d) = sim(q, d)$
  - Vector space models
  - [JV]
    - Baseado em álgebra linear
- Probabilistic models: $f(d, q) = p(R = 1|d, q)$
  - Classic probabilistic models
  - Language models
  - Information-theoretic models

### Many extended models

- Structural models
  - Beyond bags-of-words
  - [JV]
    - As sequência de que forma as palavras estão dispostas no texto
    - Alguma tag em cada uma das palavras
- Semantic models
  - Beyond lexical matching
  - [JV]
    - Além do casamento exato, buscaria-se palavras que têm significado similar, onde tendem a representar a mesma coisa.
- Contextual models
  - Beyond queries
  - [JV]
    - Historicamente nas buscas do usuário, essa query é relevante?

### Vector Space Model (VSM)

[Imagem gráfico $R^3$ (Programming, Library, Presidential)]

- [JV]
  - Existem estruturas para armazenar vetores densos.
  - Busca-se encontrar o documento nesse espaço vetorial.
  - Cada dimensão é uma palavra do documento único.

### VSM is a framework

- Queries and documents as term vectors
  - Term as the basic concept (e.g., word or phrase)
    - [JV]
      - Poderiam ser usados outros conceitos para definir as dimensões, como sinônimos, bigramas, trigramas, etc.
- A vocabulary $V$ defines a $|V|$-dimensional space
  - Vector components as real-valued term weights
- Relevance estimated as $f(q, d) = sim(q, d)$
  - $q = (x_1, \dots, x_{|V|})$ and $d = (y_1, \dots, y_{|V|})$
    - [JV]
      - Mas como escolho qual valor colocar em cada eixo?

### What VSM doesn't say

- How to define vector dimensions
  - Concepts are assumed to be orthogonal
- How to place vectors in the space
  - Term weight in query indicates importance of term
  - Term weight in document indicates topicality
- How to define the similarity measure

---

- [Imagem gráfico $R^3$ (?, ?, ?)]
  - $q = (x_1, \dots, x_{|V|}), x_i = ?$
  - $d = (y_1, \dots, y_{|V|}), y_i = ?$
  - $sim(q, d) = ?$

### Dimensions as a bag of words (BOW)

- Vocabulary: $V = (w_1, \dots, w_{|V|})$
- [Imagem gráfico $R^3$ $(w_1, w_2, w_3)$]

#### Vectors placed as bit vectors

- $x_i, y_i \in {0,1}$

  - 1: word $w_i$ is present
  - 0: word $w_i$ is absent

- [Imagem gráfico $R^3$ $(w_1, w_2, w_3)$]
  - $q = (1, 1, 1)$
  - $d = (0, 1, 1)$

### Similarity as dot product

- $sim(q, d)$

  - $= q \cdot d$
  - $= x_1 y_1 + \dots + x_{|V|} y_{|V|}$
  - $= \sum_{i=1}^{|V|} x_i y_i$

- [Imagem gráfico $R^3$ $(w_1, w_2, w_3)$]

  - $q = (1, 1, 1)$
  - $d = (0, 1, 1)$

- [JV]
  - Essa multiplicação representa a quantidade de palavras que a query tem que o documento também tem.
  - Embora simples, ainda assim é bastante prática e útil.

### Simplest VSM = BOW + bit vectors + dot

- $q = (x_1, \dots, x_{|V|})$
- $d = (y_1, \dots, y_{|V|})$
- $x_i, y_i \in {0,1}$
  - 1: word $w_i$ is present
  - 0: word $w_i$ is absent
- $sim(q, d)$

  - $= q \cdot d$
  - $= x_1 y_1 + \dots + x_{|V|} y_{|V|}$
  - $= \sum_{i=1}^{|V|} x_i y_i$

- What does this ranking function intuitively capture?
- Is this a good ranking function?

### How would you rank these documents?

- $q$ = [ news about presidential campaign ]
- $d_1$ = [ ... **news about** ... ]
- $d_2$ = [ ... **news about** organic food **campaign** ... ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]
- $d_5$ = [ ... **news** of organic food **campaign** ... **campaign** ... **campaign** ... **campaign** ... ]

- [JV]
  - $d_1$, $d_2$ e $d_5$ Seriam irrelevantes.

---

| Document | Ideal rank |
| -------- | ---------- |
| $d_1$    | $d_4 +$    |
| $d_2$    | $d_3 +$    |
| $d_3$    | $d_1 -$    |
| $d_4$    | $d_2 -$    |
| $d_5$    | $d_5 -$    |

### Ranking using the simplest VSM

- $q$ = [ news about presidential campaign ]
- $d_1$ = [ ... **news about** ... ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]
- $V = { news, about, presidential, campaign, food, ... }$
  - $q = (1, 1, 1, 1, 0, \dots )$
  - $d_1 = (1, 1, 0, 0, 0, \dots )$: $sim(q, q_1) = 2$
  - $d_3 = (1, 0, 1, 1, 0, \dots )$: $sim(q, q_3) = 3$

### Is it effective?

- $q$ = [ news about presidential campaign ]
- $d_1$ = [ ... **news about** ... ]
- $d_2$ = [ ... **news about** organic food **campaign** ... ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]
- $d_5$ = [ ... **news** of organic food **campaign** ... **campaign** ... **campaign** ... **campaign** ... ]

| Document | $f(q, d)$ | ranking |   Ideal |
| -------: | --------: | ------: | ------: |
|    $d_1$ |         2 |   $d_2$ | $d_4 +$ |
|    $d_2$ |         3 |   $d_3$ | $d_3 +$ |
|    $d_3$ |         3 |   $d_4$ | $d_1 -$ |
|    $d_4$ |         3 |   $d_1$ | $d_2 -$ |
|    $d_5$ |         2 |   $d_5$ | $d_5 -$ |

- [JV]
  - Poderiam ser feitos swaps para alternar as ordenações para melhorar.

### What's wrong with it?

- $q$ = [ news about presidential campaign ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]

| Document | $f(q, d)$ | ranking |   Ideal |
| -------: | --------: | ------: | ------: |
|    $d_1$ |         2 |   $d_2$ | $d_4 +$ |
|    $d_2$ |         3 |   $d_3$ | $d_3 +$ |
|    $d_3$ |         3 |   $d_4$ | $d_1 -$ |
|    $d_4$ |         3 |   $d_1$ | $d_2 -$ |
|    $d_5$ |         2 |   $d_5$ | $d_5 -$ |

- Matching "presidential" **more times** deserves more credit!

### Vectors placed as tf (Term Frequency (?)) vectors

- $x_i, y_i \in \mathbb{N}$
  - $x_i: tf_{w_{i, q}}$
  - $y_i: tf_{w_{i, d}}$
- [Imagem gráfico $R^3$ $(w_1, w_2, w_3)$]
  - $q = (1, 1, 1)$
  - $d = (2, 0, 5)$

### Ranking using VSM with tf vectors

- $q$ = [ news about presidential campaign ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]

- $V = \{ news, about, presidential, campaign, food, \dots \}$
  - $q = (1, 1, 1, 1, 0, \dots )$
    - [JV] É comum que as buscas acabem tendendo a ter uma pesquisa parecida com binária nessa representação de frequência.
  - $d_3$ = (1, 0, 1, 1, 0, $\dots$ ): $sim(q, d_3) = 3$
  - $d_4$ = (1, 0, 2, 1, 0, $\dots$ ): $sim(q, d_4) = 4$

### What's wrong with it? (2)

- $q$ = [ news about presidential campaign ]
- $d_2$ = [ ... **news about** organic food **campaign** ... ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]

| Document | $f(q, d)$ | ranking |  Ideal  |
| :------: | :-------: | :-----: | :-----: |
|    -     |     -     |  $d_2$  | $d_4 +$ |
|  $d_2$   |     3     |  $d_3$  | $d_3 +$ |
|  $d_3$   |     3     |  $d_4$  | $d_1 -$ |
|    -     |     -     |  $d_1$  | $d_2 -$ |
|    -     |     -     |  $d_5$  | $d_5 -$ |

- Matching "presidential" is **more important** than matching "about"!

- [JV]
  - Presidential acaba sendo mais raro que about, logo, mais significativo.

### Vectors placed as tf-idf vectors

- $x_i, y_i \in \mathbb{R}$
  - $x_i: tf_{w_{i, q}} \cdot idf_{w_i}$
  - $y_i: tf_{w_{i, d}} \cdot idf_{w_i}$
  - [JV]
    - $tf$ é o inteiro, a frequência que já temos calculado
    - $idf$ será o peso real.
      - Existem várias aplicações dela na literatura.
- [Imagem gráfico $R^3$ $(w_1, w_2, w_3)$]
  - $q = (1, 1, 1)$
  - $d = (2, 0, 5)$

### Inverse document frequency (idf)

- $idf_w = \log \frac{n+1}{n_w}$
  - [JV] O $i$ é de inversa.
  - $n$: number of documents in the corpus
  - $n_w$: number of documents where $w$ appears

### Why a log-based penalization?

- [Imagem gráfico $R^2: (n_w, idf_w = \log \frac{n+1}{n_w})$]
  - Rapid decay after a small fraction of the corpus
  - [JV]
    - Esse decaimento rápido busca rapidamente penalizar a existência de repetições.
    - Dúvida: ora, mas e se uma palavra ocorrer por acaso em um documento, mas em n outros mais importantes ela aparecer algumas poucas vezes a mais, nesse caso, nesses mais relevantes, eles em si teriam um peso menor nesse cálculo. Não seria interessante uma outra curva diferente de log?
      - Resposta: "In the big scheme of things", ou em português, "no frigir dos ovos", esses casos podem acabar sendo mais raros, então não impactaria tanto.

### Ranking using VSM with tf-idf vectors

- $q$ = [ news about presidential campaign ]
- $d_2$ = [ ... **news about** organic food **campaign** ... ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]
- $V = \{ news, about, presidential, campaign, food, \dots \}$
- $idf = (1.5, 1.0, 2.5, 3.1, 1.8, \dots)$

  - $q = (1, 1, 1, 1, 0, \dots )$
  - $d_2 =$ (1 \* 1.5, **1 \* 1.0**, 0, 1 \* 3.1, 0, $\dots$): $sim(q, d_2) = 5.6$
  - $d_3 =$ (1 \* 1.5, 0, **1 \* 2.5**, 1 \* 3.1, 0, $\dots$): $sim(q, d_3) = 7.1$

- [JV]:

| **V** | News     | About        | Presidential | Campaign | Food | $\dots$ |
| ----- | -------- | ------------ | ------------ | -------- | ---- | ------- |
| $idf$ | 1.5      | 1.0          | 2.5          | 3.1      | 1.8  | $\dots$ |
| $d_2$ | 1 \* 1.5 | **1 \* 1.0** | 0            | 1 \* 3.1 | 0    | $\dots$ |
| $d_3$ | 1 \* 1.5 | 0            | **1 \* 2.5** | 1 \* 3.1 | 0    | $\dots$ |

### Is it effective? (2)

- $q$ = [ news about presidential campaign ]
- $d_1$ = [ ... **news about** ... ]
- $d_2$ = [ ... **news about** organic food **campaign** ... ]
- $d_3$ = [ ... **news** of **presidential campaign** ... ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]
- $d_5$ = [ ... **news** of organic food **campaign** ... **campaign** ... **campaign** ... **campaign** ... ]

| Document | $f(q, d)$ | ranking |  Ideal  |
| :------: | --------: | :-----: | :-----: |
|  $d_1$   |       2.5 |  $d_5$  | $d_4 +$ |
|  $d_2$   |       5.6 |  $d_4$  | $d_3 +$ |
|  $d_3$   |       7.1 |  $d_3$  | $d_1 -$ |
|  $d_4$   |       9.6 |  $d_2$  | $d_2 -$ |
|  $d_5$   |      13.9 |  $d_1$  | $d_5 -$ |

---

- $q$ = [ news about presidential campaign ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]
- $d_5$ = [ ... **news** of organic food **campaign** ... **campaign** ... **campaign** ... **campaign** ... ]

- $V = \{ news, about, presidential, campaign, food, \dots \}$
- $idf = (1.5, 1.0, 2.5, 3.1, 1.8, \dots)$
  - $q = (1, 1, 1, 1, 0, \dots )$
- $q$ = [ news about presidential campaign ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]
- $d_5$ = [ ... **news** of organic food **campaign** ... **campaign** ... **campaign** ... **campaign** ... ]

### Ranking using VSM with tf-idf vectors (2)

- $q$ = [ news about presidential campaign ]
- $d_4$ = [ ... **news** of **presidential candidate** ... **presidential** candidate ... ]
- $d_5$ = [ ... **news** of organic food **campaign** ... **campaign** ... **campaign** ... **campaign** ... ]

- $V = \{ news, about, presidential, campaign, food, \dots \}$
- $idf = (1.5, 1.0, 2.5, 3.1, 1.8, \dots)$

  - $q = (1, 1, 1, 1, 0, \dots )$
  - $d_4 =$ (1 \* 1.5, 0, 2 \* 2.5, 1 \* 3.1, 0, $\dots$): $sim(q, d_4) = 9.6$
  - $d_5 =$ (1 \* 1.5, 0, 0, **4 \* 3.1**, 1 \* 1.8, $\dots$): $sim(q, d_5) = 13.9$

### Transforming tf

[Imagem Gráfico $R^2$ $(c(w, d), tf_{w, d})$]

- $tf_{w, d} = c(w, d)$
- $tf_{w, d} = \log(1 + c(w, d))$
- $tf_{w, d} = \log(1 + \log(1 + c(w, d)))$
- $tf_{w, d} = 1(c(w, d) > 0)$

- [JV] Estamos saturando a utilidade de determinado documento

### What about document length?

- q = [news about presidential campaign]
- $d_4$: [... **news** of **presidential campaign** ... **presidential** candidate ...]: 100 words
- $d_6$: [... **campaign** ... **campaign** ... ... **news** ... ... ... **news** ... ... **presidential** ... **presidential** ... ]: 5000 words

- $f(q, d_6) > f(q, d_4)$?

### Document length normalization

- Penalize long documents
  - [JV] Embora possa penalizar bons documentos, essa heurística muitas vezes funciona.
  - Avoid matching by chance
  - Must also avoid over-penalization
- A document is long because
  - It uses more words $\to$ more penalization
  - It has more content $\to$ less penalization

### Pivoted length normalization (pln)

- $pln_d = (1-b) + b \frac{|d|}{avdl}$
  - $|d|$: document length in tokens
  - $avdl$: average document length in the corpus
  - $b \in [0,1]$: parameter

---

- $pln_d = (1-b) + b \frac{|d|}{avdl}$

[Imagem: gráfico $R^2$ $(|d|, pln_d)$, relação entre recompensa e penalização. Recompensa quando é menro que avdl e penalização quando é maior que avdl]

- [JV]
  - Inclusive isso me lembra um pouco o PID.
  - A ideia é que, quando o documento é menor que a média, ele acaba sendo mais relevante, então a recompensa é maior. Quando ele é maior que a média, ele acaba sendo penalizado.

### State-of-the-art VSM ranking

- Pivoted length normalization VSM [Singhal et al. 1996]
  - $f(q, d) = \sum_{w \in q} c(w, q) \frac{\ln (1 + \ln(1 + c(w, d)))}{(1 - b) + b \frac{|d|}{avgdl}} \log \frac{n+1}{n_w}$
- Okapi/BM25 [Robertson and Walker, 1994]

  - $f(q, d) = \sum_{w \in q} c(w, q) \frac{(k_1 + 1)(c(w, d) + k_1)}{c(w, d) + k_1 ((1-b) + b \frac{|d|}{avgdl})} \log \frac{n+1}{n_w}$

- [JV] Não decorem as fórmulas, mas as feature emergentes das fórmulas

### Summary - Aula 09

- Fundamental ranking components
  - Term and document frequency
  - Document length
- VSM is a framework
  - Components as term and document weights
  - Relevance as query-document similarity

---

- Lack of theoretical justification
  - Axiomatic approaches, probabilistic approaches
- Room for further improvement
  - Structure, semantics, feedback, context
  - Feature-based models

### References - Aula 09

- [Pivoted document length normalization Singhal et al., SIGIR 1996][Link_1996]
- [Some simple effective approximations to the 2-Poisson model for probabilistic weighted retrieval Robertson and Walker, SIGIR 1994][Link_1994]
- [The probability ranking principle in IR Robertson, J. Doc. 1977][Link_1977]

[Link_1996]: https://dl.acm.org/doi/10.1145/243199.243206
[Link_1994]: https://dl.acm.org/doi/10.5555/188490.188561
[Link_1977]: https://www.emerald.com/insight/content/doi/10.1108/eb026647/full/html

### Coming Next... Language Models

## Aula 10 - 24/04/2025 - Language Models - Slide: 10-language-models

### The ranking problem (Aula 10)

- $q$
- $d$
- $f(q, d)$

### Ranking models recap

- **Boolean model**
  - Boolean query
  - Set-based retrieval (no actual ranking)
- **Vector space models**
  - Query and documents as vectors
  - Similarity-based ranking

### Language modeling approach

- **Key intuition**
  - Users who try to think of a good query, think of words that are likely to appear in relevant documents
  - A document is a good match to a query if it uses the same underlying language as the query

### Statistical language model

- A probability distribution over word sequences
  - $P("Today is Wednesday") \approx 0.001$
  - $P("Today Wednesday is") \approx 0.0000000000001$
  - $P("The eigenvalue is positive") \approx 0.00001$
- Can also be regarded as a probabilistic mechanism for "generating" text, thus also called a "generative" model

### Types of language models

- Full dependence model

  - $P(w_1 \dots  w_k) = P(w_1)\,P(w_2 | w_1)\, \dots \,P(w_k | w_1 \dots  w_{k-1})$
  - [JV]
    - Estimar essas probabilidades é complexo e muito caro
    - Acaba que por falta de contexto, pode-se estimar erroneamente a probabilidade de uma palavra

- Infeasible in practice

  - Expensive computation
  - Weak estimates (data sparsity)

---

- Tunable dependence via n-grams
  - 3-gram ("trigram")
    - $P(w_1 \dots  w_k) = P(w_1)\,P(w_2 | w_1)\, \dots \,P(w_k | w_{k-2}, w_{k-1})$
  - 2-gram ("bigram")
    - $P(w_1 \dots  w_k) = P(w_1)\,P(w_2 | w_1)\, \dots \,P(w_k | w_{k-1})$
  - 1-gram ("unigram")
    - $P(w_1 \dots  w_k) = P(w_1)\,P(w_2)\, \dots \,P(w_k)$

### Unigram language model

- The simplest language model

  - A one-state probabilistic finite automaton

- State Emission Probabilities

| Word  | Probability |
| :---- | ----------: |
| the   |        0.20 |
| the   |        0.20 |
| a     |        0.10 |
| frog  |        0.01 |
| toad  |        0.01 |
| said  |        0.03 |
| likes |        0.02 |
| that  |        0.04 |
| ...   |         ... |
| STOP  |        0.20 |

- $P("frog said that toad likes frog STOP") = 0.01 \times 0.03 \times 0.04 \times 0.01 \times 0.02 \times 0.01 \times 0.02 = 0.0000000000048$

### Example Text Generation

- Model $\theta$:

### Evaluation of language models

- [JV] Conceitos de Teoria da Informação

### Applications of language models

- **...**
- **Document Ranking**

### Query likelihood model

- $f(q, d) \approx P(q, d)$
  - $f(q, d) = P(d) \cdot P(q | d)$ Bayes' rule
  - Two core components:
    - $P(q | d)$: query likelihood
    - $P(d)$: document prior
      - [JV] Ele basicamente faz um ranqueamento prévio global para cada um dos documentos

#### Computing $P(d)$

- $P(d) = 1 / n$, for $n$ documents in the corpus

#### Computing $P(q|d)$

##### Ranking Query Likelihood

##### Computing $P(q|d)$ (2)

- $P(q|\theta_d) = \prod_{t \in q} P(t|\theta_d)^{tf_{t,q}}$

  - [JV]

    - O $tf_{t,q}$ seria o expotente dada a frequência de determinada palavra na consulta.
    - Acaba ocorrendo problema de underflow por ser um número muito pequeno.

    - A utilidade de usar o log é que ela converte números minúsculos em números maiores.
    - $\propto$

- $P(q|\theta_d) = \prod_{t \in q} P(t|\theta_d)^{tf_{t,q}} \propto \sum_{t \in q} tf_{t,q} \log P(t|\theta_d)$

#### How to estimate $P(t| ...)$?

- $P_{MLE}(t|\theta_d) = \frac{tf_{t,d}}{|d|}$

  - [JV] O $|d|$ é o número total de palavras no documento.
  - [JV] O $tf_{t,d}$ é a contagem de frequência da palavra $t$ no documento $d$.

- Problems
  - Observed
  - Unobserved
    - [JV] Talvez uma solução seria pegar o contexto geral e dar alguma probabilidade média a palavras próximas do contexto não presentes.

#### Smoothing Probabilities

- [JV] Esse Smoothing ocorrerá através da análise de probabilidade considerando todo o Corpus

---

- General form
  - $P(t|\theta_d) = (1-\alpha) P_{MLE}(t|\theta_d) + \alpha P_{MLE}(t|\theta_C)$

#### Jelinek-Mercer Smoothed Model

- $f(q, d) \propto \prod_{t \in q} P(t|\theta_d)^{tf_{t,q}}$
- $f(q, d) = \prod_{t \in q} \left( (1-\lambda) \frac{tf_{t,d}}{|d|} + \lambda \frac{tf_{t,C}}{|C|} \right)$

#### Where is tf-idf wighting?

...

#### How about Document Length?

- [JV] Se for um documento muito longo, então, ele tende a aumentar a intensidade da relevância das palavras no corpus, senão foca no documento pequeno.

#### How effective are these?

#### Extended Approaches

#### Document Likelihood model

#### Model comparison

Estado da arte

## Aula 11 - 28/04/2025 - Experimental Methods

### One Problem

### Many Solutions

- Similarity-based models
- Probabilistic models
- Extended models
- Machine-learned models

### Why Evaluate

- Lots of alternative solutions
  - Which one to choose?
  - How to improve upon them?
- Evaluation enables an informed choice
  - Rigor of science
  - Efficiency of practice

### What to evaluate?

- Three fundamental types of IR research
  - Systems (efficiency)
  - Methods (effectiveness)
  - Applications (user utility)
- Evaluation plays a critical role for all three

  - Our primary focus is on "methods" research

- [JV]
  - Geralmente é muito difícil avaliar um sistema de busca, dificilmente tendo uma teoria que explique bem.

### How to evaluate?

- Scientifically, of course!
  - [JV]
    - A Microsoft é um dos que mais divulga sobre as pesquisas internas que fazem.
    - Nem sempre dá pra publicar resultado negativo, mas para mestrado e doutorado até que daria.

```mermaid
flowchart LR
  AskQ['Ask a question']
  Back['Do background research']
  Hypo['Formulate a hypothesis']
  Test['Test with an experiment']
  Proc['Procedure Working?']
  Nope['No']
  Yess['Yes']
  Alyz['Analyze data and draw conclusions']
  HypY['Result support hypothesis']
  HypN['Result do not support hypothesis']
  Comu['Communicate results']

  AskQ <--> Back
  Back --> Hypo
  Hypo --> Test
  Test --> Proc
  Proc --> Nope
  Nope -->|Troubleshoot| Test
  Proc --> Yess
  Yess --> Alyz
  Alyz --> HypY
  HypY --> Comu
  Alyz --> HypN
  HypN -->|Reformulate| Hypo
```

### Asking questions

- What problem are you trying to solve?
  - Or in IR parlance, what task?
- Hard to solve an ill-defined task!
  - Is it a well-known task? Review the literature!
  - Is it unlike anything done before?

#### Asking (new) questions

- Characterize the task
  - How is the system used?
  - What are the inputs? Outputs?
  - How do you define success?

### Formulating hypotheses

- A hypothesis must be falsifiable
  - Ideally concerning an isolated component
- e.g., _length normalization improves ranking_
- It either holds or does not...
  - ... with respect to the considered data (scope)
  - ... perhaps under certain conditions (extent)

### Performing experiments

- Key components
  - Experimental setup
  - Analysis of results
- Key concern: **reproducibility**

  - Must specify each and every detail needed for reproducing our method and the experiment

- [JV]
  - Segundo ele, computação é mais atrasado na parte científica porque na parte da medicina e biologia, se eles cometem um erro, as implicações são seríssimas.
  - Como facilitar a vida de quem desejará reproduzir o experimento?

### Experimental setup

- Research questions
- Evaluation methodology
- Evaluation benchmarks
- Reference comparisons
- Parameter tuning

### Research questions

- Methods are not devised arbitrarily
  - We always have a hypothesis (whether implicit or explicit) for why our work should improve
  - Even the best results are useless if nobody understands what you are trying to solve
- So, spell out your research questions!

### Evaluation methodology

- We want to know
  - What users consider relevant
- We can observe
  - What users tell us (explicit feedback)
  - What users do (implicit feedback)
- These are _noisy_ measurements
  - [JV] Situações usuais mas distintos do comportamento esperado: tipo o amigo que curte o vídeo não por gostar do vídeo mas por gostar de amigo.

---

- Prospective experiments
  - How well can we predict future preferences?
- Benchmarked using live user interactions
  - Poorly reproducible
  - Highly realistic

---

- Retrospective experiments
  - How well can we predict (hidden) past preferences?
- Benchmarked using static test collections
  - Highly reproducible
  - Poorly realistic

---

- Feedback

  - Implicit
  - Explicit

- Mode

  - Retrospective
  - Prospective

- Retrospective+Implicit: Counterfactual evaluation
- **Retrospective+Explicit:** Offline evaluation
  - [JV] Nessa disciplina, focaremos nessa
- Prospective+(Implicit|Explicit): Online evaluation

### Public test collections

- Text REtrieval Conference
  - TREC has collections on Web, blog, tweet, video, question-answering, legal documents, medical records, chemicals, genomics, ... search
  - <http://trec.nist.gov/tracks.html>
  - <http://trec.nist.gov/data.html>

### You can build your own

- Three core components
  - A corpus of documents
  - A set of users' queries
  - A map of users' relevance assessments

---

- Document corpus
  - Go crawl it!
- Queries
  - The more the better (e.g., at least 50)
  - Representative of the population (e.g., from a log)
- Relevance judgments

### How to judge relevance?

- Who does it?
  - Hired judges? Volunteers? Experts? Live users?
  - [JV]
    - Se estou em um caso de uso específico, qualquer um poderia avaliar o ranking? Não, só especialistas.
    - Mechanical alguma coisa na AWS
- What are the instructions?
  - Short queries? Long narratives?
- What is the level of agreement?
  - Redundancy to counter subjectivity

### WHat to judge for relevance

- Exhaustive assessment is not practical
  - Alternative: document sampling
- Stratified sampling via pooling
  - Top $k$ results from $m$ rankers merged
  - Unique (up to $km$) results submitted for judgment
- Generally robust for evaluating new rankers

### Reference comparisons (aka baselines)

- _My method achieves 0.9 precision_
  - Meaningless without a reference comparison
  - Rephrasing: is it better or worse?
- Choice of baseline depends on the hypothesis
  - Key question: what are you trying to show?

### Choosing baselines

- Vanilla baselines
  - Have the proposed effect turned off
    - **e.g.**, ranking without length normalization
- Competing baselines
  - Exploit the proposed effect in a different manner
    - **e.g.**, alternative length normalization

### Parameter tuning

- Your method may have parameters
  - Your baselines may also have parameters
    - **e.g.**, $b$ for pivoted length normalization
- Which parameters need tuning?
  - Which can stay fixed?
  - How to tune?

### Analysis of results

- Measure, compare, slice and dice results
  - Helps prove (or disprove) your hypotheses
  - Demonstrates how your methods or systems compare against the existing state-of-the-art
  - Provides fundamental insights into the underlying research problems being addressed

### Evaluation metrics

- General form: $\Delta (R, G)$
  - $R𝑅$: ranking produced by model $f$ for query $q$
  - $G$: ground-truth produced for query $q$
- Metrics should be chosen according to the task
  - Web search (precision) vs. legal search (recall) (more on next class)
    - [JV] O Recall seria trazer o que algum outro item relevante pro caso atual.

<!-- Cabelímetro -->

### Results significance

- Effectiveness varies across queries
  - Large average improvement may not be consistent
  - Might improve a lot on some queries, hurt on many

### Variable effectiveness

- A2
  - Average gain: 15%
  - Improved queries: 40
  - Harmed queries: 0
- A1
  - Average gain: 15%
  - Improved queries: 20
  - Harmed queries: 20

[IMG: Gráfico $R^2$ onde o A1 tem maior variação, podendo ser muito bom, mas também um pouco ruim. Já no A2 é mais consistente e sempre melhor]

### Results significance (Aula 11)

- Effectiveness varies across queries
  - Large average improvement may not be consistent
  - Might improve a lot on some queries, hurt on many
- Improvements should be tested for significance
  - Statistical significance (see next class)
  - Practical significance

### Deeper analyses

- My method beats the baseline...
  - ... phew, let's call it a victory and go home! **# NOT**
- Deeper analyses may provide further insights
  - Why the method works
  - When the method works
  - And when it doesn't!

---

- Parameter sensitivity analysis
  - How sensitive is the method to its parameters?
- Breakdown analysis
  - How does it perform for different queries?
- Failure analysis
  - What are the main reasons for failure?

### Summary (Aula 11)

- Experimentation drives search innovation

  - Experiments should be economically practical
  - Experiments should be scientifically rigorous
  - Experiments should be reproducible
  - Experiments should provide insights

- [JV] Não conseguimos melhorar o que não conseguimos medir

### References (Aula 11)

- [Link][Aula_11.1] Experimental methods for information retrieval Metzler and Kurland, SIGIR 2012
- [Link][Aula_11.2] Introduction to Information Retrieval, Ch. 8 Manning et al., 2008
- [Link][Aula_11.3] Search Engines: Information Retrieval in Practice, Ch. 8 Croft et al., 2009

[Aula_11.1]: https://dl.acm.org/doi/10.1145/2348283.2348534
[Aula_11.2]: https://www.amazon.com/Introduction-Information-Retrieval-Christopher-Manning/dp/0521865719
[Aula_11.3]: https://www.amazon.com/Search-Engines-Information-Retrieval-Practice/dp/0136072240

## Aula 12 - 30/04/2025 - Offline Evaluation - Slide: 13-offline-evaluation

### Ranking evaluation

- Lots of alternative solutions
  - Which one to choose?
  - How to improve upon them?
- Evaluation enables an informed choice
  - Rigor of science
  - Efficiency of practice

### Evaluation methodology (Aula 12)

- Feedback
  - Implicit
  - Explicit
- Mode

  - Retrospective
  - Prospective

- Retrospective+Implicit: Counterfactual evaluation
  - [JV] Simula o real, usando dados históricos. Usa a teoria de causalidade
- **Retrospective+Explicit:** Offline evaluation
- Prospective+(Implicit|Explicit): Online evaluation

### Test collection-based evaluation

- Three core components
  - A corpus of documents
  - A set of users' queries
  - A map of users' relevance assessments

### TREC topic example

```xml
<top>
  <num> Number: 794
  <title> pet therapy
  <desc> Description: How are pets or animals used in therapy for humans and what are the benefits?
  <narr> Narrative: Relevant documents must include details of how pet- or animal-assisted therapy is or has been used. Relevant details include information about pet therapy programs, descriptions of the circumstances in which pet therapy is used, the benefits of this type of therapy, the degree of success of this therapy, and any laws or regulations governing it.
</top>
```

### Evaluation metrics (Aula 12)

- General form: $\Delta (R_q, G_q)$
  - $R_q$: ranking produced by model $f$ for query $q$
    - [JV] Ranking que chegamos
  - $G_q$: ground-truth produced for query $q$
    - [JV] Quais os rankings oficiais.
- Metrics should be chosen according to the task

### Precision and recall

- Given a query $q$:

  - [Imagem: Conjuntos $R_q$ e $G_q$ que intersectam.]
  - $R_q$: retrieved documents
  - $G_q$: relevant documents

- **Precision**
  - Percentage of retrieved documents that are relevant
  - $Prec(R_q, G_q) = \frac{|R_q \cap G_q|}{|R_q|}$
  - [JV] Quanto eu acertei do que eu mostrei pro usuário?

---

- **Recall**
  - Percentage of relevant documents that are retrieved
  - $Rec(R_q, G_q) = \frac{|R_q \cap G_q|}{|G_q|}$
  - [JV] Quanto eu acertei do que eu encontrei?

---

[Imagem]

---

[Imagem]

- **Precision**
  - $Prec(R_q, G_q) = \frac{|R_q \cap G_q|}{|R_q|} = \frac{2}{4} = 0.50$
- **Recall**
  - $Rec(R_q, G_q) = \frac{|R_q \cap G_q|}{|G_q|} = \frac{2}{3} = 0.67$

---

- **Precision** is about having mostly useful stuff in the ranking
  - Not wasting the user's time
  - Key assumption: there is more useful stuff than the user wants to examine
- **Recall** is about not missing useful stuff in the ranking
  - Not making a bad oversight
  - Key assumption: the user has time to filter through ranked results
- We can also combine both
  - $F1(R, G) = 2 \frac{Prec(R, G) \cdot Rec(R, G)}{Prec(R, G) + Rec(R, G)}$
  - [JV] Frequência Harmônica

- [JV]
  - Exemplos de situações:
    - Recall: Pesquisa acadêmica, pesquisa de jurisprudência

### Errors

- Type 1 Error: False Positive "You're pregnant!" [Um médico falando para um idoso]
- Type 2 Error: False Negative "You're not pregnant!" [Uma médica falando para uma mulher grávida]

### Classification Errors

- Type I error: probability of retrieving non-relevants
  - $FallOut (R_q, G_q) = \frac{|R_q \cap \bar{G_q}|}{|\bar{G_q}|}$
- Type II error: probability of missing relevants
  - $MissRate (R_q, G_q) = 1 - Rec(R_q, G_q)$

### Beyond Decision Support

- Modern document corpora are huge
  - User may not be willing to inspect large sets
- Consider top-5 rankings
  - Ranker #1: + + + + −
  - Ranker #2: − + + + +
- Ranker #2 misplaces a highly visible item
  - [JV] Mas a precisão e revocação não conseguem diferenciar esses dois.

### Evaluation Cutoffs

- Calculate precision and recall at fixed rank positions
  - e.g., Prec@10, Rec@10
- Calculate precision at standard recall levels
  - e.g., Prec@Rec=30%

### Precision vs recall graph

[Imagem]

### Precision vs recall graph (interpolated)

[Imagem]

### Precision vs recall graph (averaged)

[Imagem]

### Position Blindness

[Imagem]

These have exactly the same Prec@4 (0.25)
◦ Are they equally good?

### Position-aware metrics

- Why ranking?
  - Place documents in order of preference
- Key assumption
  - Users will inspect retrieved documents from top to bottom (or left to right)

### Average precision (AP)

- Simple idea: average precision values at the ranking positions where relevant documents were found
  - $AP(R_q, G_q) =$
  - [JV] vai varrer cada uma das precisões 


Simple idea: averaging precision values at the ranking
positions where relevant documents were found
AP 𝑅𝑞, 𝐺𝑞 = 1
|𝐺𝑞| σ𝑖=1
𝑘 1 𝑔𝑞𝑑𝑖 > 0 Prec@𝑖
---

- [JV] O cálculo da média, baseando sobre o G_q a gente penaliza devidamente para evitar que situações como consultas que retornam apenas um por exemplo

MAP (Mean Average Precision)

### Reciprocal Rank (RR)

MRR

---

1/1

---

1/3

### Discounted Cumulative Gain (DCG)

- $DCG(R_q, G_q) = \sum_{i=1}^{k} \frac{g_{qd_i}}{\log_2(i+1)}$
  - $\frac{\text{Linear gain (e.g., in a graded scale)}{\text{position-based discount}}}$

[JV] A imagem tem ordenado o mais relevante com o maior valor no topo e a base começa com 1

[Dúvida] Como surgem essas fórmulas?
[Resposta]: É empírico. Eles vão gerando modelos de usuários. Exemplos: Usuário que o interesse vai decaindo a medida que vai passando pelos arquivos VS usuário que, após encontrar um relevante, o interesse vai pra 0.

---

---

- [JV] Essas avaliações são como termômetros para poder avaliar o quanto o modelo está bom ou não.
  - Alguns problemas dessa avaliação:
    - Não fica claro qual que é o teto dessa avaliação.
    - Não é verificado o quão negativos são os documentos não relevantes encontrados.
  - A ideia do Discounted é a perda de valor por resultados que estão lá no baixo do ranking encontrado

### Ideal Discounted Cumulative Gain (iDCG)

### Normalized Discounted Cumulative Gain (nDCG)

### Average nDCG

### Significance test

- [JV] Prova por negação

### Paired Testing

### $t$-test

- Média dos valores de B-A, multiplicado pela raiz da quantidade de itens medidos.
- Se t é pequeno, então realmente há forte similaridade entre os dois. Senão, eles são muito diferentes.
- O $\sigma$(?) é o desvio padrão para atenuar baseado na quantidade de itens

### Paired $t$-test

- [JV] Precisaremos ver quão provável é encontrar o tal valor que vimos.
- [JV] Não seria interessante ter também um upper and lower bound dos valores encontrados?

---

### $t$-distribuition ($v=1$)

Numero da amostra -1 que é usando níveis de graus de liberdade

Métodos quantitativos

### $t$-distribuition ($v=2$)

### $t$-distribuition ($v=3$)

### $t$-distribuition ($v=5$)

### $t$-distribuition ($v=10$)

### $t$-distribuition ($v=30$)

Acaba sendo uma observação empírica esse valor de 30 onde a curva t tende à normal

### One-sided vs two-sided tests

Afinal, quero comparar se A é melhor que B, ou se A é igual a B?

### One-sided test ($A > B$)

### Two-sided test ($A \neq B$)

Gera um cenário mais rigoroso pro experimento

### $t$-table

---

Onesided: 5% de serem equivalentes
Two-sided: 10% de serem equivalentes

### Paired $t$-test

Deve-se considerar um $p$ value para reprovar. 0.05 é recorrente por é abaixo dos 95% de confiança

Define-se isso de antemão para não **Roubar** e ter viés

### Criticisms



Essa parte estatística pode ser abusada

Alternativas: Melhorar muito o B; Reduzir a variância; Aumentar a amostra

Aumentar a amostra é o mais fácil, mas não necessariamente o melhor

Isso seria o $p$-Hacking; É uma má prática

---

> It is quite possible, and unfortunately quite common, for a result to be statistically significant and trivial. It is also possible for a result to be statistically nonsignificant and important.

- Ellis, 2010

---

[Imagem: Diagrama de Euler entre: All hypothesis, Statistically significant results, Published results, Interesting results]

### Sumary

- No single measure is the correct one for any application
  - Choose measures appropriate for task
  - Use a combination to highlight different aspects
- Use significance tests (two-sided paired 𝑡-test)
  - Also report effect sizes!
- Analyze performance of individual queries

### Query Summary

[Imagem: Queries X Percentage Gain or Loss]

### References (Aula 12)

- [Link] Search Engines: Information Retrieval in Practice, Ch. 8 Croft et al., 2009
- [Link] Introduction to Information Retrieval, Ch. 8 Manning et al., 2008
- [Link] Test collection based evaluation of IR systems Sanderson, FnTIR 2010

---

- [Link] Statistical reform in information retrieval? Sakai, SIGIR Forum 2014
- [Link] Statistical significance testing in theory and in practice Carterette, SIGIR 2017
- [Link] Statistical significance testing in information retrieval: an empirical analysis of type I, type II and type III errors Urbano et al., SIGIR 2019

### Coming next... Exam #1

- [JV]
  - Prova: algum calculo mas que dá pra fazer na mão
  - Prova aberta, umas 8 a 10 questões

## Aula 13 - 05/05/2025 - Exam #1

## Aula 14 - 07/05/2025 - Quality Models

## Aula 15 - 12/05/2025 - Feedback Models

## Aula 16 - 14/05/2025 - Diversification Models

## Aula 17 - 19/05/2025 - Learning to Rank: Fundamentals

## Aula 18 - 21/05/2025 - Learning to Rank: Algorithms

## Aula 19 - 26/05/2025 - Neural Models: Reranking

## Aula 20 - 28/05/2025 - Neural Models: Retrieval

## Aula 21 - 02/06/2025 - Online Evaluation

## Aula 22 - 04/06/2025 - Online Learning to Rank

## Aula 23 - 09/06/2025 - Seminars

## Aula 24 - 11/06/2025 - Seminars

## Aula XX - 16/06/2025 - Exam #2

## Aula 25 - 18/06/2025 - Recess: Corpus Christi

## Aula 26 - 23/06/2025 - RC Development (off-class)

## Aula 27 - 25/06/2025 - RC Presentations

## Aula 28 - 30/06/2025 - RC Presentations

## Aula 29 - XX/07/2025 - Replacement Exam

## Aula 30 - XX/07/2025 - Replacement Exam
