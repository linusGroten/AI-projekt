import pandas as pd
import re
from string import punctuation          

file_path = './projekt/data/grouped_data_with_liverelevans_cleaned .xlsx'

df = pd.read_excel(file_path)
for column in df.columns:
    if df[column].dtype == object:  
        df[column] = df[column].astype(str) 
        df[column] = df[column].apply(lambda x: re.sub("[%s]" % re.escape(punctuation), "", x))


csv_file_path = "./projekt/data/grouped_data_with_liverelevans_cleaned.csv"

df.to_csv(csv_file_path, index=False,encoding='utf-8', quotechar='"')


