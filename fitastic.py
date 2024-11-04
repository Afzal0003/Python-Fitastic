import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
from pathlib import Path

class HealthAndFitnessTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitastic")
        self.root.geometry("800x600")
        
        # Initialize data storage
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.activity_file = self.data_dir / "activity_log.csv"
        self.health_file = self.data_dir / "health_data.csv"
        self.date = datetime.now().strftime("%Y-%m-%d")
        
        # Initialize files
        self.init_files()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.create_activity_tab()
        self.create_health_tab()
        self.create_progress_tab()
        self.create_future_goals_tab()  # New Future Goals tab
        
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', padding=5)
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)

    def init_files(self):
        """Initialize CSV files with headers if they don't exist."""
        if not self.activity_file.exists():
            with open(self.activity_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Steps", "Calories Burned", "Water Intake (L)", "Exercise"])

        if not self.health_file.exists():
            with open(self.health_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Weight (kg)", "Height (cm)", "BMI"])

    def create_activity_tab(self):
        """Create the daily activity logging tab."""
        activity_frame = ttk.Frame(self.notebook)
        self.notebook.add(activity_frame, text='Log Activity')
        
        ttk.Label(activity_frame, text="Daily Activity Log", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Create entry fields
        entry_frame = ttk.Frame(activity_frame)
        entry_frame.pack(pady=10)
        
        # Steps
        ttk.Label(entry_frame, text="Steps:").grid(row=0, column=0, padx=5, pady=5)
        self.steps_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.steps_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Calories
        ttk.Label(entry_frame, text="Calories Burned:").grid(row=1, column=0, padx=5, pady=5)
        self.calories_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.calories_var).grid(row=1, column=1, padx=5, pady=5)
        
        # Water
        ttk.Label(entry_frame, text="Water Intake (L):").grid(row=2, column=0, padx=5, pady=5)
        self.water_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.water_var).grid(row=2, column=1, padx=5, pady=5)
        
        # Exercise
        ttk.Label(entry_frame, text="Exercise Details:").grid(row=3, column=0, padx=5, pady=5)
        self.exercise_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.exercise_var).grid(row=3, column=1, padx=5, pady=5)
        
        # Submit button
        ttk.Button(activity_frame, text="Log Activity", command=self.log_daily_activity).pack(pady=20)

    def create_health_tab(self):
        """Create the health data updating tab."""
        health_frame = ttk.Frame(self.notebook)
        self.notebook.add(health_frame, text='Update Health')
        
        ttk.Label(health_frame, text="Health Measurements", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Create entry fields
        entry_frame = ttk.Frame(health_frame)
        entry_frame.pack(pady=10)
        
        # Weight
        ttk.Label(entry_frame, text="Weight (kg):").grid(row=0, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.weight_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Height
        ttk.Label(entry_frame, text="Height (cm):").grid(row=1, column=0, padx=5, pady=5)
        self.height_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.height_var).grid(row=1, column=1, padx=5, pady=5)
        
        # BMI Display
        self.bmi_label = ttk.Label(health_frame, text="")
        self.bmi_label.pack(pady=10)
        
        # Submit button
        ttk.Button(health_frame, text="Update Health Data", command=self.update_health_data).pack(pady=20)

    def create_progress_tab(self):
        """Create the progress viewing tab."""
        progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(progress_frame, text='View Progress')
        
        # Create notebook for sub-tabs
        progress_notebook = ttk.Notebook(progress_frame)
        progress_notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Activity Log tab
        activity_frame = ttk.Frame(progress_notebook)
        progress_notebook.add(activity_frame, text='Activity Log')
        
        # Create Treeview for activity data
        self.activity_tree = ttk.Treeview(activity_frame, columns=("Date", "Steps", "Calories", "Water", "Exercise"), show="headings")
        self.setup_treeview(self.activity_tree, 
                          [("Date", 100), ("Steps", 100), ("Calories", 100), ("Water", 100), ("Exercise", 200)])
        
        # Health Data tab
        health_frame = ttk.Frame(progress_notebook)
        progress_notebook.add(health_frame, text='Health Data')
        
        # Create Treeview for health data
        self.health_tree = ttk.Treeview(health_frame, columns=("Date", "Weight", "Height", "BMI"), show="headings")
        self.setup_treeview(self.health_tree, 
                          [("Date", 100), ("Weight", 100), ("Height", 100), ("BMI", 100)])
        
        # Refresh button
        ttk.Button(progress_frame, text="Refresh Data", command=self.refresh_progress).pack(pady=10)
        
        # Initial data load
        self.refresh_progress()

    def create_future_goals_tab(self):
        """Create the future goals tab."""
        future_goals_frame = ttk.Frame(self.notebook)
        self.notebook.add(future_goals_frame, text="Future Goals")

        ttk.Label(future_goals_frame, text="Future Goals", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        entry_frame = ttk.Frame(future_goals_frame)
        entry_frame.pack(pady=10)
        
        # Current Weight
        ttk.Label(entry_frame, text="Current Weight (kg):").grid(row=0, column=0, padx=5, pady=5)
        self.current_weight_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.current_weight_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Target Weight
        ttk.Label(entry_frame, text="Target Weight (kg):").grid(row=1, column=0, padx=5, pady=5)
        self.target_weight_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.target_weight_var).grid(row=1, column=1, padx=5, pady=5)
        
        # Submit button
        ttk.Button(future_goals_frame, text="Calculate Goals", command=self.calculate_future_goals).pack(pady=20)

    def setup_treeview(self, tree, columns):
        """Setup a treeview with given columns and widths."""
        for col, width in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree.master, orient="vertical", command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(expand=True, fill='both')

    def validate_number(self, value, allow_float=True):
        """Validate numerical input."""
        try:
            return float(value) >= 0 if allow_float else int(value) >= 0
        except ValueError:
            return False

    def calculate_bmi(self, weight, height):
        """Calculate BMI from weight and height."""
        return round(weight / ((height / 100) ** 2), 2)

    def log_daily_activity(self):
        """Log daily activity."""
        if not all(self.validate_number(var.get()) for var in [self.steps_var, self.calories_var, self.water_var]):
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return
        
        with open(self.activity_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.date, self.steps_var.get(), self.calories_var.get(), self.water_var.get(), self.exercise_var.get()])
        
        messagebox.showinfo("Success", "Daily activity logged successfully.")
    
    def update_health_data(self):
        """Update health data."""
        if not all(self.validate_number(var.get()) for var in [self.weight_var, self.height_var]):
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return
        
        weight = float(self.weight_var.get())
        height = float(self.height_var.get())
        bmi = self.calculate_bmi(weight, height)
        
        with open(self.health_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.date, weight, height, bmi])
        
        self.bmi_label.config(text=f"Your BMI: {bmi}")
        messagebox.showinfo("Success", "Health data updated successfully.")

    def refresh_progress(self):
        """Refresh data in the progress tabs."""
        for tree, file in [(self.activity_tree, self.activity_file), (self.health_tree, self.health_file)]:
            for row in tree.get_children():
                tree.delete(row)
            with open(file, mode="r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    tree.insert("", tk.END, values=row)

    def calculate_future_goals(self):
        """Calculate future calorie intake goals to reach the target weight."""
        try:
            current_weight = float(self.current_weight_var.get())
            target_weight = float(self.target_weight_var.get())
            bmr = 22 * current_weight  # Simplified BMR: 22 * weight in kg
            calorie_deficit_needed = (current_weight - target_weight) * 7700
            days_to_goal = 30  # Adjust as needed
            daily_calorie_intake = bmr - (calorie_deficit_needed / days_to_goal)
            
            messagebox.showinfo(
                "Caloric Goal",
                f"To reach your target weight of {target_weight} kg, aim for a daily calorie intake of approximately {daily_calorie_intake:.2f} calories."
            )
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthAndFitnessTrackerGUI(root)
    root.mainloop()
