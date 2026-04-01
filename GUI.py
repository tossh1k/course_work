import tkinter as tk
from tkinter import ttk, messagebox
import Matrix

class MatrixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")
        self.root.geometry("1200x600")
        
        self.matrix_a = None
        self.matrix_b = None
        self.result_matrix = None
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        right_frame = ttk.Frame(main_frame, width=200)
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E))
        right_frame.columnconfigure(0, weight=1)
        
        ttk.Label(right_frame, text="Select Operation:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.operation_var = tk.StringVar(value="Addition")
        operations = ["Addition", "Subtraction", "Multiplication", "Transpose", "Inverse", "Determinant"]
        self.operation_combo = ttk.Combobox(right_frame, textvariable=self.operation_var, 
                                           values=operations, state="readonly")
        self.operation_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.operation_combo.bind('<<ComboboxSelected>>', self.on_operation_change)
        
        ttk.Button(right_frame, text="Calculate", command=self.calculate).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(right_frame, text="Clear All", command=self.clear_all).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(right_frame, text="Random Fill A", command=lambda: self.fill_random('A')).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(right_frame, text="Random Fill B", command=lambda: self.fill_random('B')).grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.on_operation_change()
        
    def on_operation_change(self, event=None):
        operation = self.operation_var.get()
        
        for widget in self.left_frame.winfo_children():
            widget.destroy()
            
        if operation in ["Addition", "Subtraction", "Multiplication"]:
            self.create_two_matrix_view()
        elif operation in ["Transpose", "Inverse", "Determinant"]:
            self.create_single_matrix_view()
            
    def create_two_matrix_view(self):
        matrices_container = ttk.Frame(self.left_frame)
        matrices_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        matrix_a_frame = ttk.LabelFrame(matrices_container, text="Matrix A", padding="5")
        matrix_a_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        operation_symbol = "+"
        if self.operation_var.get() == "Subtraction":
            operation_symbol = "-"
        elif self.operation_var.get() == "Multiplication":
            operation_symbol = "×"
            
        operation_label = ttk.Label(matrices_container, text=operation_symbol, font=("Arial", 24))
        operation_label.grid(row=0, column=1, padx=15, pady=20)
        
        matrix_b_frame = ttk.LabelFrame(matrices_container, text="Matrix B", padding="5")
        matrix_b_frame.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        equals_label = ttk.Label(matrices_container, text="=", font=("Arial", 24))
        equals_label.grid(row=0, column=3, padx=15, pady=20)
        
        result_frame = ttk.LabelFrame(matrices_container, text="Result", padding="5")
        result_frame.grid(row=0, column=4, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        dim_frame = ttk.Frame(self.left_frame)
        dim_frame.grid(row=1, column=0, pady=15)
        
        ttk.Label(dim_frame, text="Matrix A:").grid(row=0, column=0, padx=(0, 5))
        ttk.Label(dim_frame, text="Rows:").grid(row=0, column=1, padx=2)
        self.rows_a_var = tk.StringVar(value="3")
        rows_a_spin = ttk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.rows_a_var, width=5)
        rows_a_spin.grid(row=0, column=2, padx=2)
        
        ttk.Label(dim_frame, text="Cols:").grid(row=0, column=3, padx=2)
        self.cols_a_var = tk.StringVar(value="3")
        cols_a_spin = ttk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.cols_a_var, width=5)
        cols_a_spin.grid(row=0, column=4, padx=2)
        
        ttk.Label(dim_frame, text="Matrix B:").grid(row=0, column=5, padx=(20, 5))
        ttk.Label(dim_frame, text="Rows:").grid(row=0, column=6, padx=2)
        self.rows_b_var = tk.StringVar(value="3")
        rows_b_spin = ttk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.rows_b_var, width=5)
        rows_b_spin.grid(row=0, column=7, padx=2)
        
        ttk.Label(dim_frame, text="Cols:").grid(row=0, column=8, padx=2)
        self.cols_b_var = tk.StringVar(value="3")
        cols_b_spin = ttk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.cols_b_var, width=5)
        cols_b_spin.grid(row=0, column=9, padx=2)
        
        ttk.Button(dim_frame, text="Update Dimensions", command=self.update_dimensions).grid(row=0, column=10, padx=20)
        
        self.matrix_a_entries = self.create_matrix_widgets(matrix_a_frame, 3, 3)
        self.matrix_b_entries = self.create_matrix_widgets(matrix_b_frame, 3, 3)
        self.result_entries = self.create_matrix_widgets(result_frame, 3, 3, readonly=True)
        
    def create_single_matrix_view(self):
        matrices_container = ttk.Frame(self.left_frame)
        matrices_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        matrix_a_frame = ttk.LabelFrame(matrices_container, text="Matrix A", padding="5")
        matrix_a_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        operation_symbol = self.operation_var.get()
        if operation_symbol == "Transpose":
            operation_symbol = "T"
        elif operation_symbol == "Inverse":
            operation_symbol = "⁻¹"
        elif operation_symbol == "Determinant":
            operation_symbol = "det"
            
        operation_label = ttk.Label(matrices_container, text=operation_symbol, font=("Arial", 20))
        operation_label.grid(row=0, column=1, padx=15, pady=20)
        
        equals_label = ttk.Label(matrices_container, text="=", font=("Arial", 24))
        equals_label.grid(row=0, column=2, padx=15, pady=20)
        
        result_frame = ttk.LabelFrame(matrices_container, text="Result", padding="5")
        result_frame.grid(row=0, column=3, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        dim_frame = ttk.Frame(self.left_frame)
        dim_frame.grid(row=1, column=0, pady=15)
        
        ttk.Label(dim_frame, text="Rows:").grid(row=0, column=0, padx=2)
        self.rows_a_var = tk.StringVar(value="3")
        rows_spin = ttk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.rows_a_var, width=5)
        rows_spin.grid(row=0, column=1, padx=2)
        
        ttk.Label(dim_frame, text="Cols:").grid(row=0, column=2, padx=2)
        self.cols_a_var = tk.StringVar(value="3")
        cols_spin = ttk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.cols_a_var, width=5)
        cols_spin.grid(row=0, column=3, padx=2)
        
        ttk.Button(dim_frame, text="Update Dimensions", command=self.update_dimensions).grid(row=0, column=4, padx=20)
        
        self.matrix_a_entries = self.create_matrix_widgets(matrix_a_frame, 3, 3)
        self.matrix_b_entries = None
        self.result_entries = self.create_matrix_widgets(result_frame, 3, 3, readonly=True)
        
    def create_matrix_widgets(self, parent, rows, cols, readonly=False):
        entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                if readonly:
                    entry = ttk.Entry(parent, width=6, state="readonly", justify="center")
                else:
                    entry = ttk.Entry(parent, width=6, justify="center")
                    entry.insert(0, "0")
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            entries.append(row_entries)
        return entries
        
    def update_dimensions(self):
        try:
            rows_a = int(self.rows_a_var.get())
            cols_a = int(self.cols_a_var.get())
            
            operation = self.operation_var.get()
            
            if operation in ["Addition", "Subtraction", "Multiplication"]:
                rows_b = int(self.rows_b_var.get())
                cols_b = int(self.cols_b_var.get())
                
                self.update_matrix_widgets(self.matrix_a_entries, rows_a, cols_a)
                self.update_matrix_widgets(self.matrix_b_entries, rows_b, cols_b)
                
                if operation == "Multiplication":
                    result_rows, result_cols = rows_a, cols_b
                else:
                    result_rows, result_cols = rows_a, cols_a
                    
                self.update_matrix_widgets(self.result_entries, result_rows, result_cols, readonly=True)
                
            else:
                self.update_matrix_widgets(self.matrix_a_entries, rows_a, cols_a)
                
                if operation == "Transpose":
                    result_rows, result_cols = cols_a, rows_a
                elif operation == "Inverse":
                    result_rows, result_cols = rows_a, cols_a
                else:
                    result_rows, result_cols = 1, 1
                    
                self.update_matrix_widgets(self.result_entries, result_rows, result_cols, readonly=True)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dimensions")
            
    def update_matrix_widgets(self, entries, new_rows, new_cols, readonly=False):
        if entries:
            parent = entries[0][0].master
        else:
            return
            
        for row in entries:
            for entry in row:
                entry.destroy()
                
        entries.clear()
        for i in range(new_rows):
            row_entries = []
            for j in range(new_cols):
                if readonly:
                    entry = ttk.Entry(parent, width=6, state="readonly", justify="center")
                else:
                    entry = ttk.Entry(parent, width=6, justify="center")
                    entry.insert(0, "0")
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            entries.append(row_entries)
            
    def get_matrix_from_entries(self, entries):
        rows = len(entries)
        cols = len(entries[0])
        matrix = Matrix.Matrix(rows, cols)
        
        for i in range(rows):
            for j in range(cols):
                try:
                    value = float(entries[i][j].get())
                    matrix[i, j] = value
                except ValueError:
                    matrix[i, j] = 0.0
                    
        return matrix
        
    def set_matrix_to_entries(self, matrix, entries):
        rows = len(entries)
        cols = len(entries[0])
        
        for i in range(rows):
            for j in range(cols):
                entries[i][j].config(state="normal")
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, f"{matrix[i, j]:.2f}")
                if entries == self.result_entries:
                    entries[i][j].config(state="readonly")
        
    def calculate(self):
        try:
            operation = self.operation_var.get()
            
            self.matrix_a = self.get_matrix_from_entries(self.matrix_a_entries)
            
            if operation in ["Addition", "Subtraction", "Multiplication"]:
                self.matrix_b = self.get_matrix_from_entries(self.matrix_b_entries)
                
                if operation == "Addition":
                    self.result_matrix = self.matrix_a + self.matrix_b
                elif operation == "Subtraction":
                    self.result_matrix = self.matrix_a - self.matrix_b
                elif operation == "Multiplication":
                    self.result_matrix = self.matrix_a * self.matrix_b
                    
            elif operation == "Transpose":
                self.result_matrix = self.matrix_a.transpose()
                
            elif operation == "Inverse":
                self.result_matrix = self.matrix_a.inverse()
                
            elif operation == "Determinant":
                det = self.matrix_a.calculate_determinant()
                messagebox.showinfo("Determinant", f"The determinant is: {det:.4f}")
                return
                
            self.set_matrix_to_entries(self.result_matrix, self.result_entries)
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            
    def clear_all(self):
        for entries in [self.matrix_a_entries, self.matrix_b_entries, self.result_entries]:
            if entries:
                for row in entries:
                    for entry in row:
                        entry.config(state="normal")
                        entry.delete(0, tk.END)
                        entry.insert(0, "0")
                        if entries == self.result_entries:
                            entry.config(state="readonly")
        
    def fill_random(self, matrix_id):
        try:
            if matrix_id == 'A':
                matrix = self.get_matrix_from_entries(self.matrix_a_entries)
                matrix.fill_random()
                self.set_matrix_to_entries(matrix, self.matrix_a_entries)
            elif matrix_id == 'B' and self.matrix_b_entries:
                matrix = self.get_matrix_from_entries(self.matrix_b_entries)
                matrix.fill_random()
                self.set_matrix_to_entries(matrix, self.matrix_b_entries)
        except Exception as e:
            messagebox.showerror("Error", f"Random fill error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixGUI(root)
    root.mainloop()
