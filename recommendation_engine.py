import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from datetime import datetime, timedelta
from collections import defaultdict
import pickle
import os

class RecommendationEngine:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.content_similarity_matrix = None
        self.user_item_matrix = None
        self.svd_model = None
        self.movie_features = {}
        
    def build_content_based_model(self):
        """Build content-based filtering model using TF-IDF"""
        from models import Movie
        
        movies = Movie.query.all()
        
        # Create feature strings for each movie
        movie_features = []
        movie_ids = []
        
        for movie in movies:
            features = f"{movie.title} {movie.overview} {movie.genres} {movie.cast} {movie.director}"
            movie_features.append(features)
            movie_ids.append(movie.id)
        
        # Calculate TF-IDF matrix
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(movie_features)
        
        # Calculate cosine similarity
        self.content_similarity_matrix = cosine_similarity(tfidf_matrix)
        self.movie_ids = movie_ids
        
        return self.content_similarity_matrix
    
    def build_collaborative_model(self):
        """Build collaborative filtering model using SVD"""
        from models import Rating
        
        ratings = Rating.query.all()
        
        # Create user-item matrix
        data = []
        for rating in ratings:
            data.append({
                'user_id': rating.user_id,
                'movie_id': rating.movie_id,
                'rating': rating.rating
            })
        
        if not data:
            return None
        
        df = pd.DataFrame(data)
        self.user_item_matrix = df.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating'
        ).fillna(0)
        
        # Apply SVD
        self.svd_model = TruncatedSVD(n_components=min(50, len(self.user_item_matrix) - 1))
        self.user_factors = self.svd_model.fit_transform(self.user_item_matrix)
        self.item_factors = self.svd_model.components_.T
        
        return self.user_item_matrix
    
    def get_content_based_recommendations(self, movie_id, limit=10):
        """Get similar movies based on content"""
        from models import Movie
        
        if self.content_similarity_matrix is None:
            self.build_content_based_model()
        
        try:
            movie_idx = self.movie_ids.index(movie_id)
        except ValueError:
            return []
        
        # Get similarity scores
        similarity_scores = list(enumerate(self.content_similarity_matrix[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get top similar movies (excluding itself)
        similar_indices = [i[0] for i in similarity_scores[1:limit+1]]
        similar_movie_ids = [self.movie_ids[i] for i in similar_indices]
        
        # Filter movies that have valid poster URLs
        movies = Movie.query.filter(
            Movie.id.in_(similar_movie_ids),
            Movie.poster_url.isnot(None),
            Movie.poster_url != ''
        ).all()
        
        return [{
            **movie.to_dict(),
            'similarity_score': similarity_scores[similar_indices.index(self.movie_ids.index(movie.id)) + 1][1],
            'reason': f'Similar content to your selection'
        } for movie in movies]
    
    def get_collaborative_recommendations(self, user_id, limit=10):
        """Get recommendations based on collaborative filtering"""
        from models import Movie
        
        if self.user_item_matrix is None or self.svd_model is None:
            self.build_collaborative_model()
        
        if self.user_item_matrix is None:
            return []
        
        if user_id not in self.user_item_matrix.index:
            return []
        
        # Get user's latent factors
        user_idx = list(self.user_item_matrix.index).index(user_id)
        user_vector = self.user_factors[user_idx]
        
        # Calculate predicted ratings
        predicted_ratings = np.dot(user_vector, self.item_factors.T)
        
        # Get user's already rated movies
        rated_movies = self.user_item_matrix.loc[user_id]
        rated_movie_ids = rated_movies[rated_movies > 0].index.tolist()
        
        # Create recommendations
        movie_scores = []
        for idx, movie_id in enumerate(self.user_item_matrix.columns):
            if movie_id not in rated_movie_ids:
                movie_scores.append((movie_id, predicted_ratings[idx]))
        
        # Sort by predicted rating
        movie_scores = sorted(movie_scores, key=lambda x: x[1], reverse=True)[:limit]
        
        recommended_movie_ids = [m[0] for m in movie_scores]
        # Filter movies that have valid poster URLs
        movies = Movie.query.filter(
            Movie.id.in_(recommended_movie_ids),
            Movie.poster_url.isnot(None),
            Movie.poster_url != ''
        ).all()
        
        return [{
            **movie.to_dict(),
            'predicted_rating': movie_scores[recommended_movie_ids.index(movie.id)][1],
            'reason': 'Users with similar taste enjoyed this'
        } for movie in movies]
    
    def get_hybrid_recommendations(self, user_id, limit=20):
        """Combine content-based and collaborative filtering"""
        from models import Rating, Movie
        
        # Check if user has ratings
        user_ratings = Rating.query.filter_by(user_id=user_id).count()
        
        if user_ratings < 5:
            # Cold start: use content-based + popular
            return self.cold_start_recommendations(user_id, limit)
        
        # Get both types of recommendations
        collab_recs = self.get_collaborative_recommendations(user_id, limit)
        
        # Get user's top-rated movies
        top_rated = Rating.query.filter_by(user_id=user_id).order_by(
            Rating.rating.desc()
        ).limit(3).all()
        
        content_recs = []
        for rating in top_rated:
            content_recs.extend(
                self.get_content_based_recommendations(rating.movie_id, limit=5)
            )
        
        # Combine and deduplicate
        all_recs = {}
        
        # Weight collaborative filtering higher
        for rec in collab_recs:
            all_recs[rec['id']] = {
                **rec,
                'score': rec.get('predicted_rating', 0) * 0.6
            }
        
        # Add content-based recommendations
        for rec in content_recs:
            if rec['id'] in all_recs:
                all_recs[rec['id']]['score'] += rec.get('similarity_score', 0) * 0.4
                all_recs[rec['id']]['reason'] += ' & ' + rec['reason']
            else:
                all_recs[rec['id']] = {
                    **rec,
                    'score': rec.get('similarity_score', 0) * 0.4
                }
        
        # Sort by combined score
        sorted_recs = sorted(all_recs.values(), key=lambda x: x['score'], reverse=True)
        
        return sorted_recs[:limit]
    
    def cold_start_recommendations(self, user_id, limit=20):
        """Recommendations for new users"""
        from models import Movie, UserPreference
        
        # Get user preferences
        pref = UserPreference.query.filter_by(user_id=user_id).first()
        
        # Filter movies that have valid poster URLs
        query = Movie.query.filter(
            Movie.poster_url.isnot(None),
            Movie.poster_url != ''
        )
        
        if pref and pref.favorite_genres:
            genres = pref.favorite_genres.split(',')
            genre_filter = '|'.join(genres)
            query = query.filter(Movie.genres.op('REGEXP')(genre_filter))
        
        if pref and pref.preferred_languages:
            languages = pref.preferred_languages.split(',')
            query = query.filter(Movie.language.in_(languages))
        
        # Get popular movies
        movies = query.order_by(
            Movie.popularity.desc(),
            Movie.avg_rating.desc()
        ).limit(limit).all()
        
        return [{
            **movie.to_dict(),
            'reason': 'Popular in your preferred genres'
        } for movie in movies]
    
    def get_trending_movies(self, days=7, limit=20):
        """Get trending movies based on recent activity"""
        from models import Movie, Rating, WatchHistory, db
        from sqlalchemy import func
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get movies with most recent ratings and views, filter those with valid posters
        trending = db.session.query(
            Movie,
            func.count(Rating.id).label('rating_count'),
            func.count(WatchHistory.id).label('view_count')
        ).outerjoin(Rating, Movie.id == Rating.movie_id)\
         .outerjoin(WatchHistory, Movie.id == WatchHistory.movie_id)\
         .filter(
             Movie.poster_url.isnot(None),
             Movie.poster_url != '',
             (Rating.timestamp >= cutoff_date) | (WatchHistory.watched_at >= cutoff_date)
         ).group_by(Movie.id)\
         .order_by(
             (func.count(Rating.id) + func.count(WatchHistory.id)).desc()
         ).limit(limit).all()
        
        return [{
            **movie.to_dict(),
            'trending_score': rating_count + view_count,
            'reason': f'Trending in last {days} days'
        } for movie, rating_count, view_count in trending]
    
    def get_similar_movies(self, movie_id, limit=6):
        """Get similar movies for a given movie"""
        return self.get_content_based_recommendations(movie_id, limit)
    
    def update_user_profile(self, user_id):
        """Update user profile after new rating"""
        # Rebuild collaborative model
        self.build_collaborative_model()
