import pandas as pd

# Läs in Excel-filerna
df1 = pd.read_excel("./live_music_events12.xlsx")
df2 = pd.read_excel("./live_music_events13.xlsx")

# Lägg till kolumn för ursprunglig radposition
df1['OriginalRow_df1'] = df1.index + 2  # Antag att det finns en rubrik, så data börjar på rad 2 i Excel
df2['OriginalRow_df2'] = df2.index + 2  # Samma antagande här

# Filtrera df1 för 'LIVEMUSIK'
df1_livemusik = df1[df1['Label'] == 'LIVEMUSIK']

# Gör en sammanfogning
combined_df = pd.merge(df1_livemusik, df2, on='EveNamn', how='left', suffixes=('', '_df2'), indicator=True)

# Beräkna om det finns skillnader i 'Label' mellan df1 och df2
combined_df['label_diff'] = combined_df.apply(lambda row: row['Label'] != row['Label_df2'] if pd.notnull(row['Label_df2']) else False, axis=1)

# Hitta rader där 'Label' skiljer sig mellan df1 och df2, samt rader som endast finns i df1
label_diffs = combined_df[combined_df['label_diff'] | (combined_df['_merge'] == 'left_only')]

# Exportera till Excel, inkluderar OriginalRow_df1 för att visa ursprungliga radnumret i df1
label_diffs.to_excel('label_diffs_including_original_rows.xlsx', index=False)

print(f"Antal 'LIVEMUSIK'-rader i df1: {df1_livemusik.shape[0]}")
print(f"Totalt antal rader i combined_df: {combined_df.shape[0]}")
print(f"Antal rader med skillnader + saknas i df2: {label_diffs.shape[0]}")
