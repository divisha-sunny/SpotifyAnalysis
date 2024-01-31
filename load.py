import extract
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///tracks.sqlite"

if __name__ == "__main__":

#Importing the songs_df from the Extract.py
    load_df=extract.unique_df

#Loading into Database
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('tracks.sqlite')
    cursor = conn.cursor()

    #SQL Query to Create Played Songs
    sql_query_1 = """
    CREATE TABLE IF NOT EXISTS tracks(
        Track_ID             VARCHAR(200),
        Track_name           VARCHAR(200),
        Artist_name          VARCHAR(200),
        Popularity_score     INT,
        Release_year         VARCHAR(200),
        Genre                VARCHAR(200),
        danceability        FLOAT,
        energy              FLOAT,
        key                  INT,
        loudness            FLOAT,
        mode                 INT,
        speechiness         FLOAT,
        acousticness        FLOAT,
        instrumentalness    FLOAT,
        liveness            FLOAT,
        valence             FLOAT,
        tempo               FLOAT,
        type                 VARCHAR(200),
        id                   VARCHAR(200),
        uri                  VARCHAR(200),
        track_href           VARCHAR(200),
        analysis_url         VARCHAR(200),
        duration_ms         INT,
        time_signature      INT,
        CONSTRAINT primary_key_constraint PRIMARY KEY (Track_ID)
    );
"""
    cursor.execute(sql_query_1)
    print("Opened database successfully")

    #We need to only Append New Data to avoid duplicates
    try:
        load_df.to_sql("tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    #cursor.execute('DROP TABLE tracks')
    #cursor.execute('DROP TABLE fav_artist')

    conn.close()
    print("Close database successfully")