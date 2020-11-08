from flask import Flask
from flask import make_response, jsonify, request
from flask_restful import Resource, Api, reqparse
import sqlite3 as sql
import os
import json


### Pull in Config Data
programConfig = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
with open(programConfig) as json_data_file:
    data = json.load(json_data_file)
    myDb = data['dbName']




app = Flask(__name__)
api = Api(app)



conn = sql.connect(myDb)
conn.execute('CREATE TABLE IF NOT EXISTS Scans (id INTEGER PRIMARY KEY AUTOINCREMENT, BarCodeID TEXT, BeginTime datetime, EndTime datetime, Email TEXT, Phone TEXT)')
conn.close()

##endpoint that would be used in event we use singular message solution
class scanEmission(Resource):
    ##doubt we need a get - but just for testing...
    def get(self):
        with sql.connect(myDb) as con:
            try:
                sqlCmd = "SELECT BarCodeID, BeginTime, EndTime, Email, Phone FROM Scans"            
                cur = con.cursor()
                cur.execute(sqlCmd)
                rows = cur.fetchall(); 

            except Exception as e:  ##Revisit this to make more robust
                con.rollback()
                msg = f"({repr(e)})"
            finally:
                return rows

    def post(self):
        scanData = request.get_json()

        with sql.connect(myDb) as con:
            try:
                BarCodeID = scanData['BarCodeID']
                BeginTime = scanData['BeginTime']
                EndTime = scanData['EndTime']
                Email = scanData['Email']
                Phone = scanData['Phone']
         
            
                cur = con.cursor()
                cur.execute("INSERT INTO Scans (BarCodeID,BeginTime,EndTime,Email,Phone) VALUES (?,?,?,?,?)",(BarCodeID,BeginTime,EndTime,Email,Phone))
                con.commit()
                msg = "Record successfully added"

                #Add Messaging interface (for email and text stuff)

                #Add Cisco Cam stuff


            except Exception as e:  ##Revisit this to make more robust
                con.rollback()
                msg = f"({repr(e)})"
            finally:
                return msg

##endpoint that would be used in event we use batched message solution
class scanEmissions(Resource):
    def post(self):
        scanItems = request.get_json()

        with sql.connect(myDb) as con:
            cur = con.cursor()
            try:
                for scanItem in scanItems:
                    BarCodeID = scanItem['BarCodeID']
                    BeginTime = scanItem['BeginTime']
                    EndTime = scanItem['EndTime']
                    Email = scanItem['Email']
                    Phone = scanItem['Phone']
                             
                    cur.execute("INSERT INTO Scans (BarCodeID,BeginTime,EndTime,Email,Phone) VALUES (?,?,?,?,?)",(BarCodeID,BeginTime,EndTime,Email,Phone))
                con.commit()
                msg = "Records successfully added"
            except Exception as e:  ##Revisit this to make more robust
                con.rollback()
                msg = f"({repr(e)})"
            finally:
                return msg

        
api.add_resource(scanEmission, '/scanEmission')
api.add_resource(scanEmissions, '/scanEmissions')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    #app.run(debug=True, host='0.0.0.0', port=80)
    app.run(HOST, 5100)