from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def index():
    return(
        "home"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    results_dic = {date: prcp for date, prcp in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.stations).all()

    results_dic = {date: prcp for date, prcp in results}

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23').all()

    results_dic = {date: tobs for date, tobs in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/<start>")
def start(startdate):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= startdate).all()

    results_dic = {date: tobs for date, tobs in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/<start>/<end>")
def startend(startdate,enddate):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= startdate, Measurement.date <= enddate).all()

    results_dic = {date: tobs for date, tobs in results}
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
