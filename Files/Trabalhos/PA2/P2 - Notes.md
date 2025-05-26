# Anotações

- Pode assumir mínimo de 2Gb de RAM

## Fórum

### Vinicius

Boa tarde professor,

Estou com dúvida em relação ao PA2, e as 3 estruturas pedidas (inverted index, document index, lexicon). No meu entendimento, o document index e o lexicon serviriam para guardar as estatísticas de cada documento e termo (ex. tamanho de cada documento), alguns que precisariam futuramente ser utilizadas pelos rankers (TF-IDF, BM25). Porém, o query processor, no caso, receberia apenas o arquivo de índice reverso ("the path to an index file")?

A formatação e os campos do document index e lexicon ficam a critério do aluno também? Minha ideia era usar o lexicon para também mapear termo -> (offset e length) da posting list do termo no indíce reverso

#### Resposta Rodrygo

Oi, Vinícius.

> Estou com dúvida em relação ao PA2, e as 3 estruturas pedidas (inverted index, document index, lexicon). No meu entendimento, o document index e o lexicon serviriam para guardar as estatísticas de cada documento e termo (ex. tamanho de cada documento), alguns que precisariam futuramente ser utilizadas pelos rankers (TF-IDF, BM25). Porém, o query processor, no caso, receberia apenas o arquivo de índice reverso ("the path to an index file")?

Boa observação. Seu código pode assumir que os demais arquivos estão no mesmo diretório que o índice invertido.

> A formatação e os campos do document index e lexicon ficam a critério do aluno também? Minha ideia era usar o lexicon para também mapear termo -> (offset e length) da posting list do termo no indíce reverso

Sim, ficam a seu critério. O uso que você pensou faz bastante sentido.

Rodrygo
