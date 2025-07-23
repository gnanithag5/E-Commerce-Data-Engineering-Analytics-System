import logging
from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.feature import VectorAssembler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("predict.log"),
        logging.StreamHandler()
    ]
)

def predict_total_amount(year, month, product_price, quantity):
    try:
        spark = SparkSession.builder.appName("SalesPredictor").getOrCreate()
        logging.info("Spark session started.")

        model = LinearRegressionModel.load("sales_projection_model")
        logging.info("Model loaded from 'sales_projection_model'.")

        data = [[year, month, product_price, quantity]]
        columns = ["year", "month", "product_price", "quantity"]
        df = spark.createDataFrame(data, columns)

        assembler = VectorAssembler(inputCols=columns, outputCol="features")
        transformed_df = assembler.transform(df).select("features")

        prediction = model.transform(transformed_df)
        result = prediction.select("prediction").collect()[0][0]
        logging.info(f"Predicted total amount: {result:.2f}")
        return result

    except Exception as e:
        logging.exception("Prediction failed.")
        return None

    finally:
        spark.stop()
        logging.info("Spark session stopped.")

# Run directly
if __name__ == "__main__":
    predict_total_amount(2025, 7, 249.99, 3)
