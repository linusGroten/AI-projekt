import pandas as pd

ROWS_TO_KEEP= 10000

df = pd.read_csv("./projekt/data/grouped_data_with_liverelevans_cleaned.csv")

df_reduceed=df.head(ROWS_TO_KEEP)

df_reduceed.to_csv(f"./projekt/data/grouped_data_with_liverelevans_cleaned_{ROWS_TO_KEEP}.csv", index=False)
