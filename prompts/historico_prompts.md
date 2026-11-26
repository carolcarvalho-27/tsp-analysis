# Histórico de prompts utilizados com Inteligência Artificial

Este documento registra as principais solicitações realizadas à ferramenta de Inteligência Artificial durante o desenvolvimento do trabalho sobre análise empírica e otimização do Problema do Caixeiro Viajante (TSP).

Os prompts estão organizados cronologicamente e agrupados conforme a etapa do desenvolvimento. Os registros identificados como sínteses representam reconstruções dos pedidos a partir do histórico de trabalho, não transcrições literais.

## 1. Planejamento e estruturação do projeto

**Prompt 1 — Planejamento da implementação**

Solicitação de orientação para organizar o desenvolvimento do trabalho de TSP, considerando a implementação dos algoritmos Branch-and-Bound, Twice-around-the-tree e Christofides, além das estratégias de solução inicial, instrumentação e análise experimental.

**Prompt 2 — Organização do ambiente e da estrutura do projeto**

Solicitação de auxílio para configurar o ambiente Python e organizar os diretórios e módulos do projeto, considerando o uso do VS Code, Git e bibliotecas necessárias.

## 2. Implementação dos algoritmos e componentes

**Prompt 3 — Representação das instâncias**

Solicitação de orientação para implementar a representação das instâncias do TSP, o carregamento de arquivos TSPLIB e o cálculo das matrizes de distância.

**Prompt 4 — Implementação das soluções iniciais**

Solicitação de auxílio para implementar as estratégias Nearest Neighbor, inserção baseada no fecho convexo, Twice-around-the-tree e Christofides, além da solução trivial utilizada como referência.

**Prompt 5 — Implementação do Branch-and-Bound**

Solicitação de orientação para implementar o algoritmo exato Branch-and-Bound, incluindo limite inferior, poda, solução inicial, contagem de nós e limite de tempo.

**Prompt 6 — Verificação e testes**

Solicitação de auxílio para estruturar testes automatizados e verificar a validade das soluções, a admissibilidade do limite inferior e a correção dos algoritmos.

## 3. Instrumentação e execução dos experimentos

**Prompt 7 — Registro dos resultados**

Solicitação de orientação para instrumentar os experimentos, registrando tempo de execução, memória, nós expandidos e podados, profundidade máxima e situações de timeout.

**Prompt 8 — Retomada de experimentos**

Solicitação de auxílio para implementar a retomada de campanhas experimentais interrompidas, evitando repetir estratégias já concluídas para uma mesma instância e limite de tempo.

**Prompt 9 — Interpretação da desigualdade triangular**

Solicitação de auxílio para verificar empiricamente a propriedade da desigualdade triangular nas instâncias selecionadas e compreender suas implicações para as garantias teóricas dos algoritmos de aproximação.

## 4. Preparação da campanha experimental

**Prompt 10 — Execução da campanha definitiva**

Foi solicitada orientação sobre a execução sequencial dos experimentos e a possibilidade de iniciar a campanha definitiva enquanto a elaboração do relatório ocorre em paralelo.

## 5. Versionamento e documentação

**Prompt 11 — Preparação do primeiro commit**

Foi solicitada orientação para adicionar ao Git os arquivos já desenvolvidos, evitando incluir o ambiente virtual e arquivos temporários.

**Prompt 12 — Correção de erro ao adicionar diretórios**

Foi apresentado o erro:

`fatal: pathspec 'reports/latex/' did not match any files`

Foi solicitada ajuda para compreender e corrigir o problema durante a preparação do primeiro commit.

**Prompt 13 — Extração do histórico de prompts**

Solicitação para organizar as interações realizadas com a ferramenta de IA em um registro que possa ser incluído na seção de prompts do trabalho.

---

*Observação: este histórico apresenta uma síntese das principais interações. Para uma transcrição integral e literal, devem ser consultadas as mensagens originais da conversa no link a seguir.*

https://chatgpt.com/share/6b061a31-93e8-83ea-a6c2-fbe9aa7f3f15
