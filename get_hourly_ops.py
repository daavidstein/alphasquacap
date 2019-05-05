
from __future__ import print_function
import operator
import platform
from operator import add
import findspark
import csv

# Initialize pyspark finder
findspark.init()
# Get pyspark
import pyspark

conf = pyspark.SparkConf()
conf.set('spark.local.dir', '/Akamai_scratch/tmp_spark/')
conf.set('spark.executor.memory', '15g')
conf.set('spark.driver.memory', '15g')

# Tell Spark to use all the local clusters
sc = pyspark.SparkContext('local[*]', 'airports', conf)
# Tell spark to create a session
from pyspark.sql import SparkSession
#sess = SparkSession(sc).builder.config(sc.getConf).config("spark.local.dir", "/Akamai_scratch/").getOrCreate()
sess = SparkSession(sc)

# Hold back on the error messages
sc.setLogLevel("ERROR")

# First path points to one small csv for testing
path1 = "/Akamai_scratch/airport_alpha/raw_bts/001.csv"
# Second path is to full data
path2 = "/Akamai_scratch/airport_alpha/raw_bts/*.csv"

# Select airport of interest
ap_select = "ATL"
# All major airports
major_aps = ["SLC","OAK","IAH","MDW","SAN","PHX","BWI","LAS","CVG", \
             "MCO","TPA","LAX","PDX","DEN","STL","ATL","DTW","FLL", \
             "MSP","IAD","DFW","DCA","SEA","CLT","MIA","SFO","BOS", \
             "PHL","ORD","JFK","EWR","LGA"]

# Get the data, split on commas, handle encoding issue where
# all strings have single quotes around double quotes. 
raw_data = sc.textFile(path2) \
            .map(lambda line: line.split(",")) \
            .map(lambda x: [z.encode("utf-8", "ignore").strip('\"') for z in x])

# Define header as first row
header = raw_data.first() 
# Remove header
airport = raw_data.filter(lambda x: x != header) 

# Remove reviews that share date, origin, destination, dep_time, dep_delay
# Note that the entire row is the value here
all_dupes = airport.map(lambda x: ((x[3], x[6], x[10], x[13], x[14]), x))
# Group by row values, dropping duplicates
airport = all_dupes.reduceByKey(lambda x, y: x) \
                   .map(lambda x: x[1])

# Check against selected airport
def is_selected(x):
    return x == ap_select

def extract_hour(x):
  """This extracts an hour between 1 and 24 from numbers formatted like '425' or '1345'."""
  x = str(x).strip()
  if len(x) == 3:
    return int(x[0])
  elif len(x) == 4 and x[:2] != '24':
    return int(x[:2])
  elif len(x) < 3 or (len(x) == 4 and x[:2] == '24'):
    return(0)
 
# x[0] is year
# x[1] is month
# x[2] is day of the month
# x[8] is origin
# x[13] is departure time
 
# filter out rows with no arrival time
#get count of arrivals for every unique pair (day_of_month, hour) in the month
arrs_per_hour = airport.filter(lambda x: x[8] == ap_select and x[13] != '') \
	                   .map(lambda x: ((x[0], x[1], x[2], (extract_hour(x[13]))), 1)) \
                           .reduceByKey(lambda x, y: x+y) 

#print("arrs_per_hour:")
#print(arrs_per_hour.count())
# x[12] is destination
# x[16] is arrival time

#get count of departures for every unique pair (day_of_month, hour) in the month
deps_per_hour = airport.filter(lambda x: x[12] == ap_select and x[16] != '')  \
               .map(lambda x: ((x[0], x[1], x[2], (extract_hour(x[16]))), 1)) \
               .reduceByKey(lambda x, y: x+y) 

# join on the complex keys
hours = arrs_per_hour.join(deps_per_hour) \
	             .map(lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[1][0], x[1][1]))

#rdd = airport.map(lambda x:(x[0], 1)) \
#             .reduceByKey(lambda x, y: x+y)

print("Python version: " + platform.python_version())
#print("RDD count: " + str(rdd.count()))

print(hours.take(15))

# collect and save as csv
#with open('/Akamai_scratch/airport_alpha/test_csv_stl.csv', 'wb') as myfile:
#    wr = csv.writer(myfile, delimiter = ',', quoting=csv.QUOTE_ALL)
#    wr.writerow(rdd.collect())

#from pyspark import SparkContext, SparkConf
#from pyspark.sql import SparkSession
#conf = SparkConf()
#sc = SparkContext(conf=conf)
#spark = SparkSession.builder.config(conf=conf).getOrCreate() 


df = sess.createDataFrame(hours, ['year','month', 'day_of_month', 'hour', 'arrivals', 'departures'])
#df = sess.createDataFrame(rdd, ['year', 'count'])
df.coalesce(1).write.save(path='./test_csv_atl.csv', format='csv', mode='append')

