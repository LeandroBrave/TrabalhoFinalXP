import psycopg2
from abc import ABC, abstractmethod
from pyspark.sql import DataFrame
from pyspark.sql.types import NumericType
from utils.base_etl import BaseETL


class TransformacaoSilver(BaseETL, ABC):
    def __init__(self, app_name: str = "ETL POstgres para Silver"):
        super().__init__(app_name)
    
    def postgres_read_table(self, table_name: str) -> DataFrame:
        df = self.spark.read.jdbc(
            url=self.pg_url,
            table=table_name,
            properties=self.pg_properties
        )

        df_limpo = self.clean_data(df)

        return df_limpo
    
    def clean_data(self, df: DataFrame) -> DataFrame:
        # Remove duplicatas
        df_no_duplicates = df.dropDuplicates()

        # Identifica colunas numéricas e não numéricas
        colunas_numericas = [f.name for f in df_no_duplicates.schema.fields if isinstance(f.dataType, NumericType)]
        colunas_nao_numericas = [f.name for f in df_no_duplicates.schema.fields if f.name not in colunas_numericas]

        # Preenche nulos em numéricas com zero
        df_tratado = df_no_duplicates.fillna({col: 0 for col in colunas_numericas})

        # Remove linhas com nulos em colunas não numéricas
        df_tratado = df_tratado.dropna(subset=colunas_nao_numericas)

        return df_tratado
    
    def save_to_postgres(self, df: DataFrame, table_name: str, mode: str = "append"):
        # Conectar ao Postgres para truncar a tabela
        conn = psycopg2.connect(
            host=self.pg_host,
            port=self.pg_port,
            dbname=self.pg_dbname,
            user=self.pg_user,
            password=self.pg_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(f'TRUNCATE TABLE {table_name};')
        finally:
            cursor.close()
            conn.close()

        # Escrever os dados no modo append (já que a tabela está vazia)
        df.write.jdbc(
            url=self.pg_url,
            table=table_name,
            mode=mode,
            properties=self.pg_properties
        )

        self.spark.stop()

    @abstractmethod
    def rename_columns(self, df: DataFrame) -> DataFrame:
        """Cada subclasse implementa seu renomear específico"""
        pass

