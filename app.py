import pandas as pd
import numpy as np
import pickle
import math
from flask import Flask, request, jsonify

# モデルをロード
model_f1 = pickle.load(open('newmodel_f1.pkl', 'rb'))
model_f2 = pickle.load(open('newmodel_f2.pkl', 'rb'))

app = Flask(__name__)

@app.route('/stress/predict', methods=['POST'])
def predict():
    try:        
        # 必要な入力データを取得（ここでは10つの特徴量を想定）
        features = request.get_json()['list']
        if not features or len(features) != 10:
            return jsonify({"error": "Invalid numbers of features."}), 400
        
        # NumPy配列に変換
        input_array_f1 = np.array(features[:5]).reshape(1, -1)
        input_array_f2 = np.array(features[5:]).reshape(1, -1)
        
        # 予測を実行
        prediction_f1 = model_f1.predict(input_array_f1)[0]
        prediction_f2 = model_f2.predict(input_array_f2)[0]
        
        # 各特徴量の影響度を計算
        feature_impact_f1 = []
        for i in range(5):
            modified_input = input_array_f1.copy()
            modified_input[0, i] += 1  # その特徴量だけ +1
            modified_prediction = model_f1.predict(modified_input)[0]
            impact = abs(modified_prediction - prediction_f1)
            feature_impact_f1.append(impact)
        
        feature_impact_f2 = []
        for i in range(5):
            modified_input = input_array_f2.copy()
            modified_input[0, i] += 1  # その特徴量だけ +1
            modified_prediction = model_f2.predict(modified_input)[0]
            impact = abs(modified_prediction - prediction_f2)
            feature_impact_f2.append(impact)
        
        # 影響が最も大きい上位3つの質問を特定
        top_indices_f1 = np.argsort(feature_impact_f1)[-3:][::-1]
        top_impactful_questions_f1 = [i for i in top_indices_f1]
        top_impact_values_f1 = [feature_impact_f1[i] for i in top_indices_f1]
        
        top_indices_f2 = np.argsort(feature_impact_f2)[-3:][::-1]
        top_impactful_questions_f2 = [i+5 for i in top_indices_f2]
        top_impact_values_f2 = [feature_impact_f2[i] for i in top_indices_f2]
        
        # 結果をJSONで返す
        return jsonify({
            "prediction_f1": prediction_f1,
            "top_impactful_questions_f1": top_impactful_questions_f1,
            "top_impact_values_f1": top_impact_values_f1,
            "prediction_f2": prediction_f2,
            "top_impactful_questions_f2": top_impactful_questions_f2,
            "top_impact_values_f2": top_impact_values_f2
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)