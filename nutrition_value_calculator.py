import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv('API_ID')
API_KEY = os.getenv('API_KEY')
API_URL = 'https://api.edamam.com/api/nutrition-data'


class NutritionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nutrition Calculator")
        self.set_dark_theme()

        self.recipe_mode = False
        self.current_recipe = {}
        self.ingredients = []

        self.create_main_frame()

    def set_dark_theme(self):
        self.root.configure(bg='#2e2e2e')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2e2e2e')
        style.configure('TLabel', background='#2e2e2e', foreground='white')
        style.configure('TButton', background='#3e3e3e', foreground='white')
        style.configure('TRadiobutton', background='#2e2e2e', foreground='white')
        style.map('TButton', background=[('active', '#4e4e4e')])
        style.configure('TEntry', fieldbackground='#3e3e3e', foreground='white')

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack()

        self.mode_var = tk.StringVar(value='separate')

        ttk.Label(self.main_frame, text="Select Mode:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Radiobutton(self.main_frame, text="Separate Products", variable=self.mode_var,
                        value='separate', command=self.set_mode).grid(row=1, column=0, sticky='w')
        ttk.Radiobutton(self.main_frame, text="Whole Recipe", variable=self.mode_var,
                        value='recipe', command=self.set_mode).grid(row=2, column=0, sticky='w')

    def set_mode(self):
        self.recipe_mode = self.mode_var.get() == 'recipe'
        self.main_frame.destroy()

        if self.recipe_mode:
            self.create_recipe_name_window()
        else:
            self.create_separate_products_window()

    def create_recipe_name_window(self):
        self.recipe_window = tk.Toplevel(self.root)
        self.recipe_window.title("Recipe Details")
        self.recipe_window.configure(bg='#2e2e2e')

        ttk.Label(self.recipe_window, text="Dish Name:").grid(row=0, column=0, padx=10, pady=10)
        self.dish_entry = ttk.Entry(self.recipe_window)
        self.dish_entry.grid(row=0, column=1, padx=10, pady=10)

        btn_frame = ttk.Frame(self.recipe_window)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Continue",
                   command=self.create_recipe_ingredients).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Return to Main Menu",
                   command=self.return_to_main).grid(row=0, column=1, padx=5)

    def create_recipe_ingredients(self):
        self.current_recipe['name'] = self.dish_entry.get()
        self.recipe_window.destroy()

        self.ingredient_frame = ttk.Frame(self.root, padding=20)
        self.ingredient_frame.pack()

        ttk.Label(self.ingredient_frame, text="Ingredient Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.ingredient_frame, text="Quantity (g):").grid(row=0, column=1, padx=5, pady=5)

        self.ingredient_entry = ttk.Entry(self.ingredient_frame)
        self.quantity_entry = ttk.Entry(self.ingredient_frame)
        self.ingredient_entry.grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add and Delete buttons in a frame
        button_frame = ttk.Frame(self.ingredient_frame)
        button_frame.grid(row=1, column=2, padx=5)

        self.submit_btn = ttk.Button(button_frame, text="Add", command=self.add_ingredient)
        self.submit_btn.pack(side='left', padx=2)

        self.delete_btn = ttk.Button(button_frame, text="Delete",
                                     command=self.delete_selected_ingredient)
        self.delete_btn.pack(side='left', padx=2)

        self.ingredient_entry.bind('<Return>', lambda event: self.add_ingredient())
        self.quantity_entry.bind('<Return>', lambda event: self.add_ingredient())

        self.ingredient_list = tk.Listbox(self.ingredient_frame, width=50,
                                          bg='#3e3e3e', fg='white', selectmode=tk.SINGLE)
        self.ingredient_list.grid(row=2, column=0, columnspan=3, pady=10)

        btn_frame = ttk.Frame(self.ingredient_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)

        self.end_input_btn = ttk.Button(btn_frame, text="End Input",
                                        command=self.show_recipe_results, state=tk.DISABLED)
        self.end_input_btn.grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Return to Main Menu",
                   command=self.return_to_main).grid(row=0, column=1, padx=5)

    def delete_selected_ingredient(self):
        selected = self.ingredient_list.curselection()
        if selected:
            index = selected[0]
            self.ingredient_list.delete(index)
            del self.ingredients[index]
            # Disable End Input button if no ingredients left
            if not self.ingredients:
                self.end_input_btn.config(state=tk.DISABLED)

    def add_ingredient(self):
        food = self.ingredient_entry.get()
        quantity = self.quantity_entry.get()

        if food and quantity:
            try:
                quantity = float(quantity)
                nutrition = self.get_nutrition_data(food, quantity)
                if nutrition:
                    self.ingredients.append(nutrition)
                    self.ingredient_list.insert(tk.END, f"{food} - {quantity}g")
                    self.ingredient_entry.delete(0, tk.END)
                    self.quantity_entry.delete(0, tk.END)
                    self.end_input_btn.config(state=tk.NORMAL)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantity")

    def create_separate_products_window(self):
        self.separate_frame = ttk.Frame(self.root, padding=20)
        self.separate_frame.pack()

        ttk.Label(self.separate_frame, text="Food Item:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.separate_frame, text="Quantity (g):").grid(row=0, column=1, padx=5, pady=5)

        self.food_entry = ttk.Entry(self.separate_frame)
        self.sep_quantity_entry = ttk.Entry(self.separate_frame)
        self.food_entry.grid(row=1, column=0, padx=5, pady=5)
        self.sep_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        self.submit_sep_btn = ttk.Button(self.separate_frame, text="Get Nutrition",
                                         command=self.show_separate_nutrition)
        self.submit_sep_btn.grid(row=1, column=2, padx=5, pady=5)
        self.food_entry.bind('<Return>', lambda event: self.show_separate_nutrition())
        self.sep_quantity_entry.bind('<Return>', lambda event: self.show_separate_nutrition())

        self.results_text = tk.Text(self.separate_frame, height=15, width=50, bg='#3e3e3e', fg='white')
        self.results_text.grid(row=2, column=0, columnspan=3, pady=10)

        ttk.Button(self.separate_frame, text="Return to Main Menu",
                   command=self.return_to_main).grid(row=3, column=0, columnspan=3, pady=10)

    def show_separate_nutrition(self):
        food = self.food_entry.get()
        quantity = self.sep_quantity_entry.get()

        if food and quantity:
            try:
                quantity = float(quantity)
                nutrition = self.get_nutrition_data(food, quantity)
                if nutrition:
                    result = (
                        f"{food.capitalize()} Nutrition for {quantity}g:\n"
                        f"Calories: {nutrition['Calories']} kcal\n"
                        f"Protein: {nutrition['Protein']}g\n"
                        f"Fat: {nutrition['Fat']}g\n"
                        f"Carbs: {nutrition['Carbs']}g\n{'=' * 30}\n"
                    )
                    self.results_text.insert(tk.END, result)
                    self.food_entry.delete(0, tk.END)
                    self.sep_quantity_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantity")

    def show_recipe_results(self):
        total_calories = sum(item['Calories'] for item in self.ingredients)
        total_protein = sum(item['Protein'] for item in self.ingredients)
        total_fat = sum(item['Fat'] for item in self.ingredients)
        total_carbs = sum(item['Carbs'] for item in self.ingredients)
        total_weight = sum(item['Quantity'] for item in self.ingredients)

        per_100g_cal = (total_calories / total_weight) * 100 if total_weight > 0 else 0
        per_100g_protein = (total_protein / total_weight) * 100 if total_weight > 0 else 0
        per_100g_fat = (total_fat / total_weight) * 100 if total_weight > 0 else 0
        per_100g_carbs = (total_carbs / total_weight) * 100 if total_weight > 0 else 0

        self.results_frame = ttk.Frame(self.root, padding=20)
        self.results_frame.pack()

        title = ttk.Label(self.results_frame,
                          text=f"Nutrition for {self.current_recipe['name']}",
                          font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Total Nutrition
        ttk.Label(self.results_frame, text="Total Nutrition:",
                  font=('Arial', 10, 'bold')).grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(self.results_frame, text="Calories:", font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{total_calories:.2f} kcal").grid(row=2, column=1, sticky='w')

        ttk.Label(self.results_frame, text="Protein:", font=('Arial', 9, 'bold')).grid(row=3, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{total_protein:.2f} g").grid(row=3, column=1, sticky='w')

        ttk.Label(self.results_frame, text="Fat:", font=('Arial', 9, 'bold')).grid(row=4, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{total_fat:.2f} g").grid(row=4, column=1, sticky='w')

        ttk.Label(self.results_frame, text="Carbs:", font=('Arial', 9, 'bold')).grid(row=5, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{total_carbs:.2f} g").grid(row=5, column=1, sticky='w')

        # Per 100g Nutrition
        ttk.Label(self.results_frame, text="Per 100g:",
                  font=('Arial', 10, 'bold')).grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Label(self.results_frame, text="Calories:", font=('Arial', 9, 'bold')).grid(row=7, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{per_100g_cal:.2f} kcal").grid(row=7, column=1, sticky='w')

        ttk.Label(self.results_frame, text="Protein:", font=('Arial', 9, 'bold')).grid(row=8, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{per_100g_protein:.2f} g").grid(row=8, column=1, sticky='w')

        ttk.Label(self.results_frame, text="Fat:", font=('Arial', 9, 'bold')).grid(row=9, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{per_100g_fat:.2f} g").grid(row=9, column=1, sticky='w')

        ttk.Label(self.results_frame, text="Carbs:", font=('Arial', 9, 'bold')).grid(row=10, column=0, sticky='e')
        ttk.Label(self.results_frame, text=f"{per_100g_carbs:.2f} g").grid(row=10, column=1, sticky='w')

        # Buttons
        btn_frame = ttk.Frame(self.results_frame)
        btn_frame.grid(row=11, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Save Recipe", command=self.save_recipe).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Return to Main Menu", command=self.return_to_main).grid(row=0, column=1, padx=5)

    def get_nutrition_data(self, food_name, quantity):
        params = {
            'app_id': API_ID,
            'app_key': API_KEY,
            'ingr': f"{quantity}g {food_name}"
        }
        try:
            response = requests.get(API_URL, params=params)
            data = response.json()

            if 'totalNutrients' in data:
                return {
                    'Calories': data['calories'],
                    'Protein': data['totalNutrients'].get('PROCNT', {}).get('quantity', 0),
                    'Fat': data['totalNutrients'].get('FAT', {}).get('quantity', 0),
                    'Carbs': data['totalNutrients'].get('CHOCDF', {}).get('quantity', 0),
                    'Quantity': quantity,
                    'Food': food_name
                }
            else:
                messagebox.showerror("Error", f"Could not find data for {food_name}")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"API request failed: {str(e)}")
            return None

    def save_recipe(self):
        total_cal = sum(item['Calories'] for item in self.ingredients)
        total_protein = sum(item['Protein'] for item in self.ingredients)
        total_fat = sum(item['Fat'] for item in self.ingredients)
        total_carbs = sum(item['Carbs'] for item in self.ingredients)
        total_weight = sum(item['Quantity'] for item in self.ingredients)

        content = f"Recipe: {self.current_recipe['name']}\n\nIngredients:\n"
        for item in self.ingredients:
            content += f"- {item['Food']}: {item['Quantity']}g\n"

        content += "\nTotal Nutrition:\n"
        content += f"Calories: {total_cal:.2f} kcal\n"
        content += f"Protein: {total_protein:.2f} g\n"
        content += f"Fat: {total_fat:.2f} g\n"
        content += f"Carbs: {total_carbs:.2f} g\n\n"

        content += "Per 100g:\n"
        content += f"Calories: {(total_cal / total_weight) * 100:.2f} kcal\n"
        content += f"Protein: {(total_protein / total_weight) * 100:.2f} g\n"
        content += f"Fat: {(total_fat / total_weight) * 100:.2f} g\n"
        content += f"Carbs: {(total_carbs / total_weight) * 100:.2f} g"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", "Recipe saved successfully")

    def return_to_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if hasattr(self, 'recipe_window') and self.recipe_window:
            self.recipe_window.destroy()
        self.recipe_mode = False
        self.current_recipe = {}
        self.ingredients = []
        self.create_main_frame()


if __name__ == '__main__':
    root = tk.Tk()
    app = NutritionApp(root)
    root.mainloop()