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
keywords = spark.sql('select keywords from tweets').collect()

keywords_dict = dict()

for keywords_list in keywords:
  all_keywords = keywords_list.keywords
  # print(all_keywords)
  for keyword in all_keywords:
    keywords_dict[keyword] = keywords_dict[keyword] + 1 if keyword in keywords_dict else 1

top_languages = pd.DataFrame(keywords_dict.items(), columns=['language', 'count']).head(10)

top_languages.rename(columns={"count": "Quantidade de tweets"}) \
                .sort_values(by=["Quantidade de tweets"]) \
                .plot(
                    figsize=(15,7),
                    kind="barh", \
                    title="Linguagens de programação mais populares no Twitter", \
                    x="language", \
                    xlabel="Linguagem", \
                ) \

plt.savefig('barh-languages')
print("\nTop 10 linguagens mais populares no Twitter")
print(top_languages)

# count = 0
# while count < 10:
#     # time.sleep( 60 )
#     stream = pd.DataFrame(list(db.tweets.aggregate(pipeline)))
#     plt.figure( figsize = ( 16, 8 ) )
#     ax = sns.barplot( x="_id", y="count", data=stream.head(10))
#     ax.set(xlabel='Keywords', ylabel='counts')
#     plt.show()
#     count = count + 1