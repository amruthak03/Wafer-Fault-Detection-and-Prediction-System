from wsgiref import simple_server
from flask import Flask, request, render_template, jsonify
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

"""
This code sets up a web application using Flask to handle machine learning model training and predictions. 
It provides endpoints to train a model with uploaded data and make predictions using the trained model.
"""
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)  # Adds a monitoring dashboard to the application.
CORS(app)  # Allows cross-origin resource sharing, enabling requests from different domains.

# Home route - Renders the index.html template, typically the homepage for the app
@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']
            # object initialization
            pred_val = pred_validation(path)
            # calling the prediction_validation function
            pred_val.prediction_validation()
            pred = prediction(path)
            # predicting for a dataset
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at" + str(path)+ 'and few of the predictions are '
                            +str(json.loads(json_predictions)))
        elif request.form is not None:
            path = request.form['filepath']
            pred_val = pred_validation(path)
            pred_val.prediction_validation()
            pred = prediction(path)
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at " + str(path) + 'and Few of the predictions are \n' + str(
                json.loads(json_predictions)))
        else:
            print('Nothing Matched')

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path) # Object initialization
            train_valObj.train_validation() # Calling the train_validation method
            trainModelObj = trainModel()
            trainModelObj.trainingModel() # Traing the model for files in the table

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training successfully!!")


port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
    app.run(debug=True)