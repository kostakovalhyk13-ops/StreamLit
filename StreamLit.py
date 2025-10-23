import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Дашборд успішності студентів", layout="wide")
st.title("Дашборд успішності студентів")

# --- Автоматичне завантаження CSV ---
# Шукаємо перший CSV у поточній папці
csv_files = [f for f in os.listdir() if f.endswith(".csv")]

if not csv_files:
    st.error("Не знайдено жодного CSV файлу у папці з кодом!")
    st.stop()
else:
    csv_path = csv_files[0]
    st.success(f"Файл '{csv_path}' успішно завантажено!")
    df = pd.read_csv(csv_path)

st.subheader("Перегляд даних")
st.dataframe(df.head())

# --- Фільтри ---
group_filter = st.selectbox("Виберіть групу", options=["Всі"] + sorted(df['Група'].unique()))
subject_filter = st.selectbox("Виберіть предмет", options=["Всі"] + sorted(df['Предмет'].unique()))
semester_filter = st.selectbox("Виберіть семестр", options=["Всі"] + sorted(df['Семестр'].unique()))

filtered_df = df.copy()
if group_filter != "Всі":
    filtered_df = filtered_df[filtered_df['Група'] == group_filter]
if subject_filter != "Всі":
    filtered_df = filtered_df[filtered_df['Предмет'] == subject_filter]
if semester_filter != "Всі":
    filtered_df = filtered_df[filtered_df['Семестр'] == semester_filter]

st.subheader("Відфільтровані дані")
st.dataframe(filtered_df)

# --- Діаграми середніх оцінок ---
st.subheader("Середні оцінки за предметами")
if "Оцінка" in filtered_df.columns:
    avg_scores = filtered_df.groupby('Предмет')['Оцінка'].mean()
    st.bar_chart(avg_scores)
else:
    st.warning("У CSV має бути колонка 'Оцінка'.")

# --- Кореляція між предметами ---
st.subheader("Кореляція між предметами")
pivot_df = filtered_df.pivot_table(index='Студент', columns='Предмет', values='Оцінка')
if pivot_df.shape[1] > 1:
    corr = pivot_df.corr()
    st.dataframe(corr)
else:
    st.info("Для обчислення кореляції потрібно мінімум 2 предмети.")

   

