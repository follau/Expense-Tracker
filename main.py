import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

FILE_NAME = "expenses.json"


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")

        self.expenses = []

        tk.Label(root, text="Сумма").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Категория").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(root, text="Добавить расход", command=self.add_expense).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        tk.Label(root, text="Фильтр по категории").grid(row=4, column=0, padx=5, pady=5)
        self.filter_category = tk.Entry(root)
        self.filter_category.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата с").grid(row=5, column=0, padx=5, pady=5)
        self.date_from = tk.Entry(root)
        self.date_from.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата по").grid(row=6, column=0, padx=5, pady=5)
        self.date_to = tk.Entry(root)
        self.date_to.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(root, text="Фильтровать", command=self.filter_expenses).grid(row=7, column=0, pady=10)
        tk.Button(root, text="Подсчитать сумму", command=self.calculate_total).grid(row=7, column=1, pady=10)
        tk.Button(root, text="Показать все", command=self.show_all).grid(row=8, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(root, columns=("Amount", "Category", "Date"), show="headings", height=10)
        self.tree.heading("Amount", text="Сумма")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("Date", text="Дата")
        self.tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.load_data()

    def validate_input(self, amount, date):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return False

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD")
            return False

        return True

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not category.strip():
            messagebox.showerror("Ошибка", "Введите категорию")
            return

        if not self.validate_input(amount, date):
            return

        expense = {"amount": float(amount), "category": category, "date": date}
        self.expenses.append(expense)
        self.tree.insert("", tk.END, values=(amount, category, date))
        self.save_data()

        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def get_filtered_expenses(self):
        category = self.filter_category.get().lower().strip()
        date_from = self.date_from.get().strip()
        date_to = self.date_to.get().strip()

        filtered = self.expenses

        if category:
            filtered = [exp for exp in filtered if exp["category"].lower() == category]
        if date_from:
            filtered = [exp for exp in filtered if exp["date"] >= date_from]
        if date_to:
            filtered = [exp for exp in filtered if exp["date"] <= date_to]

        return filtered

    def filter_expenses(self):
        self.update_table(self.get_filtered_expenses())

    def calculate_total(self):
        total = sum(exp["amount"] for exp in self.get_filtered_expenses())
        messagebox.showinfo("Итог", f"Общая сумма: {total}")

    def update_table(self, expenses):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for exp in expenses:
            self.tree.insert("", tk.END, values=(exp["amount"], exp["category"], exp["date"]))

    def show_all(self):
        self.update_table(self.expenses)

    def save_data(self):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(self.expenses, file, indent=4, ensure_ascii=False)

    def load_data(self):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                self.expenses = json.load(file)
                self.update_table(self.expenses)
        except (FileNotFoundError, json.JSONDecodeError):
            self.expenses = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
