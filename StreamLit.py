import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Успішність студентів", layout="wide")
st.title("🎓 Дашборд університету – успішність студентів")

# --- Автоматичне підвантаження CSV ---
csv_path = "students.csv"  # Файл повинен бути у тій же папці, що скрипт
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")

    # --- Фільтри ---
    col1, col2, col3 = st.columns(3)
    with col1:
        group_filter = st.selectbox("Група", ["Всі"] + df["Група"].unique().tolist())
    with col2:
        subject_filter = st.selectbox("Предмет", ["Всі"] + df["Предмет"].unique().tolist())
    with col3:
        semester_filter = st.selectbox("Семестр", ["Всі"] + df["Семестр"].astype(str).unique().tolist())

    filtered_df = df.copy()
    if group_filter != "Всі": filtered_df = filtered_df[filtered_df["Група"] == group_filter]
    if subject_filter != "Всі": filtered_df = filtered_df[filtered_df["Предмет"] == subject_filter]
    if semester_filter != "Всі": filtered_df = filtered_df[filtered_df["Семестр"].astype(str) == semester_filter]

    st.subheader("Відфільтровані дані")
    st.dataframe(filtered_df)

    # --- Діаграма середніх оцінок ---
    if not filtered_df.empty:
        avg = filtered_df.groupby("Предмет")["Оцінка"].mean().sort_values()
        fig, ax = plt.subplots(figsize=(8, max(3, 0.4 * len(avg))))
        sns.barplot(x=avg.values, y=avg.index, ax=ax, palette="viridis")
        ax.set_xlabel("Середня оцінка")
        ax.set_ylabel("Предмет")
        ax.set_title("Середні оцінки студентів")
        st.pyplot(fig)

        st.metric("📊 Середня оцінка вибірки", f"{filtered_df['Оцінка'].mean():.2f}")
    else:
        st.warning("Немає даних для графіка середніх оцінок.")

    pip install matplotlib seaborn pandas streamlit

