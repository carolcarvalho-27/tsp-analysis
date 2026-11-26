# Histórico de prompts utilizados com Inteligência Artificial

Este documento apresenta uma síntese das principais solicitações realizadas à ferramenta de Inteligência Artificial durante o desenvolvimento do trabalho sobre análise empírica e otimização do Problema do Caixeiro Viajante (TSP).

As interações estão organizadas cronologicamente, de acordo com as etapas do projeto. Os registros representam sínteses dos pedidos realizados, não transcrições literais das mensagens originais.

## 1. Planejamento e modelagem do problema

**Prompt 1 — Planejamento da análise empírica**

Solicitação de orientação para estruturar o trabalho, definir os algoritmos a serem avaliados e estabelecer os objetivos da comparação entre métodos exatos e aproximados para o TSP.

**Prompt 2 — Seleção e representação das instâncias**

Solicitação de auxílio para trabalhar com instâncias da biblioteca TSPLIB, compreender seus formatos e implementar a representação dos dados, incluindo coordenadas, matrizes de distância e características das instâncias.

## 2. Implementação dos algoritmos

**Prompt 3 — Algoritmos de aproximação**

Solicitação de orientação para implementar os algoritmos Nearest Neighbor, Twice-around-the-tree e Christofides, compreendendo suas etapas, funcionamento e garantias teóricas.

**Prompt 4 — Estratégia de inserção pelo fecho convexo**

Solicitação de auxílio para desenvolver uma heurística de construção de ciclos baseada no fecho convexo, utilizando a inserção progressiva dos vértices restantes.

**Prompt 5 — Implementação do Branch-and-Bound**

Solicitação de orientação para desenvolver o algoritmo exato Branch-and-Bound, incluindo a construção da árvore de busca, cálculo de limites inferiores, poda de subárvores e utilização de soluções iniciais como limites superiores.

**Prompt 6 — Estratégias de solução inicial (warm-start)**

Solicitação de auxílio para integrar e comparar diferentes estratégias de inicialização do Branch-and-Bound: ciclo trivial, Nearest Neighbor, fecho convexo, Twice-around-the-tree e Christofides.

## 3. Validação e instrumentação

**Prompt 7 — Testes de correção e validação dos algoritmos**

Solicitação de orientação para elaborar testes que verificassem a validade dos ciclos produzidos, a correção dos algoritmos e a admissibilidade dos limites inferiores utilizados pelo Branch-and-Bound.

**Prompt 8 — Instrumentação e métricas de desempenho**

Solicitação de auxílio para definir e registrar métricas experimentais, incluindo tempo de execução, memória utilizada, quantidade de nós expandidos e podados, profundidade máxima da busca e ocorrência de timeouts.

**Prompt 9 — Análise da desigualdade triangular**

Solicitação de auxílio para verificar a propriedade da desigualdade triangular nas instâncias selecionadas e compreender como sua presença ou ausência afeta as garantias de aproximação dos algoritmos avaliados.

## 4. Execução e análise experimental

**Prompt 10 — Planejamento e execução da campanha experimental**

Solicitação de orientação para organizar a execução sistemática dos algoritmos nas instâncias selecionadas, considerando as diferentes estratégias de solução inicial e o limite de tempo estabelecido para cada execução.

**Prompt 11 — Análise dos resultados experimentais**

Solicitação de correção na interpretação dos resultados obtidos, comparação os custos das soluções iniciais, avaliação o desempenho do Branch-and-Bound e análise das diferenças entre as estratégias.

**Prompt 12 — Análise estatística e comportamento assintótico**

Solicitação de orientação para realizar regressões entre o tamanho das instâncias e o esforço de busca, interpretar coeficientes, R² e RMSE, além de discutir as limitações das estimativas diante das execuções interrompidas por timeout.

**Prompt 13 — Comparação entre qualidade da solução inicial e esforço de busca**

Solicitação de auxílio para investigar a relação entre os gaps das soluções iniciais e o desempenho do Branch-and-Bound, considerando principalmente o tempo de execução e a quantidade de nós expandidos.

## 5. Elaboração e documentação do trabalho

**Prompt 14 — Estruturação do relatório científico**

Solicitação de verificação da organização do artigo no formato SBC, definir as seções e subseções e apresentar a metodologia, os experimentos e os resultados de maneira coerente.

**Prompt 15 — Revisão das conclusões e documentação do desenvolvimento**

Solicitação de auxílio para revisar a interpretação dos resultados, explicitar limitações experimentais, formular conclusões compatíveis com as evidências obtidas e documentar o uso de Inteligência Artificial ao longo do projeto.

---

*Observação: este histórico apresenta uma síntese das principais interações realizadas durante o desenvolvimento do trabalho. Os registros não correspondem necessariamente à ordem exata nem à redação literal dos prompts originais. Para uma transcrição integral, devem ser consultadas as mensagens originais da conversa.*

https://chatgpt.com/share/6b061a31-93e8-83ea-a6c2-fbe9aa7f3f15
