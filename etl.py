import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    song_files=get_files(filepath)
    song_files_iterator=iter(song_file)
    file=next(song_files_iterator)
    df = read_json(file, lines=True)
    for song_file in song_files_iterator:
        df.append(read_json(song_file, lines=True),ignore_index=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude','artist_longitude']]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    log_file=get_files(file_path)
    log_files_iterator=iter(log_file)
    file=next(log_files_iterator)
    df=read_json(log_file)
    for log_file in log_file_iterator:
        df.append(read_json(log_file, line=True),ignore_index=True)


    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t =pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    time_data = []
    for time in t:
        time_data.append([time,time.hour,time.day,time.week,time.month,time.year,time.day_name()])
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')

    time_df = pd.DataFrame(time_data,columns=column_labels)
    cur.execute(time_df, time_table_insert)

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
songplay_data = (index, pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId,row.location,\ row.userAgent)
    cur.execute(songplay_table_insert, songplay_data)
    conn.commit()


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
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