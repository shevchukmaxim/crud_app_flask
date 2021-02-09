from app import db


class User(db.Model):
    """
    Create an User Table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    surname = db.Column(db.String(60), index=True)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname
        }
