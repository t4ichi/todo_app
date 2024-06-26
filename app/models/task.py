from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)
    favorite = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, server_default=db.func.now())
    updated_date = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Task id:{} title:{} description:{} done:{} favorite:{} creator_id:{}>'.format(
            self.id, self.title, self.description, self.done, self.favorite, self.creator_id)