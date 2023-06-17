from constant import FILE_PATH
import pandas as pd

def get_data():
    return pd.read_csv(FILE_PATH)
def update_data(updated_data):
    updated_data.to_csv(FILE_PATH, index=False, mode='w')
