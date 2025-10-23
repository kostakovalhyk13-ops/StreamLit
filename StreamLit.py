import pandas as pd

# --- 1. Завантаження CSV ---
file = input("Введіть шлях до CSV: ")
df = pd.read_csv(file)

# --- 2. Фільтри ---
groups = ["Всі"] + df["Група"].unique().tolist()
subjects = ["Всі"] + df["Предмет"].unique().tolist()
semesters = ["Всі"] + df["Семестр"].astype(str).unique().tolist()

g = input(f"Оберіть групу {groups}: ")
s = input(f"Оберіть предмет {subjects}: ")
sem = input(f"Оберіть семестр {semesters}: ")

filtered_df = df.copy()
if g != "Всі": filtered_df = filtered_df[filtered_df["Група"] == g]
if s != "Всі": filtered_df = filtered_df[filtered_df["Предмет"] == s]
if sem != "Всі": filtered_df = filtered_df[filtered_df["Семестр"].astype(str) == sem]

print("\nВідфільтровані дані:")
print(filtered_df)

# --- 3. Середні оцінки ---
avg = filtered_df.groupby("Предмет")["Оцінка"].mean()
print("\nСередні оцінки за предметами:")
print(avg)

# --- 4. Кореляція ---
pivot = filtered_df.pivot_table(index="ПІБ", columns="Предмет", values="Оцінка")
if pivot.shape[1] >= 2:
    corr = pivot.corr()
    print("\nКореляція між предметами:")
    print(corr)
else:
    print("\nНедостатньо предметів для кореляції.")



