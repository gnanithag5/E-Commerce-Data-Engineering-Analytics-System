import os
import logging
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from config import POSTGRES_URL, POSTGRES_PROPERTIES, JDBC_JAR_PATH

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("model.log"),
        logging.StreamHandler()
    ]
)

def get_spark_session():
    return SparkSession.builder \
        .appName("DW_Sales_Analytics") \
        .config("spark.jars", JDBC_JAR_PATH) \
        .getOrCreate()

def load_table(spark, table_name):
    logging.info(f"Loading table: {table_name}")
    return spark.read.jdbc(POSTGRES_URL, table_name, properties=POSTGRES_PROPERTIES)

def prepare_features(fact_sales, dim_product, dim_date):
    logging.info("Joining fact and dimension tables...")
    joined = fact_sales.join(dim_product, "product_id") \
                       .join(dim_date, fact_sales.transaction_date == dim_date.transaction_date)

    return joined.select("year", "month", "product_price", "quantity", "total_amount")

def train_model(df):
    logging.info("Assembling features...")
    assembler = VectorAssembler(
        inputCols=["year", "month", "product_price", "quantity"],
        outputCol="features"
    )
    data = assembler.transform(df).select("features", "total_amount")
    train_data, test_data = data.randomSplit([0.8, 0.2])

    logging.info("Fitting linear regression model...")
    lr = LinearRegression(featuresCol="features", labelCol="total_amount")
    model = lr.fit(train_data)
    return model, test_data

def main():
    try:
        spark = get_spark_session()
        logging.info("Spark session started.")

        fact_sales = load_table(spark, "fact_sales")
        dim_product = load_table(spark, "dim_product")
        dim_date = load_table(spark, "dim_date")

        df = prepare_features(fact_sales, dim_product, dim_date)

        model, test_data = train_model(df)

        logging.info("Making predictions on test data...")
        predictions = model.transform(test_data)
        predictions.select("features", "total_amount", "prediction").show(10)

        model.save("sales_projection_model")
        logging.info("Model saved to 'sales_projection_model'")

    except Exception as e:
        logging.exception("Error occurred during model training.")

if __name__ == "__main__":
    main()
