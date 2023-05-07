from flask_migrate import Migrate
from application import create_app, db
from application.models import Admin

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)