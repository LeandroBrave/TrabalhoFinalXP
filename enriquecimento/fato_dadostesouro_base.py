import pandas as pd
from sqlalchemy import create_engine
from utils.base_etl import BaseETL  

class FatoDadosTesouroBase(BaseETL):
    def __init__(self, app_name="ETL Fato Dados Tesouro Base"):
        super().__init__(app_name=app_name)
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_dbname}"
        )

    def load_fato_tesouro_base(self):
        query_ipca = """
            SELECT 
              d.data_base,
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
              d.data_base,
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

        df_ipca = pd.read_sql(query_ipca, self.engine)
        df_pre = pd.read_sql(query_pre, self.engine)
        df = pd.concat([df_ipca, df_pre], ignore_index=True)

        # Criar campo ano_mes de data de base
        df["data_base_ano_mes"] = pd.to_datetime(df["data_base"]).dt.strftime("%Y%m")

        # Agregação por base
        df_agg = df.groupby(["data_base_ano_mes", "id_tipo"], as_index=False).agg({
            "compra": "sum",
            "venda": "sum",
            "pu_compra": "sum",
            "pu_venda": "sum",
            "pu_base": "sum",
            "dt_update": "max"
        })

        # Carrega na nova fato
        df_agg.to_sql("fato_dadostesouro_base", self.engine, schema="gold", if_exists="append", index=False)
