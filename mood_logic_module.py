class MoodGenreMapper:
    def __init__(self):
        self.mood_genres = {
            "funny": ["Comedy", "Animation", "Family"],
            "love": ["Romance", "Musical", "Music"],
            "sad": ["Drama"],
            "bored": ["Adventure", "Action", "Fantasy", "Sci-Fi"],
            "surprise": None,
            "fear": ["Horror", "Thriller"],
            "nostalgy": ["Family", "Animation", "Classic"],
            "inspiration": ["Biography", "History", "Documentary"],
            "psychology": ["Mystery"],
            "family": ["Family", "Animation"]
        }

    def get_genres_for_moods(self, selected_moods):
        all_genres = []
        for mood in selected_moods:
            genres = self.mood_genres.get(mood)
            if genres is None:
                return None
            all_genres.extend(genres)
        return list(set(all_genres))