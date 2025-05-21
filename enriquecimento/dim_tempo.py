import pandas as pd
import holidays
from sqlalchemy import create_engine
from dotenv import load_dotenv
from utils.base_etl import BaseETL

class DimTempo(BaseETL):
    def __init__(self, dt_inicial: str, dt_final: str):
        super().__init__(use_spark=False)
        self.dt_inicial = dt_inicial
        self.dt_final = dt_final

    def load_dim_tempo(self):
        # Criar intervalo de datas
        date_range = pd.date_range(self.dt_inicial, self.dt_final, freq='D')

        # Montar DataFrame
        df_time = pd.DataFrame({'data': date_range})
        df_time['ano'] = df_time['data'].dt.year
        df_time['mes'] = df_time['data'].dt.month
        df_time['nome_mes'] = df_time['data'].dt.strftime('%B')
        df_time['dia'] = df_time['data'].dt.day
        df_time['dia_da_semana'] = df_time['data'].dt.dayofweek + 1
        df_time['nome_dia_semana'] = df_time['data'].dt.strftime('%A')
        df_time['semana_do_ano'] = df_time['data'].dt.isocalendar().week
        df_time['trimestre'] = df_time['data'].dt.quarter
        df_time['eh_fim_de_semana'] = df_time['data'].dt.weekday >= 5
        df_time['ano_mes'] = df_time['data'].dt.strftime('%Y%m')
        #df_time['id_data'] = df_time['data'].dt.strftime('%Y%m%d').astype(int)

        df_time['data'] = df_time['data'].dt.date
        
        # Feriados
        br_holidays = holidays.Brazil()
        df_time['eh_feriado'] = df_time['data'].isin(br_holidays)

        # Criar engine SQLAlchemy com as credenciais da BaseETL
        engine = create_engine(
            f"postgresql+psycopg2://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_dbname}"
        )
        conn = engine.raw_connection()
        cursor = conn.cursor()

        # Apagar apenas o range que será inserido
        cursor.execute("""
            DELETE FROM gold.dim_tempo
            WHERE data BETWEEN %s AND %s
        """, (self.dt_inicial, self.dt_final))
        conn.commit()

        # Inserir novos dados
        df_time.to_sql("dim_tempo", engine, schema="gold", if_exists="append", index=False)

        # Fechar conexões
        cursor.close()
        conn.close()
