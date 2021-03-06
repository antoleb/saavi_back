import os
from pathlib import Path

current_path = str(Path(__file__).parent.absolute())

raw_data_directory = current_path + '/../data/'
os.makedirs(raw_data_directory, exist_ok=True)

raw_data_path = raw_data_directory + '/final_transaction_table.csv'
raw_zipped_data_path = current_path + '/../data/final_transaction_table.csv.zip'
raw_data_web_path = 'https://sandbox.apis.op-palvelut.fi/junction/v2020/datasets/transactions'

zip_file_path = current_path + '/../data/final_transaction_table.csv.zip'
post_processed_data_path = current_path + '/../data/final_transaction_table_post_processed.csv'

subscription_dataset_path = current_path + '/../resourses/new_sub.csv'
