# Twitter data 


WARNING: This code uses Twitter API. You must fill your keys in the .YML file contained in this folder if you want to do anything. 



This folder contains the code that was used to identify tweets mentioning 
the specific disinformation ``keywords'' identified earlier in the process. 

In this module you will find the code that: 
- connects to the twitter API
- queries twitters for all tweets over the netherlands containing at least some keywords (by categories)
- flagging of tweets for all their relenvant categories (only one keyword is enough to be taged, and then the tweet content is checked for it 
  participating in more than one category - so a tweet can contribute to more than one!)
- identify trends by category, for all tweets from the Netherlands (sample from twitter dev. API) over the studied period of time. 





# Notes

The "test_output" folder contains partial results - you may comfortably ignore the content of that folder. 

if you want to re-use the code from this folder, be aware you will need to provide your Tweeter API key in 
the file called  "api_cred.yaml" - which should currently only contain the keys without their associated values.
