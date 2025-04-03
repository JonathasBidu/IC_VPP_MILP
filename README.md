<!-- # **Otimização de Despacho de Recursos Energéticos Distribuídos (REDs)**  

Este repositório faz parte do meu projeto de **Iniciação Científica** na **Universidade Federal Fluminense (UFF)**, dentro do curso de **Engenharia Elétrica**. O objetivo da pesquisa é desenvolver métodos para **agregar Recursos Energéticos Distribuídos (REDs)** e coordenar seus despachos de forma otimizada, permitindo que operem como se fossem uma única usina virtual (**Virtual Power Plant - VPP**).  

## 🔍 **Descrição do Projeto**  
Nesta etapa da pesquisa, estou reformulando o problema, que originalmente envolvia **equações não lineares**, para uma abordagem com **equações lineares**, tornando a otimização mais eficiente e viável computacionalmente.  

O programa implementado aqui resolve esse problema utilizando **algoritmos genéticos (GA)** para encontrar despachos energéticos ótimos, maximizando o lucro e garantindo o atendimento às restrições operacionais.  

## ⚙️ **Principais funcionalidades**  
- Modelagem de uma **Virtual Power Plant (VPP)** para otimização de despacho de REDs.  
- Utilização de **cenários de geração renovável e consumo** para simulações.  
- Implementação de um **otimizador baseado em Algoritmos Genéticos (GA)**.  
- Reformulação matemática para uma abordagem **linear**, facilitando a resolução do problema.  

## 📁 **Estrutura do Código**  
- `decompose_vetor.py` → Decompõe o vetor de soluções nas variáveis de decisão.  
- `eq_constraints.py` → ...  
- `generator_scenarios.py` → Gera, salva e importa os cenários de operação.  
- `get_limits.py` → ...  
- `ieq_constraints.py` → ...  
- `load_projections.py` → ...  
- `objetive_function.py` → ...  
- `optimazer_GA.py` → Contém a implementação do Algoritmo Genético para otimização.  
- `script.py` → ...  
- `vpp_data.py` → Organiza os dados  da Virtual Power Plant (VPP).  
- `vpp_plot.py` → Gera visualizações gráficas dos resultados.  

## 🚀 **Execução do Programa**  
1. Defina o período da simulação (exemplo: 24h).  
2. O programa carregará os dados dos REDs e cenários de operação.  
3. O **otimizador GA** será executado para encontrar o melhor despacho.  
4. A solução será visualizada graficamente e o lucro será exibido.  

## 🏆 **Resultados Esperados**  
- Um despacho otimizado para a VPP, maximizando o **lucro** e garantindo o **atendimento às restrições**.  
- Redução da complexidade computacional ao reformular o problema para **equações lineares**.  

## 🤝 **Contribuição**  
Caso queira contribuir com este projeto, fique à vontade para abrir uma issue ou fazer um pull request!  

---  
💡 **Sinta-se à vontade para contribuir ou entrar em contato para discussões sobre otimização energética!** 🚀⚡
 -->
# **Otimização de Despacho de Recursos Energéticos Distribuídos (REDs)**  

Este repositório faz parte do meu projeto de **Iniciação Científica** na **Universidade Federal Fluminense (UFF)**, dentro do curso de **Engenharia Elétrica**. O objetivo da pesquisa é desenvolver métodos para **agregar Recursos Energéticos Distribuídos (REDs)** e coordenar seus despachos de forma otimizada, permitindo que operem como se fossem uma única usina virtual (**Virtual Power Plant - VPP**).  

## 🔍 **Descrição do Projeto**  
Nesta etapa da pesquisa, estou reformulando o problema, que originalmente envolvia **equações não lineares**, para uma abordagem com **equações lineares**, tornando a otimização mais eficiente e viável computacionalmente.  

O programa implementado aqui resolve esse problema utilizando **algoritmos genéticos (GA)** para encontrar despachos energéticos ótimos, maximizando o lucro e garantindo o atendimento às restrições operacionais.  

## 🔗 **Repositórios Relacionados**  
Este projeto é a terceira etapa de uma pesquisa mais ampla sobre **otimização de despacho de Recursos Energéticos Distribuídos (REDs)**. As etapas anteriores exploraram diferentes abordagens para a modelagem e solução do problema:  

1. **[Abordagem Determinística](URL_DO_REPOSITORIO)**  
   - Formulação do problema como um modelo determinístico, assumindo **dados conhecidos e sem incertezas**.  
   - Otimização do despacho utilizando programação matemática clássica.  

2. **[Abordagem Estocástica de Dois Níveis](URL_DO_REPOSITORIO)**  
   - Introdução da **incerteza na geração e no consumo** através de um modelo estocástico.  
   - Estrutura de dois níveis, onde um nível superior coordena a operação considerando previsões probabilísticas.  

3. **(Este Repositório) Abordagem com Reformulação Linear**  
   - Conversão do problema para uma **formulação linear**, tornando a solução computacionalmente mais eficiente.  
   - Implementação de um **otimizador baseado em Algoritmos Genéticos (GA)** para encontrar despachos ótimos.  

Esta evolução permite comparar os métodos e entender os benefícios e desafios de cada abordagem.  

## ⚙️ **Principais funcionalidades**  
- Modelagem de uma **Virtual Power Plant (VPP)** para otimização de despacho de REDs.  
- Utilização de **cenários de geração renovável e consumo** para simulações.  
- Implementação de um **otimizador baseado em Algoritmos Genéticos (GA)**.  
- Reformulação matemática para uma abordagem **linear**, facilitando a resolução do problema.  

## 📁 **Estrutura do Código**  
- `decompose_vetor.py` → Decompõe o vetor de soluções nas variáveis de decisão.  
- `eq_constraints.py` → Define as restrições de igualdade do problema.  
- `generator_scenarios.py` → Gera, salva e importa os cenários de operação.  
- `get_limits.py` → Determina os limites superior e inferior das variáveis de decisão.  
- `ieq_constraints.py` → Define as restrições de desigualdade do problema.  
- `load_projections.py` → Carrega projeções de dados para a simulação.  
- `objetive_function.py` → Implementa a função objetivo a ser otimizada.  
- `optimazer_GA.py` → Contém a implementação do Algoritmo Genético para otimização.  
- `script.py` → Arquivo principal que executa o programa.  
- `vpp_data.py` → Organiza os dados da Virtual Power Plant (VPP).  
- `vpp_plot.py` → Gera visualizações gráficas dos resultados.  

## 🚀 **Execução do Programa**  
1. Defina o período da simulação (exemplo: 24h).  
2. O programa carregará os dados dos REDs e cenários de operação.  
3. O **otimizador GA** será executado para encontrar o melhor despacho.  
4. A solução será visualizada graficamente e o lucro será exibido.  

## 🏆 **Resultados Esperados**  
- Um despacho otimizado para a VPP, maximizando o **lucro** e garantindo o **atendimento às restrições**.  
- Redução da complexidade computacional ao reformular o problema para **equações lineares**.  

## 🤝 **Contribuição**  
Caso queira contribuir com este projeto, fique à vontade para abrir uma issue ou fazer um pull request!  

---  
💡 **Sinta-se à vontade para contribuir ou entrar em contato para discussões sobre otimização energética!** 🚀⚡
