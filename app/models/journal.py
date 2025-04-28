from app import db
from datetime import datetime
import json

class Journal(db.Model):
    __tablename__ = 'journals'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scores = db.Column(db.Text, nullable=True)
    
    user = db.relationship('User', backref=db.backref('journals', lazy=True))
    
    def __repr__(self):
        return f'<Journal {self.id}>'
    
    def set_scores(self, scores):
        """
        Save LIWC analysis scores as JSON string
        """
        self.scores = json.dumps(scores)
    
    def get_scores(self):
        """
        Get LIWC analysis scores as Python dictionary
        """
        if self.scores:
            return json.loads(self.scores)
        return None
    
    def to_dict(self):
        scores_dict = self.get_scores() if self.scores else None
        return {
            'id': self.id,
            'text': self.text,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'scores': scores_dict
        }
