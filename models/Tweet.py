import json
from configs.database import Database
from configs.const import *
from pathlib import Path
from datetime import datetime


class Tweet(object):

    tracks = []

    def __init__(self):

        # Connect to database
        self.db = Database().connect()
        self.cursor = self.db.cursor()

        # Some settings for storing emoji to database
        # Still wondering why this works....
        self.cursor.execute('SET NAMES utf8mb4')
        self.cursor.execute("SET CHARACTER SET utf8mb4")

    # Insert tweet to database
    def create(self, status):

        # SQL query for new tweet
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

            # Value of the query
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

            # Send message to console
            print("! -- Inserting [{}].".format(status.id_str))

            # Execute query then commit to database
            self.cursor.execute(sql, val)
            self.db.commit()

            # Send message to console
            print("+ -- [{}] inserted.".format(status.id_str))

            return True

        except Exception as e:

            # Rollback last committed query
            self.db.rollback()

            # Send message to console
            print("Error: unable to insert data")
            print('Exception:' + e)

            # Log error and tweet json
            now = datetime.now()
            txt_file_name = now.strftime("%H_%M_%S") + ".txt"

            Path(EXPERIMENT_PATH + EXPERIMENT_FOLDER).mkdir(parents=True, exist_ok=True)

            with open(EXPERIMENT_PATH + EXPERIMENT_FOLDER + txt_file_name, 'w+') as out:
                out.write(str(e))
                out.write(',\n')
                out.write(json.dumps(status._json, sort_keys=True, indent=4))
                out.write('\n\n')

            return False

    # Update tweet to database
    def update(self, status):

        tracks = None

        # SQL query to find existing tweet non-null tracks value
        sql = "SELECT tracks FROM tweets WHERE id_str = '%s' AND tracks IS NOT NULL" % status.id_str

        try:

            # Execute query then get the first row
            self.cursor.execute(sql)
            row = self.cursor.fetchone()

            # If the tracks value is not current streamer tracks value,
            #   then save the concatenation of the last tracks and the current tracks
            # Otherwise,
            #   save the current tracks
            if row is not None and row[0] != str(self.tracks):
                tracks = str(self.tracks) + "," + str(row[0])
            else:
                tracks = str(self.tracks)

        except Exception as e:

            # Send message to console
            print("Error: unable to find tracks data")
            print('Exception:' + e)

            # Should returns 0, but exception makes me doubt
            return False

        try:

            # SQL query for update tweet
            sql = "UPDATE tweets " \
                  "SET " \
                  "retweet_count = %s, " \
                  "tracks = %s " \
                  "WHERE id_str = %s"

            # Send message to console
            print("! -- Updating [{}].".format(status.id_str))

            # Execute query then commit to database
            self.cursor.execute(sql, (status.retweet_count, tracks, status.id_str))
            self.db.commit()

            # Send message to console
            print("* -- [{}] updated.".format(status.id_str))

        except Exception as e:

            # Rollback last committed query
            self.db.rollback()

            # Send message to console
            print("Error: unable to update data")
            print('Exception:' + e)

    # Check if tweet already exists by id_str
    def is_tweet_exists(self, id_str):

        # SQL query for check is tweet exists
        sql = "SELECT id_str FROM tweets WHERE id_str = '%s'" % id_str

        try:

            # Execute query
            self.cursor.execute(sql)

            # Return row count
            return self.cursor.rowcount

        except Exception as e:

            # Send message to console
            print("Error: unable to check existing data")
            print('Exception:' + e)

            # Should returns 0, but exception makes me doubt
            return False
