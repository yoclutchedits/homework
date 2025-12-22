import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from colorama import init, Fore
import sys

init(autoreset=True)

def load_data(file_path=r"C:\Users\Acer\Downloads\AI_Movie_recommendation_system_boilerplate_code_AIEPCM1L6-1c2b\imdb_top_1000.csv"):
    try:
        df = pd.read_csv(file_path)

        # rename columns to match code
        df = df.rename(columns={
            'Genre': 'genres',
            'Overview': 'overview',
            'IMDB_Rating': 'imdb_rating',
            'Series_Title': 'title'
        })

        df['combined_features'] = df['genres'].fillna('') + " " + df['overview'].fillna('')
        return df

    except FileNotFoundError:
        print(Fore.RED + f'error: File not found at {file_path}.')
        sys.exit()

movies_df = load_data()

Tfidf = TfidfVectorizer(stop_words='english')
Tfidf_matrix = Tfidf.fit_transform(movies_df['combined_features'])
cosine_sim = cosine_similarity(Tfidf_matrix, Tfidf_matrix)

def list_genres(df):
    return sorted(
        set(
            genre.strip()
            for sublist in df['genres'].dropna().str.split(',')
            for genre in sublist
        )
    )

genres = list_genres(movies_df)

def reccomend_movies_by_genre(genre=None, mood=None, rating=None, top_n=5):
    filtered_df = movies_df.copy()

    if genre:
        filtered_df = filtered_df[filtered_df['genres'].str.contains(genre, case=False, na=False)]

    if rating:
        filtered_df = filtered_df[filtered_df['imdb_rating'] >= rating]

    filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)

    recommendations = []

    for _, row in filtered_df.iterrows():
        overview = row['overview']
        if pd.isna(overview):
            continue

        polarity = TextBlob(overview).sentiment.polarity

        if mood:
            mood_polarity = TextBlob(mood).sentiment.polarity
            if mood_polarity > 0 and polarity <= 0:
                continue
            if mood_polarity < 0 and polarity >= 0:
                continue

        recommendations.append(
            (row['title'], row['imdb_rating'], row['genres'])
        )
        if len(recommendations) >= top_n:
            break
    return recommendations
def print_recommendations(recommendations):
    if not recommendations:
        print(Fore.RED + "No recommendations found based on your criteria.")
        return

    print(Fore.GREEN + "\nHere are your movie recommendations:\n")
    for title, rating, genres in recommendations:
        print(Fore.YELLOW + f"Title: {title}")
        print(Fore.CYAN + f"IMDB Rating: {rating}")
        print(Fore.MAGENTA + f"Genres: {genres}\n")
def main():
    print(Fore.GREEN + "Welcome to the Movie Recommendation System!")
    name = input(Fore.YELLOW + "What's your name? ")
    print(Fore.GREEN + f"Nice to meet you, {name}!")

    while True:
        print(Fore.GREEN + "\nAvailable genres:")
        for g in genres:
            print(Fore.CYAN + f"- {g}")

        genre = input(Fore.YELLOW + "\nEnter a genre (or 'exit' to quit): ")
        if genre.lower() == 'exit':
            print(Fore.GREEN + f"Goodbye, {name}!")
            break

        mood = input(Fore.YELLOW + "Describe your current mood (optional): ")
        rating_input = input(Fore.YELLOW + "Minimum IMDB rating (0-10, optional): ")
        rating = float(rating_input) if rating_input else None

        recommendations = reccomend_movies_by_genre(genre=genre, mood=mood, rating=rating, top_n=5)
        print_recommendations(recommendations) 
if __name__ == "__main__":
    main()