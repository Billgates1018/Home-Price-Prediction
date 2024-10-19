from flask import Flask, request, jsonify, render_template
import util

app = Flask(__name__)

# Route for the root URL
@app.route('/')
def home():
    return render_template('index1.html')  # Make sure you have index.html in your templates folder

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        response = jsonify({
            'locations': util.get_location_names()
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return a 500 error on failure

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except ValueError as e:
        return jsonify({'error': 'Invalid input: ' + str(e)}), 400  # Bad request error
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return a 500 error on failure

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)  # Set debug=True for development
