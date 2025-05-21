from transformacao.transformacao_silver import TransformacaoSilver
from pyspark.sql import DataFrame
from pyspark.sql.functions import to_date, col

class TransSilverDadostesouroipca(TransformacaoSilver):
    def rename_columns(self, df: DataFrame) -> DataFrame:
        return df.withColumnRenamed("CompraManha", "compra") \
                 .withColumnRenamed("VendaManha", "venda") \
                 .withColumnRenamed("PUCompraManha", "pu_compra") \
                 .withColumnRenamed("PUVendaManha", "pu_venda") \
                 .withColumnRenamed("PUBaseManha", "pu_base") \
                 .withColumnRenamed("Tipo", "tipo") \
                 .withColumnRenamed("Data_Vencimento", "data_vencimento") \
                 .withColumnRenamed("Data_Base", "data_base") \
                 .withColumn("data_vencimento", to_date(col("data_vencimento"))) \
                 .withColumn("data_base", to_date(col("data_base")))
