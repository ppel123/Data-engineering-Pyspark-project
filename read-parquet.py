"""
# Title : PySpark Script - Read Parquet
# Description : This script is used to read a parquet file and save it to a Spark dataframe
# Usage : spark-submit read-parquet.py
"""

# First import the neccesary modules
from pyspark.sql import SparkSession
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

# current time variable to be used for logging purpose
dt_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

AppName = "Spark-Project"

def main():

    # Start spark code
    spark = SparkSession.builder.appName(AppName+"_"+str(dt_string)).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    logger.info("Starting spark application")

    # Read Parquet File into a Spark Dataframe
    logger.info("Reading Parquet File")
    parquet_file = spark.read.parquet("/files/test")
    
    # Preview Spark Dataframe
    logger.info("Previewing Parquet File Data")
    print(parquet_file.show(10))
    
    logger.info("Ending spark application")
   
    spark.stop()
    return None

# Starting point for PySpark
if __name__ == '__main__':
    main()
    sys.exit()
