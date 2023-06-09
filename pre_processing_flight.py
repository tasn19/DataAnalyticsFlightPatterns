# -*- coding: utf-8 -*-
"""Pre-processing - Flight.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Yhbd57oYNbqvAK-C3RClMv2uhhabYvnU
"""

! pip install kaggle
! mkdir ~/.kaggle
! cp /content/kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json
! kaggle datasets download --force robikscube/flight-delay-dataset-20182022

# unzip the downloaded file
import zipfile
! unzip -q /content/flight-delay-dataset-20182022.zip -d Airlines

# All the imports
!pip install pyspark
import pyspark
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

#Loading all csvs into pyspark dataframes

years = ['2018', '2019', '2020', '2021', '2022']
dfs = []

spark = SparkSession.builder.master("local[1]") \
          .appName("SparkByExamples.com") \
          .getOrCreate()

for y in years:
  df = spark.read.options(header='True', inferSchema='True').csv(f"Airlines/Combined_Flights_{y}.csv")
  dfs.append(df)

# Pre-processing 
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, IntegerType, ArrayType
from pyspark.sql.functions import udf
from pyspark.sql.functions import when
from pyspark.sql.functions import lit


# DEFs
def time_to_hour(x):
  if x == '-1':
    return '-1'
  
  return x[:2] if len(x) == 4 else x[:1]

def time_to_minute(x):
  if x == '-1':
    return '-1'

  if len(x) >= 3:
    return x[-2:]
  
  return 0

def year_to_1h(x):
  cats = 5
  idx = x % cats
  res = [0] * cats
  res[idx] = 1

  return res

def pan_to_1h(x):
  cats = 3
  idx = x % cats
  res = [0] * cats
  res[idx] = 1

  return res

def geo_to_1h(x):
  cats = 4
  idx = x % cats
  res = [0] * cats
  res[idx] = 1

  return res

# UDFs

udf_time_to_hour = udf(time_to_hour, StringType())
udf_time_to_minute = udf(time_to_minute, StringType())
# udf_range_to_name = udf(lambda x: 'Late Night' if x == 1 else 
#                         'Early Morning' if x == 2 else
#                         'Morning' if x == 3 else
#                         'Noon' if x == 4 else
#                         'Evening' if x == 5 else
#                         'Night' if x == 6 else
#                         'ERROR'
#                         , StringType())
udf_to_is_delay = udf(lambda x: 1 if x > 0 else 0, IntegerType())
udf_to_is_early = udf(lambda x: 1 if x < 0 else 0, IntegerType())
udf_dist_to_sh_lo = udf(lambda x: 0 if x < 790 else 1, IntegerType())
udf_day_to_mo_half = udf(lambda x: 0 if x <= 15 else 1, IntegerType())
udf_city_to_state = udf(lambda x: x.split(',')[0], StringType())

West = ['WA','OR','ID','MT','CA','NV','UT','AZ','CO','NM','AK','WY'] 
MidWest = ['ND','SD','NE','KS','MN','IA','MO','WI','IL','MI','IN','OH'] 
South = ['TX','OK','LA','AR','MS','AL','TN','KY','WV','FL','GA','SC','NC','VA','MD','DC','DE'] 
NorthEast = ['PA','NY','VT','NJ','CT','RI','MA','NH','ME','PR','VI']
udf_state_to_geo = udf(lambda x: 0 if x in West else # west
                      1 if x in MidWest else # midwest
                      2 if x in South else # south
                      3 if x in NorthEast else # northeast
                      4 # error
                      , IntegerType())

udf_year_to_1h = udf(year_to_1h, ArrayType(IntegerType(), False))
udf_pan_to_1h = udf(pan_to_1h, ArrayType(IntegerType(), False))
udf_geo_to_1h = udf(geo_to_1h, ArrayType(IntegerType(), False))

#Pre-processing code
def pre_process(df):
  # we should have two fillna s because:
  # each time pyspark will fill the nulls of the given type
  df = df.fillna('-1')
  df = df.fillna(-1)
  df = df.withColumn("Cancelled",col("Cancelled").cast("Integer"))
  df = df.withColumn("Diverted",col("Diverted").cast("Integer"))

  df = df.withColumn("CRSDepTime",col("CRSDepTime").cast("Integer"))
  df = df.withColumn("CRSDepTime",col("CRSDepTime").cast("String"))
  df = df.withColumn("DepTime",col("DepTime").cast("Integer"))
  df = df.withColumn("DepTime",col("DepTime").cast("String"))

  df = df.withColumn("CRSDepHour", udf_time_to_hour("CRSDepTime"))
  df = df.withColumn("CRSDepHour",col("CRSDepHour").cast("Integer"))

  df = df.withColumn("DepHour", udf_time_to_hour("DepTime"))
  df = df.withColumn("DepHour",col("DepHour").cast("Integer"))

  df = df.withColumn("DepMinutes", udf_time_to_minute("DepTime"))
  df = df.withColumn("DepMinutes",col("DepMinutes").cast("Integer"))

  df = df.withColumn("IsDepDelay", udf_to_is_delay("DepDelay"))
  df = df.withColumn("IsDepEarly", udf_to_is_early("DepDelay"))

  # Same pre-processing techniques as applied to departure columns

  df = df.withColumn("CRSArrTime",col("CRSArrTime").cast("Integer"))
  df = df.withColumn("CRSArrTime",col("CRSArrTime").cast("String"))
  df = df.withColumn("ArrTime",col("ArrTime").cast("Integer"))
  df = df.withColumn("ArrTime",col("ArrTime").cast("String"))

  df = df.withColumn("CRSArrHour", udf_time_to_hour("CRSArrTime"))
  df = df.withColumn("CRSArrHour",col("CRSArrHour").cast("Integer"))
  
  df = df.withColumn("ArrHour", udf_time_to_hour("ArrTime"))
  df = df.withColumn("ArrHour",col("ArrHour").cast("Integer"))
  
  df = df.withColumn("ArrMinutes", udf_time_to_minute("ArrTime"))
  df = df.withColumn("ArrMinutes",col("ArrMinutes").cast("Integer"))

  df = df.withColumn("IsArrDelay", udf_to_is_delay("ArrDelay"))
  df = df.withColumn("IsArrEarly", udf_to_is_early("ArrDelay"))

  df = df.withColumn("ShortOrLong", udf_dist_to_sh_lo("Distance"))
  df = df.withColumn("TimeofMonth", udf_day_to_mo_half("DayofMonth"))

  df = df.withColumn("OriginCityName", udf_city_to_state("OriginCityName"))
  df = df.withColumn("DestCityName", udf_city_to_state("DestCityName"))

  df = df.withColumn("GeoOrientation", udf_state_to_geo("OriginState"))

  df = df.withColumn("DepDelayMinutes",col("DepDelayMinutes").cast("Integer"))
  df = df.withColumn("AirTime",col("AirTime").cast("Integer"))
  df = df.withColumn("ActualElapsedTime",col("ActualElapsedTime").cast("Integer"))
  df = df.withColumn("ArrDelayMinutes",col("ArrDelayMinutes").cast("Integer"))
  df = df.withColumn("TaxiOut",col("TaxiOut").cast("Integer"))
  df = df.withColumn("TaxiIn",col("TaxiIn").cast("Integer"))

  # I Tried this and it worked. Created 3 categories pre-pandemic - 1 , pandemic - 2, post pandemic - 3 - Mithila
  # Note - Please double check if the conditions are correct :)
  # Travel ban started March 2020 and ended November 2021 in the USA
  df = df.withColumn("Pandemic", \
                     when(df.Year == 2019, 1) \
                     .when((df.Year == 2020) & (df.Month <= 3), 1) \
                     .when((df.Year == 2020) & (df.Month > 3), 2) \
                     .when((df.Year == 2021) & (df.Month <= 3), 2) \
                     .otherwise(3)
                     )

  df = df.withColumn("Year", udf_year_to_1h("Year"))
  df = df.withColumn("Pandemic", udf_pan_to_1h("Pandemic"))
  df = df.withColumn("GeoOrientation", udf_geo_to_1h("GeoOrientation"))

  to_be_dropped = ('Distance',
                   'WheelsOff',
                   #'DayofMonth', # TN - don't remove, needed for combining all flights per day
                   'FlightDate',
                   'CRSDepTime',
                  #  'DepTime', # Rmin: maybe we need it
                   'WheelsOn',
                   'CRSArrTime',
                  #  'ArrTime', # Rmin: maybe we need it
                   'ArrDelay',
                   'OriginStateName',
                   'DestStateName',
                   'Operated_or_Branded_Code_Share_Partners',
                   'DOT_ID_Marketing_Airline',
                   'IATA_Code_Marketing_Airline',
                   'Flight_Number_Marketing_Airline',
                   'DOT_ID_Operating_Airline',
                   'IATA_Code_Operating_Airline',
                   'Tail_Number',
                   'Flight_Number_Operating_Airline',
                   'OriginAirportID',
                   'OriginAirportSeqID',
                   'OriginCityMarketID',
                   'DestAirportID',
                   'DestAirportSeqID',
                   'DestCityMarketID',
                   'DivAirportLandings',
                   'OriginWac',
                   'OriginStateFips',
                   'DestStateFips',
                   'DestWac',
                   'Marketing_Airline_Network',
                   'DepartureDelayGroups', #Added by Mithila # Rmin: great!
                   'DepTimeBlk',
                   'Operating_Airline',
                   'DepDelay', # we are using DepDelayMinutes instead cuz it doesnt have neg vals for early flights
                   'DepartureDelayGroups',
                   'DepTimeBlk',
                   'ArrivalDelayGroups',
                   'ArrTimeBlk',
                   'CRSElapsedTime',
                   'DistanceGroup', #Do we need this column? # Rmin: no i dont think so
                   'DepDel15',
                   'ArrDel15',
                   'CRSDepTime',
                   'DepTime',
                   'CRSArrTime',
                   'ArrTime'
                   )
  
  df = df.drop(*to_be_dropped)
  return df

# call the pre processing code
pp_dfs = [pre_process(df) for df in dfs]

# Frequency encoding

# Note - for visualization purpose, please comment this frequency encoding part and save the csv before encoding.
import pyspark.sql.functions as pfn

cat_dfs = []
categorical_columns = ['Airline', 
                       'Origin', 
                       'Dest', 
                       'OriginCityName', 
                       'OriginState',
                       'DestCityName',
                       'DestState',
                       ]
# categorical_columns = []

for df in pp_dfs:
  res = df
  total = df.count()

  for cc in categorical_columns:
    freq = df.groupBy(cc).agg(pfn.count("*") / total).withColumnRenamed(f'(count(1) / {total})', cc + "ID")
    res = res.join(freq, cc, "left") 

  cat_dfs.append(res)

final_df = cat_dfs[0]
for df in cat_dfs[1:]:
  final_df = final_df.union(df)


# write final csv to drive
from google.colab import drive
drive.mount('/content/drive')
final_df.repartition(1).write.option("header", True).format('parquet').save('/content/drive/MyDrive/DA/final_df')