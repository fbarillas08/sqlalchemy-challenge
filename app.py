## Flask Application that runs desired queries about Hawaii's Weather

import numpy as np
import pandas as pd
import datetime as dt


from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Create the app
app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"Hawaii Weather Metrics Available Routes<br/>"
        f"  Lists the Stations in the system: <br/>"
        f"/api/v1.0/stations<br/>"
        f"Lists Precipitation for the past 12 months: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Lists Temperatures for the past 12 months: <br/>"
        f"/api/v1.0/temperatures<br/>"
        f"Lists the precipitation after the specified date: <br/>"
        f"/api/v1.0/start<br/>"
        f"Lists the precipitation between the specified dates: <br/> "
        f"/api/v1.0/start/end<br/>"
        f"------<br/>"
        f"Date format is like 2012-02-28"
    )


# Define function for list of stations
@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.station).all()
    stat = list(np.ravel(all_stations))
    return jsonify(stations=stat)


# Define function for precipitation: Last 12 months sorted by date
@app.route("/api/v1.0/precipitation")
def precipitation():    
    OneYearAgoDate = dt.date(2017,8,23) - dt.timedelta(days=365)
    OneYearPrecipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= OneYearAgoDate).all()
    OneYearPRCP_df = pd.DataFrame(OneYearPrecipitation)
    # Save OneYear_PRCP as a json file
    OneYearPRCP_df.to_json(r'C:\Users\Corsair_Barillas\Documents\FAB\Quant\UMBootcamp\UM_Homework\HW10-Sqlalchemy\Outputs\OneYear.json')
    # Display json file in the designated route
    prcp_oneyear = list(np.ravel(OneYearPrecipitation))
    return jsonify(oneyearrain=prcp_oneyear)

# Define function for temperature: Last 12 months sorted by date
@app.route("/api/v1.0/temperatures")
def temperature():
    OneYearAgoDate1 = dt.date(2017,8,23) - dt.timedelta(days=365)
    OneYearTemperatures = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= OneYearAgoDate1).all()
    OneYearTOBS_df = pd.DataFrame(OneYearTemperatures)
    # Save OneYear_TOBS as a json file
    OneYearTOBS_df.to_json(r'C:\Users\Corsair_Barillas\Documents\FAB\Quant\UMBootcamp\UM_Homework\HW10-Sqlalchemy\Outputs\OneYeartobs.json')
    # Display json file in the designated route
    tobs_oneyear = list(np.ravel(OneYearTemperatures))
    return jsonify(oneyeartemps=tobs_oneyear)


#Define function for temp_start
@app.route('/api/v1.0/<start>')
def tobs_start(start=None):    
    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).all()    

    tobs_all = []
    tobs_dict = {}
    for min,avg,max in start_query:
        tobs_dict["Min"]= min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_all.append(tobs_dict)

    return jsonify(tobs_all=tobs_all)


#Define function for temp_start_end
# @app.route('/api/v1.0/<start>/<end>')
# def calc_temps(start=None, end=None):   
#     calc= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start).filter(Measurement.date <= end).all()
#     variable = list(np.ravel(calc))
#     return jsonify(variable=variable)


@app.route('/api/v1.0/<start>/<end>')
def tobs_period(start=None, end=None):    
    period_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).filter(Measurement.date <= end).all()    

    tobs1_all = []
    tobs1_dict = {}
    for min1,avg1,max1 in period_query:
        tobs1_dict["Min"]= min1
        tobs1_dict["Average"] = avg1
        tobs1_dict["Max"] = max1
        tobs1_all.append(tobs1_dict)

    return jsonify(tobs1_all=tobs1_all)




# Close Session
session.close()

if __name__ == "__main__":
    app.run(debug=True)







