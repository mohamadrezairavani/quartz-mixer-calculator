"""
سیستم محاسبه‌گر میکسر کوارتز - نسخه بهینه شده
Optimized Quartz Mixer Calculator System

سیستم جامع برای محاسبه فرمول تولید سنگ مهندسی کوارتز
"""

from typing import Dict, List, Tuple
import json
from datetime import datetime


class QuartzMaterial:
    """کلاس برای نمایندگی یک ماده"""
    
    def __init__(self, name: str, name_fa: str, density: float, default_percentage: float = 0):
        """
        Args:
            name: نام انگلیسی ماده
            name_fa: نام فارسی ماده
            density: چگالی ماده (g/cm³)
            default_percentage: درصد پیش‌فرض
        """
        self.name = name
        self.name_fa = name_fa
        self.density = density
        self.default_percentage = default_percentage
        self.percentage = default_percentage
    
    def set_percentage(self, percentage: float):
        """تنظیم درصد ماده"""
        self.percentage = max(0, min(100, percentage))
    
    def calculate_quantity(self, total_weight: float) -> float:
        """محاسبه مقدار ماده برای وزن کلی"""
        return (self.percentage / 100) * total_weight


class VoidAnalyzer:
    """کلاس برای تجزیه فضای خالی"""
    
    def __init__(self, sieve_data: Dict[str, float]):
        """
        Args:
            sieve_data: فرهنگ بازه‌های الک و درصد آن‌ها
                مثال: {'0-0.1': 10.0, '0.1-0.2': 25.0, ...}
        """
        self.sieve_ranges = [
            {'min': 0.0, 'max': 0.1, 'name': '0-0.1'},
            {'min': 0.1, 'max': 0.2, 'name': '0.1-0.2'},
            {'min': 0.2, 'max': 0.3, 'name': '0.2-0.3'},
            {'min': 0.3, 'max': 0.4, 'name': '0.3-0.4'}
        ]
        self.sieve_data = sieve_data
        self.max_sieve = 0.4
    
    def calculate_void_fraction(self, sieve_range_name: str) -> float:
        """محاسبه فضای خالی برای یک بازه"""
        for sieve in self.sieve_ranges:
            if sieve['name'] == sieve_range_name:
                d_avg = (sieve['min'] + sieve['max']) / 2
                if d_avg == 0:
                    return 0.40
                void_fraction = (self.max_sieve - d_avg) / self.max_sieve
                return max(0, min(1, void_fraction))
        return 0
    
    def get_comprehensive_analysis(self) -> List[Dict]:
        """تجزیه جامع فضای خالی"""
        analysis = []
        
        for range_name, percentage in self.sieve_data.items():
            void_fraction = self.calculate_void_fraction(range_name)
            packing_density = 1 - void_fraction
            
            analysis.append({
                'sieve_range': range_name,
                'percentage': percentage,
                'void_fraction': round(void_fraction, 4),
                'void_percentage': round(void_fraction * 100, 2),
                'packing_density': round(packing_density, 4)
            })
        
        return analysis


class QuartzFormulaCalculator:
    """محاسبه‌گر فرمول کوارتز - نسخه بهینه شده"""
    
    def __init__(self):
        """مقداردهی اولیه"""
        # تعریف مواد
        self.materials = {
            'quartz': QuartzMaterial('Quartz', 'سیلیکا/کوارتز', 2.65, 60),
            'resin': QuartzMaterial('Resin', 'رزین (Resin)', 1.2, 15),
            'pigment': QuartzMaterial('Pigment', 'پیگمنت (Pigment)', 1.5, 15),
            'carbon_black': QuartzMaterial('Carbon Black', 'دوده (Carbon Black)', 1.8, 8),
            'peroxide': QuartzMaterial('Peroxide', 'پراکسید (Peroxide)', 1.4, 2)
        }
        
        # پارامترهای پیش‌فرض
        self.test_weight = 100  # گرم
        self.target_production = 100  # کیلو
        
        # داده‌های تست
        self.test_results = None
        self.void_analyzer = None
    
    def set_test_data(self, test_weight: float, results: Dict[str, float]):
        """تنظیم داده‌های تست"""
        self.test_weight = test_weight
        self.test_results = results
        self.void_analyzer = VoidAnalyzer(results)
    
    def set_material_percentage(self, material_name: str, percentage: float):
        """تنظیم درصد یک ماده"""
        if material_name in self.materials:
            self.materials[material_name].set_percentage(percentage)
    
    def get_all_material_percentages(self) -> Dict[str, float]:
        """گرفتن تمام درصد‌های مواد"""
        return {name: mat.percentage for name, mat in self.materials.items()}
    
    def validate_percentages(self) -> Tuple[bool, str]:
        """اعتبارسنجی درصد‌ها"""
        total = sum(mat.percentage for mat in self.materials.values())
        
        if abs(total - 100) > 0.01:
            return False, f"مجموع درصد‌ها باید 100 باشد، فعلاً {total:.2f}%"
        
        return True, "✅ درصد‌ها معتبر هستند"
    
    def calculate_material_quantities(self, total_weight: float) -> Dict[str, float]:
        """محاسبه مقدار مواد برای وزن کلی"""
        quantities = {}
        
        for name, material in self.materials.items():
            quantity = material.calculate_quantity(total_weight)
            quantities[name] = round(quantity, 2)
        
        return quantities
    
    def calculate_formula_100kg(self) -> Dict:
        """محاسبه فرمول برای 100 کیلو"""
        is_valid, message = self.validate_percentages()
        
        if not is_valid:
            raise ValueError(message)
        
        # محاسبه مقدار مواد اولیه
        materials_qty = self.calculate_material_quantities(self.target_production)
        
        # تجزیه فضای خالی
        void_analysis = self.void_analyzer.get_comprehensive_analysis() if self.void_analyzer else []
        
        # محاسبه فاکتور تصحیح برای فضای خالی
        total_void_percentage = sum(item['void_percentage'] for item in void_analysis) / len(void_analysis) if void_analysis else 0
        
        # تصحیح برای حذف فضای خالی
        void_factor = 1 + (total_void_percentage / 100) if total_void_percentage > 0 else 1
        
        return {
            'target_production': self.target_production,
            'materials': materials_qty,
            'material_percentages': self.get_all_material_percentages(),
            'void_analysis': void_analysis,
            'void_factor': round(void_factor, 4),
            'total_weight_before_adjustment': sum(materials_qty.values()),
            'total_weight_after_adjustment': round(sum(materials_qty.values()) * void_factor, 2)
        }
    
    def get_detailed_report(self) -> Dict:
        """گزارش دقیق"""
        formula = self.calculate_formula_100kg()
        
        adjusted_materials = {}
        adjustment_factor = formula['void_factor']
        
        for material_name, quantity in formula['materials'].items():
            adjusted_qty = quantity * adjustment_factor
            
            material = self.materials[material_name]
            adjusted_materials[material_name] = {
                'name_fa': material.name_fa,
                'percentage': round(material.percentage, 2),
                'quantity_before_adjustment': round(quantity, 2),
                'quantity_after_adjustment': round(adjusted_qty, 2),
                'density': material.density
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'test_data': {
                'total_test_weight': self.test_weight,
                'test_results': self.test_results if self.test_results else {}
            },
            'formula_100kg': {
                'total_production': self.target_production,
                'adjustment_factor': adjustment_factor,
                'materials': adjusted_materials,
                'total_weight': round(sum(m['quantity_after_adjustment'] for m in adjusted_materials.values()), 2)
            },
            'void_analysis': formula['void_analysis']
        }
    
    def print_complete_report(self):
        """چاپ گزارش کامل"""
        report = self.get_detailed_report()
        materials_data = report['formula_100kg']['materials']
        
        print("\n" + "="*100)
        print("🏭 گزارش جامع فرمول تولید سنگ کوارتز مهندسی")
        print("="*100)
        
        # بخش داده‌های تست
        if self.test_results:
            print(f"\n🧪 داده‌های تست آزمایشگاهی:")
            print("-"*100)
            print(f"وزن کل تست: {self.test_weight} گرم")
            print(f"\nبازه الک (mm)      وزن (g)        درصد")
            print("-"*100)
            
            for range_name, weight in self.test_results.items():
                percentage = (weight / self.test_weight) * 100
                print(f"{range_name:<20} {weight:<15} {percentage:<15.2f}%")
        
        # بخش فضای خالی
        if report['void_analysis']:
            print("\n" + "="*100)
            print("📐 تجزیه فضای خالی بین ذرات:")
            print("-"*100)
            print(f"{'بازه الک':<20} {'درصد':<15} {'فضای خالی (%)':<20} {'چگالی Packing':<20}")
            print("-"*100)
            
            for item in report['void_analysis']:
                print(f"{item['sieve_range']:<20} {item['percentage']:<15.2f} {item['void_percentage']:<20.2f} {item['packing_density']:<20.4f}")
        
        # بخش فرمول نهایی
        print("\n" + "="*100)
        print("🏭 فرمول نهایی برای 100 کیلو (با تصحیح فضای خالی):")
        print("="*100)
        
        print(f"\nفاکتور تصحیح: {report['formula_100kg']['adjustment_factor']}")
        print(f"\n{'نام ماده':<25} {'درصد':<12} {'قبل تصحیح (kg)':<18} {'بعد تصحیح (kg)':<18}")
        print("-"*100)
        
        for material_name, data in materials_data.items():
            print(f"{data['name_fa']:<25} {data['percentage']:<12.2f}% {data['quantity_before_adjustment']:<18.2f} {data['quantity_after_adjustment']:<18.2f}")
        
        print("-"*100)
        print(f"{'کل':<25} {'100':<12}% {sum(m['quantity_before_adjustment'] for m in materials_data.values()):<18.2f} {report['formula_100kg']['total_weight']:<18.2f}")
        
        print("\n" + "="*100)
        print("✅ پایان گزارش")
        print("="*100 + "\n")
    
    def export_json(self, filename: str = None) -> str:
        """صادرات به JSON"""
        report = self.get_detailed_report()
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return f"✅ فایل ذخیره شد: {filename}"
        
        return json.dumps(report, indent=2, ensure_ascii=False)


# مثال استفاده
def example_usage():
    """مثال استفاده"""
    
    print("\n" + "="*100)
    print("📌 مثال استفاده از محاسبه‌گر کوارتز بهینه شده")
    print("="*100)
    
    # ایجاد محاسبه‌گر
    calculator = QuartzFormulaCalculator()
    
    # تنظیم داده‌های تست (100 گرم رزین)
    test_data = {
        '0-0.1': 10,
        '0.1-0.2': 25,
        '0.2-0.3': 35,
        '0.3-0.4': 30
    }
    
    calculator.set_test_data(weight_grams=100, results=test_data)
    
    # تنظیم درصد‌های مواد (اختیاری - می‌توان پیش‌فرض را استفاده کرد)
    calculator.set_material_percentage('quartz', 60)
    calculator.set_material_percentage('resin', 15)
    calculator.set_material_percentage('pigment', 15)
    calculator.set_material_percentage('carbon_black', 8)
    calculator.set_material_percentage('peroxide', 2)
    
    # نمایش گزارش
    calculator.print_complete_report()
    
    # صادرات JSON
    print("\n📁 صادرات داده‌ها:")
    print(calculator.export_json('quartz_formula.json'))


if __name__ == "__main__":
    example_usage()
