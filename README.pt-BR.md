<div align="center">

<sub><a href="https://github.com/lucasschn1">English</a> · <b>Português</b></sub>

# Lucas Schneider C.

**Desenvolvedor Full Stack**

Construo APIs testadas e os apps que as usam · PHP · TypeScript · React

<img src="https://img.shields.io/badge/%E2%97%8F%20dispon%C3%ADvel%20agora-2ea043?style=for-the-badge" alt="Disponível agora" />
<img src="https://img.shields.io/badge/vagas-Backend%20%2F%20Full%20Stack-30363d?style=for-the-badge&labelColor=161b22" alt="Aberto a vagas Backend / Full Stack" />
<img src="https://img.shields.io/badge/modelo-remoto%20%C2%B7%20h%C3%ADbrido%2Fpresencial%20em%20Curitiba%2C%20PR-30363d?style=for-the-badge&labelColor=161b22" alt="Modelo: remoto, ou híbrido/presencial em Curitiba, PR" />

[Sobre mim](#sobre-mim) · [Projetos](#projetos) · [Tecnologias](#tecnologias) · [Contato](#contato)

</div>

---

## Contribuições

<img src="./assets/contrib-heatmap.svg" width="100%" alt="Mapa de calor de contribuições do último ano" />

<br>

## Sobre mim

<img src="./assets/whoami-card.svg" width="100%" alt="Retrato em ASCII ao lado de um card no estilo neofetch: sistema, cargo, IDE, linguagens, hobbies e contato" />

Construo e testo serviços de backend — APIs REST, autenticação, pagamentos e
agendamento — com foco em design SOLID e cobertura de testes de verdade. No dia
a dia isso significa PHP 8.2 numa camada de Services com PHPUnit, modelagem de
dados relacional e integrações com Mercado Pago, Brevo e Notion, entregues com
Docker e GitHub Actions.

<br>

## Projetos

<table>
<tr>
<td>

<img align="right" src="https://img.shields.io/badge/NO%20AR-39d353?style=flat-square" alt="No ar" />

### Finanças — App de finanças pessoais (PWA)

<sub><code>projeto pessoal · da ideia à produção</code></sub>

Um projeto pessoal que criei para substituir a planilha que eu usava no meu
próprio orçamento. Hoje é um app web em produção, que pode ser instalado no
celular e funciona offline. Fiz de ponta a ponta: requisitos, arquitetura,
interface, testes automatizados, CI/CD e documentação.

<a href="https://financas-demo.web.app/"><img src="https://img.shields.io/badge/Ver%20demo-financas--demo.web.app-2ea043?style=for-the-badge&logo=firebase&logoColor=white" alt="Ver demo: financas-demo.web.app" /></a>
<sub>&nbsp;dados fictícios, sem login — melhor no celular</sub>

<p align="center">
<a href="https://financas-demo.web.app/"><img src="./assets/financas/inicio.webp" width="23%" alt="Tela inicial: saldo projetado, entradas, saídas e o orçamento da semana" /></a>
<a href="https://financas-demo.web.app/"><img src="./assets/financas/cartoes.webp" width="23%" alt="Cartões: fatura calculada a partir das compras, com os últimos itens" /></a>
<a href="https://financas-demo.web.app/"><img src="./assets/financas/conta-corrente.webp" width="23%" alt="Conta corrente: previsão do saldo dia a dia e quanto dá para gastar por dia" /></a>
<a href="https://financas-demo.web.app/"><img src="./assets/financas/guardar.webp" width="23%" alt="Guardar: objetivos numa linha do tempo e quanto dá para guardar sem apertar a conta" /></a>
<br>
<sub>Início · Cartões · Conta corrente · Guardar — toque numa tela para abrir a demo</sub>
</p>

- **Produto** — lançar um gasto em segundos, faturas de cartão e parcelamentos, previsão do caixa para 12 meses e um simulador *"Posso gastar?"* que responde perguntas em linguagem natural
- **Arquitetura** — código TypeScript em camadas com fronteiras verificadas no CI, regras de negócio em funções puras e testáveis, valores em centavos inteiros para evitar erros de arredondamento
- **Segurança e custo** — sem servidor próprio, no plano gratuito do Firebase, com controle de acesso nas regras de segurança do Firestore cobertas por testes automatizados
- **Prática de engenharia** — testes de unidade, de interface e das regras de segurança com Vitest; deploy de preview para cada pull request e deploy automático em produção; mais de 80 registros de decisões de arquitetura

![React](https://img.shields.io/badge/React%2019-61DAFB?style=flat-square&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Firebase](https://img.shields.io/badge/Firestore-FFCA28?style=flat-square&logo=firebase&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%204-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=flat-square&logo=vitest&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-5A0FC8?style=flat-square&logo=pwa&logoColor=white)

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top">

#### ClinicaAme

<sub><code>sistema de gestão de clínica</code></sub>

Backend de gestão de clínica: autenticação, módulo financeiro e agendamento de
consultas sobre um modelo de dados bastante relacional. Construído numa camada
de Services com princípios SOLID e uma suíte PHPUnit passando.

![PHP](https://img.shields.io/badge/PHP%208.2-777BB4?style=flat-square&logo=php&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![PHPUnit](https://img.shields.io/badge/PHPUnit%2011-FF6B6B?style=flat-square&logo=phpunit)

<a href="https://github.com/lucasschn1/sistema-de-agendamento"><img src="https://img.shields.io/badge/Ver%20c%C3%B3digo-24292F?style=for-the-badge&logo=github&logoColor=white" alt="Ver código" /></a>

</td>
<td width="50%" valign="top">

#### Previsão de ruído aerodinâmico (NASA)

<sub><code>machine learning · regressão</code></sub>

Random Forest dentro de um `Pipeline` do scikit-learn (sem vazamento entre
treino e teste), ajustado com `GridSearchCV` e validação cruzada sobre o
dataset de aerofólios da NASA — **MAE 1,33 dB, RMSE 1,84 dB**.

![Python](https://img.shields.io/badge/Python%203-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

<a href="https://github.com/lucasschn1/previsao-ruido-aerodinamico-nasa"><img src="https://img.shields.io/badge/Ver%20c%C3%B3digo-24292F?style=for-the-badge&logo=github&logoColor=white" alt="Ver código" /></a>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### Biblioteca Virtual Inteligente

<sub><code>estruturas de dados · algoritmos</code></sub>

Projeto de estudo de estruturas de dados: árvore binária de busca com percursos
DFS/BFS, pilha para o histórico, fila para as reservas e um grafo ponderado com
Dijkstra gerando recomendações de livros.

![Java](https://img.shields.io/badge/Java-007396?style=flat-square&logo=openjdk&logoColor=white)
![Estruturas de dados](https://img.shields.io/badge/Estruturas%20de%20dados-4A90E2?style=flat-square)
![Algoritmos](https://img.shields.io/badge/Algoritmos-7ED321?style=flat-square)

<a href="https://github.com/lucasschn1/Sistema-Biblioteca"><img src="https://img.shields.io/badge/Ver%20c%C3%B3digo-24292F?style=for-the-badge&logo=github&logoColor=white" alt="Ver código" /></a>

</td>
<td width="50%" valign="top">

#### Perfil do GitHub automatizado

<sub><code>esta página · automação</code></sub>

Uma GitHub Action agendada roda Python todo dia para gerar, como SVG, o retrato
em ASCII, o card no estilo neofetch, o card de stack e o mapa de calor de
contribuições — cada um se adapta sozinho aos temas claro e escuro do GitHub.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

<a href="https://github.com/lucasschn1/lucasschn1"><img src="https://img.shields.io/badge/Ver%20c%C3%B3digo-24292F?style=for-the-badge&logo=github&logoColor=white" alt="Ver código" /></a>

</td>
</tr>
</table>

<br>

## Tecnologias

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/tech-card-dark.svg" />
  <img src="./assets/tech-card-light.svg" alt="Stack. Backend e dados: PHP 8.2, Java, PHPUnit, MySQL, PostgreSQL, Firebase. Ciência de dados: Python, scikit-learn, pandas. Frontend: React, TypeScript, JavaScript, Tailwind CSS. Ferramentas: Docker, Git, GitHub Actions." />
</picture>

<br>

## Contato

Aberto a vagas de Backend e Full Stack — e-mail é o jeito mais rápido de falar comigo.  
<sub>Moro em São José dos Pinhais, Paraná.</sub>

<a href="mailto:lcordeiro183@gmail.com"><img src="https://img.shields.io/badge/Vamos%20conversar-lcordeiro183%40gmail.com-2ea043?style=for-the-badge&logo=gmail&logoColor=white&labelColor=1a7f37" alt="Vamos conversar: lcordeiro183@gmail.com" /></a>
<a href="https://linkedin.com/in/lucas-schneider-c"><img src="https://img.shields.io/badge/Curr%C3%ADculo-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Currículo no LinkedIn" /></a>

---

<div align="center">
<sub>Obrigado pela visita.</sub>
</div>
