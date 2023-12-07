import streamlit as st
import pandas as pd
import plotly.express as px

 

# Excelファイルを読み込む
@st.cache
def load_data():
    df = pd.read_excel("questionnaire.xlsx")
    return df

 

def calculate_avg_score(factor_data):
    total_score = 0
    for idx, row in factor_data.iterrows():
        st.markdown(f"**{row['設問名']}**")
        score = st.radio("回答", options1, key=row["設問名"])
        if not pd.isna(row["反転"]):
            score = 5 - int(score[0])
        else:
            score = int(score[0])
        total_score += score
    return total_score / len(factor_data)

 

df = load_data()
# 設問を表示
st.title("ストレスチェックアプリ")
st.caption("Created by 72回生　理数科情報班")

 

# ラジオボタンのデフォルト選択肢
options1 = ["1 全くあてはまらない", "2 あまりあてはまらない", "3 少しあてはまる", "4 とてもあてはまる"]

 

# ラジオボタンで回答を収集し、因子ごとの平均点を計算
factor_scores = {}
for factor, factor_data in df.groupby("因子名"):
    st.subheader(factor)
    avg_score = calculate_avg_score(factor_data)
    factor_scores[factor] = avg_score
    st.write(f"{factor}の平均点: {avg_score:.2f}")

 

# 一般的な平均値
general_averages = {"F1": 1.94, "F2": 2.81, "F3": 2.83}

 

# レーダーチャートを描画
if factor_scores:
    st.subheader("因子ごとの評価")

 

    # ユーザーのスコアと一般平均のスコアをDataFrameにまとめる
    chart_data = pd.DataFrame({
        "Your Score": list(factor_scores.values()),
        "General Average": list(general_averages.values())
    }, index=list(factor_scores.keys()))

 

    # レーダーチャートを作成
    fig = px.line_polar(chart_data, line_close=True)

 

    # レーダーチャートの設定を更新
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, 4]  # 半径の範囲を指定
            )
        ),
        font=dict(size=20)
    )

 

    # レーダーチャートを表示
    st.plotly_chart(fig)

 

# 各因子ごとの評価と提案メッセージ
st.subheader("＜F1　人間関係＞")
avg_score_f1 = factor_scores.get("F1", 0)
if avg_score_f1 < 1.94:
    st.write("aaa")
    st.write("aaa")
else:
    st.write("ddd")

 

st.subheader("＜F2　心理的余裕＞")
avg_score_f2 = factor_scores.get("F2", 0)
if avg_score_f2 < 2.81:
    st.write("bbb")
else:
    st.write("eee")

 

st.subheader("＜F3　食事・睡眠＞")
avg_score_f3 = factor_scores.get("F3", 0)
if avg_score_f3 < 2.83:
    st.write("CCC")
else:
    st.write("fff")