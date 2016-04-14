import tweepy, time, sys
TokensFile=open('ConsumerTokens','r')
temp = TokensFile.read().splitlines()
TokensFile.close()
cToken=temp[0]
cTokenS=temp[1]
TokensFile=open('AccessTokens','r')
temp = TokensFile.read().splitlines()
TokensFile.close()
aToken=temp[0]
aTokenS=temp[1]
auth = tweepy.OAuthHandler(cToken, cTokenS)
auth.set_access_token(aToken, aTokenS)
api = tweepy.API(auth)
api.update_status('Testing out twitter emoji :stuck_out_tongue_winking_eye: ')
#ITS ALIVE
