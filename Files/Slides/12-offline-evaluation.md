# Aula 12 - 30/04/2025 - Offline Evaluation - Slide: 13-offline-evaluation

## Ranking evaluation

- Lots of alternative solutions
  - Which one to choose?
  - How to improve upon them?
- Evaluation enables an informed choice
  - Rigor of science
  - Efficiency of practice

## Evaluation methodology (Aula 12)

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

## Test collection-based evaluation

- Three core components
  - A corpus of documents
  - A set of users' queries
  - A map of users' relevance assessments

## TREC topic example

```xml
<top>
  <num> Number: 794
  <title> pet therapy
  <desc> Description: How are pets or animals used in therapy for humans and what are the benefits?
  <narr> Narrative: Relevant documents must include details of how pet- or animal-assisted therapy is or has been used. Relevant details include information about pet therapy programs, descriptions of the circumstances in which pet therapy is used, the benefits of this type of therapy, the degree of success of this therapy, and any laws or regulations governing it.
</top>
```

## Evaluation metrics (Aula 12)

- General form: $\Delta (R_q, G_q)$
  - $R_q$: ranking produced by model $f$ for query $q$
    - [JV] Ranking que chegamos
  - $G_q$: ground-truth produced for query $q$
    - [JV] Quais os rankings oficiais.
- Metrics should be chosen according to the task

## Precision and recall

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

## Errors

- Type 1 Error: False Positive "You're pregnant!" [Um médico falando para um idoso]
- Type 2 Error: False Negative "You're not pregnant!" [Uma médica falando para uma mulher grávida]

## Classification Errors

- Type I error: probability of retrieving non-relevants
  - $FallOut (R_q, G_q) = \frac{|R_q \cap \bar{G_q}|}{|\bar{G_q}|}$
- Type II error: probability of missing relevants
  - $MissRate (R_q, G_q) = 1 - Rec(R_q, G_q)$

## Beyond Decision Support

- Modern document corpora are huge
  - User may not be willing to inspect large sets
- Consider top-5 rankings
  - Ranker #1: + + + + −
  - Ranker #2: − + + + +
- Ranker #2 misplaces a highly visible item
  - [JV] Mas a precisão e revocação não conseguem diferenciar esses dois.

## Evaluation Cutoffs

- Calculate precision and recall at fixed rank positions
  - e.g., Prec@10, Rec@10
- Calculate precision at standard recall levels
  - e.g., Prec@Rec=30%

## Precision vs recall graph

[Imagem]

## Precision vs recall graph (interpolated)

[Imagem]

## Precision vs recall graph (averaged)

[Imagem]

## Position Blindness

[Imagem]

These have exactly the same Prec@4 (0.25)

- Are they equally good?

## Position-aware metrics

- Why ranking?
  - Place documents in order of preference
- Key assumption
  - Users will inspect retrieved documents from top to bottom (or left to right)

## Average precision (AP)

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

## Reciprocal Rank (RR)

MRR

---

1/1

---

1/3

## Discounted Cumulative Gain (DCG)

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

## Ideal Discounted Cumulative Gain (iDCG)

## Normalized Discounted Cumulative Gain (nDCG)

## Average nDCG

## Significance test

- [JV] Prova por negação

## Paired Testing

## $t$-test

- Média dos valores de B-A, multiplicado pela raiz da quantidade de itens medidos.
- Se t é pequeno, então realmente há forte similaridade entre os dois. Senão, eles são muito diferentes.
- O $\sigma$(?) é o desvio padrão para atenuar baseado na quantidade de itens

## Paired $t$-test

- [JV] Precisaremos ver quão provável é encontrar o tal valor que vimos.
- [JV] Não seria interessante ter também um upper and lower bound dos valores encontrados?

## $t$-distribuition ($v=1$)

Numero da amostra -1 que é usando níveis de graus de liberdade

Métodos quantitativos

## $t$-distribuition ($v=2$)

## $t$-distribuition ($v=3$)

## $t$-distribuition ($v=5$)

## $t$-distribuition ($v=10$)

## $t$-distribuition ($v=30$)

Acaba sendo uma observação empírica esse valor de 30 onde a curva t tende à normal

## One-sided vs two-sided tests

Afinal, quero comparar se A é melhor que B, ou se A é igual a B?

## One-sided test ($A > B$)

## Two-sided test ($A \neq B$)

Gera um cenário mais rigoroso pro experimento

## $t$-table

---

Onesided: 5% de serem equivalentes
Two-sided: 10% de serem equivalentes

## Paired $t$-test (2)

Deve-se considerar um $p$ value para reprovar. 0.05 é recorrente por é abaixo dos 95% de confiança

Define-se isso de antemão para não **Roubar** e ter viés

## Criticisms

Essa parte estatística pode ser abusada

Alternativas: Melhorar muito o B; Reduzir a variância; Aumentar a amostra

Aumentar a amostra é o mais fácil, mas não necessariamente o melhor

Isso seria o $p$-Hacking; É uma má prática

---

> It is quite possible, and unfortunately quite common, for a result to be statistically significant and trivial. It is also possible for a result to be statistically nonsignificant and important.

- Ellis, 2010

---

[Imagem: Diagrama de Euler entre: All hypothesis, Statistically significant results, Published results, Interesting results]

## Sumary

- No single measure is the correct one for any application
  - Choose measures appropriate for task
  - Use a combination to highlight different aspects
- Use significance tests (two-sided paired 𝑡-test)
  - Also report effect sizes!
- Analyze performance of individual queries

## Query Summary

[Imagem: Queries X Percentage Gain or Loss]

## References (Aula 12)

- [[Link]] Search Engines: Information Retrieval in Practice, Ch. 8 Croft et al., 2009
- [[Link]] Introduction to Information Retrieval, Ch. 8 Manning et al., 2008
- [[Link]] Test collection based evaluation of IR systems Sanderson, FnTIR 2010

---

- [[Link]] Statistical reform in information retrieval? Sakai, SIGIR Forum 2014
- [[Link]] Statistical significance testing in theory and in practice Carterette, SIGIR 2017
- [[Link]] Statistical significance testing in information retrieval: an empirical analysis of type I, type II and type III errors Urbano et al., SIGIR 2019

## Coming next... Exam #1

- [JV]
  - Prova: algum calculo mas que dá pra fazer na mão
  - Prova aberta, umas 8 a 10 questões
