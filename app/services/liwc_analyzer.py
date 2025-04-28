import re
import json
import os
from app.models.category import Category, Word
from app import db

class LIWCAnalyzer:
    """
    Linguistic Inquiry and Word Count (LIWC) analyzer
    Analyzes text for the presence of words in predefined categories
    
    This analyzer implements a simplified version of the LIWC algorithm to analyze journal entries.
    It counts occurrences of words in predefined categories like positive emotions, negative emotions,
    social references, and cognitive processes.
    """
    
    @staticmethod
    def tokenize_text(text):
        """
        Tokenize text into words
        - Convert to lowercase
        - Remove punctuation
        - Split into words
        """
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        
        return words
    
    @staticmethod
    def analyze_text(text):
        """
        Analyze text and return scores for each category
        """
        words = LIWCAnalyzer.tokenize_text(text)
        
        categories = Category.query.all()
        
        scores = {}
        for category in categories:
            scores[category.name] = 0
        
        db_words = Word.query.all()
        
        word_to_category = {}
        for db_word in db_words:
            category = next((c for c in categories if c.id == db_word.category_id), None)
            if category:
                word_to_category[db_word.text.lower()] = category.name
        
        for word in words:
            word = word.lower()
            if word in word_to_category:
                category_name = word_to_category[word]
                scores[category_name] += 1
        
        total_score = sum(scores.values())
        
        return {
            'categories': scores,
            'total': total_score
        }
    
    @staticmethod
    def load_dictionary():
        """
        Load the LIWC dictionary from the JSON file
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dict_path = os.path.join(os.path.dirname(current_dir), 'data', 'liwc_dictionary.json')
            
            with open(dict_path, 'r') as f:
                dictionary = json.load(f)
            return dictionary
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            return {}
    
    @staticmethod
    def initialize_dictionary():
        """
        Initialize the LIWC dictionary with predefined categories and words from JSON file
        """
        dictionary = LIWCAnalyzer.load_dictionary()
        
        existing_categories = Category.query.all()
        if existing_categories:
            print("Dictionary already initialized")
            return
        
        for category_name, words in dictionary.items():
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()
            
            for word_text in words:
                word = Word(text=word_text, category_id=category.id)
                db.session.add(word)
        
        db.session.commit()
        print("Dictionary initialized successfully")
