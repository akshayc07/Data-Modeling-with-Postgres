#Sparkify Postgres ETL

###Process involved in the project:
1. Data Modeling using Postgres SQL 
2. Building ETL using python 


###Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
Goal is to create a Postgres database with tables designed to optimize queries on song play analysis.Created a database schema and ETL pipeline for this analysis. 


###Data:

Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. Folder Data contains all the data folders containing all json files.


###Schema for analysis:

#####Fact Table

songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent


###### Dimension Tables 

users - users in the app
user_id, first_name, last_name, gender, level
songs - songs in music database
song_id, title, artist_id, year, duration
artists - artists in music database
artist_id, name, location, latitude, longitude
time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday
    
###Files used on the project:

data folder nested at the home of the project, where all needed jsons reside.
sql_queries.py contains all your sql queries, and is imported into the files bellow.
create_tables.py drops and creates tables. You run this file to reset your tables before each time you run your ETL scripts.
test.ipynb displays the first few rows of each table to let you check your database.
etl.ipynb reads and processes a single file from song_data and log_data and loads the data into your tables.
etl.py reads and processes files from song_data and log_data and loads them into your tables.
README.md current file, provides discussion on my project.
    
    
###Project Steps:
    
 1. Wrote CREATE, DROP statements in sql_queries.py to create each table and drop each table if it exists.
 2. Run create_tables.py to create database and tables.
 3. Followed instructions in the etl.ipynb notebook to develop ETL processes for each table. 
 4. Once verified that base steps were correct by checking with test.ipynb, filled in etl.py program.
 5. Run etl in console, and verify results:
    

 