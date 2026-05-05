import pandas as pd
import numpy as np
import os

def prepare_tft_dataset(input_folder, output_file):
    all_data = []
    UPDATE_DATE = pd.to_datetime('2025-10-22')

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):

            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)
            
            item_id = filename.replace(".csv", "")
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').set_index('date')

            full_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

            df = df.reindex(full_range)

            df['is_synth'] = df['price'].isna().astype(int)

            df['price'] = df['price'].ffill()

            df['volume'] = df['volume'].fillna(0)

            df = df.reset_index().rename(columns={'index': 'date'})
            df['item_id'] = item_id
            df['afterUpdate'] = (df['date'] >= UPDATE_DATE).astype(int) #

            all_data.append(df)

    master_df = pd.concat(all_data, ignore_index=True)
    master_df.to_csv(output_file, index=False)
    print(f"Preprocessed Data into a Master File")