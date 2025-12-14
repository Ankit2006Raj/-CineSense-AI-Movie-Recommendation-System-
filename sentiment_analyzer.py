from textblob import TextBlob
import re

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_thresholds = {
            'positive': 0.1,
            'negative': -0.1
        }
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = text.lower().strip()
        return text
    
    def analyze_text(self, text):
        """Analyze sentiment of a single text"""
        cleaned_text = self.clean_text(text)
        blob = TextBlob(cleaned_text)
        
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > self.sentiment_thresholds['positive']:
            label = 'positive'
        elif polarity < self.sentiment_thresholds['negative']:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'label': label
        }
    
    def analyze_movie_reviews(self, movie_id):
        """Analyze all reviews for a movie"""
        from models import Review
        
        reviews = Review.query.filter_by(movie_id=movie_id).all()
        
        if not reviews:
            return {
                'overall_sentiment': 'neutral',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'avg_polarity': 0.0,
                'total_reviews': 0
            }
        
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for review in reviews:
            if not review.sentiment_score:
                sentiment = self.analyze_text(review.content)
                review.sentiment_score = sentiment['polarity']
                review.sentiment_label = sentiment['label']
            
            sentiments.append(review.sentiment_score)
            
            if review.sentiment_label == 'positive':
                positive_count += 1
            elif review.sentiment_label == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
        
        avg_polarity = sum(sentiments) / len(sentiments)
        
        if avg_polarity > self.sentiment_thresholds['positive']:
            overall = 'positive'
        elif avg_polarity < self.sentiment_thresholds['negative']:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'overall_sentiment': overall,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'avg_polarity': avg_polarity,
            'total_reviews': len(reviews)
        }
    
    def get_sentiment_keywords(self, sentiment):
        """Get keywords associated with sentiment"""
        keywords = {
            'positive': ['excellent', 'amazing', 'great', 'wonderful', 'fantastic', 'love', 'best'],
            'negative': ['bad', 'terrible', 'awful', 'worst', 'hate', 'boring', 'disappointing'],
            'neutral': ['okay', 'average', 'decent', 'fine', 'alright']
        }
        return keywords.get(sentiment, [])
