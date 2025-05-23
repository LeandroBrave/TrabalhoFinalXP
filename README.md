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

## 🚧 Melhorias Futuras

- Criar orquestração, provavelmente com airflow
- Fazer deploy automatico de arquivos de configuração quando novos consumidores ou produtores entrarem na pipeline
- suporte a mais plataformas alem do posgres e s3


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

    Acesse o S3 e crie 2 buckets com a seguinte estrutura de pastas:
    Buckets:
        dados-pre
        dados-ipca
    Em cada bucket crie a estrutura de pastas:
        raw_data/kafka

### Passo 3: Docker
    Crie a imagem kafka:
    **Comando:**

        cd connect/custom-kafka-connectors-image
        docker buildx build . -t connect-custom:1.0.0

    Suba todos os serviços contidos no arquivo docker-compose:

    **Comando:** docker-compose up

### Passo 4: Setup Postgres

**crie um arquivo .env com o conteudo abaixo:**

    PG_URL=jdbc:postgresql://localhost:5432/postgres
    PG_USER=postgres
    PG_PASSWORD=postgres
    PG_DB=postgres
    PG_HOST=localhost
    PG_PORT=5432
    PG_DRIVER=org.postgresql.Driver

### Passo 5: Camada Bronze
    Execute o arquivo:
     Na pasta ingestao:
             importar.ipynb

### Passo 6: Camadas Silver e Gold
    Crie o schema Silver e o schema Gold no postgres
    Rode os respectivos arquivos SQL em cada schema
    Execute o codigo main.py

### Passo 7: Kafka
    Entre na maquina do broker que o docker subiu:
        **Comando:** docker exec -it broker bash
    
    Crie 2 topicos do kafka:
        **Comandos:** 
    
            kafka-topics --create --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --topic postgres-dadostesouroipca
            kafka-topics --create --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --topic postgres-dadostesouropre
    
    Cheque se os topicos foram criados:
        **Comando:** kafka-topics --bootstrap-server localhost:9092 --list
    
    Digite exit para voltar ao seu terminal local

### Passo 8: Criar os conectores Source
    Os conectores do tipo source são os produtores. Eles jogam dados dentro do topico kafka.
    Criaremos 2 deles:
    **Comandos:**

        curl -X POST -H "Content-Type: application/json" --data @connect_jdbc_postgres_ipca.config http://localhost:8083/connectors
        curl -X POST -H "Content-Type: application/json" --data @connect_jdbc_postgres_pre.config localhost:8083/connectors

     Retorne para a maquina do broker novamente
     **Comando:** 
         docker exec -it broker bash

    Execute o consumer para verificar a atividade do dado que é produzido
    **Comando:**

        kafka-console-consumer --bootstrap-server localhost:9092 --topic postgres-dadostesouroipca --from-beginning
        kafka-console-consumer --bootstrap-server localhost:9092 --topic postgres-dadostesouropre --from-beginning

### Passo 9: Criar os conectores sink
    Os conectores do tipo sink são os consumidores. Eles leem dados do topico kafka e escrevem em algum lugar.
    Criaremos 2 deles:
    **Comandos:**

        curl -X POST -H "Content-Type: application/json" --data @connect_s3_sink_ipca.config http://localhost:8083/connectors
        curl -X POST -H "Content-Type: application/json" --data @connect_s3_sink_pre.config http://localhost:8083/connectors

### Passo 10: Cheque seu AWS s3
    Após configuração do sink os dados confira se os dados chegaram nos buckets que foram criados no passo 2
