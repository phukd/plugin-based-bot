import tweepy
import re
import HTMLParser

class twitter:
  def __init__(self, bot):
    self.allowed_functions = { 'tweet':1, 'follow':2, 'reply':1, 'retweet':1, 'delete':2, 'help':1 }

    consumer_key = "RAfBYcAO4Vlak4Kq7kXd7g"
    consumer_secret = "x2JteCZQJs2G3JanhPJQ3g22xEASNotN19Kq5AEPk"
    access_token = "1223709024-aoppuF8SgXcM7EFEtEoDof1XML6WKPB7hatiRWW"
    access_token_secret = "EYHhlNFPMSltE6g6xE4awrNGhTyMcFBeJzvnYxIz0gw"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    self.api = tweepy.API(auth)
    self.bot = bot

  def tweet(self, buffer):
    text       = ' '.join(buffer.msg.split()[1:])

    if len(text) < 140:
      tweet = self.api.update_status(text)
      self.bot.msg(buffer.to, "Tweet URL: https://twitter.com/%s/status/%s" % (tweet.author.screen_name, tweet.id))

    else:
      split_msg = list(re.findall(".?"*110, text))
      length = len(split_msg)
      tweet = None

      if split_msg[-1] == "":
        length -= 1

      if length > 5:
        self.bot.msg(buffer.to, "%d messages.... really?! Asshole." % length)
        return

      for i, msg in enumerate(split_msg):
        if msg == "":
          continue
        if tweet != None:
          tweet = self.api.update_status("%d/%d ...%s -- @%s" % (i + 1, length, msg, tweet.author.screen_name), tweet.id)
        else:
          try:
            tweet = self.api.update_status("%d/%d %s" % (i + 1, length, msg))
          except Exception as e:
            self.bot.msg(buffer.to, buff.to, "%s" % e)
          self.bot.msg(buffer.to, "Tweet URL: https://twitter.com/%s/status/%s" % (tweet.author.screen_name, tweet.id))

  def follow(self, buffer):
    username   = buffer.msg.split()[1] 

    try:
      self.api.create_friendship(username)
      self.bot.msg(buffer.to, "Followed %s" % username)
    except Exception as e:
      self.bot.msg(buffer.to, "Error: %s" % str(e))

  def reply(self, buffer):
    url        = buffer.msg.split()[1]
    tweet      = ' '.join(buffer.msg.split()[2:])

    (author, tweet_id) = re.search("https?://w?w?w?\.?twitter.com/([^/]+)/statuse?s?/([^ ]+)", url).groups()
    if user not in tweet:
      tweet = user + ' ' + tweet
    tweet = self.api.update_status(tweet, tweet_id)
    self.bot.msg(buffer.to, "Tweet URL: https://twitter.com/%s/status/%s" % (tweet.author.screen_name, tweet.id))

  def retweet(self, buffer):
    tweet_id = re.search("https?://w?w?w?\.?twitter.com/.*/statuse?s?/([^ ]+)", buffer.msg).group(1)
    self.api.retweet(tweet_id)
    h = HTMLParser.HTMLParser()
    tweet = self.api.get_status(id=tweet_id)
    tweet.text = h.unescape(tweet.text)
    self.bot.msg(buffer.to, "Retweeted: <%s> %s -- %s" % (tweet.author.screen_name, tweet.text, "https://twitter.com/%s/status/%s" % (tweet.author.screen_name, tweet.id)))

  def delete(self, buffer):
    tweet_id = re.search("https?://w?w?w?\.?twitter.com/.*/statuse?s?/([^ ]+)", buffer.msg).group(1)
    tweet = self.api.destroy_status(id=tweet_id)
    self.bot.msg(buffer.to, "Deleted: %s" % ("https://twitter.com/%s/status/%s" % (tweet.author.screen_name, tweet.id)))

  def help(self, buffer):
    self.bot.msg(buffer.to, "Usage:")
    self.bot.msg(buffer.to, "  twitter.tweet   <tweet>")
    self.bot.msg(buffer.to, "  twitter.retweet <url>")
    self.bot.msg(buffer.to, "  twitter.delete  <url>")
    self.bot.msg(buffer.to, "  twitter.reply   <url>   <tweet>")
    self.bot.msg(buffer.to, "  twitter.follow  <user>")
