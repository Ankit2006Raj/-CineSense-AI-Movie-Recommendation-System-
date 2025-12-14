from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_admin = db.Column(db.Boolean, default=False)
    
    ratings = db.relationship('Rating', backref='user', lazy=True)
    watch_history = db.relationship('WatchHistory', backref='user', lazy=True)
    preferences = db.relationship('UserPreference', backref='user', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    overview = db.Column(db.Text)
    genres = db.Column(db.String(200))
    release_date = db.Column(db.Date)
    runtime = db.Column(db.Integer)
    language = db.Column(db.String(50))
    poster_url = db.Column(db.String(500))
    backdrop_url = db.Column(db.String(500))
    cast = db.Column(db.Text)
    director = db.Column(db.String(200))
    avg_rating = db.Column(db.Float, default=0.0)
    vote_count = db.Column(db.Integer, default=0)
    popularity = db.Column(db.Float, default=0.0)
    
    ratings = db.relationship('Rating', backref='movie', lazy=True)
    reviews = db.relationship('Review', backref='movie', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'overview': self.overview,
            'genres': self.genres.split(',') if self.genres else [],
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'runtime': self.runtime,
            'language': self.language,
            'poster_url': self.poster_url,
            'backdrop_url': self.backdrop_url,
            'cast': self.cast.split(',') if self.cast else [],
            'director': self.director,
            'avg_rating': self.avg_rating,
            'vote_count': self.vote_count,
            'popularity': self.popularity
        }

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'rating': self.rating,
            'timestamp': self.timestamp.isoformat()
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float)
    sentiment_label = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'user_id': self.user_id,
            'content': self.content,
            'sentiment_score': self.sentiment_score,
            'sentiment_label': self.sentiment_label,
            'created_at': self.created_at.isoformat()
        }

class WatchHistory(db.Model):
    __tablename__ = 'watch_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    watched_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'watched_at': self.watched_at.isoformat()
        }

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    favorite_genres = db.Column(db.Text)
    favorite_actors = db.Column(db.Text)
    favorite_directors = db.Column(db.Text)
    preferred_languages = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'favorite_genres': self.favorite_genres.split(',') if self.favorite_genres else [],
            'favorite_actors': self.favorite_actors.split(',') if self.favorite_actors else [],
            'favorite_directors': self.favorite_directors.split(',') if self.favorite_directors else [],
            'preferred_languages': self.preferred_languages.split(',') if self.preferred_languages else []
        }
