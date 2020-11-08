"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
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
     'BarCodeID': 'BC100001',
     'BeginTime': '2020-11-08 11:00:00',
     'EndTime': '2020-11-08 11:15:00',
     'Email': 'Kathryn.Clement@gmail.com',
     'Phone': '2074913816'
    },
    {'id': 1,
     'BarCodeID': 'BC100002',
     'BeginTime': '2020-11-08 09:43:00',
     'EndTime': '2020-11-08 10:58:00',
     'Email': 'Jason.p.clement@gmail.com',
     'Phone': '2074913816'
    }
]


@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
