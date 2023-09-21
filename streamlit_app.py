import streamlit as st
import pandas as pd
import plotly.express as px

st.title("あああああ")

# Excelファイルを読み込む
@st.cache
def load_data():
    # Excelファイルのパスを指定します
    path = "questionnaire.xlsx"
    data = pd.read_excel(path)
    return data

data = load_data()

# アンケートの回答を収集
responses = {}
for index, row in data.iterrows():
    question_number = row["設問番号"]
    question_name = row["設問名"]
    answer = st.radio(
        f"{question_number}. {question_name}",
        ["4　とてもあてはまる","3　少しあてはまる","2　あまりあてはまらない","1　全くあてはまらない"]
    )
    responses[question_number] = {"answer": int(answer[0]), "factor": row["因子名"]}

# 平均点の計算
factors = data["因子名"].unique()
avg_scores = {}
for factor in factors:
    total = sum([resp["answer"] for q_num, resp in responses.items() if resp["factor"] == factor])
    count = sum([1 for q_num, resp in responses.items() if resp["factor"] == factor])
    avg_scores[factor] = total / count

# レーダーチャートの表示
df_avg_scores = pd.DataFrame([avg_scores])
fig = px.line_polar(df_avg_scores, r=df_avg_scores.columns, theta=df_avg_scores.columns, line_close=True)
st.plotly_chart(fig)
