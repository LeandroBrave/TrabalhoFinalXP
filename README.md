# TrabalhoFinalXP# 📊 Kafka Pipeline - Tesouro IPCA e Tesouro PRE

Este repositório contém um pipeline de dados em tempo real que extrai dados do Tesouro IPCA e Tesouro PRE de um banco PostgreSQL, envia para o Apache Kafka e distribui para destinos configuráveis via Kafka Connect.

---

### 👤 Autor

**Leandro Valente** – [@LeandroBrave](https://github.com/LeandroBrave)


## ⚙️ Tecnologias Utilizadas

- **Apache Kafka** – Sistema de mensagens distribuídas.
- **Kafka Connect** – Framework para integração com sistemas externos.
- **PostgreSQL** – Banco de dados relacional utilizado como fonte e/ou destino.
- **Kafka JDBC Connector** – Conector para integração JDBC com PostgreSQL.
- **Docker e Docker Compose** – Containerização dos serviços.

---

## 🚀 Como Rodar o Projeto

### Passo 1: Clonar o repositório

Clone este repositório para sua máquina local

### Passo 2: Conta AWS

Crie uma conta amazon se não tiver uma
Crie um usuario através do AWS IAM
Crie um arquivo no projeto nomeado: .env_kafka_connect
Escreva no .env_kafka_connect o conteudo abaixo:
    
    AWS_ACCESS_KEY_ID=[PREENCHA COM O VALOR DO SEU USUARIO AWS]
    AWS_SECRET_ACCESS_KEY=[PREENCHA COM O VALOR DO SEU USUARIO AWS]

### Passo 3: Docker
Suba todos os serviços contidos no arquivo docker-compose:

**comando:** docker-compose up

### Passo 4: Setup Postgres

**crie um arquivo .env com o conteudo abaixo:**

    PG_URL=jdbc:postgresql://localhost:5432/postgres
    PG_USER=postgres
    PG_PASSWORD=postgres
    PG_DB=postgres
    PG_HOST=localhost
    PG_PORT=5432
    PG_DRIVER=org.postgresql.Driver
