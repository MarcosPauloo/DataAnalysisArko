# Desafio Arko - Plataforma de Análise de Dados

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-20.10-2496ED?style=for-the-badge&logo=docker)

## 📖 Descrição do Projeto

Esta é uma aplicação web desenvolvida em Django que consome, processa e armazena dados públicos do IBGE (via API) e da Receita Federal (via arquivo CSV de grande volume). A aplicação oferece uma interface web para visualização, filtragem e paginação dos dados importados, além de um sistema de autenticação para proteger o acesso às informações.

O projeto foi totalmente containerizado com Docker para garantir um ambiente de desenvolvimento e execução 100% reprodutível.

## ✨ Funcionalidades

* **Importação de Dados do IBGE:** Um comando customizado que consome a API de localidades do IBGE e popula o banco de dados com todos os estados, municípios e distritos do Brasil.
* **Importação de Dados da Receita Federal:** Um serviço robusto e otimizado para processar arquivos CSV de grande volume (milhões de registros) de forma eficiente, utilizando `pandas` para leitura em lotes (`chunks`) e `bulk_create` do Django para inserção de dados performática.
* **Interface Web:** Páginas para listar estados, municípios, distritos e empresas, com funcionalidades de **filtragem** e **paginação**.
* **Autenticação de Usuários:** Sistema de login seguro para proteger o acesso aos dados. Acesso não autenticado é redirecionado para a tela de login.
* **Ambiente Dockerizado:** Todo o projeto (aplicação Django + banco de dados PostgreSQL) é gerenciado pelo Docker Compose, simplificando a configuração e execução.
* **Boas Práticas:** O projeto foi desenvolvido seguindo as melhores práticas do mercado, incluindo:
    * Separação de responsabilidades (services, schemas de validação com Pydantic).
    * Segurança (uso de variáveis de ambiente com `.env`).
    * Qualidade de código (testes automatizados e logging).

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.11, Django
* **Banco de Dados:** PostgreSQL
* **Containerização:** Docker, Docker Compose
* **Bibliotecas Principais:**
    * `django-filter`: Para filtragem de dados.
    * `pandas`: Para processamento do CSV.
    * `pydantic`: Para validação de dados da API.
    * `psycopg2-binary`: Driver de conexão com o PostgreSQL.
    * `django-environ`: Para gerenciamento de variáveis de ambiente.
    * `uv`: Gerenciador de pacotes e ambiente virtual.

## ⚙️ Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas na sua máquina:
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/) (geralmente já vem com o Docker Desktop)

## 🚀 Como Executar o Projeto

Siga estes passos para configurar e rodar a aplicação localmente.

### 1. Clonar o Repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd <NOME_DA_PASTA_DO_PROJETO>
```

### 2. Configurar Variáveis de Ambiente
O projeto utiliza um arquivo `.env` para configurar as credenciais do banco de dados e a `SECRET_KEY` do Django.

**a.** Crie uma cópia do arquivo de exemplo:
```bash
cp .env.example .env
```

**b.** O arquivo `.env` já virá preenchido com valores padrão para o ambiente Docker. Não é necessário alterá-lo para rodar o projeto.

### 3. Baixar o Arquivo de Dados das Empresas
A importação de empresas depende de um arquivo ZIP da Receita Federal.

**a.** Crie uma pasta `data` na raiz do projeto:
```bash
mkdir data
```

**b.** Baixe o arquivo `Empresas0.zip` do link abaixo e **salve-o dentro da pasta `data`**:
* **Link:** [https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-05](https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-05)
* **Arquivo a baixar:** `Empresas0.zip`

### 4. Construir e Iniciar os Contêineres
Este comando irá construir a imagem do seu aplicativo Django, baixar a imagem do PostgreSQL e iniciar os dois serviços em segundo plano.

```bash
docker-compose up --build -d
```

### 5. Configurar o Banco de Dados
Com os contêineres no ar, execute as migrações para criar as tabelas no banco de dados.

```bash
docker-compose exec web python manage.py migrate
```

### 6. Popular o Banco de Dados
Execute os comandos customizados para importar os dados para o banco.

**a. Importar dados do IBGE (estados, municípios, distritos):**
```bash
docker-compose exec web python manage.py populate_ibge
```

**b. Importar dados das Empresas (Receita Federal):**
**Aviso:** Este processo é demorado e pode levar vários minutos, dependendo da sua máquina.
```bash
docker-compose exec web python manage.py populate_companies /app/data/Empresas0.zip
```

## 🌐 Usando a Aplicação

### 1. Criar um Usuário
Para acessar as páginas protegidas, você precisa de um usuário. Crie um superusuário com o comando abaixo e siga as instruções no terminal.

```bash
docker-compose exec web python manage.py createsuperuser
```

### 2. Acessar a Aplicação Web
* Abra seu navegador e acesse: **`http://localhost:8000/`**
* Você será redirecionado para a página de login. Use as credenciais do superusuário que você acabou de criar.
* Após o login, você será redirecionado para a página principal da aplicação, onde poderá navegar pelas listagens.

### 3. Acessar o Admin do Django
* Acesse: **`http://localhost:8000/admin/`**
* Use as mesmas credenciais do superusuário para acessar a interface de administração do Django.

---
Desenvolvido com 💙 por [Seu Nome]