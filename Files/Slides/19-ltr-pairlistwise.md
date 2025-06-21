# Aula 18 - 21/05/2025 - Learning to Rank: Algorithms; Learning to Rank: Pairwise and Listwise

- [JV]
  - São áreas atívas há décadas
  - Ele vai liberar a próxima atividade na quarta feira

## The Ranking Problem

- [Mermaid]

---

- [Mermaid]
- f(x)
- [JV] Aprendizado supervisionado

## Learning to Rank

- Combina várias features para gerar um ranking final
- Junta várias ideias de aprendizado de máquina

## Pointwise approach

- Cada documento é tratado como uma instância independente.
- Durante o treinamento já definimos quais documentos são relevantes para dadas consultas.
- Temos pares: (vetor de features, relevante ou não) para cada query
- Já temos várias abordagens funcionais
- porém "Dá pra melhorar" TM

### Limitations of the pointwise approach

- A limitação é a tentativa de dar um score, mas isso não necessariamente gera uma boa função de ranking.
- Poderia penalizar mais os que estão no topo e menos os que estão no fundo.
- Deve-se também considerar os possíveis erros de classificação dos documentos nas várias consultas

---

...

## Pairwise approach

- Pelo que entendi, basicamente tá definindo uma ranqueamento por "O primeiro é melhor que o segundo? Sim ou não."

### RankNet (Burges et al., ICML 2005)

- Na entrada são as features de um único documento por vez. Porém essa função é aplicada paralelamente para os documentos $x_u$ e $x_v$

---

- $Equação$
- Os outputs da rede neural são números reais
- Cross Entropy Loss (Entropia Cruzada)
  - Busca minimizar a entropia da rede.
  - Consideremos o label como "1" para $x_u > x_v$ verdadeiro.
  - Na prática, só uma das parcelas da equação vai ser ativada e calculada, porque o $y$ só será 1 ou 0.
  - Se acerta, não penaliza nada.
  - Analisar para $\{0, 1\}^2$
  - Quando erra, o log de algo próximo a 0 tende a infinito.
- A ideia é que use-se o par para treinar a função pairwise, que será o resultado final: uma função de ranqueamento.

#### Ranking SVM (Herbrich et al., ALMC 2000; Joachims, KDD 2002)

- Busca encontrar uma "superfície de separação de mais alta margem"
- Multiplicar rótulos positivos e negativos, se previu certo, dá positivo, senão, negativo ($1 \cdot 1$ vs $-1 \cdot -1$)
- Na Hinge loss, mesmo quando acerta ainda há loss; Só após uma margem de segurança que passa a não ter loss.
- É importante lembrar que às vezes os rótulos são 0 e 1, às vezes são -1 e 1.

##### Kernel Trick

- Imagens mt maneiras de mudança de dimensão

#### Limitations of the pairwise approach

- Ignora-se o quão intensas são as relações entre os itens

## Can we optimize ranking metrics directly

- Por que usar Loss functions e não a própria função?

### Ranking metrics generally non-differentiable

- Piecewise constant functions

- O nDCG por exemplo não é diferenciável
- Quando o score nDCG reduz, significa que um menos relevante foi posto na frente de um mais relevante.
- Nos degraus, as derivadas são zero. Se usamos modelos que usam a derivada como passo de correção, não daria certo. O mesmo quando tem salto, que aí é indeterminado (?)

### LambdaRank (Burges, NIPS 2006)

- Evolução do RankNet
- Pode gerar esse gradiente esperado

---

- Geralmente alterações em documentos mais relevantes terão maior impacto do que os que estão mais abaixo.

---

- Verifica-se o impacto de um swap entre documentos

---

Lambda Function

- Delta nDCG é a intensidade do swap entre documentos

### LambdaMART (Wu et al., Tech. Report 2008)

MART = Multiple Additive Regression Trees

- Gera uma nova árvore que maximiza a lambda function relacionado ao nDCG

## Listwise approach

- Duas famílias: otimização por métrica de avaliação como nDCG

### Metric-specific listwise ranking

Como tornar uma loss function diferenciável? Pensar num proxy.

#### SoftRank

- Ideia: suavizar o score em uma variável aleatória de distribuição.

---

O softrank, com a distribuição, amostram-se várias vezes e daí consegue-se uma média, não entendi exatamente de que forma no final vira uma função amena.

#### AdaRank (Xu and Li, SIGIR 2007)

"Boosting é isso: modelinhos que remendam o modelão"

Com o tempo, é esperado que o ensemble comece a não performar tão bem, e então precisamos encontrar um modelinho que tenha o melhor remendo do momento.

Não precisa de derivadas.

### Ranking Loss is non-trivial

Em termos absolutos eles são igualmente bons ou ruins

#### ListNet (Cao et al.)

Calcular scores sobre permutações.

o f(B)/f(B) daria 1, por isso tá omitida.

Em teoria da informação, pode-se comparar a divergência entre distribuições

##### Divergence between

##### KL Divergence Loss

Quanto maior a divergência, pior é.

## Summary

- Comparar pares vs comparar listas
- "Escolher o martelo mais adequado pro problema"
- Podemos otimizar função de ranking pelo caso de uso?
- LETOR: fornecem datasets para benchmarks

## Ranklib Tutorial

Uma das primeiras e mais robustas

---

PA3: usaremos ferramentas prontas e teremos uma competição no Kaggle

## References

## Coming Next: Neural Models

-
