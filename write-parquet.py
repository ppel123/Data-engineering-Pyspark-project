"""
# Title : PySpark Script - Create Parquet
# Description : This script is used to read a CSV file, clean it and persist it to Parquet file
# Usage : spark-submit write-parquet.py
"""

# First import the neccesary modules
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DecimalType
import sys,logging
from datetime import datetime

# Logging configuration
formatter = logging.Formatter('[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Schema Configuration
# Here we define a schema for the CSV File read
# If a record is not compatible with the CSV, a null value is read

schema = StructType([
    StructField("trasaction_timestamp", TimestampType(), True),
    StructField("transaction_amount", DecimalType(4, 4), True),
    StructField("transaction_channel", StringType(), True)])

# current time variable to be used for logging purpose
dt_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

AppName = "Spark-Project"

def main():

    # Start spark code
    spark = SparkSession.builder.appName(AppName+"_"+str(dt_string)).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    logger.info("Starting spark application")

    # Read CSV File into a Spark Dataframe
    logger.info("Reading CSV File")
    df = spark.read.load('hdfs://localhost:9000/files/data.csv', format="csv", sep=",", header="false", schema=schema) 
    
    # Preview Spark Dataframe (for the project's purposes we use df.show(200) to see all records)
    logger.info("Previewing CSV File Data")
    print(df.show(10))
    
    # Clean and Transform the Spark Dataframe
    # When string (and generally a data type) is transformed to timestamp (to another data type) and doesn't match timestamp (this data type) format null is returned
    
    # Define the wanted values for the transaction_channel column
    # Assumption: Only Call and Email Values valid
    type_list = ["Call", "Email"]
    
    # Keep only the rows that have these values
    df = df.filter(df["transaction_channel"].isin(type_list))
    
    # Drop the rows with null
    df = df.na.drop()
    
    logger.info("Ending spark application")
    
    # Persist to parquet file, overwrite if already exists, and save it to HDFS
    df.write.mode("overwrite").parquet("/files/test")
       
    spark.stop()
    return None

# Starting point for PySpark
if __name__ == '__main__':
    main()
    sys.exit()
