from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, City, WeatherData,DailySummary
from etl import fetch_weather_data, process_weather_data, load_weather_data,generate_daily_summary
from scripts.config import Config

# Criação do app e configuração
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/etl', methods=['GET'])
def run_etl():
    """
    Endpoint para executar o pipeline ETL para várias cidades.
    """
    cities = ["Rio de Janeiro", "Curitiba", "São Paulo"]
    results = []

    for city_name in cities:
        try:
            # Extração
            raw_data = fetch_weather_data(city_name)
            # Transformação
            processed_data = process_weather_data(raw_data)
            # Carga
            load_weather_data(city_name, processed_data)
            results.append({"city": city_name, "status": "success", "message": f"Dados para {city_name} inseridos com sucesso!"})
        except Exception as e:
            results.append({"city": city_name, "status": "error", "message": str(e)})

    return jsonify(results)


@app.route('/cities', methods=['GET'])
def get_cities():
    """
    Endpoint para listar todas as cidades cadastradas no banco.
    """
    cities = City.query.all()
    return jsonify([{"id": city.id, "name": city.name} for city in cities])

@app.route('/weather/hot-cities', methods=['GET'])
def get_hot_cities():
    """
    Endpoint para listar cidades onde a temperatura foi superior a 25°C.
    """
    try:
        # Query para filtrar dados de clima com temperatura superior a 25°C
        hot_weather_data = (
            db.session.query(City.name, WeatherData.temperature)
            .join(WeatherData, City.id == WeatherData.city_id)
            .filter(WeatherData.temperature > 25)
            .all()
        )
        if not hot_weather_data:
            return jsonify({"message": "Nenhuma cidade encontrada com temperatura acima de 25°C."}), 404

        # Formata a resposta como uma lista de dicionários
        result = [{"city": city, "temperature": temp} for city, temp in hot_weather_data]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather/avg-temperature', methods=['GET'])
def get_avg_temperature():
    """
    Endpoint para calcular a temperatura média por cidade.
    """
    try:
        # Query para calcular a temperatura média por cidade
        avg_temp_data = (
            db.session.query(City.name, db.func.avg(WeatherData.temperature).label('avg_temperature'))
            .join(WeatherData, City.id == WeatherData.city_id)
            .group_by(City.name)
            .all()
        )
        
        if not avg_temp_data:
            return jsonify({"message": "Nenhum dado de temperatura encontrado."}), 404

        # Formata a resposta como uma lista de dicionários
        result = [{"city": city, "avg_temperature": round(avg_temp, 2)} for city, avg_temp in avg_temp_data]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/daily_summary', methods=['GET'])
def get_daily_summary():
    """
    Endpoint para listar os resumos diários por cidade.
    """
    summaries = DailySummary.query.all()
    return jsonify([{
        "city_name": summary.city.name,
        "date": summary.date.strftime("%Y-%m-%d"),
        "avg_temperature": summary.avg_temperature,
        "avg_humidity": summary.avg_humidity,
        "record_count": summary.record_count
    } for summary in summaries])



@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Endpoint para listar todas as informações climáticas no banco, 
    incluindo os novos campos.
    """
    weather_data = WeatherData.query.all()
    return jsonify([{
        "city": data.city.name,  # Nome da cidade (relacionamento com City)
        "country": data.city.country,  # País
        "latitude": data.city.latitude,  # Latitude
        "longitude": data.city.longitude,  # Longitude
        "temperature": data.temperature,  # Temperatura
        "humidity": data.humidity,  # Umidade
        "timestamp": data.timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
        "windspeed": data.windspeed,  # Velocidade do vento
        "weather_condition": data.weather_condition,  # Condição climática
        "precipitation": data.precipitation  # Precipitação
    } for data in weather_data])

@app.route('/generate_summary', methods=['GET'])
def generate_summary():
    generate_daily_summary()
    return {"message": "Resumo diário gerado com sucesso!"}, 200


if __name__ == '__main__':
    app.run(debug=True)
