"""
پروژه محاسبه‌گر میکسر کوارتز
Quartz Mixer Calculator Project

این برنامه فضای خالی بین دانه‌بندی را محاسبه کرده و مواد را برای 100 کیلو ترکیب می‌کند
"""

class QuartzMixerCalculator:
    """
    کلاس محاسبه‌گر میکسر کوارتز
    محاسبه فضای خالی بین دانه‌بندی و ترکیب مواد
    """
    
    def __init__(self, batch_size=100):
        """
        مقداردهی اولیه
        batch_size: وزن کل دسته (کیلوگرم)
        """
        self.batch_size = batch_size
        self.sieve_sizes = [0, 0.1, 0.2, 0.3, 0.4]  # میلی‌متر
        
        # درصد مواد اولیه
        self.materials = {
            'quartz': 70,      # 70% کوارتز
            'carbon_black': 15, # 15% دوده
            'peroxide': 10,     # 10% پراکسید
            'resin': 5          # 5% رزین
        }
        
    def calculate_void_fraction(self, sieve_size):
        """
        محاسبه فضای خالی بین دانه‌بندی
        بر اساس اندازه الک (سیو)
        
        فرمول: Void Fraction = (d_max - d) / d_max
        """
        d_max = max(self.sieve_sizes)
        if sieve_size == 0:
            void_fraction = 0.4  # مقدار پیش‌فرض برای اندازه صفر
        else:
            void_fraction = (d_max - sieve_size) / d_max
        
        return void_fraction
    
    def calculate_packing_density(self, sieve_size):
        """
        محاسبه چگالی پacking (چگالی انباشتگی)
        Packing Density = 1 - Void Fraction
        """
        void_fraction = self.calculate_void_fraction(sieve_size)
        packing_density = 1 - void_fraction
        return packing_density
    
    def calculate_material_quantities(self):
        """
        محاسبه مقدار هر ماده برای 100 کیلو
        Returns: dict with quantities in kg
        """
        result = {}
        for material, percentage in self.materials.items():
            quantity = (percentage / 100) * self.batch_size
            result[material] = quantity
        
        return result
    
    def calculate_void_for_all_sieves(self):
        """
        محاسبه فضای خالی برای تمام اندازه‌های الک
        """
        results = []
        for sieve_size in self.sieve_sizes:
            void_fraction = self.calculate_void_fraction(sieve_size)
            packing_density = self.calculate_packing_density(sieve_size)
            
            results.append({
                'sieve_size_mm': sieve_size,
                'void_fraction': round(void_fraction, 4),
                'packing_density': round(packing_density, 4),
                'void_percentage': round(void_fraction * 100, 2)
            })
        
        return results
    
    def generate_formula(self):
        """
        تولید فرمول کامل برای 100 کیلو سنگ کوارتز
        """
        materials = self.calculate_material_quantities()
        void_data = self.calculate_void_for_all_sieves()
        
        formula = {
            'batch_size_kg': self.batch_size,
            'materials': materials,
            'void_analysis': void_data,
            'total_weight': sum(materials.values())
        }
        
        return formula
    
    def print_report(self):
        """
        چاپ گزارش کامل
        """
        print("=" * 70)
        print("گزارش محاسبه‌گر میکسر کوارتز - Quartz Mixer Report")
        print("=" * 70)
        
        # بخش تجزیه فضای خالی
        print("\n📊 تجزیه فضای خالی بین دانه‌بندی")
        print("-" * 70)
        print(f"{'اندازه الک (mm)':<20} {'فضای خالی':<20} {'چگالی Packing':<20}")
        print("-" * 70)
        
        void_data = self.calculate_void_for_all_sieves()
        for item in void_data:
            print(f"{item['sieve_size_mm']:<20} {item['void_percentage']:.2f}%{'':<14} {item['packing_density']:.4f}")
        
        # بخش فرمول مواد
        print("\n" + "=" * 70)
        print("📋 فرمول ترکیب مواد برای 100 کیلو")
        print("=" * 70)
        
        materials = self.calculate_material_quantities()
        
        print(f"\n{'نام ماده':<30} {'درصد':<15} {'وزن (کیلوگرم)':<15}")
        print("-" * 70)
        
        material_names = {
            'quartz': 'کوارتز (Quartz)',
            'carbon_black': 'دوده (Carbon Black)',
            'peroxide': 'پراکسید (Peroxide)',
            'resin': 'رزین (Resin)'
        }
        
        for material, quantity in materials.items():
            percentage = self.materials[material]
            name = material_names[material]
            print(f"{name:<30} {percentage:<15}% {quantity:<15.2f} kg")
        
        print("-" * 70)
        print(f"{'کل':<30} {'100':<15}% {sum(materials.values()):<15.2f} kg")
        
        print("\n" + "=" * 70)
        print("✅ پایان گزارش")
        print("=" * 70)


def main():
    """
    تابع اصلی برنامه
    """
    # ایجاد محاسبه‌گر
    calculator = QuartzMixerCalculator(batch_size=100)
    
    # چاپ گزارش کامل
    calculator.print_report()
    
    # نمایش داده‌های JSON برای استفاده در برنامه‌های دیگر
    print("\n📁 داده‌های فرمول (JSON):")
    print("-" * 70)
    
    import json
    formula = calculator.generate_formula()
    print(json.dumps(formula, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
