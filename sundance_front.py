from flask import Flask, render_template, request, jsonify
from flask.ext.bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import socket
import struct
import datetime

UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def dashboard():
    return render_template('dashboard.jinja2')


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


@app.route('/ip_converter', methods=['POST', 'GET'])
def ip_converter_form():
    return render_template('ip_converter.jinja2')


@app.route('/ip_converter/ip', methods=['POST', 'GET'])
def ip_converter_ip():
    print(request.form['ip'])
    return jsonify({'answer': ip2long(request.form['ip'])})


@app.route('/ip_converter/int', methods=['POST', 'GET'])
def ip_converter_int():
    return jsonify({'answer': long2ip(int(request.form['int']))})


@app.route('/time_converter', methods=['POST', 'GET'])
def time_converter_form():
    return render_template('time_converter.jinja2')


@app.route('/time_converter/unix', methods=['POST', 'GET'])
def time_converter_unix():
    return jsonify({'answer': unix2datetime(request.form['unix'])})


@app.route('/chillberry', methods=['POST', 'GET'])
def chillberry():
    return render_template('chillberry.jinja2')


@app.route('/chillberry/upload', methods=['POST'])
def chillberry_upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('chillberry.jinja2', {'table_data': get_table_data()})

@app.route('/sundance', methods=['GET', 'POST'])
def sundance():
    return render_template('sundance.jinja2', coat=1)

# @staticmethod
def get_table_data():
    pass


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def unix2datetime(unix):
    return str(datetime.datetime.fromtimestamp(int(unix)))


def ip2long(ip):
    return struct.unpack('!L', socket.inet_aton(ip))[0]


def long2ip(ip):
    return socket.inet_ntoa(struct.pack('!I', ip))


if __name__ == '__main__':
    app.run(debug=True)