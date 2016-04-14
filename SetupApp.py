import tweepy, time, sys
#all tokens are stored in file and not hard coded, these files are in the .gitignore, to prevent strangers from accessing the API
cTokensFile=open('ConsumerTokens','r') #get the consumer tokens from their file
#tokens are always stored, normal on the first line, secret on the second
temp = cTokensFile.read().splitlines()
cTokensFile.close()
cToken=temp[0]
cTokenS=temp[1]
auth = tweepy.OAuthHandler(cToken,cTokenS)#create the auth of the twitter app using tweepy
try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)#generates a URL and outputs it to the shell
    verifier = input('Verifier:')#takes the verifier PIN from twitter,
    auth.get_access_token(verifier)#generates the access Tokens 
    aToken=auth.access_token
    aTokenS=auth.access_token_secret
    aTokensFile = open('AccessTokens','w')#writes the access tokens to file
    aTokensFile.write(aToken+'\n')
    aTokensFile.write(aTokenS+'\n')
    aTokensFile.close()
    #all done, the app now has permission to tweet, and read the user's tweets
except tweepy.TweepError:
    print ('Error! Failed to get request token.')

