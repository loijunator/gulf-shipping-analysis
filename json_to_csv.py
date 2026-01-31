import pandas as pd
import json
import os
import glob

json_dir = 'scraped_jsons/'
json_files = glob.glob(os.path.join(json_dir, '*json')) 

dfs = []

for file_path in json_files:
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    vessels = json_data['data']['rows']

    #create temp df and set index??? why
    temp_df = pd.DataFrame(vessels)
    temp_df.set_index('SHIP_ID', inplace=True)

    dfs.append(temp_df)

combined_df = pd.concat(dfs, axis=0, sort=False)

combined_df.to_csv('all_ships.csv')
