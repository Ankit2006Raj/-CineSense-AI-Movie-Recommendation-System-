from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from functools import wraps
import secrets

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cinesense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db from models and initialize with app
from models import db
db.init_app(app)

# Initialize extensions
bcrypt = Bcrypt(app)
CORS(app)

# Global variables for AI components (will be initialized in main)
recommender = None
sentiment_analyzer = None
mood_mapper = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Import models after db initialization
from models import User, Movie, Rating, Review, WatchHistory, UserPreference

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    try:
        user_id = session['user_id']
        limit = request.args.get('limit', 20, type=int)
        
        recommendations = recommender.get_hybrid_recommendations(user_id, limit)
        
        return jsonify({
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/mood', methods=['POST'])
@login_required
def mood_recommendations():
    try:
        data = request.json
        mood = data.get('mood')
        user_id = session['user_id']
        
        recommendations = mood_mapper.get_mood_based_recommendations(mood, user_id)
        
        return jsonify({
            'mood': mood,
            'recommendations': recommendations
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/trending', methods=['GET'])
def trending_recommendations():
    try:
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # For demo purposes, if no trending data, return popular movies
        from models import Movie
        # Filter movies that have valid poster URLs
        movies = Movie.query.filter(
            Movie.poster_url.isnot(None),
            Movie.poster_url != ''
        ).order_by(Movie.popularity.desc()).limit(limit).all()
        
        trending = [{
            **movie.to_dict(),
            'reason': f'Popular movie'
        } for movie in movies]
        
        return jsonify({
            'trending': trending,
            'period': f'Last {days} days'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    # Get sentiment analysis
    sentiment = sentiment_analyzer.analyze_movie_reviews(movie_id)
    
    # Get similar movies
    similar = recommender.get_similar_movies(movie_id, limit=6)
    
    return jsonify({
        'movie': movie.to_dict(),
        'sentiment': sentiment,
        'similar_movies': similar
    }), 200

@app.route('/api/rate', methods=['POST'])
@login_required
def rate_movie():
    data = request.json
    user_id = session['user_id']
    
    rating = Rating.query.filter_by(
        user_id=user_id,
        movie_id=data['movie_id']
    ).first()
    
    if rating:
        rating.rating = data['rating']
        rating.timestamp = datetime.now()
    else:
        rating = Rating(
            user_id=user_id,
            movie_id=data['movie_id'],
            rating=data['rating']
        )
        db.session.add(rating)
    
    db.session.commit()
    
    # Update recommendations in real-time
    recommender.update_user_profile(user_id)
    
    return jsonify({'message': 'Rating saved successfully'}), 200

@app.route('/api/watch-history', methods=['POST'])
@login_required
def add_watch_history():
    data = request.json
    user_id = session['user_id']
    
    history = WatchHistory(
        user_id=user_id,
        movie_id=data['movie_id'],
        watched_at=datetime.now()
    )
    
    db.session.add(history)
    db.session.commit()
    
    return jsonify({'message': 'Added to watch history'}), 200

@app.route('/api/preferences', methods=['GET', 'POST'])
@login_required
def user_preferences():
    user_id = session['user_id']
    
    if request.method == 'POST':
        data = request.json
        
        pref = UserPreference.query.filter_by(user_id=user_id).first()
        if not pref:
            pref = UserPreference(user_id=user_id)
            db.session.add(pref)
        
        pref.favorite_genres = ','.join(data.get('genres', []))
        pref.favorite_actors = ','.join(data.get('actors', []))
        pref.favorite_directors = ','.join(data.get('directors', []))
        pref.preferred_languages = ','.join(data.get('languages', []))
        
        db.session.commit()
        
        return jsonify({'message': 'Preferences saved'}), 200
    
    else:
        pref = UserPreference.query.filter_by(user_id=user_id).first()
        if pref:
            return jsonify(pref.to_dict()), 200
        return jsonify({}), 200

@app.route('/api/search', methods=['GET'])
def search_movies():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    # Filter movies that have valid poster URLs
    movies = Movie.query.filter(
        Movie.title.ilike(f'%{query}%'),
        Movie.poster_url.isnot(None),
        Movie.poster_url != ''
    ).limit(limit).all()
    
    return jsonify({
        'results': [movie.to_dict() for movie in movies]
    }), 200

@app.route('/api/cold-start', methods=['POST'])
@login_required
def cold_start_setup():
    data = request.json
    user_id = session['user_id']
    
    # Save initial preferences
    pref = UserPreference(
        user_id=user_id,
        favorite_genres=','.join(data.get('genres', [])),
        preferred_languages=','.join(data.get('languages', []))
    )
    db.session.add(pref)
    db.session.commit()
    
    # Get initial recommendations
    recommendations = recommender.cold_start_recommendations(user_id)
    
    return jsonify({
        'message': 'Preferences saved',
        'recommendations': recommendations
    }), 200

def initialize_app():
    """Initialize the application with models and AI components"""
    global recommender, sentiment_analyzer, mood_mapper
    
    with app.app_context():
        # Import after app context is ready
        from recommendation_engine import RecommendationEngine
        from sentiment_analyzer import SentimentAnalyzer
        from mood_mapper import MoodMapper
        from models import Movie
        
        # Initialize AI components
        recommender = RecommendationEngine()
        sentiment_analyzer = SentimentAnalyzer()
        mood_mapper = MoodMapper()
        
        # Create database tables
        db.create_all()
        
        # Initialize sample data
        from data_loader import load_sample_data
        if Movie.query.count() == 0:
            load_sample_data()

if __name__ == '__main__':
    initialize_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
