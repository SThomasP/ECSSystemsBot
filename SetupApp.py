import tweepy, time, sys
cTokensFile=open('ConsumerTokens','r')
temp = cTokensFile.read().splitlines()
cTokensFile.close
cToken=temp[0]
cTokenS=temp[1]
auth = tweepy.OAuthHandler(cToken,cTokenS)
try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
    verifier = input('Verifier:')
    auth.get_access_token(verifier)
    aToken=auth.access_token
    aTokenS=auth.access_token_secret
    aTokensFile = open('AccessTokens','w')
    aTokensFile.write(aToken+'\n')
    aTokensFile.write(aTokenS+'\n')
    aTokensFile.close()
except tweepy.TweepError:
    print ('Error! Failed to get request token.')

