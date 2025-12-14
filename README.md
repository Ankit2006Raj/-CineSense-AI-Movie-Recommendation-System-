# CineSense AI - Movie Recommendation System

AI-powered movie recommendation system with mood-based suggestions and sentiment analysis.

## Features

- 🎭 **Mood-Based Recommendations** - Get movie suggestions based on 12 different moods
- 🤖 **AI-Powered Engine** - Collaborative and content-based filtering
- 💬 **Sentiment Analysis** - Analyze movie reviews and ratings
- 🎬 **136 Movies** - All with real TMDB posters
- 🔍 **Smart Search** - Find movies by title, genre, or mood
- ⭐ **User Ratings** - Rate movies and get personalized recommendations

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open Browser
Navigate to: `http://localhost:5000`

## Project Structure

```
Movie_recommanadation/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── config.py                   # Configuration settings
├── mood_mapper.py              # Mood-to-genre mapping
├── recommendation_engine.py    # Recommendation algorithms
├── sentiment_analyzer.py       # Review sentiment analysis
├── tmdb_integration.py         # TMDB API integration
├── requirements.txt            # Python dependencies
├── instance/
│   └── cinesense.db           # SQLite database
├── static/
│   ├── css/
│   │   └── style.css          # Styles
│   └── js/
│       └── app.js             # Frontend JavaScript
└── templates/
    └── index.html             # Main HTML template
```

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **AI/ML**: Scikit-learn, NLTK
- **APIs**: TMDB (The Movie Database)

## Features in Detail

### Mood Categories
- Happy 😊
- Sad 😢
- Romantic 💕
- Motivated 💪
- Thriller 😱
- Scared 👻
- Adventurous 🗺️
- Relaxed 😌
- Nostalgic 🎞️
- Curious 🤔
- Energetic ⚡
- Thoughtful 🧠

### Recommendation Algorithms
1. **Collaborative Filtering** - Based on user ratings and preferences
2. **Content-Based Filtering** - Based on movie genres, cast, and director
3. **Hybrid Approach** - Combines both methods for better accuracy

### User Features
- Create account and login
- Rate movies (1-10 scale)
- Save watch history
- Set genre and language preferences
- Get personalized recommendations

## Database

The application uses SQLite with the following tables:
- `users` - User accounts
- `movies` - Movie information with TMDB posters
- `ratings` - User movie ratings
- `reviews` - User reviews with sentiment scores
- `watch_history` - Movies watched by users
- `user_preferences` - User genre/language preferences

## API Endpoints

- `GET /` - Home page
- `POST /signup` - Create new account
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /api/movies/<id>` - Get movie details
- `POST /api/rate` - Rate a movie
- `GET /api/recommendations` - Get personalized recommendations
- `POST /api/recommendations/mood` - Get mood-based recommendations
- `GET /api/recommendations/trending` - Get trending movies
- `GET /api/search` - Search movies

## Development

### Adding New Movies
Movies are stored in the SQLite database with TMDB poster URLs. To add new movies, use the TMDB integration module.

### Customizing Moods
Edit `mood_mapper.py` to modify mood-to-genre mappings.

### Styling
Modify `static/css/style.css` for custom styling.

## License

MIT License

## Credits

- Movie data and posters from [TMDB](https://www.themoviedb.org/)
- Built with Flask and modern web technologies
