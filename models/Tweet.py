import json
from configs.database import Database
from configs.const import *
from pathlib import Path
from datetime import datetime


class Tweet(object):

    tracks = []

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

        # SQL Insert query (INSERT INTO tweets)
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
              "created_at," \
              "tracks)" \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            # SQL Insert query (VALUES ())
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
                str(self.tracks)
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

            now = datetime.now()
            txt_file_name = now.strftime("%H_%M_%S") + ".txt"

            Path(EXPERIMENT_PATH + EXPERIMENT_FOLDER).mkdir(parents=True, exist_ok=True)
            Path(txt_file_name).touch(exist_ok=True)

            with open(EXPERIMENT_PATH + EXPERIMENT_FOLDER + txt_file_name, 'w+') as out:
                out.write(str(e))
                out.write(',\n')
                out.write(json.dumps(status._json, sort_keys=True, indent=4))
                out.write('\n\n')
            print(e)
            self.db.rollback()
            return False

    # Update tweet to database
    def update(self, status):
        tracks = None

        sql = "SELECT tracks FROM tweets WHERE id_str = '%s' AND tracks IS NOT NULL" % status.id_str

        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()

            if row is not None and row[0] != str(self.tracks):
                # print("Current tracks : {}".format(self.tracks))
                # print("Status tracks  : {}".format(row[0]))

                tracks = str(self.tracks) + "," + str(row[0])
            else:
                tracks = str(self.tracks)

        except Exception as e:
            print(str(e))
            # Should returns 0, but exception makes me doubt
            return False

        try:
            # TODO add favorite_count
            # TODO add tracks
            sql = "UPDATE tweets " \
                  "SET " \
                  "retweet_count = %s, " \
                  "tracks = %s " \
                  "WHERE id_str = %s"

            print("Updating {}.".format(status.id_str))
            self.cursor.execute(sql, (status.retweet_count, tracks, status.id_str))
            print("{} updated.".format(status.id_str))
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            print("Error: unable to update data")
            print('Exception:' + e)

    # Check if tweet already exists by id_str
    def is_tweet_exist(self, id_str):

        sql = "SELECT id_str FROM tweets WHERE id_str = '%s'" % id_str

        try:
            self.cursor.execute(sql)
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            # Should returns 0, but exception makes me doubt
            return False