import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Успішність студентів", layout="wide")
st.title("🎓 Дашборд університету – успішність студентів")

file = st.file_uploader("📂 Завантажте CSV", type="csv")

if file:
    df = pd.read_csv(file)
    df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")

    col1, col2, col3 = st.columns(3)
    g = col1.selectbox("Група", ["Всі"] + df["Група"].unique().tolist())
    s = col2.selectbox("Предмет", ["Всі"] + df["Предмет"].unique().tolist())
    sem = col3.selectbox("Семестр", ["Всі"] + df["Семестр"].unique().astype(str).tolist())

    if g != "Всі": df = df[df["Група"] == g]
    if s != "Всі": df = df[df["Предмет"] == s]
    if sem != "Всі": df = df[df["Семестр"].astype(str) == sem]

    st.dataframe(df)

    avg = df.groupby("Предмет")["Оцінка"].mean().sort_values()
    fig, ax = plt.subplots()
    sns.barplot(x=avg.values, y=avg.index, ax=ax)
    st.pyplot(fig)

    pivot = df.pivot_table(index="ПІБ", columns="Предмет", values="Оцінка")
    if pivot.shape[1] >= 2:
        corr = pivot.corr()
        fig2, ax2 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax2)
        st.pyplot(fig2)
else:
    st.warning("⬆️ Завантажте CSV-файл.")

