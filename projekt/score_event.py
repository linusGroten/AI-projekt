import pandas as pd
def calculate_score(row):
    score = 0
    keywords = ['livemusik', 'band', 'live', 'scen', 'bandet', 'album', 'konsert', 
                'rock', 'låtar', 'sång', 'trummor', 'gitarr', 'scenen', 'musiken', 'bas', 'artister', 'jazz', 
                'sound', 'albumet', 'konserten', 'förköp', 'piano', 'show', 'pop', 'musiker', 'artist', 'blues', 
                'ep', 'konserter', 'skivan', 'spelningar', 'publik', 'turné', 'records', 'bandets']  # LISTA KEYWORDS HÄR
    category_keywords = ['Band', 'Musician', 'Choir', 'Musician/band', 'Artist', 'Orchestra', 'Live Music Venue', 'Musician/band', 'Music', 'Jazz & Blues Club', 'Musician/band • Orchestra',  'Record Label', 'Record label', 'Concert Tour', 'Live music venue', 'Concert Venue', 'Concert Band'] # ORG KATEGORIER
    category_keywords_second = ['Performing Arts', 'Arts & entertainment', 'night_club', 'Entertainment website • Event Planner • Talent Agent', 'Performance art theatre', 'Performance & Event Venue', 'Tour Agency', 'Music Lessons & Instruction School', 'Arts/Entertainment/Nightlife', 'album', 'Performing arts'] # ORG lvl 2 KATEGORIER
    loc_keywords = ['Performance Art Theatre', 'Arts & entertainment', 'Live Music Venue', 'Pub',  'Performance & Event Venue','Arts/Entertainment/Nightlife', 'Concert venue', 'Performing Arts', 'Jazz & Blues Club', 'Music Lessons & Instruction School', 'Musician']
    
    def exact_match(keyword, text):
        return any(f" {keyword} " in f" {text} ".lower() for keyword in keywords)
 
    if any(exact_match(keyword, row['EveNamn']) for keyword in keywords):
        score += 2
        
    if any(exact_match(keyword, row['EveBesk']) for keyword in keywords):
        score += 1.5
        
    negative_words = ['Dansshow', 'trip', 'film', '%quiz', 'lag', 'Ställ', 'informationskväll', 'Dropin', 'Föreläsning', 'Samtal', 'Padel', 'Föreläsare', 'tränar', 'Tävlas', 'Tävling', 'Meet', 'Movie', 'raser', 'workshop', 'mål', 'yoga', 'intensivkurs', 'kurs', 'spelare', 'liga']
    if any(word.lower() in row['EveBesk'].lower() for word in negative_words):
        score -= 3
 
    if pd.notna(row['Event Lineup']):
        lineup_values = row['Event Lineup'].split(',')  
        for value in lineup_values:
            if value.strip():  
                score += 0.5
 
    if isinstance(row['Organizer Category'], str) and any(category_keyword in row['Organizer Category'] for category_keyword in category_keywords):
        score += 2
        
    if isinstance(row['Organizer Category'], str) and any(category_keyword_second in row['Organizer Category'] for category_keyword_second in category_keywords_second):
        score += 1
        
    if isinstance(row['Location Category'], str) and any(loc_keyword in row['Location Category'] for loc_keyword in loc_keywords):
        score += 0.5
 
    return score
 
#df['score'] = df.apply(calculate_score, axis=1)
 
#print(df)
 
output_file = "output_with_score_2024_1.xlsx"
#df.to_excel(output_file, index=False)