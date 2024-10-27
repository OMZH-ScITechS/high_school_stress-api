import pandas as pd
import numpy as np
import pickle
from flask import Flask, request, jsonify

results = []
model = pickle.load(open('newmodel.pkl', 'rb'))
app = Flask(__name__)

@app.route('/stress/predict', methods=['POST'])
def handle_json():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        results = request.get_json()['list']
        results_array = np.array(results).reshape(1, -1)
        prediction = model.predict(results_array)

        # 応答データの作成
        response_data = {
            "received_data": request.get_json()['list'],
            "prediction" : prediction[0]
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