#Developed by Kenneth Shaw Friedman

#YOU MUST INSTALL THE TWITTER PACKAGE FROM THE FOLLOWING WEBSITE
#FOR THIS SCRIPT TO WORK
#	available here: http://mike.verdone.ca/twitter/#install
import twitter
import time

######################################################################
############################## OPTIONS ###############################
######################################################################

#authorize
token =	"PUT 'Access Token' HERE"
tKey  =	"PUT 'Access Token Secret'"
conSec= "PUT 'Consumer Key (API Key)' HERE"
conKey= "PUT 'Consumer Secret (API Secret)' HERE" 

#constants
READ_STORY_WHILE_SCROLLING_DOWN = True				#False will reverse the direction
NAME_OF_FILE_IN_SAME_DIRECTORY = "story.txt"		#Keep .txt in same directory as this .py
SECONDS_BETWEEN_TWEETS = 37							#37 will tweet <100 times an hour

######################################################################
########################## end of options ############################
######################################################################

#warning: modifying the code below will change the indended behavior of this script

def textFileToArrayOfTweets(textFilename):
	text = ""
	with open (textFilename, "r") as myfile:
		text = myfile.read()
	wordList = text.split()
	tweets = []
	while len(wordList)>0:
		tempTweet = ""
		while len(wordList)>0 and len(tempTweet)+len(wordList[0])<=139:
			tempTweet = tempTweet + wordList[0] + " "
			del wordList[0]
		tempTweet = tempTweet.strip()
		tweets.append(tempTweet)
	return tweets

#constant text strings
TEXT_PROPER_ORDER	= "Tweets will be in proper reading order.\n"
TEXT_INVERT_ORDER	= "You will have to start at the bottom of the list to read the story correctly.\n"
TEXT_COMPLETION		= " until completion. Let's go!\n"
TEXT_DONE 			= "DONE!"
TEXT_TW 			= "TW "
TEXT_OF 			= " of "
TEXT_PR 			= " printed. TWEET: "

#######  STEP 00: OAuth with Twitter #################################
my_auth = twitter.OAuth(token, tKey, conSec, conKey)
twit = twitter.Twitter(auth=my_auth)

#######  STEP 01: Get the array of tweets from method above ##########
tweets = textFileToArrayOfTweets(NAME_OF_FILE_IN_SAME_DIRECTORY)
numTweets = len(tweets)

#######  STEP 02: Calculate how long it will take to tweet ##########
#################### (this is due to twitter API limits) ############
print str(SECONDS_BETWEEN_TWEETS*numTweets/60.0) + TEXT_COMPLETION

#######  STEP 03: Decide which direction you are reading tweets ######
if READ_STORY_WHILE_SCROLLING_DOWN:
	print TEXT_PROPER_ORDER
	tweets.reverse()
else:
	print TEXT_INVERT_ORDER

#######  STEP 04: Print each tweet in the list of tweets ##########
tweetPrinted = 0
for tweet in tweets:
	tweetPrinted+=1
	time.sleep(SECONDS_BETWEEN_TWEETS)
	twit.statuses.update(status=tweet)
	print TEXT_TW + str(tweetPrinted) + TEXT_OF + str(numTweets) + TEXT_PR + tweet

#######  STEP 05: Confirm completion ##########
print TEXT_DONE