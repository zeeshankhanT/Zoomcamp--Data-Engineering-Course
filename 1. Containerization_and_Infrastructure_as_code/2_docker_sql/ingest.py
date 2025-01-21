import pandas as pd
from sqlalchemy import create_engine

df_iter = pd.read_csv('green_tripdata_2019-10.csv', iterator=True, chunksize=100000)

df = next(df_iter)
df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Create table
df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')

# Insert first chunk
df.to_sql(name='green_taxi_data', con=engine, if_exists='append')

# Insert remaining data
while True: 
    try:
       
        df = next(df_iter)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)    
        df.to_sql(name='green_taxi_data', con=engine, if_exists='append')

        print('inserted another chunk')
    except StopIteration:
        print('completed')
        break