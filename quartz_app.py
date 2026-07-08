"""
رابط کاربری گرافیکی یکپارچه برای محاسبه‌گر کوارتز
Unified GUI for Quartz Mixer Calculator

رابط حرفه‌ای و بهینه شده با تمام ویژگی‌ها در یک جا
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
from optimized_calculator import QuartzFormulaCalculator, QuartzMaterial


class UnifiedQuartzGUI:
    """رابط کاربری یکپارچه برای محاسبه‌گر کوارتز"""
    
    def __init__(self, root):
        """مقداردهی اولیه"""
        self.root = root
        self.root.title("محاسبه‌گر کوارتز | Quartz Mixer Calculator")
        self.root.geometry("1400x850")
        self.root.resizable(True, True)
        
        # رنگ‌ها
        self.header_color = "#1a5f7a"
        self.bg_color = "#f5f5f5"
        self.accent_color = "#2196F3"
        self.success_color = "#27ae60"
        
        self.root.configure(bg=self.bg_color)
        
        # محاسبه‌گر
        self.calculator = QuartzFormulaCalculator()
        
        # متغیرها
        self.test_weight_var = tk.IntVar(value=100)
        self.target_weight_var = tk.IntVar(value=100)
        
        self.sieve_vars = {
            '0-0.1': tk.IntVar(value=10),
            '0.1-0.2': tk.IntVar(value=25),
            '0.2-0.3': tk.IntVar(value=35),
            '0.3-0.4': tk.IntVar(value=30)
        }
        
        self.material_vars = {}
        for name, material in self.calculator.materials.items():
            self.material_vars[name] = tk.DoubleVar(value=material.percentage)
        
        self.create_widgets()
    
    def create_widgets(self):
        """ایجاد رابط کاربری"""
        # هدر
        self.create_header()
        
        # فریم اصلی
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ستون چپ - ورودی‌ها
        self.create_left_panel(main_frame)
        
        # ستون راست - نتایج
        self.create_right_panel(main_frame)
        
        # فریم پایین
        self.create_footer()
    
    def create_header(self):
        """ایجاد هدر"""
        header_frame = tk.Frame(self.root, bg=self.header_color, height=90)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(
            header_frame,
            text="🏭 محاسبه‌گر سنگ مهندسی کوارتز",
            font=("Arial", 20, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            header_frame,
            text="Quartz Engineering Stone Calculator | محاسبه فرمول دقیق با تصحیح فضای خالی",
            font=("Arial", 11),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        subtitle.pack(pady=5)
    
    def create_left_panel(self, parent):
        """ایجاد پنل چپ - ورودی‌ها"""
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)
        
        # ⚙️ پارامترهای تست
        test_frame = ttk.LabelFrame(left_frame, text="⚙️ پارامترهای تست", padding=15)
        test_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(test_frame, text="وزن تست (گرم):").pack(anchor=tk.W, pady=(0, 5))
        ttk.Spinbox(test_frame, from_=1, to=500, textvariable=self.test_weight_var, width=15).pack(anchor=tk.W, pady=(0, 15))
        
        # 🎯 وزن تولید
        prod_frame = ttk.LabelFrame(left_frame, text="🎯 وزن تولید", padding=15)
        prod_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(prod_frame, text="وزن مورد نظر (کیلو):").pack(anchor=tk.W, pady=(0, 5))
        ttk.Spinbox(prod_frame, from_=1, to=1000, textvariable=self.target_weight_var, width=15).pack(anchor=tk.W, pady=(0, 15))
        
        # 🧪 خروجی‌های تست
        sieve_frame = ttk.LabelFrame(left_frame, text="🧪 خروجی‌های الک (گرم)", padding=15)
        sieve_frame.pack(fill=tk.X, pady=10)
        
        sieve_labels = [
            ('0-0.1', '0-0.1 mm'),
            ('0.1-0.2', '0.1-0.2 mm'),
            ('0.2-0.3', '0.2-0.3 mm'),
            ('0.3-0.4', '0.3-0.4 mm')
        ]
        
        for key, label in sieve_labels:
            row = ttk.Frame(sieve_frame)
            row.pack(fill=tk.X, pady=5)
            ttk.Label(row, text=label, width=10).pack(side=tk.LEFT)
            ttk.Spinbox(row, from_=0, to=500, textvariable=self.sieve_vars[key], width=12).pack(side=tk.LEFT)
        
        # 📊 درصد‌های مواد
        mat_frame = ttk.LabelFrame(left_frame, text="📊 درصد مواد", padding=15)
        mat_frame.pack(fill=tk.X, pady=10)
        
        material_info = [
            ('quartz', 'سیلیکا/کوارتز'),
            ('resin', 'رزین'),
            ('pigment', 'پیگمنت'),
            ('carbon_black', 'دوده'),
            ('peroxide', 'پراکسید')
        ]
        
        for key, label in material_info:
            row = ttk.Frame(mat_frame)
            row.pack(fill=tk.X, pady=5)
            ttk.Label(row, text=label, width=12).pack(side=tk.LEFT)
            ttk.Spinbox(
                row,
                from_=0,
                to=100,
                textvariable=self.material_vars[key],
                width=8
            ).pack(side=tk.LEFT, padx=5)
            ttk.Label(row, text="%", width=2).pack(side=tk.LEFT)
        
        # دکمه‌ها
        button_frame = tk.Frame(left_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=20)
        
        calc_btn = tk.Button(
            button_frame,
            text="📐 محاسبه",
            command=self.calculate,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12
        )
        calc_btn.pack(fill=tk.X, pady=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ پاک کردن",
            command=self.clear_all,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        clear_btn.pack(fill=tk.X, pady=5)
    
    def create_right_panel(self, parent):
        """ایجاد پنل راست - نتایج"""
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Notebook برای تب‌ها
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # تب 1: فرمول نهایی
        formula_frame = ttk.Frame(notebook)
        notebook.add(formula_frame, text="🏭 فرمول نهایی")
        self.create_formula_tree(formula_frame)
        
        # تب 2: فضای خالی
        void_frame = ttk.Frame(notebook)
        notebook.add(void_frame, text="📐 فضای خالی")
        self.create_void_tree(void_frame)
        
        # تب 3: گزارش متنی
        report_frame = ttk.Frame(notebook)
        notebook.add(report_frame, text="📄 گزارش")
        self.create_report_text(report_frame)
        
        # دکمه‌های صادرات
        export_frame = tk.Frame(right_frame, bg=self.bg_color)
        export_frame.pack(fill=tk.X, pady=10)
        
        json_btn = tk.Button(
            export_frame,
            text="💾 صادرات JSON",
            command=self.export_json,
            bg=self.success_color,
            fg="white",
            padx=15,
            pady=8
        )
        json_btn.pack(side=tk.LEFT, padx=5)
        
        report_btn = tk.Button(
            export_frame,
            text="📄 صادرات گزارش",
            command=self.export_report,
            bg="#e67e22",
            fg="white",
            padx=15,
            pady=8
        )
        report_btn.pack(side=tk.LEFT, padx=5)
    
    def create_formula_tree(self, parent):
        """ایجاد جدول فرمول"""
        scrollbar = ttk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.formula_tree = ttk.Treeview(
            parent,
            columns=('Material', 'Percent', 'Before', 'After'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.formula_tree.yview)
        
        self.formula_tree.column('#0', width=0)
        self.formula_tree.column('Material', width=150)
        self.formula_tree.column('Percent', width=100)
        self.formula_tree.column('Before', width=120)
        self.formula_tree.column('After', width=120)
        
        self.formula_tree.heading('#0', text='')
        self.formula_tree.heading('Material', text='نام ماده')
        self.formula_tree.heading('Percent', text='درصد')
        self.formula_tree.heading('Before', text='قبل تصحیح (kg)')
        self.formula_tree.heading('After', text='بعد تصحیح (kg)')
        
        self.formula_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_void_tree(self, parent):
        """ایجاد جدول فضای خالی"""
        scrollbar = ttk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.void_tree = ttk.Treeview(
            parent,
            columns=('Range', 'Percent', 'Void', 'Packing'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.void_tree.yview)
        
        self.void_tree.column('#0', width=0)
        self.void_tree.column('Range', width=100)
        self.void_tree.column('Percent', width=100)
        self.void_tree.column('Void', width=120)
        self.void_tree.column('Packing', width=120)
        
        self.void_tree.heading('#0', text='')
        self.void_tree.heading('Range', text='بازه (mm)')
        self.void_tree.heading('Percent', text='درصد (%)')
        self.void_tree.heading('Void', text='فضای خالی (%)')
        self.void_tree.heading('Packing', text='چگالی Packing')
        
        self.void_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_report_text(self, parent):
        """ایجاد متن گزارش"""
        scrollbar = ttk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.report_text = tk.Text(
            parent,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        scrollbar.config(command=self.report_text.yview)
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_footer(self):
        """ایجاد فریم پایین"""
        footer_frame = tk.Frame(self.root, bg=self.header_color, height=40)
        footer_frame.pack(fill=tk.X, padx=0, pady=0, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            footer_frame,
            text="آماده برای محاسبه...",
            font=("Arial", 10),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        self.status_label.pack(pady=8)
    
    def update_status(self, message):
        """بروزرسانی وضعیت"""
        self.status_label.config(text=message)
        self.root.update()
    
    def calculate(self):
        """انجام محاسبات"""
        try:
            self.update_status("🔄 در حال محاسبه...")
            
            # گرفتن داده‌های ورودی
            test_weight = self.test_weight_var.get()
            target_weight = self.target_weight_var.get()
            
            # تجمیع داده‌های تست
            test_results = {key: var.get() for key, var in self.sieve_vars.items()}
            total_test = sum(test_results.values())
            
            # اعتبارسنجی
            if test_weight <= 0 or target_weight <= 0:
                messagebox.showerror("خطا", "وزن باید بیشتر از صفر باشد")
                self.update_status("❌ خطا: وزن نامعتبر")
                return
            
            if total_test != test_weight:
                messagebox.showerror(
                    "خطا",
                    f"مجموع خروجی‌های الک ({total_test}g) ≠ وزن کل ({test_weight}g)"
                )
                self.update_status("❌ خطا: عدم تطابق وزن")
                return
            
            # تنظیم درصد‌ها
            total_percent = sum(self.material_vars[name].get() for name in self.calculator.materials)
            if abs(total_percent - 100) > 0.01:
                messagebox.showerror("خطا", f"مجموع درصد‌ها باید 100 باشد، فعلاً {total_percent:.2f}%")
                self.update_status("❌ خطا: درصد‌ها معتبر نیستند")
                return
            
            # تنظیم محاسبه‌گر
            self.calculator.set_test_data(test_weight, test_results)
            self.calculator.target_production = target_weight
            
            for name, var in self.material_vars.items():
                self.calculator.set_material_percentage(name, var.get())
            
            # محاسبه
            report = self.calculator.get_detailed_report()
            
            # نمایش نتایج
            self.populate_formula_tree(report)
            self.populate_void_tree(report)
            self.populate_report_text(report)
            
            self.update_status("✅ محاسبات با موفقیت انجام شد")
            messagebox.showinfo("موفقیت", "✅ محاسبات تکمیل شد!")
            
        except Exception as e:
            messagebox.showerror("خطا", f"خطا: {str(e)}")
            self.update_status(f"❌ خطا: {str(e)}")
    
    def populate_formula_tree(self, report):
        """پر کردن جدول فرمول"""
        for item in self.formula_tree.get_children():
            self.formula_tree.delete(item)
        
        materials = report['formula_100kg']['materials']
        
        for mat_name, data in materials.items():
            self.formula_tree.insert('', 'end', values=(
                data['name_fa'],
                f"{data['percentage']:.2f}%",
                f"{data['quantity_before_adjustment']:.2f}",
                f"{data['quantity_after_adjustment']:.2f}"
            ))
        
        self.formula_tree.insert('', 'end', values=(
            'کل',
            '100.00%',
            f"{sum(m['quantity_before_adjustment'] for m in materials.values()):.2f}",
            f"{report['formula_100kg']['total_weight']:.2f}"
        ), tags=('total',))
        
        self.formula_tree.tag_configure('total', background='#d5f4e6')
    
    def populate_void_tree(self, report):
        """پر کردن جدول فضای خالی"""
        for item in self.void_tree.get_children():
            self.void_tree.delete(item)
        
        for item in report['void_analysis']:
            self.void_tree.insert('', 'end', values=(
                item['sieve_range'],
                f"{item['percentage']:.2f}%",
                f"{item['void_percentage']:.2f}%",
                f"{item['packing_density']:.4f}"
            ))
    
    def populate_report_text(self, report):
        """پر کردن متن گزارش"""
        self.report_text.delete(1.0, tk.END)
        
        text = f"""
{'='*80}
📊 گزارش جامع فرمول سنگ کوارتز مهندسی
{'='*80}

🎯 پارامترهای محاسبه:
- وزن کل تست: {report['test_data']['total_test_weight']} گرم
- وزن تولید مورد نظر: {report['formula_100kg']['total_production']} کیلو
- فاکتور تصحیح: {report['formula_100kg']['adjustment_factor']}

{'='*80}
🏭 فرمول نهایی (با تصحیح فضای خالی):
{'='*80}

{'نام ماده':<25} {'درصد':<12} {'قبل (kg)':<15} {'بعد (kg)':<15}
{'-'*70}
"""
        
        materials = report['formula_100kg']['materials']
        for mat_name, data in materials.items():
            text += f"{data['name_fa']:<25} {data['percentage']:<12.2f}% {data['quantity_before_adjustment']:<15.2f} {data['quantity_after_adjustment']:<15.2f}\n"
        
        total_before = sum(m['quantity_before_adjustment'] for m in materials.values())
        total_after = report['formula_100kg']['total_weight']
        
        text += f"{'-'*70}\n"
        text += f"{'کل':<25} {'100':<12}% {total_before:<15.2f} {total_after:<15.2f}\n"
        
        text += f"\n{'='*80}\n"
        text += "✅ این فرمول بدون فضای خالی بین ذرات است\n"
        text += f"{'='*80}\n"
        
        self.report_text.insert(1.0, text)
    
    def export_json(self):
        """صادرات JSON"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON", "*.json"), ("All", "*.*")],
                initialfile=f"quartz_formula_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if filename:
                self.calculator.export_json(filename)
                messagebox.showinfo("موفقیت", f"✅ فایل ذخیره شد:\n{filename}")
                self.update_status(f"✅ JSON ذخیره شد")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا: {str(e)}")
    
    def export_report(self):
        """صادرات گزارش"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text", "*.txt"), ("All", "*.*")],
                initialfile=f"quartz_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.report_text.get(1.0, tk.END))
                messagebox.showinfo("موفقیت", f"✅ گزارش ذخیره شد:\n{filename}")
                self.update_status(f"✅ گزارش ذخیره شد")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا: {str(e)}")
    
    def clear_all(self):
        """پاک کردن همه‌چیز"""
        for item in self.formula_tree.get_children():
            self.formula_tree.delete(item)
        for item in self.void_tree.get_children():
            self.void_tree.delete(item)
        self.report_text.delete(1.0, tk.END)
        self.update_status("✨ نتایج پاک شدند")


def main():
    """برنامه اصلی"""
    root = tk.Tk()
    app = UnifiedQuartzGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
