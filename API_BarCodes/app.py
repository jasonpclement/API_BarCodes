"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask import request, jsonify, make_response, abort

import sqlite3
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# temporary test data 
netNewScans = [
    {'id': 0,
     'BarCodeID': 'BC100001',
     'BeginTime': '2020-11-08 12:43:00',
     'EndTime': '2020-11-08 12:58:00',
     #Not 100% sure what we need for fields at this stage, but here's some placeholders
     'Email': 'Jason.p.clement@gmail.com', 
     'Phone': '2074913816'
    },
    {'id': 1,
     'BarCodeID': 'BC200001',
     'BeginTime': '2020-11-08 11:00:00',
     'EndTime': '2020-11-08 11:15:00',
     'Email': 'Kathryn.Clement@gmail.com',
     'Phone': '2074913816'
    },
    {'id': 2,
     'BarCodeID': 'BC100002',
     'BeginTime': '2020-11-08 09:43:00',
     'EndTime': '2020-11-08 10:58:00',
     'Email': 'Jason.p.clement@gmail.com',
     'Phone': '2074913816'
    }
]


@app.route('/')
def index():
    siteDef = ""
    for scan in netNewScans:
        scan['id']
        siteDef = siteDef + (
            f"<p>BarCodeID:{scan['BarCodeID']}" + 
            f"\t\tBeginTime:{scan['BeginTime']}" + 
            f"\t\tEndTime:{scan['EndTime']}</p>"
        )
       
    return siteDef

@app.route('/api/PushScanSingular', methods=['POST'])
def PushScanSingular():
    conn = sqlite3.connect('scans.db')
    cur = conn.cursor()


    ##all_books = cur.execute('SELECT * FROM books;').fetchall()
    #netNewScans

    ##if not request.json or not 'title' in request.json:
    ##    abort(400)

    scansToSync = {
        'title': request.json['title']
    }

    return jsonify({'Scans': scansToSync}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, 5100)
