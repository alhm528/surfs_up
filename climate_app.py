import numpy as np

import sqlalchemy

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

from datetime import datetime

import datetime as dt

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite",
                       connect_args={'check_same_thread': False}, echo=True)

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)

# Flask Setup

app = Flask(__name__)

# Set up Flask Routes


@app.route("/")
def home():
    """List all available api routes."""

    return (f"Hawaii Weather Data API<br/>"

            f"/api/v1.0/precipitation<br/>"

            f"/api/v1.0/stations<br/>"

            f"/api/v1.0/tobs<br/>"

            f"/api/v1.0/<start>/<br/>"

            f"/api/v1.0/<start>/<end>/")


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Docstring
    """Return a list of precipitation from last year"""

    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    max_date = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()

    # Get the first element of the tuple

    max_date = max_date[0]

    # Calculate the date 1 year ago from today

    year_ago = dt.datetime.strptime(
        max_date, "%Y-%m-%d") - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores

    results_precipitation = session.query(
        Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # Convert list of tuples into normal list

    precipitation_dict = dict(results_precipitation)

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():

    # Docstring
    """Return a JSON list of stations from the dataset."""

    # Query stations

    results_stations = session.query(
        Measurement.station).group_by(Measurement.station).all()

    # Convert list of tuples into normal list

    stations_list = list(np.ravel(results_stations))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():

    # Docstring
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""

    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    max_date = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()

    # Get the first element of the tuple

    max_date = max_date[0]

    # Calculate the date 1 year ago from today

    year_ago = dt.datetime.strptime(
        max_date, "%Y-%m-%d") - dt.timedelta(days=366)

    # Query tobs

    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= year_ago).all()

    # Convert list of tuples into normal list

    tobs_list = list(results_tobs)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start):

    start_date = datetime.strptime(start, '%Y-%m-%d')

    minimum = session.query(func.min(Measurement.tobs)).filter(
        Measurement.date >= start_date).scalar()

    average = session.query(func.round(func.avg(Measurement.tobs))).filter(
        Measurement.date >= start_date).scalar()

    maximum = session.query(func.max(Measurement.tobs)).filter(
        Measurement.date >= start_date).scalar()

    result = [{"TMIN": minimum}, {"TMAX": maximum}, {"TAVG": average}]

    return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def StartEnd(start, end):

    start_date = datetime.strptime(start, '%Y-%m-%d')

    end_date = datetime.strptime(end, '%Y-%m-%d')

    minimum = session.query(func.min(Measurement.tobs)).filter(
        Measurement.date.between(start_date, end_date)).scalar()

    average = session.query(func.round(func.avg(Measurement.tobs))).filter(
        Measurement.date.between(start_date, end_date)).scalar()

    maximum = session.query(func.max(Measurement.tobs)).filter(
        Measurement.date.between(start_date, end_date)).scalar()

    result = [{"TMIN": minimum}, {"TMAX": maximum}, {"TAVG": average}]

    return jsonify(result)


if __name__ == '__main__':

    app.run(debug=True)
