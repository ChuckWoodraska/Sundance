from sklearn.ensemble import RandomForestClassifier
from numpy import asarray
import pymysql.cursors
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
connection = pymysql.connect(config['DATABASE']['HOST'], config['DATABASE']['DBUSER'], config['DATABASE']['DBPASS'],
                             config['DATABASE']['DBNAME'])
try:
    data = []
    ratings = None
    cursor = connection.cursor()
    sql = "SELECT temp, code, today_code, high, low, wind_chill, wind_direction, wind_speed," \
          "pressure, rising, visibility, forecast_low1, forecast_high1, forecast_code1, forecast_low2, forecast_high2," \
          "forecast_code2, forecast_low3, forecast_high3, forecast_code3, forecast_low4, forecast_high4, forecast_code4," \
          "sunrise, sunset FROM weather WHERE chuck_rating IS NOT NULL AND rating IS NOT NULL"
    cursor.execute(sql)
    data = cursor.fetchall()

    sql = "SELECT temp, code, today_code, high, low, wind_chill, wind_direction, wind_speed," \
          "pressure, rising, visibility, forecast_low1, forecast_high1, forecast_code1, forecast_low2, forecast_high2," \
          "forecast_code2, forecast_low3, forecast_high3, forecast_code3, forecast_low4, forecast_high4, forecast_code4," \
          "sunrise, sunset FROM weather WHERE rating IS NULL"
    cursor.execute(sql)
    data_to_predict = cursor.fetchall()

    sql = "SELECT chuck_rating FROM weather WHERE chuck_rating IS NOT NULL"
    cursor.execute(sql)
    ratings = cursor.fetchall()

    new_data = asarray(data)
    X = new_data[:, [x for x in range(0, 25)]]
    Y = asarray([rating[0] for rating in ratings])

    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X, Y)
    predictions = clf.predict(data_to_predict)
    print(predictions)
    print(clf.feature_importances_)
    sql = "SELECT id FROM weather WHERE chuck_rating IS NULL AND rating IS NULL"
    cursor.execute(sql)
    ids = cursor.fetchall()

    for x in range(len(ids)):
        sql = "UPDATE weather SET rating=%s WHERE id=%s"
        sql_params = [str(predictions[x]), ids[x][0]]
        cursor.execute(sql, sql_params)
        connection.commit()
except Exception as e:
    print(e)
finally:
    connection.close()