import pandas as pd
melbourne_file_path = 'C:/Users/Margo/PycharmProjects/python-projects/Kaggle/Home prices/melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path)
print(melbourne_data.columns)
melbourne_data = melbourne_data.dropna(axis=0)