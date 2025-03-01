import pandas as pd
import numpy as np
import pickle
import math
from flask import Flask, request, jsonify

results = []
model_f1 = pickle.load(open('newmodel_f1.pkl', 'rb'))
model_f2 = pickle.load(open('newmodel_f2.pkl', 'rb'))
app = Flask(__name__)

@app.route('/stress/predict', methods=['POST'])
def handle_json():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        results = request.get_json()['list']
        results_f1 = results[:5]
        results_f2 = results[5:]
        results_array_f1 = np.array(results_f1).reshape(1, -1)
        results_array_f2 = np.array(results_f2).reshape(1, -1)
        prediction_f1 = model_f1.predict(results_array_f1)
        prediction_f2 = model_f2.predict(results_array_f2)

        # 応答データの作成
        response_data = {
            "received_data": request.get_json()['list'],
            "prediction_f1": math.floor(prediction_f1[0]*100)/100,
            "prediction_f2": math.floor(prediction_f2[0]*100)/100
        }

        # JSON形式で応答を返す
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# エラーハンドリング
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request"}), 400

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
    print('server stated')