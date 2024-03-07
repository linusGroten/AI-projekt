from npl_step import clean_text
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd


df = pd.read_csv(f"./projekt/data/grouped_data_with_liverelevans_cleaned.csv")


class Event_Score:
    #funktions innehåll syftar till att skapa en komplett representation av ett evenemang 
    def __init__(self, eve_namn, eve_besk,eve_relevance):
        self.eve_namn = eve_namn
        self.eve_besk = eve_besk
        self.eve_relevance = eve_relevance
        #self.original_score = score
        self.cleaned_data_text = clean_text(f"{eve_namn}, {eve_besk}")
        self.score= self.calculate_score()
        self.lable = self.assign_lable()

    #Räknar ut poäng baserat på ord som används som vikter för AI-modellen.
    def calculate_score(self):
        keyword_score= 0
        neg_keyword_score = 0
        keyword = ['livemusik', 'band', 'live', 'scen', 'bandet', 'album', 'konsert','blues','storband', 
                'rock', 'låtar', 'sång', 'trummor', 'gitarr', 'scenen', 'musiken', 'bas', 'artister', 'jazz', 
                'sound', 'albumet', 'konserten', 'förköp', 'piano', 'show', 'pop', 'musiker', 'artist', 'blues', 
                'ep', 'konserter', 'skivan', 'spelningar', 'publik', 'turné', 'records', 'bandets','musik',
                'Band', 'Musician', 'Choir', 'Musician/band', 'Artist', 'Orchestra', 'Live Music Venue', 'Musician/band', 'Music', 'Jazz & Blues Club', 'Musician/band • Orchestra',  'Record Label', 'Record label', 'Concert Tour', 'Live music venue', 'Concert Venue', 'Concert Band', 'gospel','sings'] 
        
        neg_keywords = [ 'Dans','Dansshow', 'trip', 'film', 'quiz', 'lag', 'Ställ', 'informationskväll', 'Dropin', 'Föreläsning', 'Samtal', 'Padel', 'Föreläsare', 'tränar', 'Tävlas', 'Tävling', 'Meet', 'Movie', 'raser', 'workshop', 'mål', 'yoga', 'intensivkurs', 'kurs', 'spelare', 'liga','comedy','politik','EU',
                        'bio','cinema','modevisning','avsnitt','bio','forskare','seminar','springa','springer','podd','samtal', 'Painting','yrken','böcker','bok','aktiviteter']
        for keyword in keyword:
            if keyword.lower() in self.cleaned_data_text:
                keyword_score  += 1
        
        for keyword in neg_keywords:
            if keyword.lower() in self.cleaned_data_text:
                neg_keyword_score-=1

        
        
        additinal_score = self.eve_relevance /1000

        total_score = keyword_score + neg_keyword_score + additinal_score 

        return total_score
    
    def assign_lable(self):

        threshold = 1.5
        return  "LIVEMUSIK" if self.score > threshold else" EJ LIVEMUSIK"



liveevents=[]

for index, row in df.iterrows():
    event =Event_Score(row["EveNamn"], row["EveBesk"], row["Event Relevance"])
    liveevents.append(event)
        
# förbereda datamängd för träning och testning av , test_size=0.2 anger att 20% av datamängden ska användas för testning, medan de återstående 80% används för träning.
#random_state=42 är en parameter som säkerställer att uppdelningen är reproducerbar;
training_data, test_data = train_test_split(liveevents, test_size=0.2, random_state=42)
 #.train_X Detta är input-variablerna som modellen kommer att träna på
train_X = [event.cleaned_data_text for event in training_data]
# train_Y Detta är "labels" eller målvariablerna som modellen kommer att försöka förutsäga
train_Y = [event.lable for event in training_data]

# test_X innehåller de bearbetade texterna som används som input till modellen för att göra förutsägelser, och test_Y innehåller de korrekta etiketterna som används för att utvärdera modellens förutsägelser.
test_X = [event.cleaned_data_text for event in test_data]
test_Y = [event.lable for event in test_data]

# ngram_range=(1,2)hjälper modellen att fånga upp både enskilda ord och deras sammanhang när de förekommer tillsammans. max_features=5000, begränsar antalet funktioner till de 5000 mest frekventa orden som finns i din träningsdatamängd
tfidf_vectorizer =TfidfVectorizer(ngram_range=(1,2), max_features=5000, preprocessor=clean_text)
tfidf_vectors = tfidf_vectorizer.fit_transform(train_X)
clf = SVC(C=10, kernel="rbf",class_weight='balanced' ) # . Detta hjälper till att ge mer vikt åt minoritetsklassen under träningen. efter som det är en obalans i data
clf.fit(tfidf_vectors, train_Y)

#Används för att ta testa och ta fram de bästa inställningarna för modell 
#param_grid = {
#    'kernel': ['linear', 'rbf', 'poly'],
#    'C': [0.1, 1, 10, 100]
#}

#grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring="accuracy")
#grid_search.fit(tfidf_vectors, train_Y)
#print("Bästa parametrarna:", grid_search.best_params_)
#print("Bästa noggrannheten:", grid_search.best_score_)
#best_params = grid_search.best_params_
#clf_best = SVC(kernel=best_params['kernel'], C=best_params['C'])

test_vectors = tfidf_vectorizer.transform(test_X)
prediction = clf.predict(test_vectors)

live_music_count = sum(event.lable == "LIVEMUSIK" for event in liveevents)

print(f"Antal evenemang märkta som LIVEMUSIK: {live_music_count}")

# Beräkna noggrannheten
accuracy = accuracy_score(test_Y,prediction)
print(f"Noggrannhet: {accuracy}")

# Fullständig klassificeringsrapport
report = classification_report(test_Y, prediction)
print("Klassificeringsrapport:\n", report)

event_df = pd.DataFrame([{
    "EveNamn" : event.eve_namn,
    "EveBesk" : event.eve_besk,
    "Event Relevance" : event.eve_relevance,
    'Cleaned Text': event.cleaned_data_text,
    "Score": event.score,
    "Label": event.lable
}for event in liveevents])


for i, event in enumerate(test_X):
    event_df.loc[event_df["Cleaned Text"]== event, "Predicted Label"] = prediction[i]

    # Ta bort eventuella dubbletter
df = df.drop_duplicates()
event_df = event_df.drop_duplicates()

# Sammanfoga de ursprungliga data med de nya resultaten
combined_df = pd.merge(df, event_df, on=["EveNamn", "EveBesk", "Event Relevance"], how="left")
#samlar datan i en ny excel
combined_df.to_excel("live_music_events14.xlsx", index=False)
