from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, redirect, url_for, request,jsonify
import os.path

app = Flask(__name__)
db_filename = 'castle_sessions.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///castle_sessions.db' #3 Slashes is relative path, everything is stored in test.db
db = SQLAlchemy(app)

#DATABASE##############################################################################################################
class CastleSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    benchid = db.Column(db.String,nullable=False)
    username = db.Column(db.String,nullable=False)

    pipversion = db.Column(db.String,nullable=False)
    fwversion = db.Column(db.String,nullable=False)
    prj = db.Column(db.String,nullable=False)
    team = db.Column(db.String,nullable=False)
    loc = db.Column(db.String,nullable=False)

    is_calibrated  = db.Column(db.String,nullable=False)
    calib_date = db.Column(db.String,nullable=False)
    defects = db.Column(db.String,nullable=False)


    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<User(benchid='%s', username='%s', time'%s', pipversion'%s', fwversion'%s', prj'%s', team'%s', loc'%s')>" % (
                               self.benchid, self.username, self.date_created, self.pipversion,self.fwversion,self.prj,self.team,self.loc)


def add_session_to_db(benchid,username, time,pipversion,fwversion , prj ,team,loc,is_calibrated,calib_date,defects):
    request = "New Request =" + benchid + "-" + username + "-" + time + "-" + str(pipversion) + "-" + str(fwversion) + "-" + str(prj) + "Team" + "-" + str(team)+ "-" + str(loc)
    new_session = CastleSession(benchid=benchid,username =username, pipversion=pipversion,fwversion=fwversion,prj=prj,team=team,loc=loc,is_calibrated=is_calibrated,calib_date=calib_date,defects=defects )
    db.session.add(new_session)
    db.session.commit()
    print(request)
    return request


@app.route('/success/<msg>')
def success(msg):
    print("Valid Request:" + msg)
    return 'Request Added %s' % msg


@app.route('/failure/<msg>')
def failure(msg):
    print("Bad Request:"+ msg)
    return 'Bad Request %s' % msg



@app.route('/')
@app.route('/sessions',methods = ['GET'])
@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':

        response = {}

        json_data = request.json
        #Validate Input
        if 'benchid' not in json_data :
            response["ERROR"] = "<benchid> key is missing"
            return jsonify(response)
        if 'username' not in json_data :
            response["ERROR"] = "<username> key is missing"
            return jsonify(response)
        if 'time' not in json_data :
            response["ERROR"] = "<time> key is missing"
            return jsonify(response)
        if 'pipversion' not in json_data :
            error = "<pipversion> key is missing"
            return jsonify(response)
        if 'fwversion' not in json_data :
            response["ERROR"] = "<fwversion> key is missing"
            return jsonify(response)
        if 'prj' not in json_data :
            response["ERROR"] = "<prj> key is missing"
            return jsonify(response)
        if 'hmi' not in json_data :
            response["ERROR"] = "<hmi> key is missing"
            return jsonify(response)
        if 'loc' not in json_data :
            response["ERROR"] = "<loc> key is missing"
            return jsonify(response)
        if 'calib' not in json_data :
            response["ERROR"] = "<calib> key is missing"
            return jsonify(response)
        if 'calib_date' not in json_data :
            response["ERROR"] = "<calib_date> key is missing"
            return jsonify(response)
        if 'defects' not in json_data :
            response["ERROR"] = "<defects> key is missing"
            return jsonify(response)

        # Process Request
        benchid = str(json_data["benchid"])
        username = str(json_data["username"])
        time = str(json_data["time"])
        pipversion = str(json_data["pipversion"])
        fwversion = str(json_data["fwversion"])
        prj = str(json_data["prj"])
        team = str(json_data["hmi"])
        loc = str(json_data["loc"])
        is_calibrated = str(json_data["calib"])
        calib_date = str(json_data["calib_date"])
        defects = str(json_data["defects"])

        print(benchid)
        print(calib_date)
        print(defects)

        rq = add_session_to_db(benchid,username, time,pipversion,fwversion , prj ,team,loc,is_calibrated,calib_date,defects)


        response["MESSAGE"] = rq

        return jsonify(response)
    else:
        sessions = CastleSession.query.order_by(CastleSession.date_created).all()
        return render_template('index.html', sessions=sessions)

#Enable only on first run, let us add a check to create it if it doesn't exist.
create_db = False

if __name__ == '__main__':
    #if os.path.isfile(db_filename)  == False:
        #print("Creating Database"+db_filename)
    db.create_all()

    #app.run(debug = True)
    #app.run(host = '0.0.0.0')
    app.run(threaded=True, port=5000)