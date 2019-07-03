import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end<br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and precipitation"""
    # Query all precips
    p_results = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date<='2017-08-23').filter(Measurement.date>='2016-08-24').all()


    # Convert list of tuples into normal list
    year_prcp = list(np.ravel(p_results))

    return jsonify(year_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all precips
    stat_results = session.query(Station.station, Station.name).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stat_results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures for the last year"""
    # Query all temperatures from last 12 month
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
filter(Measurement.date<='2017-08-23').filter(Measurement.date>='2016-08-24').order_by(Measurement.date.asc()).all()

    all_tobs = list(np.ravel(tobs_results))

    return jsonify(all_tobs)


###############################
#Start date API

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of average, min and max temps for year after start date"""
    # Return avg, max, min from start date
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_yr = dt.datetime(days=365)
    start = start_date - last_yr
    end = dt.date (2017,8,23)
    trip_data= session.query(func.min(Measurement.tobs, func.avg(Measurement.tobs\
    , func.max(Measurement.tobs))))\
    .filter(Measurement.date>=start)\
    .filter(Measurement.date<=end).all()
    year_data=list(np.ravel(trip_data))

    return jsonify (year_data)
   

####Start and End Date##################

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Return a list of average, min and max temps for year after start date"""
    # Return avg, max, min from start date
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(start, '%Y-%m-%d')
    start = start_date - end_date
    end=end_date
    new_trip_data= session.query(func.min(Measurement.tobs, func.avg(Measurement.tobs\
    , func.max(Measurement.tobs))))\
    .filter(Measurement.date>=start)\
    .filter(Measurement.date<=end).all()
    start_end_data=list(np.ravel(new_trip_data))

    return jsonify (start_end_data)

if __name__ == '__main__':
    app.run(debug=True)
