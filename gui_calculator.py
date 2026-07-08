"""
رابط کاربری گرافیکی برای محاسبه‌گر میکسر کوارتز
GUI Interface for Quartz Mixer Calculator

استفاده از Tkinter برای ایجاد رابط کاربری حرفه‌ای
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
from quartz_calculator import QuartzMixerCalculator
import threading


class QuartzMixerGUI:
    """
    رابط کاربری گرافیکی برای محاسبه‌گر میکسر کوارتز
    """
    
    def __init__(self, root):
        """
        مقداردهی اولیه رابط کاربری
        """
        self.root = root
        self.root.title("محاسبه‌گر میکسر کوارتز | Quartz Mixer Calculator")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # تنظیم رنگ‌های پایه
        self.bg_color = "#f0f0f0"
        self.header_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.success_color = "#27ae60"
        
        self.root.configure(bg=self.bg_color)
        
        # ایجاد محاسبه‌گر
        self.calculator = None
        
        # ایجاد رابط
        self.create_widgets()
    
    def create_widgets(self):
        """
        ایجاد تمام ابزارهای رابط کاربری
        """
        # هدر
        self.create_header()
        
        # فریم ورودی
        self.create_input_frame()
        
        # فریم دکمه‌ها
        self.create_button_frame()
        
        # فریم نتایج
        self.create_results_frame()
        
        # فریم پایین (نوار وضعیت)
        self.create_footer()
    
    def create_header(self):
        """
        ایجاد بخش هدر
        """
        header_frame = tk.Frame(self.root, bg=self.header_color, height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(
            header_frame,
            text="🏭 محاسبه‌گر میکسر کوارتز",
            font=("Arial", 18, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Quartz Mixer Calculator | محاسبه فضای خالی و ترکیب مواد برای 100 کیلو",
            font=("Arial", 10),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        subtitle_label.pack(pady=5)
    
    def create_input_frame(self):
        """
        ایجاد فریم ورودی
        """
        input_frame = ttk.LabelFrame(
            self.root,
            text="⚙️ تنظیمات",
            padding=15
        )
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # وزن دسته
        ttk.Label(input_frame, text="وزن دسته (کیلوگرم):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.batch_size_var = tk.IntVar(value=100)
        batch_spinbox = ttk.Spinbox(
            input_frame,
            from_=1,
            to=1000,
            textvariable=self.batch_size_var,
            width=15
        )
        batch_spinbox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # فریم مواد
        materials_frame = ttk.LabelFrame(input_frame, text="📊 درصد مواد", padding=10)
        materials_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        self.material_vars = {}
        materials_list = [
            ('quartz', 'کوارتز (Quartz)', 70),
            ('carbon_black', 'دوده (Carbon Black)', 15),
            ('peroxide', 'پراکسید (Peroxide)', 10),
            ('resin', 'رزین (Resin)', 5)
        ]
        
        for idx, (key, label, default_value) in enumerate(materials_list):
            ttk.Label(materials_frame, text=label).grid(row=idx, column=0, sticky=tk.W, pady=5)
            
            var = tk.IntVar(value=default_value)
            self.material_vars[key] = var
            
            spinbox = ttk.Spinbox(
                materials_frame,
                from_=0,
                to=100,
                textvariable=var,
                width=10
            )
            spinbox.grid(row=idx, column=1, sticky=tk.W, padx=10, pady=5)
            
            ttk.Label(materials_frame, text="%").grid(row=idx, column=2, sticky=tk.W, padx=5)
    
    def create_button_frame(self):
        """
        ایجاد فریم دکمه‌ها
        """
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # دکمه محاسبه
        calc_button = tk.Button(
            button_frame,
            text="📐 محاسبه",
            command=self.calculate,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        calc_button.pack(side=tk.LEFT, padx=5)
        
        # دکمه صادرات JSON
        export_json_button = tk.Button(
            button_frame,
            text="💾 صادرات JSON",
            command=self.export_json,
            bg=self.success_color,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        export_json_button.pack(side=tk.LEFT, padx=5)
        
        # دکمه صادرات CSV
        export_csv_button = tk.Button(
            button_frame,
            text="📊 صادرات CSV",
            command=self.export_csv,
            bg="#e67e22",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        export_csv_button.pack(side=tk.LEFT, padx=5)
        
        # دکمه پاک کردن
        clear_button = tk.Button(
            button_frame,
            text="🗑️ پاک کردن",
            command=self.clear_results,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def create_results_frame(self):
        """
        ایجاد فریم نتایج
        """
        # فریم Notebook برای تب‌ها
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # تب فضای خالی
        self.void_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.void_frame, text="📊 فضای خالی")
        
        # تب فرمول مواد
        self.materials_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.materials_frame, text="📋 فرمول مواد")
        
        # تب JSON
        self.json_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.json_frame, text="📁 JSON")
        
        # ایجاد درخت برای هر تب
        self.create_void_tree()
        self.create_materials_tree()
        self.create_json_text()
    
    def create_void_tree(self):
        """
        ایجاد جدول فضای خالی
        """
        # اسکرول بار
        scrollbar = ttk.Scrollbar(self.void_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # درخت
        self.void_tree = ttk.Treeview(
            self.void_frame,
            columns=('Sieve', 'Void', 'Packing'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.void_tree.yview)
        
        # تنظیم ستون‌ها
        self.void_tree.column('#0', width=0, stretch=tk.NO)
        self.void_tree.column('Sieve', anchor=tk.CENTER, width=150)
        self.void_tree.column('Void', anchor=tk.CENTER, width=150)
        self.void_tree.column('Packing', anchor=tk.CENTER, width=150)
        
        # تنظیم هدر
        self.void_tree.heading('#0', text='', anchor=tk.W)
        self.void_tree.heading('Sieve', text='اندازه الک (mm)', anchor=tk.CENTER)
        self.void_tree.heading('Void', text='فضای خالی (%)', anchor=tk.CENTER)
        self.void_tree.heading('Packing', text='چگالی Packing', anchor=tk.CENTER)
        
        self.void_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_materials_tree(self):
        """
        ایجاد جدول مواد
        """
        # اسکرول بار
        scrollbar = ttk.Scrollbar(self.materials_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # درخت
        self.materials_tree = ttk.Treeview(
            self.materials_frame,
            columns=('Name', 'Percentage', 'Weight'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.materials_tree.yview)
        
        # تنظیم ستون‌ها
        self.materials_tree.column('#0', width=0, stretch=tk.NO)
        self.materials_tree.column('Name', anchor=tk.CENTER, width=200)
        self.materials_tree.column('Percentage', anchor=tk.CENTER, width=150)
        self.materials_tree.column('Weight', anchor=tk.CENTER, width=150)
        
        # تنظیم هدر
        self.materials_tree.heading('#0', text='', anchor=tk.W)
        self.materials_tree.heading('Name', text='نام ماده', anchor=tk.CENTER)
        self.materials_tree.heading('Percentage', text='درصد', anchor=tk.CENTER)
        self.materials_tree.heading('Weight', text='وزن (کیلوگرم)', anchor=tk.CENTER)
        
        self.materials_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_json_text(self):
        """
        ایجاد جعبه متن JSON
        """
        # اسکرول بار
        scrollbar = ttk.Scrollbar(self.json_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # متن
        self.json_text = tk.Text(
            self.json_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier", 10),
            wrap=tk.WORD
        )
        scrollbar.config(command=self.json_text.yview)
        self.json_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_footer(self):
        """
        ایجاد فریم پایین
        """
        footer_frame = tk.Frame(self.root, bg=self.header_color, height=30)
        footer_frame.pack(fill=tk.X, padx=0, pady=0, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            footer_frame,
            text="آماده برای محاسبه...",
            font=("Arial", 9),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        self.status_label.pack(pady=5)
    
    def update_status(self, message):
        """
        بروزرسانی پیام وضعیت
        """
        self.status_label.config(text=message)
        self.root.update()
    
    def calculate(self):
        """
        انجام محاسبات
        """
        try:
            self.update_status("🔄 در حال محاسبه...")
            
            # ایجاد محاسبه‌گر با مقادیر سفارشی
            batch_size = self.batch_size_var.get()
            
            materials = {
                'quartz': self.material_vars['quartz'].get(),
                'carbon_black': self.material_vars['carbon_black'].get(),
                'peroxide': self.material_vars['peroxide'].get(),
                'resin': self.material_vars['resin'].get()
            }
            
            # بررسی درصد‌ها
            total_percentage = sum(materials.values())
            if abs(total_percentage - 100) > 0.01:
                messagebox.showerror(
                    "خطا",
                    f"مجموع درصد مواد باید 100 باشد، اما {total_percentage} است"
                )
                self.update_status("❌ خطا: درصد مواد باید 100 باشد")
                return
            
            # ایجاد محاسبه‌گر
            from quartz_calculator import QuartzMixerCalculator as Calculator
            
            self.calculator = Calculator(batch_size=batch_size)
            self.calculator.materials = materials
            
            # محاسبه نتایج
            formula = self.calculator.generate_formula()
            void_data = self.calculator.calculate_void_for_all_sieves()
            
            # پر کردن جداول
            self.populate_void_table(void_data)
            self.populate_materials_table(formula)
            self.populate_json_text(formula)
            
            self.update_status("✅ محاسبات با موفقیت انجام شد")
            messagebox.showinfo("موفقیت", "محاسبات با موفقیت انجام شدند!")
            
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد:\n{str(e)}")
            self.update_status(f"❌ خطا: {str(e)}")
    
    def populate_void_table(self, void_data):
        """
        پر کردن جدول فضای خالی
        """
        # پاک کردن جدول قدیم
        for item in self.void_tree.get_children():
            self.void_tree.delete(item)
        
        # اضافه کردن داده‌های جدید
        for data in void_data:
            self.void_tree.insert(
                '',
                'end',
                values=(
                    f"{data['sieve_size_mm']:.2f}",
                    f"{data['void_percentage']:.2f}%",
                    f"{data['packing_density']:.4f}"
                )
            )
    
    def populate_materials_table(self, formula):
        """
        پر کردن جدول مواد
        """
        # پاک کردن جدول قدیم
        for item in self.materials_tree.get_children():
            self.materials_tree.delete(item)
        
        # نام‌های فارسی
        material_names = {
            'quartz': 'کوارتز (Quartz)',
            'carbon_black': 'دوده (Carbon Black)',
            'peroxide': 'پراکسید (Peroxide)',
            'resin': 'رزین (Resin)'
        }
        
        # اضافه کردن داده‌های جدید
        for material, quantity in formula['materials'].items():
            percentage = self.calculator.materials[material]
            name = material_names[material]
            
            self.materials_tree.insert(
                '',
                'end',
                values=(
                    name,
                    f"{percentage}%",
                    f"{quantity:.2f} kg"
                )
            )
        
        # اضافه کردن کل
        self.materials_tree.insert(
            '',
            'end',
            values=(
                'کل',
                '100%',
                f"{formula['total_weight']:.2f} kg"
            ),
            tags=('total',)
        )
        
        self.materials_tree.tag_configure('total', background='#d5f4e6')
    
    def populate_json_text(self, formula):
        """
        پر کردن متن JSON
        """
        self.json_text.delete(1.0, tk.END)
        
        json_str = json.dumps(formula, indent=2, ensure_ascii=False)
        self.json_text.insert(1.0, json_str)
    
    def export_json(self):
        """
        صادرات به JSON
        """
        if not self.calculator:
            messagebox.showwarning("هشدار", "ابتدا محاسبات را انجام دهید")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=f"quartz_formula_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if filename:
                result = self.calculator.export_to_json(filename)
                messagebox.showinfo("موفقیت", result)
                self.update_status(f"✅ فایل ذخیره شد: {filename}")
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در صادرات:\n{str(e)}")
    
    def export_csv(self):
        """
        صادرات به CSV
        """
        if not self.calculator:
            messagebox.showwarning("هشدار", "ابتدا محاسبات را انجام دهید")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"quartz_formula_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                result = self.calculator.export_to_csv(filename)
                messagebox.showinfo("موفقیت", result)
                self.update_status(f"✅ فایل ذخیره شد: {filename}")
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در صادرات:\n{str(e)}")
    
    def clear_results(self):
        """
        پاک کردن نتایج
        """
        # پاک کردن جداول
        for item in self.void_tree.get_children():
            self.void_tree.delete(item)
        
        for item in self.materials_tree.get_children():
            self.materials_tree.delete(item)
        
        self.json_text.delete(1.0, tk.END)
        
        self.calculator = None
        self.update_status("✨ نتایج پاک شدند")


def main():
    """
    تابع اصلی برنامه
    """
    root = tk.Tk()
    app = QuartzMixerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
