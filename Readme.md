# API Vitivinicultura Embrapa

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

Plano de Arquitetura e Deploy
6.1. Descrição de Componentes (Resumo)
Fontes da Embrapa (CSV)
– Download manual ou via script agendado.

API Flask (REST + JWT + Swagger)
– Endpoints para cada aba,
– Documentação em Swagger.

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

