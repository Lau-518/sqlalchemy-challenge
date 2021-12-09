import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Latest Date
#################################################


query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station


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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
       


    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitaion data for every date"""
    # Query all precipation data per date
    results = session.query(Measurement.date, Measurement.prcp).\
                  filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_Measurement = []
    for date, prcp in results:


        Measurement_dict = {}
        Measurement_dict["date"] = date
        Measurement_dict["prcp"] = prcp
        all_Measurement.append(Measurement_dict)

    return jsonify(all_Measurement)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations in the database"""
    # Query all precipation data per date
    results = session.query(Station.id, Station.station).\
                  filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_Station = []
    for id, station in results:


        Station_dict = {}
        Station_dict["id"] = id
        Station_dict["station"] = station
        all_Station.append(Station_dict)

    return jsonify(all_Station)

@app.route("/api/v1.0/tobs")

def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs for the most active station in the database"""
    # Query all precipation data per date
    # results = session.query(Station.id, Station.station).all()

    most_active_station = session.query(Measurement.date, Measurement.station, 
                        Measurement.tobs).\
                  filter(Measurement.station == "USC00519281").\
                  filter(Measurement.date >= query_date).all()
                    



    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    Station_mostactive = []
    for date, station, tobs in most_active_station:
        most_active_Station_dict = {}
        most_active_Station_dict["date"] = date
        most_active_Station_dict["station"] = station
        most_active_Station_dict["tobs"] = tobs

        Station_mostactive.append(most_active_Station_dict)


    return jsonify(Station_mostactive)

@app.route("/api/v1.0/<start_date>")

def start_date_climate(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs for the most active station in the database"""


    start_date_climate = session.query(func.min(Measurement.tobs), 
                       func.avg(Measurement.tobs), 
                        func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start_date).all()
                  



    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers

    start_date_climate = []
    for tobs_min,tobs_avg, tobs_max  in start_date_climate:
        start_date_climate_dict = {}
        start_date_climate_dict["tobs_min"] = tobs_min
        start_date_climate_dict["tobs_avg"] = tobs_avg
        start_date_climate_dict["tobs_max"] = tobs_max


        start_date_climate.append(start_date_climate_dict)

      


    return jsonify(start_date_climate)

@app.route("/api/v1.0/<start_date>/<end_date>")

def start_end_date_climate(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs for the most active station in the database"""

    start_end_date_climate = session.query(func.min(Measurement.tobs), 
                       func.avg(Measurement.tobs), 
                        func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start_date).\
                filter(Measurement.date <= end_date).all()
                



    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers

    start_end_date_climate = []
    for tobs_min,tobs_avg, tobs_max  in start_end_date_climate:
        start_end_date_climate_dict = {}
        start_end_date_climate_dict["tobs_min"] = tobs_min
        start_end_date_climate_dict["tobs_avg"] = tobs_avg
        start_end_date_climate_dict["tobs_max"] = tobs_max


        start_end_date_climate.append(start_end_date_climate_dict)

   
    


    return jsonify(start_end_date_climate)


if __name__ == '__main__':
    app.run(debug=True)
