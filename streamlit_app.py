import streamlit as st
import pandas as pd
import plotly.express as px

# フィードバックを表示する関数
def display_feedback(feedback_data, factor):
    feedback_rows = feedback_data[factor].dropna()
    markup_rows = feedback_data['マークダウン'].dropna()
    for markup, row in zip(markup_rows, feedback_rows):
        # マークダウン列に何かが入力されている場合は、その記号を使う
        if pd.notna(markup):
            st.markdown(f"{markup} {row} ")
        else:
            st.markdown(row)

# Excelファイルを読み込む関数
@st.cache_resource
def load_data(file_path):
    df_questions = pd.read_excel(file_path, sheet_name='質問項目')
    df_factors_avg = pd.read_excel(file_path, sheet_name='因子平均')
    feedback_above = pd.read_excel(file_path, sheet_name='フィードバック（基準以上）')
    feedback_below = pd.read_excel(file_path, sheet_name='フィードバック（基準未満）')
    return df_questions, df_factors_avg, feedback_above, feedback_below

file_path = 'questionnaire.xlsx'
df_questions, df_factors_avg, feedback_above, feedback_below = load_data(file_path)

# ラジオボタンのデフォルト選択肢
options1 = ["4 とてもあてはまる", "3 少しあてはまる", "2 あまりあてはまらない", "1 全くあてはまらない"]

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
        st.markdown(f"**{row['設問名']}**")
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


    # レーダーチャート用のデータの準備
    user_scores_list = list(user_scores.values())
    avg_scores_list = [df_factors_avg[df_factors_avg["因子名"] == factor]["平均値"].iloc[0] for factor in user_scores]

    # プロット用のDataFrameを作成
    radar_data = pd.DataFrame({
        '因子': list(user_scores.keys()),
        'ユーザースコア': user_scores_list,
        '全体平均': avg_scores_list
    })

    # レーダーチャートのプロット
    fig = px.line_polar(radar_data, r='ユーザースコア', theta='因子', line_close=True, title='ユーザースコアと全体平均の比較')
    fig.add_trace(px.line_polar(radar_data, r='全体平均', theta='因子', line_close=True).data[0])

    # ユーザースコアの線の色を青に設定
    fig.data[0].line.color = 'blue'

    # 全体平均の線の色を赤に設定
    fig.data[1].line.color = 'red'

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, 4]  # 必要に応じて範囲を調整
            )
        ),
        font=dict(size=20),
        showlegend=True  # 凡例を表示する
    )
    st.plotly_chart(fig)

# ユーザーのスコアを評価し、適切なフィードバックを表示
for factor in user_scores:
    avg_value = df_factors_avg[df_factors_avg["因子名"] == factor]["平均値"].iloc[0]
    st.subheader(f"＜{factor}＞")
    if user_scores[factor] >= avg_value:
        # ユーザーの因子得点を表示
        st.markdown(f"###### あなたの因子得点は「{user_scores[factor]:.2f}」です。")
        st.markdown(f"###### （ 全体平均は「{avg_value:.2f}」 ）")
        # 平均値以上の場合のフィードバック
        display_feedback(feedback_above, factor)
    else:
        # ユーザーの因子得点を表示
        st.markdown(f"###### あなたの因子得点は「{user_scores[factor]:.2f}」です。")
        st.markdown(f"###### （ 全体平均は「{avg_value:.2f}」 ）")
        # 平均値未満の場合のフィードバック
        display_feedback(feedback_below, factor)