from wsgiref import simple_server
from flask import Flask, render_template, request, jsonify
from flask import Response
from flask_cors import CORS,cross_origin
from logistic_deploy import predObj
import pickle

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

class ClientApi:

    def __init__(self):
        self.predObj = predObj()

@app.route("/predict", methods=['GET','POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
           # reading the input from user

            Pregnancies =float(request.form['Pregnancies'])
            Glucose = float(request.form['Glucose'])
            BloodPressure=float(request.form['BloodPressure'])
            SkinThickness=float(request.form['SkinThickness'])
            Insulin = float(request.form['Insulin'])
            BMI = float(request.form['BMI'])
            DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
            Age = float(request.form['Age'])
            filename = 'modelForPrediction.sav'
            loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
            scalar = pickle.load(open('sandardScalar.sav', 'rb'))
            # predictions using the loaded model file
            prediction = loaded_model.predict(scalar.transform([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]))
            print('prediction is', prediction)
            # showing predictions in UI
            if prediction == 1:
                prediction = 'You are diabetic'
                return render_template('results.html', prediction=prediction)
            else:
                prediction = 'You are not diabetic'
                return render_template('dia_no.html', prediction=prediction)
            # showing the prediction results in a UI

        except Exception as e:
            print('The Exception message is: ',str(e))
            return 'something is wrong'
    #return render_template('results.html',prediction=prediction[0])

    # else:
    #return render_template('index.html')

@app.route('/from_postman', methods=['POST'])
def from_postman():
    if (request.method == 'POST'):
        try:
            # reading the input from user

            Pregnancies = float(request.json['Pregnancies'])
            Glucose = float(request.json['Glucose'])
            BloodPressure = float(request.json['BloodPressure'])
            SkinThickness = float(request.json['SkinThickness'])
            Insulin = float(request.json['Insulin'])
            BMI = float(request.json['BMI'])
            DiabetesPedigreeFunction = float(request.json['DiabetesPedigreeFunction'])
            Age = float(request.json['Age'])
            filename = 'modelForPrediction.sav'
            loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
            scalar = pickle.load(open('sandardScalar.sav', 'rb'))
            # predictions using the loaded model file
            prediction = loaded_model.predict(scalar.transform([[Pregnancies, Glucose, BloodPressure, SkinThickness,
                                                                 Insulin, BMI, DiabetesPedigreeFunction, Age]]))
            print('prediction is', prediction)
            return jsonify({"prediction": prediction})


        except ValueError:
           return Response("Value not found")
        except Exception as e:
            print('exception is   ', e)
            return Response(e)


if __name__ == "__main__":
    clntApp = ClientApi()
    host = '0.0.0.0'
    port = 5000
    app.run(debug=True)
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()