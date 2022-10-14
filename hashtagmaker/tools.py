import tweepy

def getTagPopularity(tag:str, client:tweepy.Client):
    print(tag)
    resp=client.get_recent_tweets_count(f"#{tag}", granularity="day" )
    return (tag, int(resp[3]['total_tweet_count']))