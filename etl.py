import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """
    Description: This fuction reads the information stored in the song data in JSON format row by row and saves data into two datasets: song_data and artist_data

    Arguments:
    cur: the cursor object. 
    filepath: song data file path. 

    Returns:
    None
    """
    # This fuction reads the information of song_data stored in a JSON files row by row and saves data into two datasets: song_data and artist_data
    # Arguments:
    # cursor: Dabase cursor 
    #filepath: location of file in dir
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data =  df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This fuction reads the information stored in log data in JSON format row by row and saves data into two datasets: time_data and user_data

    Arguments:
    cur: the cursor object. 
    filepath: log data file path. 

    Returns:
    None
    """"
    # This fuction reads the information of song_data stored in a JSON files row by row and saves data into two datasets: time_data and user_data
    # Arguments:
    # cursor: Dabase cursor 
    #filepath: location of file in dir
    # open log file
    df= pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query('page == "NextSong"')

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    time_data = list(zip(list(t),list(t.dt.hour),list(t.dt.day),list(t.dt.weekofyear),list(t.dt.month),list(t.dt.year),list(t.dt.dayofweek) ))
    column_labels =['timestamp','hour','day','week','month','year','weekday']
    time_df = pd.DataFrame(data=time_data,columns = column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        
        songplay_data = (index,pd.to_datetime(row['ts'],unit='ms'),row.userId,row.level, songid, artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This fuction gets all the matching files from the directory

    Arguments:
    all_files: get all files in directory
    

    Returns:
    num_files: find the total number of files in directory. 
    datafile: show number of files processed 
    """"
   
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()