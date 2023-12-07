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
        # ユーザーからの回答を取得
        score = st.radio("回答", options1, key=f"{row['設問名']}_{idx}")
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
    fig = px.line_polar(chart_data, line_close=True, 
                        color_discrete_sequence=px.colors.sequential.Plasma_r)

 

    # ユーザーのスコアを追加
    fig.add_trace(px.line_polar(chart_data, r='Your Score', theta=chart_data.index, 
                                line_close=True, 
                                color_discrete_sequence=['blue']).data[0])

 

    # 一般平均のスコアを追加
    fig.add_trace(px.line_polar(chart_data, r='General Average', theta=chart_data.index, 
                                line_close=True, 
                                color_discrete_sequence=['red']).data[0])

 

    # レーダーチャートの設定を更新
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, 4]  # 半径の範囲を指定
            )
        ),
        showlegend=True,
        font=dict(size=20)
    )

 

    # レーダーチャートを表示
    st.plotly_chart(fig)

 

# 各因子ごとの評価と提案メッセージ
st.subheader("＜F1　人間関係＞")
avg_score_f1 = factor_scores.get("F1", 0)
st.write(f"あなたの[ F1 人間関係 ]のスコアは {avg_score_f1} です。")
if avg_score_f1 < 1.94:
    st.write("aaa")
    st.write("aaa")
else:
    st.write("ddd")

 

st.subheader("＜F2　心理的余裕＞")
avg_score_f2 = factor_scores.get("F2", 0)
st.write(f"あなたの[ F2　心理的余裕 ]のスコアは {avg_score_f2}です。")
if avg_score_f2 < 2.81:
    st.write("bbb")
else:
    st.write("eee")

 

st.subheader("＜F3　食事・睡眠＞")
avg_score_f3 = factor_scores.get("F3", 0)
st.write(f"あなたの[ F2　心理的余裕 ]のスコアは {avg_score_f3 }です。")
if avg_score_f3 < 2.83:
    st.write("CCC")
else:
    st.write("fff")