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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     return()

# @app.route("/api/v1.0/stations")
# def stations():
#     return()

# @app.route("/api/v1.0/tobs")
# def tobs():
#     return()

if __name__ == "__main__":
    app.run(debug=True)
