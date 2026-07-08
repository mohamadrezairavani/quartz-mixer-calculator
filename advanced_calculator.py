"""
محاسبه‌گر پیشرفته میکسر کوارتز
Advanced Quartz Mixer Calculator

این فایل نسخه پیشرفته‌تری از محاسبه‌گر است که امکان سفارشی‌سازی بیشتری دارد
"""

import json
from typing import Dict, List, Tuple
import csv
from datetime import datetime


class AdvancedQuartzCalculator:
    """
    محاسبه‌گر پیشرفته کوارتز
    """
    
    def __init__(self, batch_size=100, custom_materials=None, custom_sieves=None):
        """
        مقداردهی اولیه با امکان سفارشی‌سازی
        
        Args:
            batch_size: وزن کل دسته (کیلوگرم)
            custom_materials: فرهنگ سفارشی برای مواد
            custom_sieves: لیست سفارشی اندازه‌های الک
        """
        self.batch_size = batch_size
        
        # سفارشی‌سازی مواد
        self.materials = custom_materials or {
            'quartz': 70,
            'carbon_black': 15,
            'peroxide': 10,
            'resin': 5
        }
        
        # سفارشی‌سازی الک‌ها
        self.sieve_sizes = sorted(custom_sieves or [0, 0.1, 0.2, 0.3, 0.4])
        
        # اعتبارسنجی
        self._validate_materials()
        
    def _validate_materials(self):
        """
        اعتبارسنجی اینکه مجموع درصد‌ها 100 است
        """
        total = sum(self.materials.values())
        if abs(total - 100) > 0.01:
            raise ValueError(f"مجموع درصد مواد باید 100 باشد، اما {total} است")
    
    def calculate_void_fraction(self, sieve_size: float) -> float:
        """
        محاسبه فضای خالی
        """
        d_max = max(self.sieve_sizes) if self.sieve_sizes else 0.4
        if sieve_size == 0:
            return 0.4
        return (d_max - sieve_size) / d_max if d_max > 0 else 0
    
    def calculate_bulk_density(self, material_density: float, sieve_size: float) -> float:
        """
        محاسبه چگالی حجمی
        Bulk Density = Material Density × (1 - Void Fraction)
        """
        void_fraction = self.calculate_void_fraction(sieve_size)
        return material_density * (1 - void_fraction)
    
    def calculate_material_quantities(self) -> Dict[str, float]:
        """
        محاسبه مقدار مواد برای دسته
        """
        return {
            material: (percentage / 100) * self.batch_size
            for material, percentage in self.materials.items()
        }
    
    def get_detailed_analysis(self) -> Dict:
        """
        تجزیه تفصیلی کامل
        """
        materials = self.calculate_material_quantities()
        void_analysis = []
        
        for sieve_size in self.sieve_sizes:
            void_fraction = self.calculate_void_fraction(sieve_size)
            void_analysis.append({
                'sieve_size_mm': sieve_size,
                'void_fraction': void_fraction,
                'void_percentage': void_fraction * 100,
                'packing_density': 1 - void_fraction
            })
        
        return {
            'batch_size': self.batch_size,
            'timestamp': datetime.now().isoformat(),
            'materials': materials,
            'material_percentages': self.materials,
            'void_analysis': void_analysis,
            'total_weight': sum(materials.values())
        }
    
    def export_to_json(self, filename: str = None) -> str:
        """
        صادرات به JSON
        """
        data = self.get_detailed_analysis()
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return f"فایل ذخیره شد: {filename}"
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, filename: str = 'quartz_formula.csv'):
        """
        صادرات به CSV
        """
        data = self.get_detailed_analysis()
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            
            # رأس فایل
            writer.writerow(['گزارش میکسر کوارتز', '', ''])
            writer.writerow(['تاریخ', data['timestamp'], ''])
            writer.writerow(['وزن کل (کیلوگرم)', data['batch_size'], ''])
            writer.writerow(['', '', ''])
            
            # بخش مواد
            writer.writerow(['نام ماده', 'درصد', 'وزن (کیلوگرم)'])
            for material, quantity in data['materials'].items():
                percentage = data['material_percentages'][material]
                writer.writerow([material, f"{percentage}%", f"{quantity:.2f}"])
            
            writer.writerow(['کل', '100%', f"{data['total_weight']:.2f}"])
            writer.writerow(['', '', ''])
            
            # بخش تجزیه فضای خالی
            writer.writerow(['اندازه الک (mm)', 'فضای خالی (%)', 'چگالی Packing'])
            for item in data['void_analysis']:
                writer.writerow([
                    item['sieve_size_mm'],
                    f"{item['void_percentage']:.2f}",
                    f"{item['packing_density']:.4f}"
                ])
        
        return f"فایل ذخیره شد: {filename}"
    
    def print_comprehensive_report(self):
        """
        چاپ گزارش جامع
        """
        data = self.get_detailed_analysis()
        
        print("\n" + "="*80)
        print("📊 گزارش جامع محاسبه‌گر میکسر کوارتز - Advanced Quartz Mixer Report")
        print("="*80)
        
        print(f"\n⏰ تاریخ و زمان: {data['timestamp']}")
        print(f"📦 وزن کل دسته: {data['batch_size']} کیلوگرم")
        
        # بخش مواد
        print("\n" + "-"*80)
        print("📋 ترکیب مواد برای 100 کیلو:")
        print("-"*80)
        print(f"{'نام ماده':<30} {'درصد':<15} {'وزن (کیلوگرم)':<20}")
        print("-"*80)
        
        for material, quantity in data['materials'].items():
            percentage = data['material_percentages'][material]
            print(f"{material:<30} {percentage:>6}% {quantity:>18.2f} kg")
        
        print("-"*80)
        print(f"{'کل':<30} {'100':>6}% {data['total_weight']:>18.2f} kg")
        
        # بخش فضای خالی
        print("\n" + "-"*80)
        print("🔍 تجزیه فضای خالی بین دانه‌بندی:")
        print("-"*80)
        print(f"{'اندازه الک (mm)':<20} {'فضای خالی (%)':<20} {'چگالی Packing':<20}")
        print("-"*80)
        
        for item in data['void_analysis']:
            print(f"{item['sieve_size_mm']:<20.2f} {item['void_percentage']:>18.2f}% {item['packing_density']:>18.4f}")
        
        print("\n" + "="*80)
        print("✅ پایان گزارش")
        print("="*80 + "\n")


def example_usage():
    """
    مثال‌های استفاده
    """
    
    print("\n" + "="*80)
    print("🔧 مثال‌های استفاده از محاسبه‌گر پیشرفته")
    print("="*80)
    
    # مثال 1: محاسبه پیش‌فرض
    print("\n📌 مثال 1: محاسبه با تنظیمات پیش‌فرض")
    calculator1 = AdvancedQuartzCalculator(batch_size=100)
    calculator1.print_comprehensive_report()
    
    # مثال 2: سفارشی‌سازی مواد
    print("\n📌 مثال 2: محاسبه با مواد سفارشی")
    custom_materials = {
        'quartz': 75,
        'carbon_black': 12,
        'peroxide': 8,
        'resin': 5
    }
    calculator2 = AdvancedQuartzCalculator(
        batch_size=100,
        custom_materials=custom_materials
    )
    calculator2.print_comprehensive_report()
    
    # مثال 3: صادرات به فرمت‌های مختلف
    print("\n📌 مثال 3: صادرات داده‌ها")
    
    # صادرات به JSON
    json_result = calculator1.export_to_json('quartz_formula.json')
    print(json_result)
    
    # صادرات به CSV
    csv_result = calculator1.export_to_csv('quartz_formula.csv')
    print(csv_result)
    
    print("\n✅ تمام مثال‌ها اجرا شدند!")


if __name__ == "__main__":
    example_usage()
