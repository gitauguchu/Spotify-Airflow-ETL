import extract
import transform 
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json 
from datetime import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

if __name__ == "__main__":
    #Importing the songs_df from extract.py
    load_df = extract.return_dataframe()
    if(transform.Data_Quality(load_df) == False):
        raise ("Failed at data validation")
    Transformed_df = transform.Transform_df(load_df)
    #The two data frames that need to be loaded into the database

    #Loading into the database
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    #SQL Query to create played songs
    sql_query_1 = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY_KEY (played_at)
        )
    """

    #SQL Query to create the most listened artist
    sql_query_2 = """
    CREATE TABLE IF NOT EXISTS fav_artist(
        timestamp VARCHAR(200),
        ID VARCHAR(200),
        artist_name VARCHAR(200),
        count VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (ID)
    )
    """
    cursor.execute(sql_query_1)
    cursor.execute(sql_query_2)
    print("Opened database successfully")

    #We need to only append new data to avoid duplicates
    try:
        load_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")
    try:
        Transformed_df.to_sql("fav_artist", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database 2")

    conn.close()
    print("Closed database successfully")