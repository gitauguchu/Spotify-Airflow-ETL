import extract
import pandas as pd

#Set of data quality checks needed to perform before loading
def Data_Quality(load_df):
    #Checking whether the dataframe is empty
    if load_df.empty:
        print("No songs extracted")
        return False
    
    #Enforcing primary keys since we don't need duplicates
    if pd.Series(load_df['played_at']).is_unique:
        pass
    else:
        #The reason for using an exception is to immediately terminate the program and avoid further processing
        raise Exception("Primary key exception, data might contain duplicates")
    
    #Checking for nulls in our dataframe
    if load_df.isnull().values.any():
        raise Exception("Null values found")
    
#Writing some transformation queries to get the count of artist
def Transform_df(load_df):
    #Applying the transformation logic
    Transformed_df = load_df.groupby(['timestamp', 'artist_name'], as_index=False).count()
    Transformed_df.rename(columns={'played_at':'count'}, inplace=True)

    #Creating a primary key based on timestamp and artist name
    Transformed_df["ID"] = Transformed_df['timestamp'].astype(str) +"-"+ Transformed_df["artist_name"]

    return Transformed_df[['ID', 'timestamp', 'artist_name', 'count']]

if __name__ == "__main__":
    #Importing the songs_df from extract.py
    load_df = extract.return_dataframe()
    Data_Quality(load_df)
    #Calling the transformation
    Transformed_df=Transform_df(load_df)
    print(Transformed_df)