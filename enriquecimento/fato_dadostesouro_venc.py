from pyspark.sql.functions import date_format, sum as _sum, max as _max
from utils.base_etl import BaseETL

class FatoDadosTesouroVenc(BaseETL):
    def __init__(self, app_name="ETL Fato Dados Tesouro Venc"):
        super().__init__(app_name=app_name)

    def load_fato_tesouro_venc(self):
        query_ipca = """
            SELECT 
              d.data_vencimento,
              t.id_tipo,
              d.compra,
              d.venda,
              d.pu_compra,
              d.pu_venda,
              d.pu_base,
              d.dt_update
            FROM silver.dadostesouroipca d
            JOIN gold.dim_tipo t ON LOWER(t.tipo) = 'ipca'
        """

        query_pre = """
            SELECT 
              d.data_vencimento,
              t.id_tipo,
              d.compra,
              d.venda,
              d.pu_compra,
              d.pu_venda,
              d.pu_base,
              d.dt_update
            FROM silver.dadostesouropre d
            JOIN gold.dim_tipo t ON LOWER(t.tipo) = 'pre-fixados'
        """

        df_ipca = self.spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{self.pg_host}:{self.pg_port}/{self.pg_dbname}") \
            .option("dbtable", f"({query_ipca}) as ipca") \
            .option("user", self.pg_user) \
            .option("password", self.pg_password) \
            .option("driver", "org.postgresql.Driver") \
            .load()

        df_pre = self.spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{self.pg_host}:{self.pg_port}/{self.pg_dbname}") \
            .option("dbtable", f"({query_pre}) as pre") \
            .option("user", self.pg_user) \
            .option("password", self.pg_password) \
            .option("driver", "org.postgresql.Driver") \
            .load()

        df = df_ipca.unionByName(df_pre)

        # Criar coluna ano_mes de data de vencimento
        df = df.withColumn("data_vencimento_ano_mes", date_format("data_vencimento", "yyyyMM"))

        # Agregação
        df_agg = df.groupBy("data_vencimento_ano_mes", "id_tipo").agg(
            _sum("compra").alias("compra"),
            _sum("venda").alias("venda"),
            _sum("pu_compra").alias("pu_compra"),
            _sum("pu_venda").alias("pu_venda"),
            _sum("pu_base").alias("pu_base"),
            _max("dt_update").alias("dt_update")
        )

        # Escrita no Postgres
        df_agg.write \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{self.pg_host}:{self.pg_port}/{self.pg_dbname}") \
            .option("dbtable", "gold.fato_dadostesouro_venc") \
            .option("user", self.pg_user) \
            .option("password", self.pg_password) \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
