# Streamlitライブラリをインポート
import streamlit as st

import streamlit as st
import pandas as pd

# CSVファイルから質問と選択肢を読み込む
@st.cache
def load_data(filename):
    data = pd.read_csv(filename)
    return data

filename = 'questions.csv'
data = load_data(filename)

# Streamlitアプリの設定
st.title("アンケートアプリ")
st.write("以下のアンケートにお答えいただき、ポイントを計算します。")

# ユーザーからのアンケート回答を収集
user_points = {}
for _, row in data.iterrows():
    question = row['question']
    choices = [row['choice1'], row['choice2'], row['choice3'], row['choice4']]
    answer = st.radio(question, choices)
    user_points[question] = answer

# ポイントを計算
points_per_question = {
    "質問1: あなたの年齢は？": {
        "18歳未満": 0,
        "18歳から30歳まで": 2,
        "31歳から50歳まで": 5,
        "51歳以上": 10,
    },
    "質問2: 好きな色は何ですか？": {
        "青": 3,
        "赤": 2,
        "緑": 1,
        "その他": 0,
    },
    "質問3: どのプログラミング言語を使用しますか？": {
        "Python": 5,
        "JavaScript": 3,
        "Java": 2,
        "その他": 1,
    },
}
total_points = sum(points_per_question[question][user_points[question]] for question in data['question'])

# 結果を表示
st.write(f"獲得したポイント: {total_points} ポイント")

# ポイントに応じた可視化（例：棒グラフ）
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=list(user_points.keys()), y=[points_per_question[question][user_points[question]] for question in data['question']])
plt.xticks(rotation=45)
plt.xlabel("質問")
plt.ylabel("ポイント")
plt.title("質問ごとのポイント")
st.pyplot(plt)


