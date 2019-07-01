import numpy as np

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and precipitation"""
    # Query all precips
    results = session.query(Measurement.date,Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_dates = list(np.ravel(results))

    return jsonify(all_dates)

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



# @app.route("/api/v1.0/stations")
# def stations():
#     """Return a list of stations"""
#     # Query all stations
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

if __name__ == '__main__':
    app.run(debug=True)
