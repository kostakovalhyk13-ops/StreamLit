import streamlit as st
import pandas as pd
# Налаштування сторінки
st.set_page_config(page_title="Успішність студентів", layout="wide")
st.title("🎓 Дашборд університету – успішність студентів")

# Шлях до CSV (автопідвантаження)
csv_path = "students.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")

    # Фільтри
    col1, col2, col3 = st.columns(3)
    with col1:
        group_filter = st.selectbox("Група", ["Всі"] + df["Група"].unique().tolist())
    with col2:
        subject_filter = st.selectbox("Предмет", ["Всі"] + df["Предмет"].unique().tolist())
    with col3:
        semester_filter = st.selectbox("Семестр", ["Всі"] + df["Семестр"].astype(str).unique().tolist())

    # Фільтрація даних
    filtered_df = df.copy()
    if group_filter != "Всі":
        filtered_df = filtered_df[filtered_df["Група"] == group_filter]
    if subject_filter != "Всі":
        filtered_df = filtered_df[filtered_df["Предмет"] == subject_filter]
    if semester_filter != "Всі":
        filtered_df = filtered_df[filtered_df["Семестр"].astype(str) == semester_filter]

    st.subheader("Відфільтровані дані")
    st.dataframe(filtered_df)

    # Діаграма середніх оцінок
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

    # Кореляційний аналіз
    pivot = filtered_df.pivot_table(index="ПІБ", columns="Предмет", values="Оцінка")
    if pivot.shape[1] >= 2:
        corr = pivot.corr()
        fig2, ax2 = plt.subplots(figsize=(7, max(4, 0.5 * len(corr))))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax2, vmin=-1, vmax=1)
        ax2.set_title("Кореляційна матриця предметів")
        st.pyplot(fig2)
        st.info("Кореляція показує, які предмети мають схожі тенденції в оцінках студентів.")
    else:
        st.warning("Недостатньо предметів для розрахунку кореляції.")
else:
    st.error(f"Файл {csv_path} не знайдено. Помістіть CSV у ту ж папку, що і скрипт.")

   

