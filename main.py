from transformacao.trans_silver_dadostesouroipca import TransSilverDadostesouroipca
from transformacao.trans_silver_dadostesouropre import TransSilverDadostesouropre
from enriquecimento.dim_tempo import DimTempo
from enriquecimento.dim_tipo import DimTipo
from enriquecimento.fato_dadostesouro_base import FatoDadosTesouroBase
from enriquecimento.fato_dadostesouro_venc import FatoDadosTesouroVenc

def DadosTesouroIpca():
    etl = TransSilverDadostesouroipca(app_name="ETL Tesouro IPCA")
    df = etl.postgres_read_table("dadostesouroipca") #Lê os dados, remove duplicidades e trata nulos
    df_renomeado = etl.rename_columns(df)
    etl.save_to_postgres(df_renomeado, "silver.dadostesouroipca")

def DadosTesouroPre():
    etl = TransSilverDadostesouropre(app_name="ETL Tesouro PRE")
    df = etl.postgres_read_table("dadostesouropre") #Lê os dados, remove duplicidades e trata nulos
    df_renomeado = etl.rename_columns(df)
    etl.save_to_postgres(df_renomeado, "silver.dadostesouropre")


def main():
    #silver:
    DadosTesouroIpca()
    DadosTesouroPre()

    #gold:
    DimTempo("2000-01-01", "2055-01-01").load_dim_tempo()
    DimTipo().load_dim_tipo()
    FatoDadosTesouroBase().load_fato_tesouro_base()
    FatoDadosTesouroVenc().load_fato_tesouro_venc()

if __name__ == "__main__":
    main()
