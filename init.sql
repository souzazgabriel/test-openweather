
CREATE DATABASE weather_db;

USE weather_db;

 CREATE TABLE  IF NOT EXISTS  `cities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


 CREATE TABLE  IF NOT EXISTS `weather_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city_id` int NOT NULL,
  `temperature` float NOT NULL,
  `humidity` float NOT NULL,
  `timestamp` datetime NOT NULL,
  `windspeed` float DEFAULT NULL,
  `weather_condition` varchar(255) DEFAULT NULL,
  `precipitation` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `weather_data_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


 CREATE TABLE IF NOT EXISTS `daily_summary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city_id` int NOT NULL,
  `date` date NOT NULL,
  `avg_temperature` float NOT NULL,
  `avg_humidity` float NOT NULL,
  `record_count` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `daily_summary_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET SQL_SAFE_UPDATES  = 0;
ALTER TABLE cities AUTO_INCREMENT = 1;
ALTER TABLE weather_data AUTO_INCREMENT = 1;
ALTER TABLE daily_summary AUTO_INCREMENT = 1;
DELETE FROM daily_summary;
DELETE FROM weather_data;
DELETE FROM cities;
