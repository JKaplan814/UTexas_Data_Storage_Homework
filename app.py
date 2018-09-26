from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import datetime as dt
import numpy as np

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
        f"Weather API<br/>"
        f"Available Routes:<br/><br/>"
        f"Precipitation:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"Stations:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"Temperatures:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Temperature summary from a start date onwards (yyyy-mm-dd):<br/>"
        f"/api/v1.0/(start_date)<br/><br/>"
        f"Temperature summary between a start date and end date (yyyy-mm-dd):<br/>"
        f"/api/v1.0/(start_date)/(end_date)<br/><br/>"
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
    results = session.query(Station.station, Station.name).all()

    results_dic = {station: name for station, name in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23').all()

    results_dic = {date: tobs for date, tobs in results}

    return jsonify(results_dic)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    

    return jsonify(results_dic)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start, Measurement.date <= end).all()

    results_dic = list(np.ravel(results))
    
    return jsonify(results_dic)

if __name__ == "__main__":
    app.run(debug=True)
