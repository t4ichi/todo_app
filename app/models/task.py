from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)
    favorite = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return '<Task id:{} title:{} description:{} done:{} favorite:{}>'.format(
            self.id, self.title, self.description, self.done, self.favorite)