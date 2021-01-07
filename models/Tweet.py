import json
from configs.database import Database
from configs.const import *


class Tweet(object):

    def __init__(self):

        # Connecting to database
        self.db = Database().connect()
        self.cursor = self.db.cursor()

        # Some settings for storing emoji to database
        # Still wondering why this works....
        self.cursor.execute('SET NAMES utf8mb4')
        self.cursor.execute("SET CHARACTER SET utf8mb4")

    # Inserting tweet to database
    def create(self, status):

        # SQL Insert query (INSERT INTO (1))
        sql = "INSERT INTO " \
              "tweets(" \
              "id_str, " \
              "user_id_str, " \
              "screen_name, " \
              "text," \
              "is_truncated," \
              "full_text," \
              "retweet_id_str," \
              "quoted_status_id_str," \
              "in_reply_to_screen_name," \
              "in_reply_to_status_id_str," \
              "in_reply_to_user_id_str," \
              "retweet_count," \
              "lang," \
              "hashtag," \
              "created_at)" \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            # SQL Insert query (VALUES (1))
            val = (
                status.id_str,
                status.user.id_str,
                status.user.screen_name,
                status.text if hasattr(status, 'retweeted_status') is False
                else None,
                status.truncated,
                status.extended_tweet['full_text'] if status.truncated is True
                and hasattr(status, 'retweeted_status') is False
                else None,
                status.retweeted_status.id_str if hasattr(status, 'retweeted_status') is True
                else None,
                status.quoted_status_id_str if hasattr(status, 'quoted_status_id_str') else None,
                status.in_reply_to_screen_name if hasattr(status, 'in_reply_to_screen_name') else None,
                status.in_reply_to_status_id_str if hasattr(status, 'in_reply_to_status_id_str') else None,
                status.in_reply_to_user_id_str if hasattr(status, 'in_reply_to_user_id_str') else None,
                status.retweet_count,
                status.lang,
                None,
                status.created_at,
            )

            # Executing query then commit to database
            self.cursor.execute(sql, val)
            self.db.commit()

            # [4 Mar 19] - Deactivated
            # # Then, open tweets.txt to store 'inserted tweet'
            # with open(EXPERIMENT_PATH + 'e4/tweets.txt', 'a') as out:
            #     # With json format
            #         out.write(json.dumps(status._json, sort_keys=True, indent=4))
            #         out.write(',\n')

            print("{} inserted.".format(status.id_str))
            return True
        except Exception as e:
            print('Exception:')
            with open(EXPERIMENT_PATH + EXPERIMENT_FOLDER + 'errors.txt', 'a') as out:
                out.write(str(e))
                out.write(',\n')
                out.write(json.dumps(status._json, sort_keys=True, indent=4))
                out.write('\n\n')
            print(e)
            self.db.rollback()
            return False

    # Updating tweet to database
    def update(self, status):

        try:
            # TODO add favorite_count
            sql = "UPDATE tweets SET retweet_count = '%s' WHERE id_str = '%s'" % (
                status.retweet_count, status.id_str)

            self.cursor.execute(sql)
            print("{} updated.".format(status.id_str))
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            print("Error: unable to update data")
            print('Exception:' + e)

    # Check if tweet already exist by id_str
    def is_tweet_exist(self, id_str):

        sql = "SELECT id_str FROM tweets WHERE id_str = '%s'" % id_str

        try:
            self.cursor.execute(sql)
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            # Should returns 0, but exception makes me doubt
            return False
