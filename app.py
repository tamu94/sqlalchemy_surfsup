# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    func,
    inspect,
    desc,
    MetaData,
    Table,
    Column,
    ForeignKey,
    Date,
    Integer,
    String,
    Float,
    distinct,
)
import pandas as pd
import os
import pprint

import datetime as dt
from dateutil.relativedelta import relativedelta
import datetime as dt
from dateutil.relativedelta import relativedelta

# path =os.join.path(Resources, )
# Setup Engine for SQlAlchemy
engine = create_engine(
    "sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}
)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# Find the date from latest date to one year ago
year_ago = dt.date(2017, 8, 23) - relativedelta(years=1)
measurements_one_year = (
    session.query(Measurement.date, Measurement.prcp)
    .filter(Measurement.date >= year_ago)
    .all()
)
# Create dataframe from one year of measurements using only prcp and date
prcp_df = pd.DataFrame.from_records(measurements_one_year)
prcp_df.columns = ["date", "prcp"]
# drop NaN - will cause issues with Jsonify
prcp_df = prcp_df.dropna(subset=["prcp"])
# Convert to dict
prcp_dict = prcp_df.set_index("date").to_dict()["prcp"]

# Read station data table as dataframe
station_df = pd.read_sql_table("station", con=engine)
# create list of stations
station_list = station_df["station"].tolist()
# Find the date from latest date to one year ago for tobs
year_ago = dt.date(2017, 8, 18) - relativedelta(years=1)
temp_obs = (
    session.query(Measurement.date, Measurement.tobs)
    .filter(Measurement.station == "USC00519281")
    .filter(Measurement.date >= year_ago)
    .all()
)
# Create dataframe
temp_df = pd.DataFrame.from_records(temp_obs)
temp_df.columns = ["date", "tobs"]
# Drop NaN
temp_df = temp_df.dropna(subset=["tobs"])
# Convert temp_df to dict
temp_dict = temp_df.set_index("date").to_dict()["tobs"]

from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Surfs Up API<br/>"
        f"Available Routes:<br/>"
        f"<strong>/api/v1.0/precipitation</strong> &nbsp;&nbsp; <i>Returns JSON dictionary for 1 year of precipitation results</i><br/>"
        f"<strong>/api/v1.0/stations</strong>  &nbsp;&nbsp; <i>Returns a JSON list of the stations</i><br/>"
        f"<strong>/api/v1.0/tobs</strong>  &nbsp;&nbsp; <i>Returns a JSON list of dates and tobs for 1 year from the businest station</i><br/>"
        f"<strong>/api/v1.0/</strong>   &nbsp;&nbsp; <i>Returns TMIN, TAVE, and TMAX from start-date/end-date. Date format=yyyy-mm-dd**</i><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(temp_dict)


@app.route("/api/v1.0/<start>/<end>")
def range_temps(start, end):
    try:
        temps = (
            session.query(
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs),
            )
            .filter(Measurement.date >= start)
            .filter(Measurement.date <= end)
            .all()
        )
        return jsonify(temps)
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})
    return "Date not found!", 404


@app.route("/api/v1.0/<start>")
def start_temp(start):
    try:
        temps = (
            session.query(
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs),
            )
            .filter(Measurement.date >= start)
            .all()
        )
        return jsonify(temps)
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})
    return "Date not found!", 404


if __name__ == "__main__":
    app.run(debug=True)
