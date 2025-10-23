import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Дашборд успішності студентів", layout="wide")
st.title("Дашборд успішності студентів")

# --- CSV дані прямо в коді ---
csv_data = """
Студент,Група,Предмет,Семестр,Оцінка
Іванов,101,Математика,1,85
Петренко,101,Математика,1,78
Сидоренко,102,Математика,1,92
Іванов,101,Фізика,1,90
Петренко,101,Фізика,1,85
Сидоренко,102,Фізика,1,88
Іванов,101,Хімія,1,75
Петренко,101,Хімія,1,80
Сидоренко,102,Хімія,1,82
"""

# --- Завантажуємо CSV дані у DataFrame ---
df = pd.read_csv(StringIO(csv_data))

st.subheader("Перегляд даних")
st.dataframe(df)

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
avg_scores = filtered_df.groupby('Предмет')['Оцінка'].mean()
st.bar_chart(avg_scores)

# --- Кореляція між предметами ---
st.subheader("Кореляція між предметами")
pivot_df = filtered_df.pivot_table(index='Студент', columns='Предмет', values='Оцінка')
if pivot_df.shape[1] > 1:
    corr = pivot_df.corr()
    st.dataframe(corr)
else:
    st.info("Для обчислення кореляції потрібно мінімум 2 предмети.")

   

