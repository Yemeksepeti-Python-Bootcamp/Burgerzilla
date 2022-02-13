from ..utils.db import db


class Menu(db.Model):

    __tablename__ = 'menu'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False, unique=True)
    list = db.Column(db.String(), nullable=False)

    def __str__(self):
        return f"<Menu {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Restaurant(db.Model):

    __tablename__ = 'restaurant'

    id = db.Column(db.Integer(), primary_key=True)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(), nullable=False)
    menu = db.Column(db.Integer(), db.ForeignKey(Menu.id))
    is_active = db.Column(db.Boolean(), default=True)


    def __str__(self):
        return f"<Restaurant {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


