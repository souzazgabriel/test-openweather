from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # Conexão do Flask com o Banco de Dados

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)  # Nova coluna: país
    latitude = db.Column(db.Float, nullable=False)  # Nova coluna: latitude
    longitude = db.Column(db.Float, nullable=False)  # Nova coluna: longitude

    # Relacionamento com WeatherData
    weather_data = db.relationship('WeatherData', backref='city', lazy=True)

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    windspeed = db.Column(db.Float, nullable=True)  # Nova coluna: velocidade do vento
    weather_condition = db.Column(db.String(255), nullable=True)  # Nova coluna: condição do tempo
    precipitation = db.Column(db.Float, nullable=True)  # Nova coluna: precipitação

class DailySummary(db.Model):
    __tablename__ = 'daily_summary'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    avg_temperature = db.Column(db.Float, nullable=False)
    avg_humidity = db.Column(db.Float, nullable=False)
    record_count = db.Column(db.Integer, nullable=False)

    city = db.relationship('City', backref=db.backref('summaries', lazy=True))
