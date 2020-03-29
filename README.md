## Purpose ##
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is  interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
<br>
The purpose of this data engineering project is to create a Postgress database with tables designed to optimise capabilities in song play analytics. My task is to create a database schema and ETL pipeline for this analysis. 
<br>
## Datasets ##
<br>
#### Song Dataset ####
<br>
The first dataset is a subset of real data from the Million Song Dataset.
<br>
Each file is in JSON format and contains metadata about a song and the artist of that song. 
<br>
The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

` {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}`

#### Log Dataset ####
<br>
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. 
<br>
These simulate activity logs from a music streaming app based on specified configurations.
<br>
The log files in the dataset I'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

`log_data/2018/11/2018-11-12-events.json`

`log_data/2018/11/2018-11-13-events.json`

## Schema ##
<br>
I will create a **star schema* for this project with **1** Fact table and **4** Dimension Tables
<br>
## Fact Table ##
<br>
### songplays table ###
<br>
- Records in log data associated with song plays i.e. records with page NextSong
<br>
1. songplay_id INT PRIMARY KEY
<br>
2. start_time TIMESTAMP
<br>
3. user_id INT
<br>
4. level VARCHAR
<br>
5. song_id VARCHAR
<br>
6. artist_id VARCHAR
<br>
7. sessio INT
<br>
8. location VARCHAR
<br>
9. user_agent VARCHAR
<br>
<br>
## Dimesion Tables ##
<br>
#### users ####
<br>
- Users in the app
<br>
1. user_id INT PRIMARY KEY
<br>
2. first_name VARCHAR
<br>
3. last_name VARCHAR
<br>
4. gender VARCHAR
<br>
5. level VARCHAR
<br>


#### songs ####
<br>
- Songs in music database
<br>
1. song_id VARCHAR PRIMARY KEY 
<br>
2. title VARCHAR
<br>
3. artist_id VARCHAR
<br>
4. year INT
<br>
5. duration NUMBERIC 
<br>

#### artists ####
<br>
- Artists in music database
<br>
1. artist_id VARCHAR PRIMARY KEY 
<br>
2. name VARCHAR
<br>
3. location VARCHAR
<br>
4. latitude FLOAT
<br>
5. longitude FLOAT
<br>
#### time ####
<br>
- Timestamps of records in songplays broken down into specific units
<br>
1. start_time TIMESTAMP PRIMARY KEY
<br>
2. hour INT
<br>
3. day INT
<br>
4. week INT
<br>
5. month INT
<br>
6. year INT
<br>
7. weekday INT
<br>
## ETL Processes ##
In order to create tables, first of all I connect to the Sparkify database, then use the `CREATE` SQL statement to create  the 5 tables above.
<br>

### Dimension Table ###
<br>
## songs and artists tables ##
<br>
I extract all the song data from the JSON files using `get_files`. 

1. `songs_data`

- Select the columns that I need from the JSON files and turn these columns info a dataframe. 
<br>
- Then I insert all the song data row by row into the `song` table that I previously greated.

2. `artists_data`

- Select the columns that I need from the JSON files and turn these columns info a dataframe. 
<br>
- Then I insert all the artists' data row by row into the `artists` table that I previously greated.
<br>
## time and users tables ##
1. `time data`

- Select the data in the `ts` column, use `to_datetime` to turn the timestamp data from miliseconds to datetime.
<br>
- Use `datetime` functions to break the timestamp in to *hour,day, week, month, year, weekday*
<br>
- Then I insert all the time data row by row into the `time` table that I previously greated.


2. `users data`

- Select the columns that I need from the JSON files and turn these columns info a dataframe. 
<br>
- Then I insert all the users' data row by row into the `users` table that I previously greated.
<br>
## Fact Table ##
<br>

`song play table`
<br>
1. To create a fact table we need to join the `songs` and `artists` tables to get the song_id and artist_id in once place. 
<br>
2. Get all the other relevant data from the log data file 
<br>
3. Insert the data row by row into the `song play table` I previously created
<br>
### File Structure ###

`create_tables.py` - Drops and create tables in database

`etl.ipynb` - Reads and processes a single file from song_data and log_data and loads the data into tables

`etl.py` - Reads and processes multiple files from song_data and log_data and loads them into tables, responsible for the ETL job

`sql_queries.py` - Contains all sql queries, and is imported into the last three files above.

`test.ipynb` - Shows first few rows of each table after I create those tables successfully in database, the main point of this file is to validate my process
<br>
### Running the Python Scripts ###
<br>
To create the database and table structure, run the following command:
<br>
`!python create_tables.py`
<br>
To parse the log files, run the following command:
<br>
`!python etl.py`# data_modelling_with_postgres
