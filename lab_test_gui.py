"""
رابط کاربری گرافیکی برای محاسبه‌گر تست آزمایشگاهی
GUI for Lab Test Calculator

رابط حرفه‌ای برای وارد کردن داده‌های تست و محاسبه خودکار
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
from lab_test_calculator import LabTestQuartzCalculator


class LabTestGUI:
    """
    رابط کاربری گرافیکی برای محاسبه‌گر تست آزمایشگاهی
    """
    
    def __init__(self, root):
        """
        مقداردهی اولیه رابط کاربری
        """
        self.root = root
        self.root.title("محاسبه‌گر تست آزمایشگاهی | Lab Test Calculator")
        self.root.geometry("1200x900")
        self.root.resizable(True, True)
        
        # تنظیم رنگ‌های پایه
        self.bg_color = "#f0f0f0"
        self.header_color = "#1a5f7a"
        self.accent_color = "#2196F3"
        self.success_color = "#27ae60"
        self.warning_color = "#f39c12"
        
        self.root.configure(bg=self.bg_color)
        
        # ایجاد محاسبه‌گر
        self.calculator = None
        
        # متغیرهای ورودی
        self.test_weight_var = tk.IntVar(value=100)
        self.sieve_vars = {
            '0-0.1': tk.IntVar(value=0),
            '0.1-0.2': tk.IntVar(value=0),
            '0.2-0.3': tk.IntVar(value=0),
            '0.3-0.4': tk.IntVar(value=0)
        }
        
        # ایجاد رابط
        self.create_widgets()
    
    def create_widgets(self):
        """
        ایجاد تمام ابزارهای رابط کاربری
        """
        # هدر
        self.create_header()
        
        # فریم اصلی با دو ستون
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ستون چپ - ورودی
        self.create_input_frame(main_frame)
        
        # ستون راست - نتایج
        self.create_results_frame(main_frame)
        
        # فریم پایین
        self.create_footer()
    
    def create_header(self):
        """
        ایجاد بخش هدر
        """
        header_frame = tk.Frame(self.root, bg=self.header_color, height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(
            header_frame,
            text="🧪 محاسبه‌گر تست آزمایشگاهی",
            font=("Arial", 20, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Lab Test Calculator | تجزیه فضای خالی و فرمول بهینه برای 100 کیلو",
            font=("Arial", 11),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        subtitle_label.pack(pady=5)
    
    def create_input_frame(self, parent):
        """
        ایجاد فریم ورودی (ستون چپ)
        """
        input_frame = ttk.LabelFrame(
            parent,
            text="📝 وارد کردن داده‌های تست",
            padding=15
        )
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # وزن تست
        ttk.Label(input_frame, text="وزن کل تست (گرم):", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        weight_frame = ttk.Frame(input_frame)
        weight_frame.pack(fill=tk.X, pady=(0, 20))
        
        weight_spinbox = ttk.Spinbox(
            weight_frame,
            from_=1,
            to=1000,
            textvariable=self.test_weight_var,
            width=15,
            font=("Arial", 11)
        )
        weight_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(weight_frame, text="گرم", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # جداول بازه‌های الک
        ttk.Label(
            input_frame,
            text="خروجی‌های سیلیس (گرم):",
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W, pady=(10, 10))
        
        # فریم برای ورودی‌های بازه‌ها
        sieve_input_frame = ttk.LabelFrame(input_frame, text="بازه‌های الک", padding=10)
        sieve_input_frame.pack(fill=tk.X, pady=10)
        
        sieve_labels = [
            ('0-0.1', 'بازه 0-0.1 mm'),
            ('0.1-0.2', 'بازه 0.1-0.2 mm'),
            ('0.2-0.3', 'بازه 0.2-0.3 mm'),
            ('0.3-0.4', 'بازه 0.3-0.4 mm')
        ]
        
        for idx, (key, label) in enumerate(sieve_labels):
            row_frame = ttk.Frame(sieve_input_frame)
            row_frame.pack(fill=tk.X, pady=8)
            
            ttk.Label(row_frame, text=label, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
            
            spinbox = ttk.Spinbox(
                row_frame,
                from_=0,
                to=1000,
                textvariable=self.sieve_vars[key],
                width=15,
                font=("Arial", 10)
            )
            spinbox.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(row_frame, text="گرم", font=("Arial", 10)).pack(side=tk.LEFT, padx=2)
        
        # دکمه‌های عملیاتی
        button_frame = tk.Frame(input_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=20)
        
        # دکمه محاسبه
        calc_button = tk.Button(
            button_frame,
            text="📐 محاسبه",
            command=self.calculate,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            relief=tk.RAISED,
            cursor="hand2"
        )
        calc_button.pack(side=tk.LEFT, padx=5)
        
        # دکمه پاک
        clear_button = tk.Button(
            button_frame,
            text="🗑️ پاک کردن",
            command=self.clear_all,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            relief=tk.RAISED,
            cursor="hand2"
        )
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def create_results_frame(self, parent):
        """
        ایجاد فریم نتایج (ستون راست)
        """
        results_frame = ttk.LabelFrame(
            parent,
            text="📊 نتایج محاسبات",
            padding=15
        )
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook برای تب‌ها
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # تب 1: درصد‌ها
        self.percentages_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.percentages_frame, text="📊 درصد‌ها")
        
        # تب 2: فضای خالی
        self.void_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.void_frame, text="📐 فضای خالی")
        
        # تب 3: فرمول 100 کیلو
        self.formula_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.formula_frame, text="🏭 فرمول 100 کیلو")
        
        # تب 4: JSON
        self.json_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.json_frame, text="📁 JSON")
        
        # ایجاد درخت‌های نتایج
        self.create_percentages_tree()
        self.create_void_tree()
        self.create_formula_tree()
        self.create_json_text()
        
        # فریم دکمه‌های صادرات
        export_frame = tk.Frame(results_frame, bg=self.bg_color)
        export_frame.pack(fill=tk.X, pady=10)
        
        json_export_button = tk.Button(
            export_frame,
            text="💾 صادرات JSON",
            command=self.export_json,
            bg=self.success_color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        json_export_button.pack(side=tk.LEFT, padx=5)
        
        report_button = tk.Button(
            export_frame,
            text="📄 گزارش متنی",
            command=self.export_report,
            bg=self.warning_color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        report_button.pack(side=tk.LEFT, padx=5)
    
    def create_percentages_tree(self):
        """
        ایجاد جدول درصد‌ها
        """
        scrollbar = ttk.Scrollbar(self.percentages_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.percentages_tree = ttk.Treeview(
            self.percentages_frame,
            columns=('Range', 'Weight', 'Percentage'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.percentages_tree.yview)
        
        self.percentages_tree.column('#0', width=0, stretch=tk.NO)
        self.percentages_tree.column('Range', anchor=tk.CENTER, width=100)
        self.percentages_tree.column('Weight', anchor=tk.CENTER, width=100)
        self.percentages_tree.column('Percentage', anchor=tk.CENTER, width=100)
        
        self.percentages_tree.heading('#0', text='')
        self.percentages_tree.heading('Range', text='بازه (mm)', anchor=tk.CENTER)
        self.percentages_tree.heading('Weight', text='وزن (g)', anchor=tk.CENTER)
        self.percentages_tree.heading('Percentage', text='درصد (%)', anchor=tk.CENTER)
        
        self.percentages_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_void_tree(self):
        """
        ایجاد جدول فضای خالی
        """
        scrollbar = ttk.Scrollbar(self.void_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.void_tree = ttk.Treeview(
            self.void_frame,
            columns=('Range', 'Void', 'VoidPercent', 'Packing'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.void_tree.yview)
        
        self.void_tree.column('#0', width=0, stretch=tk.NO)
        self.void_tree.column('Range', anchor=tk.CENTER, width=80)
        self.void_tree.column('Void', anchor=tk.CENTER, width=80)
        self.void_tree.column('VoidPercent', anchor=tk.CENTER, width=100)
        self.void_tree.column('Packing', anchor=tk.CENTER, width=100)
        
        self.void_tree.heading('#0', text='')
        self.void_tree.heading('Range', text='بازه (mm)', anchor=tk.CENTER)
        self.void_tree.heading('Void', text='فضای خالی', anchor=tk.CENTER)
        self.void_tree.heading('VoidPercent', text='فضای خالی (%)', anchor=tk.CENTER)
        self.void_tree.heading('Packing', text='چگالی Packing', anchor=tk.CENTER)
        
        self.void_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_formula_tree(self):
        """
        ایجاد جدول فرمول 100 کیلو
        """
        scrollbar = ttk.Scrollbar(self.formula_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.formula_tree = ttk.Treeview(
            self.formula_frame,
            columns=('Range', 'Percentage', 'Weight'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.formula_tree.yview)
        
        self.formula_tree.column('#0', width=0, stretch=tk.NO)
        self.formula_tree.column('Range', anchor=tk.CENTER, width=100)
        self.formula_tree.column('Percentage', anchor=tk.CENTER, width=100)
        self.formula_tree.column('Weight', anchor=tk.CENTER, width=100)
        
        self.formula_tree.heading('#0', text='')
        self.formula_tree.heading('Range', text='بازه (mm)', anchor=tk.CENTER)
        self.formula_tree.heading('Percentage', text='درصد (%)', anchor=tk.CENTER)
        self.formula_tree.heading('Weight', text='وزن (kg)', anchor=tk.CENTER)
        
        self.formula_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_json_text(self):
        """
        ایجاد جعبه متن JSON
        """
        scrollbar = ttk.Scrollbar(self.json_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.json_text = tk.Text(
            self.json_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        scrollbar.config(command=self.json_text.yview)
        self.json_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_footer(self):
        """
        ایجاد فریم پایین
        """
        footer_frame = tk.Frame(self.root, bg=self.header_color, height=40)
        footer_frame.pack(fill=tk.X, padx=0, pady=0, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            footer_frame,
            text="آماده برای دریافت داده‌های تست...",
            font=("Arial", 10),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        self.status_label.pack(pady=8)
    
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
            
            # گرفتن داده‌های ورودی
            test_weight = self.test_weight_var.get()
            
            test_results = {
                '0-0.1': self.sieve_vars['0-0.1'].get(),
                '0.1-0.2': self.sieve_vars['0.1-0.2'].get(),
                '0.2-0.3': self.sieve_vars['0.2-0.3'].get(),
                '0.3-0.4': self.sieve_vars['0.3-0.4'].get()
            }
            
            # بررسی داده‌های ورودی
            if test_weight <= 0:
                messagebox.showerror("خطا", "وزن تست باید بیشتر از صفر باشد!")
                self.update_status("❌ خطا: وزن تست نامعتبر")
                return
            
            total_weight = sum(test_results.values())
            if total_weight != test_weight:
                messagebox.showerror(
                    "خطا",
                    f"مجموع وزن‌های خروجی ({total_weight}g) با وزن کل تست ({test_weight}g) مطابقت ندارد!"
                )
                self.update_status("❌ خطا: مجموع وزن‌های خروجی نامعتبر")
                return
            
            # ایجاد محاسبه‌گر و اضافه کردن داده‌ها
            self.calculator = LabTestQuartzCalculator()
            self.calculator.add_test_data(weight_grams=test_weight, results_dict=test_results)
            
            # پر کردن جداول
            self.populate_percentages_table()
            self.populate_void_table()
            self.populate_formula_table()
            self.populate_json_text()
            
            self.update_status("✅ محاسبات با موفقیت انجام شد")
            messagebox.showinfo("موفقیت", "محاسبات تست آزمایشگاهی با موفقیت انجام شدند!")
            
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد:\n{str(e)}")
            self.update_status(f"❌ خطا: {str(e)}")
    
    def populate_percentages_table(self):
        """
        پر کردن جدول درصد‌ها
        """
        # پاک کردن جدول قدیم
        for item in self.percentages_tree.get_children():
            self.percentages_tree.delete(item)
        
        # گرفتن داده‌ها
        percentages = self.calculator.calculate_percentages()
        
        # اضافه کردن سطرها
        for sieve_range in self.calculator.sieve_ranges:
            name = sieve_range['name']
            weight = self.calculator.test_results.get(name, 0)
            percentage = percentages[name]
            
            self.percentages_tree.insert(
                '',
                'end',
                values=(name, f"{weight}", f"{percentage:.2f}%")
            )
        
        # اضافه کردن کل
        total_weight = self.calculator.test_weight
        self.percentages_tree.insert(
            '',
            'end',
            values=('کل', f"{total_weight}", '100.00%'),
            tags=('total',)
        )
        
        self.percentages_tree.tag_configure('total', background='#d5f4e6')
    
    def populate_void_table(self):
        """
        پر کردن جدول فضای خالی
        """
        # پاک کردن جدول قدیم
        for item in self.void_tree.get_children():
            self.void_tree.delete(item)
        
        # گرفتن داده‌ها
        void_analysis = self.calculator.get_void_analysis()
        
        # اضافه کردن سطرها
        for item in void_analysis:
            self.void_tree.insert(
                '',
                'end',
                values=(
                    item['sieve_range'],
                    f"{item['void_fraction']:.4f}",
                    f"{item['void_percentage']:.2f}%",
                    f"{item['packing_density']:.4f}"
                )
            )
    
    def populate_formula_table(self):
        """
        پر کردن جدول فرمول 100 کیلو
        """
        # پاک کردن جدول قدیم
        for item in self.formula_tree.get_children():
            self.formula_tree.delete(item)
        
        # گرفتن داده‌ها
        final_recipe = self.calculator.get_final_recipe_100kg()
        
        # اضافه کردن سطرها
        for sieve_range, data in final_recipe['recipe'].items():
            self.formula_tree.insert(
                '',
                'end',
                values=(
                    sieve_range,
                    f"{data['percentage']:.2f}%",
                    f"{data['weight_kg']:.2f}"
                )
            )
        
        # اضافه کردن کل
        self.formula_tree.insert(
            '',
            'end',
            values=('کل', '100.00%', f"{final_recipe['total_weight']:.2f}"),
            tags=('total',)
        )
        
        self.formula_tree.tag_configure('total', background='#d5f4e6')
    
    def populate_json_text(self):
        """
        پر کردن متن JSON
        """
        self.json_text.delete(1.0, tk.END)
        
        json_str = self.calculator.export_to_json()
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
                initialfile=f"lab_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if filename:
                result = self.calculator.export_to_json(filename)
                messagebox.showinfo("موفقیت", result)
                self.update_status(f"✅ فایل ذخیره شد: {filename}")
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در صادرات:\n{str(e)}")
    
    def export_report(self):
        """
        صادرات گزارش متنی
        """
        if not self.calculator:
            messagebox.showwarning("هشدار", "ابتدا محاسبات را انجام دهید")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"lab_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                # ایجاد گزارش
                with open(filename, 'w', encoding='utf-8') as f:
                    # هدر
                    f.write("="*80 + "\n")
                    f.write("گزارش تجزیه تست آزمایشگاهی و فرمول بهینه\n")
                    f.write("="*80 + "\n\n")
                    f.write(f"تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # داده‌های تست
                    f.write("🧪 داده‌های تست آزمایشگاهی:\n")
                    f.write("-"*80 + "\n")
                    f.write(f"وزن کل تست: {self.calculator.test_weight} گرم\n\n")
                    
                    percentages = self.calculator.calculate_percentages()
                    f.write(f"{'بازه الک (mm)':<20} {'وزن (g)':<15} {'درصد':<15}\n")
                    f.write("-"*80 + "\n")
                    
                    for sieve_range in self.calculator.sieve_ranges:
                        name = sieve_range['name']
                        weight = self.calculator.test_results.get(name, 0)
                        percentage = percentages[name]
                        f.write(f"{name:<20} {weight:<15} {percentage:<15.2f}%\n")
                    
                    # فضای خالی
                    f.write("\n" + "="*80 + "\n")
                    f.write("📐 تجزیه فضای خالی بین سیلیکا:\n")
                    f.write("-"*80 + "\n")
                    
                    void_analysis = self.calculator.get_void_analysis()
                    f.write(f"{'بازه الک':<15} {'فضای خالی %':<20} {'چگالی Packing':<20}\n")
                    f.write("-"*80 + "\n")
                    
                    for item in void_analysis:
                        f.write(f"{item['sieve_range']:<15} {item['void_percentage']:<20.2f} {item['packing_density']:<20.4f}\n")
                    
                    # فرمول 100 کیلو
                    f.write("\n" + "="*80 + "\n")
                    f.write("🏭 فرمول برای 100 کیلو (بدون فضای خالی):\n")
                    f.write("-"*80 + "\n")
                    
                    final_recipe = self.calculator.get_final_recipe_100kg()
                    f.write(f"{'بازه الک':<20} {'درصد':<15} {'وزن (kg)':<20}\n")
                    f.write("-"*80 + "\n")
                    
                    for sieve_range, data in final_recipe['recipe'].items():
                        f.write(f"{sieve_range:<20} {data['percentage']:<15.2f}% {data['weight_kg']:<20.2f}\n")
                    
                    f.write("-"*80 + "\n")
                    f.write(f"{'کل':<20} {'100.00':<15}% {final_recipe['total_weight']:<20.2f}\n")
                    
                    f.write(f"\nیادداشت: {final_recipe['note']}\n")
                    f.write("\n" + "="*80 + "\n")
                
                messagebox.showinfo("موفقیت", f"✅ گزارش ذخیره شد:\n{filename}")
                self.update_status(f"✅ گزارش ذخیره شد: {filename}")
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در صادرات:\n{str(e)}")
    
    def clear_all(self):
        """
        پاک کردن تمام نتایج و ورودی‌ها
        """
        # پاک کردن ورودی‌ها
        self.test_weight_var.set(100)
        for key in self.sieve_vars:
            self.sieve_vars[key].set(0)
        
        # پاک کردن جداول
        for item in self.percentages_tree.get_children():
            self.percentages_tree.delete(item)
        
        for item in self.void_tree.get_children():
            self.void_tree.delete(item)
        
        for item in self.formula_tree.get_children():
            self.formula_tree.delete(item)
        
        self.json_text.delete(1.0, tk.END)
        
        self.calculator = None
        self.update_status("✨ نتایج و ورودی‌ها پاک شدند")


def main():
    """
    تابع اصلی برنامه
    """
    root = tk.Tk()
    app = LabTestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
