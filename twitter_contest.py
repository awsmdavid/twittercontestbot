import tweepy

# SETUP:
# Create Twitter OAuth Keys
# 1. Create twitter app at https://apps.twitter.com/
# 2. Follow directions
# 3. Copy keys

# For Cronjob Command (if you need virtualenv)
# source /....../bin/activate && python /..../twitter_contest.py


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
# dont reprocess same tweets (perhaps use since_id)

# Throw in possible search queries; while multiple searches will result in duplicates, it provides more results over one "super query" (hoping to cast a broader net)
search_results_1 = api.search(q="giveaway follow retweet -RT", rpp=100, lang="en")
search_results_2 = api.search(q="giveaway contest follow retweet -RT", rpp=100, lang="en")

search_results = search_results_1 + search_results_2

# 	Parameters:
# q the search query string: for more info - https://twitter.com/search-home (click operators)
# lang - Restricts tweets to the given language, given by an ISO 639-1 code.
# locale - Specify the language of the query you are sending. This is intended for language-specific clients and the default should work in the majority of cases.
# rpp - The number of tweets to return per page, up to a max of 100.
# page - The page number (starting at 1) to return, up to a max of roughly 1500 results (based on rpp * page.
# since_id - Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
# geocode - Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by "latitide,longitude,radius", where radius units must be specified as either "mi" (miles) or "km" (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly.
# show_user - When true, prepends "<user>:" to the beginning of the tweet. This is useful for readers that do not display Atom's author field. The default is false.

# iterate over each search result
for tweet in search_results:
    tweet_id = tweet.id
    tweet_text = tweet.text
    tweet_retweet_count = tweet.retweet_count
    # check if the tweet is authentic or a retweet
    # hasattr returns false if the tweet has not been retweeted, i.e., is the original tweet
    if hasattr(tweet, "retweeted_status"):
        # print "yo", tweet_text
        pass
    # check for original tweets
    # SWAG - a bunch of bots crappily follow random tweets, want to capture more authentic giveaways:
    # currently, the best method I can think of is using retweet_count>10; can't find api for determining original outside of this and the presence of "RT"
    elif tweet_retweet_count>10:
        print tweet.retweet_count
        list_of_accounts_to_follow = []

        ######################
        # Retweet and Follow #
        ######################

        # get user screen name to follow initial tweeter
        user_screen_name_to_follow = api.get_status(id=tweet_id).user.screen_name
        list_of_accounts_to_follow.append(user_screen_name_to_follow)

        try:
            # Retweet the contest promo tweet
            retweet_result = api.retweet(id=tweet_id)

            # Follow mad people
            # (certain tweets have multiple follow demands, e.g., follow @person1 AND @person2 AND @person3 to be eligible - those jerks...)

            text_list = tweet_text.split(" ")
            for text in text_list:
                text.strip("\n")
                text.strip("\t")
                if text.startswith("@"):
                    list_of_accounts_to_follow.append(text)
        except:
            pass

        # Follow all accounts mentioned
        for screen_name in list_of_accounts_to_follow:
            # Cleanse accounts of "@"
            screen_name = screen_name.replace("@", "")
            print screen_name
            try:
                Follow_result = api.create_friendship(screen_name=screen_name)
            except:
                pass

################################
# Random Notes for future use: #
################################

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
#
#
#
# If you see the following warning:
#   "InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3
#   from configuring SSL appropriately and may cause certain SSL connections to fail."
# call: pip install requests[security] (need to install security packages because your python should be 2.7.9+)
#
# Alternatively, if you dont want to upgrade or don't have sudo permission, you can surpress the warnings by downgrading your requests:
# pip install requests==2.5.3
#
#
# use this to send tweets - must have header or else will throw an error
#   Result = api.update_status(status=TweetText, in_reply_to_status_id=ReplyToTweetID, headers={'content-length': 0})
