import tweepy, time, sys
filename=open('ConsumerTokens','r')
cToken = filename.readline().splitlines()
cTokenS = filename.readline().splitlines()
auth = tweepy.OAuthHandler(cToken,cTokenS)
try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
    verifier = input('Verifier:')
    auth.get_access_token(verifier)
    print(auth.access_token)
    print(auth.access_token_secret)
except tweepy.TweepError:
    print ('Error! Failed to get request token.')
