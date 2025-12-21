<div align="center">

# 🎬 MoodMatch Cinema

### AI-Powered Movie Recommendation System

*Discover the perfect movie for your mood with intelligent recommendations*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🎯 Overview

MoodMatch Cinema is an intelligent movie recommendation system that leverages AI and sentiment analysis to suggest movies based on your current mood. Built with Flask and modern machine learning algorithms, it provides personalized movie recommendations tailored to your emotional state.

The system combines collaborative filtering, content-based filtering, and sentiment analysis to deliver accurate recommendations. Whether you're feeling happy, sad, adventurous, or thoughtful, MoodMatch analyzes your mood and suggests the perfect movie to match your emotional state.

## ✨ Key Features

- **🎭 Mood-Based Recommendations** - 12 distinct mood categories for precise matching
- **🤖 AI-Powered Engine** - Hybrid recommendation system using collaborative and content-based filtering
- **💬 Sentiment Analysis** - Advanced NLP for analyzing movie reviews and user feedback
- **🎬 Extensive Movie Database** - 136+ movies with high-quality TMDB posters
- **🔍 Smart Search** - Intelligent search by title, genre, cast, or mood
- **⭐ Personalized Ratings** - Rate movies and receive tailored recommendations
- **📊 User Profiles** - Track watch history and manage preferences
- **🌐 Modern UI** - Responsive design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Ankit2006Raj/MoodMatch-Cinema.git
cd MoodMatch-Cinema
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the application**
```bash
python app.py
```

**4. Open your browser**
```
http://localhost:5000
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database management
- **SQLite** - Lightweight database
- **Scikit-learn** - Machine learning algorithms
- **NLTK** - Natural language processing

### Frontend
- **HTML5 & CSS3** - Modern web standards
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5** - Responsive UI framework

### APIs & Services
- **TMDB API** - Movie data and poster images

## 📁 Project Structure

```
MoodMatch-Cinema/
├── app.py                      # Main Flask application
├── models.py                   # Database models (User, Movie, Rating, Review)
├── config.py                   # Application configuration
├── mood_mapper.py              # Mood-to-genre mapping logic
├── recommendation_engine.py    # ML recommendation algorithms
├── sentiment_analyzer.py       # NLP sentiment analysis
├── tmdb_integration.py         # TMDB API integration
├── data_loader.py              # Database initialization
├── requirements.txt            # Python dependencies
├── instance/
│   └── moodmatch.db           # SQLite database
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── app.js             # Frontend logic
└── templates/
    └── index.html             # Main application template
```

## 🎭 Mood Categories

The system recognizes 12 distinct emotional states:

| Mood | Genres | Example Movies |
|------|--------|----------------|
| 😊 Happy | Comedy, Family, Musical | The Grand Budapest Hotel |
| 😢 Sad | Drama, Romance | The Shawshank Redemption |
| 💕 Romantic | Romance, Drama | The Notebook |
| 💪 Motivated | Biography, Sport, Adventure | Rocky |
| 😱 Thriller | Thriller, Mystery, Crime | Inception |
| 👻 Scared | Horror, Thriller | The Conjuring |
| 🗺️ Adventurous | Adventure, Action, Fantasy | Indiana Jones |
| 😌 Relaxed | Animation, Family, Comedy | Finding Nemo |
| 🎞️ Nostalgic | Classic, Drama, History | Forrest Gump |
| 🤔 Curious | Sci-Fi, Mystery, Documentary | Interstellar |
| ⚡ Energetic | Action, Adventure, Sport | Mad Max: Fury Road |
| 🧠 Thoughtful | Drama, Mystery, Sci-Fi | The Matrix |

## 🤖 Recommendation Algorithms

### 1. Collaborative Filtering
Analyzes user behavior patterns and ratings to find similar users and recommend movies they enjoyed.

### 2. Content-Based Filtering
Matches movie attributes (genre, cast, director, plot) with user preferences and viewing history.

### 3. Hybrid Approach
Combines both methods with weighted scoring for optimal accuracy and diversity in recommendations.

### 4. Sentiment Analysis
Uses NLTK to analyze review text and extract emotional sentiment, enhancing recommendation quality.

## 📊 Database Schema

- **users** - User accounts and authentication
- **movies** - Movie metadata with TMDB integration
- **ratings** - User ratings (1-10 scale)
- **reviews** - User reviews with sentiment scores
- **watch_history** - Viewing history tracking
- **user_preferences** - Genre and language preferences

## 🎨 Customization

### Adding New Movies
Use the TMDB integration module to fetch and add new movies with poster images.

### Modifying Mood Mappings
Edit `mood_mapper.py` to customize mood-to-genre relationships.

### Styling
Customize the look and feel by modifying `static/css/style.css`.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Movie data and poster images provided by [The Movie Database (TMDB)](https://www.themoviedb.org/)
- Built with Flask and modern web technologies
- Inspired by the need for emotion-aware entertainment recommendations

---

## 👨‍💻 Author

<div align="center">

### Ankit Raj
*Full Stack Developer & AI Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-Ankit2006Raj-181717?style=for-the-badge&logo=github)](https://github.com/Ankit2006Raj)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ankit_Raj-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ankit-raj-226a36309)
[![Email](https://img.shields.io/badge/Email-ankit9905163014@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ankit9905163014@gmail.com)

</div>

---

<div align="center">

**Made with ❤️ by Ankit Raj**

*© 2024 MoodMatch Cinema. All rights reserved.*

⭐ Star this repo if you find it helpful!

</div>

