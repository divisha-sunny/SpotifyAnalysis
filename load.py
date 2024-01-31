import main
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