import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="🎓 Успішність студентів", layout="wide")
st.title("🎓 Дашборд університету – успішність студентів")

REQUIRED_COLS = {"ПІБ", "Група", "Предмет", "Семестр", "Оцінка"}

uploaded_file = st.file_uploader("📂 Завантажте CSV-файл з успішністю студентів", type=["csv"])

def normalize_columns(cols):
    # приводимо назви до стандартного вигляду (без пробілів, нижній регістр)
    return [c.strip() for c in cols]

if uploaded_file:
    try:
        # Спроба прочитати файл з різними кодуваннями
        try:
            df = pd.read_csv(uploaded_file)
        except Exception:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='utf-8', engine='python')

        # Нормалізація назв (якщо користувач має інші варіанти)
        original_cols = list(df.columns)
        cols_stripped = [c.strip() for c in original_cols]
        df.columns = cols_stripped

        st.subheader("📄 Попередній перегляд (перші 10 рядків)")
        st.dataframe(df.head(10))

        # Перевіримо наявність потрібних стовпців (робимо нечутливість до регістру)
        cols_lower_map = {c.lower(): c for c in df.columns}
        missing = []
        # спробуємо знайти кожен REQUIRED_COL у існуючих колонках нечутливо до регістру
        col_map = {}
        for rc in REQUIRED_COLS:
            key = rc.lower()
            if key in cols_lower_map:
                col_map[rc] = cols_lower_map[key]
            else:
                missing.append(rc)

        if missing:
            st.error(f"Немає очікуваних стовпців у CSV: {', '.join(missing)}. Перевірте назви колонок (ПІБ, Група, Предмет, Семестр, Оцінка).")
        else:
            # Перейменуємо колонки на очікувані українські назви
            df = df.rename(columns={col_map[k]: k for k in col_map})

            # Обробка оцінок: заміна ком у десяткових на точки, приведення до числа
            df["Оцінка"] = df["Оцінка"].astype(str).str.replace(",", ".")
            df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")
            before_drop = len(df)
            df = df.dropna(subset=["Оцінка"])
            dropped = before_drop - len(df)
            if dropped > 0:
                st.warning(f"Відкинуто {dropped} рядків через некоректні/порожні значення в 'Оцінка'.")

            # Переконаємось, що Семестр — строка (щоб selectbox працював стабільно)
            df["Семестр"] = df["Семестр"].astype(str)

            # Фільтри
            col1, col2, col3 = st.columns(3)
            with col1:
                group_filter = st.selectbox("🎯 Група", ["Всі"] + sorted(df["Група"].astype(str).unique().tolist()))
            with col2:
                subject_filter = st.selectbox("📘 Предмет", ["Всі"] + sorted(df["Предмет"].astype(str).unique().tolist()))
            with col3:
                semester_filter = st.selectbox("📅 Семестр", ["Всі"] + sorted(df["Семестр"].astype(str).unique().tolist()))

            filtered_df = df.copy()
            if group_filter != "Всі":
                filtered_df = filtered_df[filtered_df["Група"].astype(str) == group_filter]
            if subject_filter != "Всі":
                filtered_df = filtered_df[filtered_df["Предмет"].astype(str) == subject_filter]
            if semester_filter != "Всі":
                filtered_df = filtered_df[filtered_df["Семестр"].astype(str) == semester_filter]

            st.subheader("🔍 Відфільтровані дані (перші 20 рядків)")
            st.dataframe(filtered_df.head(20))

            if filtered_df.empty:
                st.warning("Після фільтрів немає рядків — спробуйте інші параметри або перевірте CSV.")
            else:
                # Вкладки для візуалізацій
                tab1, tab2 = st.tabs(["📈 Середні оцінки", "📊 Кореляційний аналіз"])

                with tab1:
                    st.subheader("📈 Середні оцінки за предметами")
                    avg_by_subject = filtered_df.groupby("Предмет")["Оцінка"].mean().sort_values(ascending=False)
                    if avg_by_subject.empty:
                        st.warning("Немає даних для побудови графіка середніх оцінок.")
                    else:
                        fig, ax = plt.subplots(figsize=(8, max(3, 0.4 * len(avg_by_subject))))
                        sns.barplot(x=avg_by_subject.values, y=avg_by_subject.index, ax=ax)
                        ax.set_xlabel("Середня оцінка")
                        ax.set_ylabel("Предмет")
                        ax.set_title("Середні оцінки студентів")
                        st.pyplot(fig)
                        st.metric("📊 Середня оцінка (вибірка)", f"{filtered_df['Оцінка'].mean():.2f}")

                with tab2:
                    st.subheader("📊 Кореляція між предметами")

                    pivot = filtered_df.pivot_table(index="ПІБ", columns="Предмет", values="Оцінка", aggfunc="mean")
                    if pivot.shape[1] < 2:
                        st.warning("Потрібно щонайменше 2 предмети для обчислення кореляції.")
                    else:
                        corr = pivot.corr()
                        fig2, ax2 = plt.subplots(figsize=(7, 0.6 * corr.shape[0] + 3))
                        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax2, vmin=-1, vmax=1)
                        ax2.set_title("Кореляційна матриця предметів")
                        st.pyplot(fig2)

                # Завантаження
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button("💾 Завантажити відфільтровані дані", csv, "filtered_results.csv", "text/csv")

    except Exception as e:
        st.error("Сталася помилка при обробці файлу.")
        st.exception(e)
else:
    st.info("⬆️ Завантажте CSV-файл, щоб переглянути дашборд.")

