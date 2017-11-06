require (twitteR)
require(RCurl)

consumer_key<- 'xxxxxx'
consumer_secret<- 'xxxxx'
access_token<- 'xxxxxx'
access_secret<- 'xxxx'

setup_twitter_oauth(consumer_key,consumer_secret,access_token, access_secret)

tweets <- searchTwitter("Codere", n=100)
tweets.df <- twListToDF(tweets)
tweets.df
write.csv(tweets.df, file="Twitter.csv")
