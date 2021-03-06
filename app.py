import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

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
        f"/api/v1.0/stations</br>"
        f"api/v1.0/tobs</br>"
        f"api/v1.0/<start></br>"
        f"api/v1.0/<start>/<end>"

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of Dates and precipitation from last year"""
    # Query
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_date
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).order_by(Measurement.date)
    # Convert to dictionary
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)

    return jsonify(precipitation_values)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of weather stations """
    # Query all stations
    results = session.query(Station.station).all()
    
    station_name= list(np.ravel(results))
    
    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations"""
    # Query all values
    results = session.query(Measurement.tobs).all()

  
    tobs_list= list(np.ravel(results))

    return jsonify(tobs_list) 

@app.route("/api/v1.0/<start>")
def starting_temp(start):

  
    """Return a JSON list of min, max, avg """

    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    return jsonify(start_temp)

    

@app.route("/api/v1.0/<start>/@app.route("/api/v1.0/<start>/<end>")
<end>")
def start_end(start, end):

    """Inbetween dates"""
    
    start_end_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(and_(Measurement.date >= start, Measurement.date <= end)).all()
    
    return jsonify(start_end_temp)



if __name__ == '__main__':
    app.run(debug=True)