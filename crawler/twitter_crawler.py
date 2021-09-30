import tweepy
from models.Tweet import *

# Keywords
tracks = ['-#porn']
tracks.extend(['Cyberpunk2077', '#Cyberpunk2077', 'Cyberpunk 2077'])
tracks.extend(['GenshinImpact', '#GenshinImpact', 'Genshin Impact'])
tracks.extend(['Minecraft'])
tracks.extend(['@redditdota2'])
tracks.extend(['#ESLOne'])
# tracks.extend(['TI'])
tracks.extend(['#Animajor'])
tracks.extend(['Weplay'])
tracks.extend(['Animajor'])
tracks.extend(['#fortnite'])
tracks.extend(['#Dota2'])
tracks.extend(['#DPC'])
tracks.extend(['Dota Pro Circuit'])
tracks.extend(['DPC'])
tracks.extend(['Dota 2'])
# tracks.extend(['esport'])
# tracks.extend(['e-sport'])
tracks.extend(['StardewValley'])
tracks.extend(['#Stardew'])
tracks.extend(['#StardewValley'])
# tracks.extend(['#LeagueofLegendsWildRift'])
# tracks.extend(['#lolwr'])
tracks.extend(['#Valorant'])
# tracks.extend(['League of Legends'])
# tracks.extend(['game'])
# tracks.extend(['#game'])

class StreamListener(tweepy.StreamListener):

    def __init__(self):

        super(StreamListener, self).__init__()
        self.count = 0

    def create(self, status):

        tweet = Tweet()
        tweet.tracks = tracks
        create = tweet.create(status)

        # Count inserted tweet and store to variable
        if create is True:
            self.count += 1

    def update(self, status):

        tweet = Tweet()
        tweet.tracks = tracks

        return tweet.update(status)

    def on_status(self, status):

        # Just deal with English language tweets
        if status.lang == 'en':

            tweet = Tweet()

            print(status.text)

            # Continue if tweet doesnt exist
            if not tweet.is_tweet_exists(status.id_str):

                # Send message to console
                print("! -- [{}] not found.".format(status.id_str))

                tweet.tracks = tracks

                # Is the tweet is retweeting?
                if hasattr(status, 'retweeted_status'):

                    # Send message to console
                    print("! -- [{}] is retweeting [{}].".format(status.id_str, status.retweeted_status.id_str))

                    # Save to database if retweeted status doesnt exist
                    if not tweet.is_tweet_exists(status.retweeted_status.id_str):
                        print("! -- [{}] not found.".format(status.retweeted_status.id_str))
                        self.create(status.retweeted_status)
                    else:
                        print("! -- [{}] exists.".format(status.retweeted_status.id_str))
                        self.update(status.retweeted_status)

                # Save to database if tweet doesnt exist
                self.create(status)

            else:

                # Update tweet in database
                self.update(status)

                # Is the tweet is retweeting?
                if hasattr(status, 'retweeted_status'):

                    # Update tweet in database
                    self.update(status.retweeted_status)

            # Send message to console
            print('Total {} tweet{} inserted.\n'.format(self.count, 's' if self.count > 1 else ''))

        else:

            # Send message to console
            print('Not an English tweet. Skipped.\n')

    def on_error(self, status_code):

        # Print status_code if it is 420
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
    my_stream.filter(
        track=tracks,
        is_async=True
    )


if __name__ == "__main__":
    start()
