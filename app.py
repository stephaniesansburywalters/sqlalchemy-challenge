import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database-ing
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create session from Python to the DB
session = Session(engine)

# Flask-ing
app = Flask(__name__)

# last 12 variable
twelve_prior = '2016-08-23'

@app.route("/")
def welcome():
    return (
        f"<p>WELCOME!</p>"
        f"<p>Usage:</p>"
        f"/api/v1.0/precipitation<br/>Returns JSON for percipitation for dates between 8/23/16 & 8/23/17<br/><br/>"
        f"/api/v1.0/stations<br/>Returns JSON for the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Returns JSON for the Temp Obs. for each station for dates between 8/23/16 & 8/23/17<br/><br/>"
        f"/api/v1.0/date<br/>Returns JSON for the min. temp, the avg temp, and the max temp for dates between the given start date and 8/23/17<br/><br/>."
        f"/api/v1.0/start_date/end_date<br/>Returns JSON for min temp, the avg temp, and the max temp for dates between the given start and end date<br/><br/>."
    )

# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Date 12 prior
    last_twelve_prcp_data = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= twelve_prior).group_by(Measurement.date).all()
    return jsonify(last_twelve_prcp_data)


# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    all_the_stations = session.query(Station.station, Station.name).all()
    return jsonify(all_the_stations)


# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    temp_obs = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= twelve_prior).all()
    return jsonify(temp_obs)


# /api/v1.0/<start>
@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    given_day_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(given_day_temp)


# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def StartEndDate(start,end):
    temp_for_so_many_days = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp_for_so_many_days)

if __name__ == "__main__":
    app.run(debug=True)