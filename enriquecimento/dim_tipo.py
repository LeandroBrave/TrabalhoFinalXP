from pyspark.sql.functions import col
from utils.base_etl import BaseETL
from sqlalchemy import create_engine
from psycopg2.extras import execute_batch

class DimTipo(BaseETL):
    def __init__(self):
        super().__init__("ETL Dim Tipo")

    def load_dim_tipo(self):

        url = f"postgresql+psycopg2://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_dbname}"
        engine = create_engine(url, connect_args={"user": self.pg_user, "password": self.pg_password})

        # Lê as tabelas da camada silver com Spark
        df_ipca = self.spark.read.jdbc(
            url=self.pg_url,
            table="silver.dadostesouroipca",
            properties=self.pg_properties
        ).select("tipo").distinct()

        df_pre = self.spark.read.jdbc(
            url=self.pg_url,
            table="silver.dadostesouropre",
            properties=self.pg_properties
        ).select("tipo").distinct()

        # Une os dados e remove duplicatas
        df_tipos = df_ipca.union(df_pre).distinct().filter(col("tipo").isNotNull())

        # Converte para Pandas (para usar psycopg2)
        df_tipos_pd = df_tipos.toPandas()

        # Defina a query de upsert (supondo que a coluna 'tipo' é única, e 'id_tipo' é serial)
        upsert_query = """
        INSERT INTO gold.dim_tipo (tipo)
        VALUES (%s)
        ON CONFLICT (tipo) DO NOTHING
        """

        conn = engine.raw_connection()
        cursor = conn.cursor()

        # Prepara os dados para o execute_batch
        data_to_insert = [(row['tipo'],) for _, row in df_tipos_pd.iterrows()]

        # Executa o batch de upsert
        execute_batch(cursor, upsert_query, data_to_insert)

        conn.commit()
        cursor.close()
        conn.close()
