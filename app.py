
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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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
#Convert to dict
prcp_dict = prcp_df.set_index("date").to_dict()["prcp"]

# Read station data table as dataframe
station_df = pd.read_sql_table("station", con=engine)
# create list of stations
station_list = station_df["station"].tolist()

from flask import Flask, jsonify, render_template, url_for

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Surfs Up API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    return jsonify(results = station_list)

# @app.route("/api/v1.0/tobs")
# def tobs():
#     return()

if __name__ == "__main__":
    app.run(debug=True)
