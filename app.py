from flask import Flask, render_template
from models import db
from routes.doctor import doctor_bp
from routes.appointment import appointment_bp
from routes.auth import auth_bp, login_manager
from routes.admin import admin_bp  
import config

app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# Ініціалізація Flask-Login
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login' 

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(doctor_bp, url_prefix='/doctors')
app.register_blueprint(appointment_bp, url_prefix='/appointments')
app.register_blueprint(admin_bp, url_prefix='/admin')  # Додайте цю строку після інших blueprint

@app.route('/')
def home():
    return render_template('index.html')  

if __name__ == '__main__':
    app.run(debug=True)


