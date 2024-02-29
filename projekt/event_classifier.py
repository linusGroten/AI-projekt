from npl_step import clean_text
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import math
import pandas as pd


df = pd.read_csv(f"./projekt/data/grouped_data_with_liverelevans_cleaned_10000.csv")


class Event_Score:
    def __init__(self, eve_namn, eve_besk,eve_relevance):
        self.eve_namn = eve_namn
        self.eve_besk = eve_besk
        self.eve_relevance = eve_relevance
        #self.original_score = score
        self.cleaned_data_text = clean_text(f"{eve_namn}, {eve_besk}")
        self.score= self.calculate_score()
        self.lable = self.assign_lable()

    def calculate_score(self):
        keyword_score= 0
        neg_keyword_score = 0
        keyword = ['livemusik', 'band', 'live', 'scen', 'bandet', 'album', 'konsert', 
                'rock', 'låtar', 'sång', 'trummor', 'gitarr', 'scenen', 'musiken', 'bas', 'artister', 'jazz', 
                'sound', 'albumet', 'konserten', 'förköp', 'piano', 'show', 'pop', 'musiker', 'artist', 'blues', 
                'ep', 'konserter', 'skivan', 'spelningar', 'publik', 'turné', 'records', 'bandets'
                'Band', 'Musician', 'Choir', 'Musician/band', 'Artist', 'Orchestra', 'Live Music Venue', 'Musician/band', 'Music', 'Jazz & Blues Club', 'Musician/band • Orchestra',  'Record Label', 'Record label', 'Concert Tour', 'Live music venue', 'Concert Venue', 'Concert Band'] 
        
        neg_keywords = [ 'Dans''Dansshow', 'trip', 'film', 'quiz', 'lag', 'Ställ', 'informationskväll', 'Dropin', 'Föreläsning', 'Samtal', 'Padel', 'Föreläsare', 'tränar', 'Tävlas', 'Tävling', 'Meet', 'Movie', 'raser', 'workshop', 'mål', 'yoga', 'intensivkurs', 'kurs', 'spelare', 'liga']
        for keyword in keyword:
            if keyword.lower() in self.cleaned_data_text:
                keyword_score  += 1
        
        for keyword in neg_keywords:
            if keyword.lower() in self.cleaned_data_text:
                neg_keyword_score-=2

        
        #log_relevance_score = math.log(self.eve_relevance + 1)
        additinal_score = self.eve_relevance /1000

        total_score = keyword_score + neg_keyword_score + additinal_score #log_relevance_score

        return total_score

        

       #return keyword_score + log_relevance_score #additinal_score
    
    def assign_lable(self):

        threshold = 1.5
        return "LIVEMUSIK" if self.score > threshold else" EJ LIVEMUSIK"

liveevents=[]

for index, row in df.iterrows():
    event =Event_Score(row["EveNamn"], row["EveBesk"], row["Event Relevance"])
    liveevents.append(event)
        

training_data, test_data = train_test_split(liveevents, test_size=0.2, random_state=42)


train_X = [event.cleaned_data_text for event in training_data]
train_Y = [event.lable for event in training_data]

test_X = [event.cleaned_data_text for event in test_data]
test_Y = [event.lable for event in test_data]

#vectorizer = CountVectorizer()
#vectors = vectorizer.fit_transform(train_X)
tfidf_vectorizer =TfidfVectorizer(ngram_range=(1,2), max_features=1000, preprocessor=clean_text)
tfidf_vectors = tfidf_vectorizer.fit_transform(train_X)
clf = SVC(C=10, kernel="rbf")

#param_grid = {
#    'kernel': ['linear', 'rbf', 'poly'],
#    'C': [0.1, 1, 10, 100]
#}

#grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring="accuracy")
#grid_search.fit(tfidf_vectors, train_Y)
#print("Bästa parametrarna:", grid_search.best_params_)
#print("Bästa noggrannheten:", grid_search.best_score_)
#clf.fit(vectors, train_Y)
#best_params = grid_search.best_params_
#clf_best = SVC(kernel=best_params['kernel'], C=best_params['C'])
clf.fit(tfidf_vectors, train_Y)

#clf.fit(tfidf_vectors, train_Y)

#test_vectors = vectorizer.transform(test_X)

#prediction = clf.predict(test_vectors)
test_vectors = tfidf_vectorizer.transform(test_X)
prediction = clf.predict(test_vectors)
#prediction = clf.predict(test_vectors)

live_music_count = sum(event.lable == "LIVEMUSIK" for event in liveevents)

print(f"Antal evenemang märkta som LIVEMUSIK: {live_music_count}")

# Beräkna noggrannheten
accuracy = accuracy_score(test_Y, prediction)
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

combined_df.to_excel("live_music_events8.xlsx", index=False)
#live_music_df = event_df[event_df["Predicted Label"]== "LIVEMUSIK"]

#live_music_df.to_excel("live_music_events3.xlsx", index=False)