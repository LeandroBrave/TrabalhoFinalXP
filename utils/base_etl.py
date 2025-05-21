# utils/base_etl.py
import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

class BaseETL:
    def __init__(self, app_name: str = None, use_spark=True):
        load_dotenv()

        if use_spark and app_name:
            self.spark = self._iniciar_spark_session(app_name)
            self.spark.sparkContext.setLogLevel("ERROR")

        self.pg_url = os.getenv("PG_URL")
        self.pg_dbname = os.getenv("PG_DB")
        self.pg_user = os.getenv("PG_USER")
        self.pg_password = os.getenv("PG_PASSWORD")
        self.pg_host = os.getenv("PG_HOST", "localhost")
        self.pg_port = os.getenv("PG_PORT", "5432")
        self.pg_driver = os.getenv("PG_DRIVER", "org.postgresql.Driver")

        self.pg_properties = {
            "user": self.pg_user,
            "password": self.pg_password,
            "driver": self.pg_driver
        }

    def _iniciar_spark_session(self, app_name: str) -> SparkSession:
        return SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.2.18") \
            .getOrCreate()
