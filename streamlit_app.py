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

    # レーダーチャートの半径を固定
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, 4]  # 半径の範囲を指定
            )
        ),
        font=dict(size=20)
    )

    st.plotly_chart(fig)


st.subheader("＜F1　人間関係＞")
if avg_score_f1 < 1.94 :
    #平均値未満の時のメッセージ
    st.write("「人間関係因子」の得点は平均値(1.94)を下回っています。")
    st.write("以下のコーピング法を提案します。\
    ①有酸素運動(ジョギングやランニング)  \
    全身を動かすことで大きなエネルギーを使うため、カロリー消費や心肺機能の向上に効果的です。\
    ②レジスタンストレーニング(スクワットやフィットネス機器等を使用したトレーニング)\
    習慣的にレジスタンストレーニングを行うと睡眠の質の向上につながります。\
    ③規則的な寝起き\
    毎日同じ時間に寝床に入り、同じ時間に起きることで、体内時計を整えることで、質の高い睡眠を促進することができます​。\
    ④リラックスの習慣\
    寝る前にリラックスする習慣を持ちましょう。深呼吸、瞑想、温かい入浴、リラックス音楽、アロマ等の匂いなどが役立ちます。\
    ⑤寝室環境の最適化\
    快適な寝室環境を整え、暗い部屋、快適な温度(13℃～29℃)や湿度(40%～60%)、静かな環境を確保しましょう。​​")
else:
    #平均値以上の時のメッセージ
    st.write("「人間関係因子」の得点は平均値(1.94)を上回っています。")

st.subheader("＜F2　心理的余裕＞")
if avg_score_f2 < 2.81 :
    #平均値未満の時のメッセージ
    st.write("「心理的余裕因子」の得点は平均値(2.81)を下回っています。")
    st.write("以下のコーピング法を提案します。\
    ①運動時間の確保\
    ヨガやウォーキングがジョギングなどがおすすめです。\
    ②規則的な寝起き\
    毎日同じ時間に寝床に入り、同じ時間に起きることで、体内時計を整えることで、質の高い睡眠を促進することができます​。\
    ③リラックスの習慣\
    寝る前にリラックスする習慣を持ちましょう。深呼吸、瞑想、温かい入浴、リラックス音楽、アロマ等の匂いなどが役立ちます。\
    ④寝室環境の最適化\
    快適な寝室環境を整え、暗い部屋、快適な温度(13℃～29℃)や湿度(40%～60%)、静かな環境を確保しましょう。​")
else:
    #平均値以上の時のメッセージ
    st.write("「心理的余裕因子」の得点は平均値(2.81)を上回っています。")

st.subheader("＜F3　食事・睡眠＞")
if avg_score_f3 < 2.83 :
    #平均値未満の時のメッセージ
    st.write("")
    st.write("「食事・睡眠」の得点は平均値(2.83)を下回っています。")
    st.write("以下のコーピング法を提案します。\
    ①規則的な寝起き\
    毎日同じ時間に寝床に入り、同じ時間に起きることで、体内時計を整えることで、質の高い睡眠を促進することができます​。\
    ②リラックスの習慣\
    寝る前にリラックスする習慣を持ちましょう。深呼吸、瞑想、温かい入浴、リラックス音楽、アロマ等の匂いなどが役立ちます。\
    ③寝室環境の最適化\
    快適な寝室環境を整え、暗い部屋、快適な温度(13℃～29℃)や湿度(40%～60%)、静かな環境を確保しましょう。\
    ④バランスのとれた​食事\
    バランスの取れた食事で必要な栄養素を摂り、高脂肪や高塩分、高糖分の食事、間食を避けることが心拍数の安定に寄与します。\
    適切な水分摂取\
    適切な水分摂取は循環を助け、心臓が効果的に働くのに役立ちます。​")
else:
    #平均値以上の時のメッセージ
    st.write("「食事・睡眠」の得点は平均値(2.83)を上回っています。")