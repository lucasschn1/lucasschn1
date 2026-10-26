<div align="center">

<sub><b>English</b> · <a href="https://github.com/lucasschn1/lucasschn1/blob/main/README.pt-BR.md">Português</a></sub>

# Lucas Schneider C.

**Full Stack Developer**

I build tested APIs and the apps that use them · PHP · TypeScript · React

<img src="https://img.shields.io/badge/%E2%97%8F%20available%20now-2ea043?style=for-the-badge" alt="Available now" />
<img src="https://img.shields.io/badge/open%20to-Backend%20%2F%20Full%20Stack%20roles-30363d?style=for-the-badge&labelColor=161b22" alt="Open to Backend / Full Stack roles" />
<img src="https://img.shields.io/badge/work%20mode-remote%20%C2%B7%20hybrid%2Fon--site%20in%20Curitiba%2C%20PR-30363d?style=for-the-badge&labelColor=161b22" alt="Work mode: remote, or hybrid/on-site in Curitiba, PR" />

[About me](#about-me) · [Projects](#projects) · [Tech stack](#tech-stack) · [Contact](#contact)

</div>

---

## Contributions

<img src="./assets/contrib-heatmap.svg" width="100%" alt="Contribution heatmap for the last year" />

<br>

## About me

<img src="./assets/whoami-card.svg" width="100%" alt="ASCII portrait next to a neofetch-style card: OS, role, IDE, languages, hobbies and contact" />

I build and test backend services — REST APIs, authentication, payments and
scheduling — with an emphasis on SOLID design and real test coverage. Day to
day that means PHP 8.2 on a Services layer with PHPUnit, relational data
modeling, and integrations with Mercado Pago, Brevo and Notion, shipped with
Docker and GitHub Actions.

<br>

## Projects

<table>
<tr>
<td>

<img align="right" src="https://img.shields.io/badge/LIVE-39d353?style=flat-square" alt="Live" />

### Finanças — Personal Finance PWA

<sub><code>personal project · from idea to production</code></sub>

A personal project I built to replace the spreadsheet I used for my own budget.
It is now a production web app, installable on the phone and usable offline. I
took it end to end: requirements, architecture, UI, automated tests, CI/CD and
documentation.

<a href="https://financas-demo.web.app/"><img src="https://img.shields.io/badge/Live%20demo-financas--demo.web.app-2ea043?style=for-the-badge&logo=firebase&logoColor=white" alt="Live demo: financas-demo.web.app" /></a>
<sub>&nbsp;fictional data, no login — works best on a phone</sub>

<p align="center">
<a href="https://financas-demo.web.app/"><img src="./assets/financas/inicio.webp" width="23%" alt="Home screen: projected balance, income, spending and this week's budget" /></a>
<a href="https://financas-demo.web.app/"><img src="./assets/financas/cartoes.webp" width="23%" alt="Credit cards: the bill computed from purchases, with the latest items" /></a>
<a href="https://financas-demo.web.app/"><img src="./assets/financas/conta-corrente.webp" width="23%" alt="Checking account: day-by-day balance forecast and how much can be spent per day" /></a>
<a href="https://financas-demo.web.app/"><img src="./assets/financas/guardar.webp" width="23%" alt="Savings: goals on a timeline and how much can be saved without straining the account" /></a>
<br>
<sub>Home · Credit cards · Cash-flow forecast · Savings goals — tap any screen to open the demo</sub>
</p>

- **Product** — log an expense in seconds, credit-card bills and installments, a 12-month cash-flow forecast and a *"Can I afford it?"* simulator that answers plain-language questions
- **Architecture** — layered TypeScript codebase with boundaries checked in CI, business logic in pure, testable functions, money stored as integer cents to avoid rounding errors
- **Security & cost** — serverless on Firebase's free tier, with access control in Firestore security rules covered by automated tests
- **Engineering practice** — unit, UI and security-rule tests with Vitest; a preview deploy for every pull request and automatic production deploys; 80+ architecture decision records

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

<sub><code>clinic management system</code></sub>

Clinic management backend: authentication, a financial module and appointment
scheduling over a fairly relational schema. Built on a Services layer with
SOLID principles and a green PHPUnit suite.

![PHP](https://img.shields.io/badge/PHP%208.2-777BB4?style=flat-square&logo=php&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![PHPUnit](https://img.shields.io/badge/PHPUnit%2011-FF6B6B?style=flat-square&logo=phpunit)

<a href="https://github.com/lucasschn1/sistema-de-agendamento"><img src="https://img.shields.io/badge/View%20code-24292F?style=for-the-badge&logo=github&logoColor=white" alt="View code" /></a>

</td>
<td width="50%" valign="top">

#### NASA Airfoil Self-Noise

<sub><code>machine learning · regression</code></sub>

Random Forest inside a scikit-learn `Pipeline` (no leakage across the
train/test split), tuned with `GridSearchCV` and cross-validation on the NASA
airfoil dataset — **MAE 1.33 dB, RMSE 1.84 dB**.

![Python](https://img.shields.io/badge/Python%203-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

<a href="https://github.com/lucasschn1/previsao-ruido-aerodinamico-nasa"><img src="https://img.shields.io/badge/View%20code-24292F?style=for-the-badge&logo=github&logoColor=white" alt="View code" /></a>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### Intelligent Virtual Library

<sub><code>data structures · algorithms</code></sub>

Study project on core data structures: a BST with DFS/BFS traversal, a stack
for history, a queue for reservations, and a weighted graph with Dijkstra
driving book recommendations.

![Java](https://img.shields.io/badge/Java-007396?style=flat-square&logo=openjdk&logoColor=white)
![Data Structures](https://img.shields.io/badge/Data%20Structures-4A90E2?style=flat-square)
![Algorithms](https://img.shields.io/badge/Algorithms-7ED321?style=flat-square)

<a href="https://github.com/lucasschn1/Sistema-Biblioteca"><img src="https://img.shields.io/badge/View%20code-24292F?style=for-the-badge&logo=github&logoColor=white" alt="View code" /></a>

</td>
<td width="50%" valign="top">

#### Automated GitHub Profile

<sub><code>this page · automation</code></sub>

A scheduled GitHub Action runs Python daily to render the ASCII portrait, the
neofetch-style card, the stack card and the contribution heatmap as SVGs — each
adapting on its own to GitHub's light and dark themes.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

<a href="https://github.com/lucasschn1/lucasschn1"><img src="https://img.shields.io/badge/View%20code-24292F?style=for-the-badge&logo=github&logoColor=white" alt="View code" /></a>

</td>
</tr>
</table>

<br>

## Tech stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/tech-card-dark.svg" />
  <img src="./assets/tech-card-light.svg" alt="Tech stack. Backend and data: PHP 8.2, Java, PHPUnit, MySQL, PostgreSQL, Firebase. Data science: Python, scikit-learn, pandas. Frontend: React, TypeScript, JavaScript, Tailwind CSS. Tooling: Docker, Git, GitHub Actions." />
</picture>

<br>

## Contact

Open to Backend and Full Stack roles — email is the fastest way to reach me.  
<sub>Based in São José dos Pinhais, Paraná, Brazil.</sub>

<a href="mailto:lcordeiro183@gmail.com"><img src="https://img.shields.io/badge/Let's%20talk-lcordeiro183%40gmail.com-2ea043?style=for-the-badge&logo=gmail&logoColor=white&labelColor=1a7f37" alt="Let's talk: lcordeiro183@gmail.com" /></a>
<a href="https://linkedin.com/in/lucas-schneider-c"><img src="https://img.shields.io/badge/Resume-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Resume on LinkedIn" /></a>

---

<div align="center">
<sub>Thanks for stopping by.</sub>
</div>
