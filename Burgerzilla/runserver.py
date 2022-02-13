from api import create_app
from api.models import users, orders, restaurants
from api.config.config import config_dict


app = create_app(config=config_dict['production'])

if __name__ == "__main__":
    with app.app_context():
        users.db.create_all()
        orders.db.create_all()
        restaurants.db.create_all()
    app.run()