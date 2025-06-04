API Vitivinicultura Embrapa

Este repositório contém a implementação de uma API REST em Python (Flask) para consulta aos dados de vitivinicultura da Embrapa, protegida por JWT e documentada via Swagger. Além disso, inclui o plano arquitetural (diagrama) que mostra como esses dados podem ser consumidos por futuras aplicações ou dashboards.

Índice

Arquitetura do Projeto

Pré-requisitos

Configuração do ambiente local

Variáveis de ambiente

Execução da API Flask

5.1. Instalar dependências

5.2. Executar localmente

5.3. Autenticação (JWT)

5.4. Swagger UI

Plano de Arquitetura e Deploy

6.1. Descrição de componentes (resumo)

6.2. Cenário de Uso / Dashboard

6.3. Deploy em Heroku (etapas rápidas)

6.4. Link Compartilhável da API

Estrutura do projeto

Arquitetura do Projeto

A seguir, diagrama ilustra o fluxo completo desde a obtenção dos dados até o cenário de uso final:



Descrição de cada bloco:

Fontes da Embrapa (CSV)

As abas “Produção”, “Processamento”, “Comercialização”, “Importação” e “Exportação” disponibilizam arquivos CSV.

Esses arquivos podem ser baixados manualmente ou via script agendado, servindo como dados de entrada.

API Flask

Expõe endpoints REST para cada aba:

GET /producao

GET /processamento

GET /comercializacao

GET /importacao

GET /exportacao

POST /login (emissão de JWT)

Cada rota faz, sob demanda, o download do CSV correspondente, processa-o e retorna JSON no formato longo (colunas: categoria, ano, valor).

O Swagger UI (Flasgger) documenta todos os endpoints, permitindo testes diretos e a geração de tokens via JWT.

Banco de Dados PostgreSQL (opcional)

Caso seja necessário armazenar histórico, pode-se criar tabelas:

producao (categoria TEXT, ano INT, valor NUMERIC)

processamento (categoria TEXT, ano INT, valor NUMERIC)

comercializacao (categoria TEXT, ano INT, valor NUMERIC)

importacao (categoria TEXT, ano INT, valor NUMERIC)

exportacao (categoria TEXT, ano INT, valor NUMERIC)

Esses dados podem ser consumidos por notebooks ou dashboards de análise.

Cenário de Uso / Dashboard

Um dashboard (por exemplo, em React ou Streamlit) pode consumir diretamente a API ou, se armazenados no banco, ler do PostgreSQL para:

Exibir séries históricas de produção, processamento, comercialização, importação e exportação por categoria/ano.

Fornecer filtros interativos (faixa de anos, seleção de categorias, etc.).

Mostrar indicadores como média móvel, variação percentual ano a ano e prever tendências básicas.

1. Pré-requisitos

Python 3.13+ instalado

pip (>=21)

(Opcional) PostgreSQL local ou serviço em nuvem, caso deseje armazenar dados

(Opcional) Heroku CLI para deploy

2. Configuração do ambiente local

Clone este repositório:

git clone https://github.com/seu_usuario/tech-challenger-vitivinicultura.git
cd tech-challenger-vitivinicultura

Crie e ative um ambiente virtual:

Linux/Mac:

python3 -m venv venv
source venv/bin/activate

Windows (PowerShell):

python -m venv venv
venv\Scripts\Activate.ps1

Instale as dependências:

pip install --upgrade pip
pip install -r requirements.txt

3. Variáveis de ambiente

Defina no terminal (antes de rodar a API) a chave para JWT:

Linux/Mac:

export JWT_SECRET_KEY="uma_chave_super_secreta"

Windows (PowerShell):

$env:JWT_SECRET_KEY = "uma_chave_super_secreta"

4. Execução da API Flask

4.1. Instalar dependências específicas

Se for usar somente a API:

pip install flask flasgger flask_jwt_extended requests pandas beautifulsoup4

4.2. Executar localmente

Certifique-se de que JWT_SECRET_KEY está definido no ambiente.

Inicie o servidor:

python app.py

A API estará disponível em:

http://127.0.0.1:5000

4.3. Autenticação (JWT)

POST /login: recebe JSON com { "username": "admin", "password": "senha123" } e retorna { "access_token": "..." }.

Use o token retornado como Bearer <token> no header Authorization para acessar as rotas protegidas.

4.4. Swagger UI

Acesse:

http://127.0.0.1:5000/documentacao

No Swagger, clique em Authorize, cole Bearer <seu_token> e autorize.

Teste os endpoints GET /producao, GET /processamento, etc.

5. Plano de Arquitetura e Deploy

5.1. Descrição de componentes (resumo)

Fontes da Embrapa (CSV)

API Flask (endpoints REST + JWT + Swagger)

Banco de Dados PostgreSQL (Não implementado)

Cenário de Uso / Dashboard

5.2. Cenário de Uso / Dashboard

"Dashboard de Monitoramento Sazonal": consome dados da API para exibir séries históricas e previsões básicas.

5.3. Deploy em Heroku (etapas rápidas)

heroku login

heroku create nome-do-app-vitibrasil

git push heroku main (ou master)

Defina JWT_SECRET_KEY no Dashboard Heroku → Settings → Config Vars

Adicione Heroku Postgres e, se desejar, armazene dados

Acesse:

https://nome-do-app-vitibrasil.herokuapp.com

e a documentação em:

https://nome-do-app-vitibrasil.herokuapp.com/documentacao

5.4. Link Compartilhável da API

Página inicial: https://nome-do-app-vitibrasil.herokuapp.com/

Swagger UI: https://nome-do-app-vitibrasil.herokuapp.com/documentacao

Endpoints: GET https://nome-do-app-vitibrasil.herokuapp.com/producao (envie o header Authorization: Bearer <token>)

6. Estrutura do projeto

/                             # raiz do repositório
├─ app.py                     # aplicação Flask + Swagger + JWT
├─ scraper.py                 # script para encontrar e processar CSVs da Embrapa
├─ requirements.txt           # lista de dependências
├─ Procfile (para Heroku)     # "web: python app.py"
├─ runtime.txt (opcional)     # para especificar versão do Python no Heroku
├─ Arquitetura.jpg            # diagrama geral do fluxo de dados
└─ README.md                  # este arquivo de instruções

Fim do README

