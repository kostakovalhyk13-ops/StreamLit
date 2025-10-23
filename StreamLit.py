import streamlit as st
import pandas as pd



st.set_page_config(page_title="Успішність студентів", layout="wide")
st.title("🎓 Дашборд університету – успішність студентів")

# --- Автоматичне підвантаження ---
csv_path = "students.csv"  # файл повинен бути у тій же папці
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")

    # --- Фільтри ---
    g = st.selectbox("Група", ["Всі"] + df["Група"].unique().tolist())
    s = st.selectbox("Предмет", ["Всі"] + df["Предмет"].unique().tolist())
    sem = st.selectbox("Семестр", ["Всі"] + df["Семестр"].astype(str).unique().tolist())

    filtered_df = df.copy()
    if g != "Всі": filtered_df = filtered_df[filtered_df["Група"] == g]
    if s != "Всі": filtered_df = filtered_df[filtered_df["Предмет"] == s]
    if sem != "Всі": filtered_df = filtered_df[filtered_df["Семестр"].astype(str) == sem]

    st.subheader("Відфільтровані дані")
    st.dataframe(filtered_df)

    # --- Діаграма середніх оцінок ---
    avg = filtered_df.groupby("Предмет")["Оцінка"].mean().sort_values()
    fig, ax = plt.subplots()
    sns.barplot(x=avg.values, y=avg.index, ax=ax)
    ax.set_xlabel("Середня оцінка")
    ax.set_ylabel("Предмет")
    st.pyplot(fig)

    # --- Кореляція ---
    pivot = filtered_df.pivot_table(index="ПІБ", columns="Предмет", values="Оцінка")
    if pivot.shape[1] >= 2:
        corr = pivot.corr()
        fig2, ax2 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax2)
        st.pyplot(fig2)
    else:
        st.warning("Недостатньо предметів для кореляції.")
else:
    st.error(f"Файл {csv_path} не знайдено. Помістіть CSV у ту ж папку, що і скрипт.")


