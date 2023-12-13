import streamlit as st
import pandas as pd
import plotly.express as px

# フィードバックを表示する関数
def display_feedback(feedback_data, factor):
    feedback_rows = feedback_data[factor].dropna()
    for row in feedback_rows:
        st.markdown(row)

# Excelファイルを読み込む関数
@st.cache  # Consider changing to st.cache_data or st.cache_resource based on your Streamlit version
def load_data(file_path):
    df_questions = pd.read_excel(file_path, sheet_name='質問項目')
    df_factors_avg = pd.read_excel(file_path, sheet_name='因子平均')
    feedback_above = pd.read_excel(file_path, sheet_name='フィードバック（基準以上）')
    feedback_below = pd.read_excel(file_path, sheet_name='フィードバック（基準未満）')
    return df_questions, df_factors_avg, feedback_above, feedback_below

file_path = 'questionnaire.xlsx'
df_questions, df_factors_avg, feedback_above, feedback_below = load_data(file_path)

# ラジオボタンのデフォルト選択肢
options1 = ["1 全くあてはまらない", "2 あまりあてはまらない", "3 少しあてはまる", "4 とてもあてはまる"]

# 設問を表示
st.title("ストレスチェックアプリ")
st.caption("Created by 72回生　理数科情報班")

# 各因子の平均点を計算
user_scores = {}
for factor, factor_data in df_questions.groupby("因子名"):
    st.subheader(f"＜{factor}＞")
    total_score = 0
    num_questions = 0
    for _, row in factor_data.iterrows():
        score = st.radio("回答", options1, key=row["設問名"])
        if not pd.isna(row["反転"]):
            score = 5 - int(score[0])
        else:
            score = int(score[0])
        total_score += score
        num_questions += 1
    avg_score = total_score / num_questions if num_questions > 0 else 0
    user_scores[factor] = avg_score

# レーダーチャートの描画
if user_scores:
    st.subheader("＜因子ごとの評価＞")
    fig = px.line_polar(
        r=list(user_scores.values()),
        theta=list(user_scores.keys()),
        line_close=True
    )
    fig.update_layout(font=dict(size=20))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, 4]  # 半径の範囲を指定
            )
        ),
        font=dict(size=20)
    )
    st.plotly_chart(fig)

# ユーザーのスコアを評価し、適切なフィードバックを表示
for factor in user_scores:
    avg_value = df_factors_avg[df_factors_avg["因子名"] == factor]["平均値"].iloc[0]
    st.subheader(f"＜{factor}＞")
    if user_scores[factor] >= avg_value:
        # ユーザーの因子得点を表示
        st.markdown(f"あなたの因子得点は「{user_scores[factor]:.2f}」です。")
        # 平均値以上の場合のフィードバック
        display_feedback(feedback_above, factor)
    else:
        # 平均値未満の場合のフィードバック
        display_feedback(feedback_below, factor)
