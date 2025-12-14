from datetime import datetime

class MoodMapper:
    def __init__(self):
        self.mood_genre_mapping = {
            'happy': {
                'genres': ['Comedy', 'Animation', 'Family', 'Musical'],
                'keywords': ['fun', 'cheerful', 'uplifting', 'lighthearted'],
                'description': 'Feel-good movies to enhance your happiness'
            },
            'sad': {
                'genres': ['Comedy', 'Animation', 'Romance', 'Drama'],
                'keywords': ['heartwarming', 'inspiring', 'uplifting', 'hopeful'],
                'description': 'Uplifting movies to brighten your mood'
            },
            'romantic': {
                'genres': ['Romance', 'Drama', 'Comedy'],
                'keywords': ['love', 'relationship', 'romantic', 'heartfelt'],
                'description': 'Romantic movies for the heart'
            },
            'motivated': {
                'genres': ['Biography', 'Drama', 'Sport', 'Documentary'],
                'keywords': ['inspiring', 'success', 'achievement', 'determination'],
                'description': 'Inspirational movies to fuel your motivation'
            },
            'thriller': {
                'genres': ['Thriller', 'Mystery', 'Crime', 'Suspense'],
                'keywords': ['suspense', 'mystery', 'intense', 'gripping'],
                'description': 'Edge-of-your-seat thrillers'
            },
            'scared': {
                'genres': ['Horror', 'Thriller', 'Mystery'],
                'keywords': ['scary', 'frightening', 'suspenseful', 'dark'],
                'description': 'Horror movies for thrill seekers'
            },
            'adventurous': {
                'genres': ['Adventure', 'Action', 'Fantasy', 'Sci-Fi'],
                'keywords': ['adventure', 'action', 'epic', 'journey'],
                'description': 'Epic adventures and action-packed movies'
            },
            'relaxed': {
                'genres': ['Drama', 'Documentary', 'Romance', 'Animation'],
                'keywords': ['calm', 'peaceful', 'slow-paced', 'contemplative'],
                'description': 'Relaxing movies for a peaceful evening'
            },
            'nostalgic': {
                'genres': ['Classic', 'Drama', 'Romance', 'Family'],
                'keywords': ['classic', 'timeless', 'memorable', 'vintage'],
                'description': 'Classic movies that bring back memories'
            },
            'curious': {
                'genres': ['Documentary', 'Mystery', 'Sci-Fi', 'Thriller'],
                'keywords': ['intriguing', 'thought-provoking', 'mysterious', 'fascinating'],
                'description': 'Mind-bending and thought-provoking films'
            },
            'energetic': {
                'genres': ['Action', 'Adventure', 'Sport', 'Music'],
                'keywords': ['energetic', 'fast-paced', 'dynamic', 'exciting'],
                'description': 'High-energy movies to pump you up'
            },
            'thoughtful': {
                'genres': ['Drama', 'Documentary', 'Mystery', 'Sci-Fi'],
                'keywords': ['contemplative', 'philosophical', 'deep', 'meaningful'],
                'description': 'Thought-provoking films for reflection'
            }
        }
        
        self.time_context_mapping = {
            'weekend': ['Action', 'Adventure', 'Comedy', 'Thriller'],
            'weekday': ['Drama', 'Documentary', 'Romance'],
            'late_night': ['Horror', 'Thriller', 'Mystery'],
            'morning': ['Comedy', 'Animation', 'Family'],
            'afternoon': ['Drama', 'Romance', 'Documentary']
        }
    
    def get_mood_based_recommendations(self, mood, user_id, limit=20):
        """Get movie recommendations based on user's mood"""
        from models import Movie, UserPreference
        
        mood = mood.lower()
        
        if mood not in self.mood_genre_mapping:
            mood = 'happy'  # Default mood
        
        mood_config = self.mood_genre_mapping[mood]
        preferred_genres = mood_config['genres']
        
        # Get user preferences
        user_pref = UserPreference.query.filter_by(user_id=user_id).first()
        
        # Build query - filter movies with valid poster URLs
        query = Movie.query.filter(
            Movie.poster_url.isnot(None),
            Movie.poster_url != ''
        )
        
        # Filter by mood genres
        genre_filter = '|'.join(preferred_genres)
        query = query.filter(Movie.genres.op('REGEXP')(genre_filter))
        
        # Apply user language preference if available
        if user_pref and user_pref.preferred_languages:
            languages = user_pref.preferred_languages.split(',')
            query = query.filter(Movie.language.in_(languages))
        
        # Order by rating and popularity
        movies = query.order_by(
            Movie.avg_rating.desc(),
            Movie.popularity.desc()
        ).limit(limit).all()
        
        return [{
            **movie.to_dict(),
            'mood': mood,
            'reason': f'Perfect for when you\'re feeling {mood}',
            'mood_description': mood_config['description']
        } for movie in movies]
    
    def get_time_based_recommendations(self, user_id, limit=20):
        """Get recommendations based on time of day"""
        from models import Movie
        
        current_hour = datetime.now().hour
        
        if current_hour < 12:
            time_context = 'morning'
        elif current_hour < 18:
            time_context = 'afternoon'
        elif current_hour < 22:
            time_context = 'weekend'
        else:
            time_context = 'late_night'
        
        preferred_genres = self.time_context_mapping.get(time_context, ['Drama'])
        
        genre_filter = '|'.join(preferred_genres)
        # Filter movies with valid poster URLs
        movies = Movie.query.filter(
            Movie.poster_url.isnot(None),
            Movie.poster_url != '',
            Movie.genres.op('REGEXP')(genre_filter)
        ).order_by(
            Movie.avg_rating.desc()
        ).limit(limit).all()
        
        return [{
            **movie.to_dict(),
            'time_context': time_context,
            'reason': f'Great for {time_context} viewing'
        } for movie in movies]
    
    def get_seasonal_recommendations(self, user_id, limit=20):
        """Get recommendations based on season/holidays"""
        from models import Movie
        
        current_month = datetime.now().month
        
        seasonal_genres = {
            12: ['Family', 'Animation', 'Fantasy'],  # December - Holiday season
            10: ['Horror', 'Thriller'],  # October - Halloween
            2: ['Romance', 'Drama'],  # February - Valentine's
            7: ['Action', 'Adventure', 'Comedy']  # July - Summer
        }
        
        genres = seasonal_genres.get(current_month, ['Drama', 'Comedy'])
        
        genre_filter = '|'.join(genres)
        # Filter movies with valid poster URLs
        movies = Movie.query.filter(
            Movie.poster_url.isnot(None),
            Movie.poster_url != '',
            Movie.genres.op('REGEXP')(genre_filter)
        ).order_by(
            Movie.popularity.desc()
        ).limit(limit).all()
        
        return [{
            **movie.to_dict(),
            'reason': 'Perfect for this season'
        } for movie in movies]
    
    def get_available_moods(self):
        """Return all available moods with descriptions"""
        return {
            mood: {
                'genres': config['genres'],
                'description': config['description']
            }
            for mood, config in self.mood_genre_mapping.items()
        }
