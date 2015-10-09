import tweepy

# Set OAuth Keys
# 1. Create twitter app at https://apps.twitter.com/
# 2. Follow directions
# 3. Copy keys
CONSUMER_KEY = "blah"
CONSUMER_SECRET = "blah"
ACCESS_TOKEN = "blah"
ACCESS_TOKEN_SECRET = "blah"

# OAuth Handshake
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Creates interface using auth keys
api = tweepy.API(auth)


# Search for stuff
# TODO: 
# Refine query parameters
search_results = api.search(q="retweet follow contest giveaway", count=100, lang="en")
# 	Parameters:
#       q (query parameters)
# 	    result_type="recent" (TBD)
#	    count=100 (Count of tweets to return)
#	    rpp=100 (I have no idea what this means)
#	    id="651925114041274368" (tweet id)

# iterate over each search result
for tweet in search_results:
    # check if the tweet is authentic or a retweet
    # hasattr returns false if the tweet has not been retweeted, i.e., is the original tweet
    if hasattr(tweet, "retweeted_status"):
    	print ""
    # for original tweets
    else:
    	# Retweet the contest promo tweet
    	retweet_result = api.retweet(id=tweet.id)

    	# Follow the user
        # TODO:
        # certain tweets have multiple follow demands, e.g., follow @person1 AND @person2 to be eligible
    	
        # get user sn
    	user_screen_name_to_follow = api.get_status(id=tweet.id).user.screen_name
    	# follow the user
        Follow_result = api.create_friendship(screen_name="user_screen_name_to_follow")

# Tweet Parameters
# print ("ID:", tweet.id)
#     print ("User ID:", tweet.user.id)
#     print ("Text:", tweet.text)
#     print ("Created:", tweet.created_at)
#     print ("Geo:", tweet.geo)
#     print ("Contributors:", tweet.contributors)
#     print ("Coordinates:", tweet.coordinates)
#     print ("Favorited:", tweet.favorited)
#     print ("In reply to screen name:", tweet.in_reply_to_screen_name)
#     print ("In reply to status ID:", tweet.in_reply_to_status_id)
#     print ("In reply to status ID str:", tweet.in_reply_to_status_id_str)
#     print ("In reply to user ID:", tweet.in_reply_to_user_id)
#     print ("In reply to user ID str:", tweet.in_reply_to_user_id_str)
#     print ("Place:", tweet.place)
#     print ("Retweeted:", tweet.retweeted)
#     print ("Retweet count:", tweet.retweet_count)
#     print ("Source:", tweet.source)
#     print ("Truncated:", tweet.truncated)


# Random Notes for future use
# use this to send tweets - must have header or else will throw an error
#   Result = api.update_status(status=TweetText, in_reply_to_status_id=ReplyToTweetID, headers={'content-length': 0})