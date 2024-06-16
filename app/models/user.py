from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),primary_key=True,nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<User id:{} username:{} email:{} password:{}>'.format(
            self.id, self.username, self.email,self.password)