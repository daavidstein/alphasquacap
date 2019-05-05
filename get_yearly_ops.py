# ISSUES
# The csv that's output at the end of this is horribly malformed. 
# Can you fix it?

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

# tmp_spark

conf = pyspark.SparkConf()
conf.set('spark.local.dir', '/Akamai_scratch/tmp_spark/')
conf.set('spark.executor.memory', '15g')
conf.set('spark.driver.memory', '15g')
#conf.setMaster('local')

# Tell Spark to use all the local clusters
sc = pyspark.SparkContext('local[*]', 'airports', conf)
# Tell spark to create a session
from pyspark.sql import SparkSession
#sess = SparkSession(sc).builder.config(sc.getConf).config("spark.local.dir", "/Akamai_scratch/").getOrCreate()
sess = SparkSession(sc)

# Hold back on the error messages
sc.setLogLevel("ERROR")

# First path points to one small csv for testing
path1 = "/Akamai_scratch/airport_alpha/raw_bts/75577152_T_ONTIME_REPORTING.csv"
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

# Check against selected airport
def is_selected(x):
    return x == ap_select

# Remove reviews that share date, tail num, origin, dest, and departure time
# Note that the entire row is the value here
all_dupes = airport.map(lambda x: ((x[3], x[6], x[11], x[15], x[16]), x))
# Group by row values, dropping duplicates
airport = all_dupes.reduceByKey(lambda x, y: x) \
                   .map(lambda x: x[1])

# x11 is ORIGIN
# x15 is DEST
# filter: select airport of interest
# map: emit: (year, (airport of interest?, airport of interest?))
# reduceByKey: count arrivals and departures by year
# map: flatten the keys and values

rdd = airport.filter(lambda x: x[8] == ap_select or x[12] == ap_select) \
             .map(lambda x: (x[0], (is_selected(x[8]), is_selected(x[12])))) \
             .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) \
             .map(lambda x: x[:-1] + x[-1])

rdd = airport.map(lambda x:(x[0], 1)) \
             .reduceByKey(lambda x, y: x+y)

print("Python version: " + platform.python_version())
#print("RDD count: " + str(rdd.count()))

print(rdd.take(15))

# collect and save as csv
#with open('/Akamai_scratch/airport_alpha/test_csv_stl.csv', 'wb') as myfile:
#    wr = csv.writer(myfile, delimiter = ',', quoting=csv.QUOTE_ALL)
#    wr.writerow(rdd.collect())

#from pyspark import SparkContext, SparkConf
#from pyspark.sql import SparkSession
#conf = SparkConf()
#sc = SparkContext(conf=conf)
#spark = SparkSession.builder.config(conf=conf).getOrCreate() 


#df = sess.createDataFrame(rdd, ['year', 'arrivals', 'departures'])
df = sess.createDataFrame(rdd, ['year', 'count'])
df.coalesce(1).write.save(path='./test_csv_stl.csv', format='csv', mode='append')
