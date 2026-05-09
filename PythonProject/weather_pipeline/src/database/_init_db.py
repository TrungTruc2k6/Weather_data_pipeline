from src.database.connection import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
-- Bảng dimension: lưu thông tin địa điểm
CREATE TABLE IF NOT EXISTS dim_location  (
    id BIGSERIAL PRIMARY KEY,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    city_name VARCHAR(20),
    CONSTRAINT unique_lat_long UNIQUE (latitude, longitude)
);

-- Bảng fact: dữ liệu thời tiết theo ngày
CREATE TABLE IF NOT EXISTS fact_weather_daily  (
    dim_location_id BIGSERIAL ,
    date DATE NOT NULL,
    temperature_2m_max DECIMAL(5,2),
    temperature_2m_min DECIMAL(5,2),
    temperature_2m_mean DECIMAL(5,2),
    relative_humidity_2m_mean SMALLINT,
    surface_pressure_mean DECIMAL(7,2),
    sea_level_pressure_mean DECIMAL(7,2),
    PRIMARY KEY (dim_location_id, date),
    CONSTRAINT fk_daily_location FOREIGN KEY (dim_location_id)
        REFERENCES dim_location(id)
);

-- Bảng fact: dữ liệu thời tiết theo giờ
CREATE TABLE IF NOT EXISTS fact_weather_hourly  (
    dim_location_id BIGSERIAL ,
    datetime TIMESTAMPTZ NOT NULL,
    temperature_2m DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    wind_direction SMALLINT,
    humidity_2m SMALLINT,
    visibility SMALLINT,
    rain DECIMAL(5,2),
    precipitation_probability SMALLINT,
    cloud_cover SMALLINT,
    surface_pressure DECIMAL(7,2),
    sea_level_pressure DECIMAL(7,2),
    PRIMARY KEY (dim_location_id, datetime),
    CONSTRAINT fk_hourly_location FOREIGN KEY (dim_location_id)
        REFERENCES dim_location(id)
);

""")
conn.commit()
conn.close()
cur.close()





