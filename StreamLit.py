import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Успішність студентів", layout="wide")

st.title("🎓 Дашборд університету – успішність студентів")

# --- 1. Завантаження CSV ---
uploaded_file = st.file_uploader("📂 Завантажте CSV-файл з успішністю", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Попередній перегляд даних")
    st.dataframe(df.head())

    # --- Очікувана структура ---
    # Стовпці: ['ПІБ', 'Група', 'Предмет', 'Семестр', 'Оцінка']

    # --- 2. Фільтри ---
    col1, col2, col3 = st.columns(3)

    with col1:
        group_filter = st.selectbox("🎯 Оберіть групу", ["Всі"] + sorted(df["Група"].unique().tolist()))
    with col2:
        subject_filter = st.selectbox("📘 Оберіть предмет", ["Всі"] + sorted(df["Предмет"].unique().tolist()))
    with col3:
        semester_filter = st.selectbox("📅 Оберіть семестр", ["Всі"] + sorted(df["Семестр"].unique().tolist()))

    filtered_df = df.copy()
    if group_filter != "Всі":
        filtered_df = filtered_df[filtered_df["Група"] == group_filter]
    if subject_filter != "Всі":
        filtered_df = filtered_df[filtered_df["Предмет"] == subject_filter]
    if semester_filter != "Всі":
        filtered_df = filtered_df[filtered_df["Семестр"] == semester_filter]

    st.subheader("🔍 Відфільтровані дані")
    st.dataframe(filtered_df)

    # --- 3. Діаграми середніх оцінок ---
    st.subheader("📈 Середні оцінки")

    avg_by_subject = filtered_df.groupby("Предмет")["Оцінка"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=avg_by_subject.values, y=avg_by_subject.index, ax=ax)
    ax.set_xlabel("Середня оцінка")
    ax.set_ylabel("Предмет")
    ax.set_title("Середні оцінки за предметами")
    st.pyplot(fig)

    # --- 4. Кореляційний аналіз між предметами ---
    st.subheader("📊 Кореляція між предметами")

    # Створюємо таблицю студент × предмет
    pivot = df.pivot_table(index="ПІБ", columns="Предмет", values="Оцінка", aggfunc="mean")

    corr = pivot.corr()

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax2)
    ax2.set_title("Кореляційна матриця предметів")
    st.pyplot(fig2)

    st.info("Кореляція показує, які предмети мають схожу тенденцію в оцінках студентів.")
else:
    st.warning("⬆️ Завантажте CSV-файл, щоб переглянути дашборд.")

