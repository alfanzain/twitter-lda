# General imports
from configs.const import *

# Third party imports
import pymysql


class Database:

    # def __init__(self):
    #
    #     # Connecting to database
    #     self.db = Database().connect()
    #     self.cursor = self.db.cursor()
    #
    #     # Some settings for storing emojis to database
    #     # Still wondering why this works....
    #     self.cursor.execute('SET NAMES utf8mb4')
    #     self.cursor.execute("SET CHARACTER SET utf8mb4")

    @staticmethod
    def connect():
        # Open database connection
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWD,
            db=DB_DB,
            charset=DB_CHARSET
        )

    # def createDatable():


        # query = "CREATE DATABASE " + DB_DB


    # def createTables():


        # # Table: Tweets
        # query = "CREATE TABLE `tweets` (" \
        #             "`id_str` varchar(255) NOT NULL, " \
        #             "user_id_str varchar(255), " \
        #             "screen_name varchar(255), " \
        #             "text text," \
        #             "is_truncated varchar(100)," \
        #             "full_text text," \
        #             "retweet_id_str varchar(255)," \
        #             "quoted_status_id_str varchar(255)," \
        #             "in_reply_to_screen_name varchar(255)," \
        #             "in_reply_to_status_id_str varchar(255)," \
        #             "in_reply_to_user_id_str varchar(255)," \
        #             "retweet_count int(9)," \
        #             "lang varchar(10)," \
        #             "hashtag varchar(255)," \
        #             "created_at varchar (255))" \
        #             "PRIMARY KEY ('id_str')" \
        #         ") ENGINE=InnoDB DEFAULT" \
        #         "CHARSET=utf8mb4" \
        #         "COLLATE=utf8mb4_bin" \
        #         "AUTO_INCREMENT=1"
