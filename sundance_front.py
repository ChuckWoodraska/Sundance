from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pymysql
import configparser
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def sundance():
    return render_template('sundance.jinja2', coat=get_rating())


def get_rating():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.curdir), 'config.ini'))
    connection = pymysql.connect(config['DATABASE']['HOST'], config['DATABASE']['DBUSER'], config['DATABASE']['DBPASS'],
                                 config['DATABASE']['DBNAME'])
    cursor = connection.cursor()
    sql = "SELECT rating FROM weather WHERE rating IS NOT NULL ORDER BY id DESC LIMIT 1"
    cursor.execute(sql)
    rating = cursor.fetchone()
    print(int(rating[0]))
    return int(rating[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
