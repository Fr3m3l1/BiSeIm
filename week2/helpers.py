import os
import glob
import pandas as pd

def load_emotibit_ppg(data_dir):
    """ 
    Load the emotibit PPG data from the given directory and return a dataframe with the PPG data.

    Parameters:
    data_dir (str): The path to the directory containing the data.

    Returns:
    pd.DataFrame: A dataframe containing the PPG data.
    """
    file_list = sorted(glob.glob(os.path.join(data_dir, '*.csv')))
    ppg_data = pd.DataFrame()
    col_map = {"PG": "PPG Green", "PI": "PPG Infrared", "PR": "PPG Red"}

    for path in file_list:
        col_name = path.split('.')[-2][-2:]
        if col_name in col_map:
            df = pd.read_csv(path, usecols=[col_name, 'LocalTimestamp'])
            df['Timestamp'] = pd.to_datetime(df['LocalTimestamp'], unit='s')
            df.drop(columns=['LocalTimestamp'], inplace=True)
            df.set_index('Timestamp', inplace=True)
            df.rename(columns={col_name: col_map[col_name]}, inplace=True)
            ppg_data = pd.concat([ppg_data, df], axis=1)
    ppg_data.index.name = None

    return ppg_data