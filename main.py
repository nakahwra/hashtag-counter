import pymongo
import pyspark
import pandas as pd
import matplotlib.pyplot as plt

working_directory = './jars/*'

spark = pyspark.sql.SparkSession \
        .builder \
        .appName('MyApp') \
        .config('spark.mongodb.input.uri', 'mongodb://127.0.0.1/hashtag_counter.tweets') \
        .config('spark.driver.extraClassPath', working_directory) \
        .getOrCreate()

tweets_df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

tweets_df.createOrReplaceTempView('tweets')
resDf = spark.sql('select keywords from tweets')
resDf.show()
spark.stop()

# count = 0
# while count < 10:
#     # time.sleep( 60 )
#     stream = pd.DataFrame(list(db.tweets.aggregate(pipeline)))
#     plt.figure( figsize = ( 16, 8 ) )
#     ax = sns.barplot( x="_id", y="count", data=stream.head(10))
#     ax.set(xlabel='Keywords', ylabel='counts')
#     plt.show()
#     count = count + 1