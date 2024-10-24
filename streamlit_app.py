import streamlit as st
import pandas as pd
import numpy as np
import pickle

model = pickle.load(open('newmodel.pkl', 'rb'))

# Excelファイルを読み込む関数
@st.cache_resource
def load_data(file_path):
    df_questions = pd.read_excel(file_path, sheet_name='質問項目')
    df_factors_avg = pd.read_excel(file_path, sheet_name='因子平均')
    return df_questions, df_factors_avg

df_questions, df_factors_avg = load_data('f1.xlsx')
rows_as_list = [row.tolist() for index, row in df_questions.iterrows()]

# ラジオボタンのデフォルト選択肢
options1 = ["5 とてもあてはまる", "4 少しあてはまる", "3 どちらともいえない", "2 あまりあてはまらない", "1 全くあてはまらない"]

st.title("ストレスチェックアプリ")
st.caption("Created by 73回生　理数科情報班")

results = [0]*8

results[6] = int(st.radio('性別を教えて下さい', ["0 男性", "1 女性"])[0])
results[7] = abs(results[6] - 1)

for row in rows_as_list:
    results[int(row[0])] = int(st.radio(row[1], options1, key=int(row[0]))[0])

results

results_array = np.array(results).reshape(1, -1)

# Make prediction using the model
if st.button("結果を予測する"):
    prediction = model.predict(results_array)
    st.write("予測結果:", prediction[0])