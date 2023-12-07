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
@@ -24,20 +21,15 @@ def calculate_avg_score(factor_data):
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
@@ -46,33 +38,22 @@ def calculate_avg_score(factor_data):
    factor_scores[factor] = avg_score
    st.write(f"{factor}の平均点: {avg_score:.2f}")



# 一般的な平均値
general_averages = {"F1": 1.94, "F2": 2.81, "F3": 2.83}


# 3つの因子F1～F3の平均値を変数に格納
avg_score_f1 = factor_scores.get("F1", 0)
avg_score_f2 = factor_scores.get("F2", 0)
avg_score_f3 = factor_scores.get("F3", 0)

# レーダーチャートを描画
if factor_scores:
    st.subheader("因子ごとの評価")
    fig = px.line_polar(
        r=list(factor_scores.values()),
        theta=list(factor_scores.keys()),
        line_close=True
    )
    fig.update_layout(font=dict(size=20))



    # ユーザーのスコアと一般平均のスコアをDataFrameにまとめる
    chart_data = pd.DataFrame({
        "Your Score": list(factor_scores.values()),
        "General Average": list(general_averages.values())
    }, index=list(factor_scores.keys()))



    # レーダーチャートを作成
    fig = px.line_polar(chart_data, line_close=True)



    # レーダーチャートの設定を更新
    # レーダーチャートの半径を固定
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
@@ -82,36 +63,31 @@ def calculate_avg_score(factor_data):
        font=dict(size=20)
    )



    # レーダーチャートを表示
    st.plotly_chart(fig)



# 各因子ごとの評価と提案メッセージ
st.subheader("＜F1　人間関係＞")
avg_score_f1 = factor_scores.get("F1", 0)
if avg_score_f1 < 1.94:
    st.write("aaa")
if avg_score_f1 < 1.94 :
    #平均値未満の時のメッセージ
    st.write("「人間関係因子」の得点は平均値(1.94)を下回っています。")
    st.write("aaa")
else:
    st.write("ddd")


    #平均値以上の時のメッセージ
    st.write("「人間関係因子」の得点は平均値(1.94)を上回っています。")

st.subheader("＜F2　心理的余裕＞")
avg_score_f2 = factor_scores.get("F2", 0)
if avg_score_f2 < 2.81:
    st.write("bbb")
if avg_score_f2 < 2.81 :
    #平均値未満の時のメッセージ
    st.write("「心理的余裕因子」の得点は平均値(2.81)を下回っています。")
else:
    st.write("eee")


    #平均値以上の時のメッセージ
    st.write("「心理的余裕因子」の得点は平均値(2.81)を上回っています。")

st.subheader("＜F3　食事・睡眠＞")
avg_score_f3 = factor_scores.get("F3", 0)
if avg_score_f3 < 2.83:
    st.write("CCC")
if avg_score_f3 < 2.83 :
    #平均値未満の時のメッセージ
    st.write(avg_score_f1)
    st.write("「食事・睡眠」の得点は平均値(2.83)を下回っています。")
else:
    st.write("fff")
    #平均値以上の時のメッセージ
    st.write("「食事・睡眠」の得点は平均値(2.83)を上回っています。")