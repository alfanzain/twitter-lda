from configs.const import *
from models.Tweet import *
import tweepy


class StreamListener(tweepy.StreamListener):

    def __init__(self):
        super(StreamListener, self).__init__()
        self.count = 0

    def create(self, status):

        tweet = Tweet()
        create = tweet.create(status)

        if create is True:
            # Count inserted tweet and store to variable
            self.count += 1

    def update(status):

        tweet = Tweet()
        return tweet.update(status)

    # When API get a status while streaming
    def on_status(self, status):

        # Insert new tweet IF has 'retweeted_status'
        if hasattr(status, 'retweeted_status'):
            print("{} is retweeting {}.".format(status.id_str, status.retweeted_status.id_str))

            tweet = Tweet()
            # Check if retweeted_status already exist
            if tweet.is_tweet_exist(status.retweeted_status.id_str) != 0:
                print("{} found!".format(status.retweeted_status.id_str))
                self.update(status.retweeted_status)
            else:
                print("{} not found.".format(status.retweeted_status.id_str))
                self.create(status.retweeted_status)

        self.create(status)

        print('Total {} status(es) inserted.\n'.format(self.count))

    def on_error(self, status_code):
        # print status_code if it is 420
        if status_code == 420:
            print(status_code)
            return False

# Main functions


def setup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)


def start():
    my_stream = tweepy.Stream(auth=setup().auth, listener=StreamListener(), tweet_mode='extended')
    my_stream.filter(track=['#game', '-#porn'])


if __name__ == "__main__":
    start()
