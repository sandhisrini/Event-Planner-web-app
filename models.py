from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    priority = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Event {self.name} on {self.date} from {self.start_time} to {self.end_time}>"
