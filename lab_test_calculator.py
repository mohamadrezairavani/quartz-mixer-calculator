"""
محاسبه‌گر میکسر کوارتز با تست‌های آزمایشگاهی
Quartz Mixer Calculator with Lab Test Data

این برنامه داده‌های تست آزمایشگاهی را می‌گیرد و فرمول بهینه ایجاد می‌کند
"""

import json
from datetime import datetime


class LabTestQuartzCalculator:
    """
    محاسبه‌گر کوارتز بر اساس داده‌های تست آزمایشگاهی
    """
    
    def __init__(self):
        """
        مقداردهی اولیه
        """
        self.sieve_ranges = [
            {'name': '0-0.1', 'min': 0, 'max': 0.1},
            {'name': '0.1-0.2', 'min': 0.1, 'max': 0.2},
            {'name': '0.2-0.3', 'min': 0.2, 'max': 0.3},
            {'name': '0.3-0.4', 'min': 0.3, 'max': 0.4}
        ]
        
        self.test_results = {}  # نتایج تست
        self.test_weight = 0  # وزن کل تست
        
    def add_test_data(self, weight_grams, results_dict):
        """
        اضافه کردن داده‌های تست
        
        Args:
            weight_grams: وزن کل تست (گرم)
            results_dict: فرهنگ خروجی‌های تست
                مثال: {
                    '0-0.1': 10,
                    '0.1-0.2': 25,
                    '0.2-0.3': 35,
                    '0.3-0.4': 30
                }
        """
        self.test_weight = weight_grams
        self.test_results = results_dict
        
        # اعتبارسنجی
        total = sum(results_dict.values())
        if abs(total - weight_grams) > 0.1:
            raise ValueError(
                f"مجموع خروجی‌های تست ({total}g) با وزن کل ({weight_grams}g) مطابقت ندارد!"
            )
    
    def calculate_percentages(self):
        """
        محاسبه درصد هر بازه
        """
        percentages = {}
        for sieve_range in self.sieve_ranges:
            name = sieve_range['name']
            weight = self.test_results.get(name, 0)
            percentage = (weight / self.test_weight) * 100
            percentages[name] = round(percentage, 2)
        
        return percentages
    
    def calculate_void_fraction_for_range(self, sieve_range_name):
        """
        محاسبه فضای خالی برای بازه‌های مختلف
        
        از فرمول: Void Fraction = (d_max - d_avg) / d_max
        """
        # پیدا کردن بازه
        sieve_range = None
        for s_range in self.sieve_ranges:
            if s_range['name'] == sieve_range_name:
                sieve_range = s_range
                break
        
        if not sieve_range:
            return 0
        
        # میانگین اندازه الک در این بازه
        d_avg = (sieve_range['min'] + sieve_range['max']) / 2
        d_max = 0.4  # بیشترین اندازه الک
        
        # محاسبه فضای خالی
        if d_avg == 0:
            void_fraction = 0.40  # برای بازه 0-0.1
        else:
            void_fraction = (d_max - d_avg) / d_max
        
        return round(void_fraction, 4)
    
    def get_void_analysis(self):
        """
        تجزیه کامل فضای خالی برای تمام بازه‌ها
        """
        analysis = []
        percentages = self.calculate_percentages()
        
        for sieve_range in self.sieve_ranges:
            name = sieve_range['name']
            void_fraction = self.calculate_void_fraction_for_range(name)
            packing_density = 1 - void_fraction
            
            analysis.append({
                'sieve_range': name,
                'weight_grams': self.test_results.get(name, 0),
                'percentage': percentages[name],
                'void_fraction': void_fraction,
                'void_percentage': round(void_fraction * 100, 2),
                'packing_density': round(packing_density, 4)
            })
        
        return analysis
    
    def calculate_formula_100kg(self):
        """
        محاسبه فرمول برای 100 کیلو بدون فضای خالی
        
        فرمول: برای هر بازه الک، مقدار ماده = (درصد بازه × 100 کیلو) / (1 - فضای خالی)
        """
        analysis = self.get_void_analysis()
        formula = {}
        total_weight = 0
        
        for item in analysis:
            sieve_range = item['sieve_range']
            void_fraction = item['void_fraction']
            percentage = item['percentage']
            
            # محاسبه مقدار ماده برای پر کردن این بازه بدون فضای خالی
            # وزن لازم = (درصد × 100 کیلو) / (1 - فضای خالی)
            required_weight = (percentage * 100) / (1 - void_fraction) if void_fraction < 1 else (percentage * 100)
            
            formula[sieve_range] = {
                'percentage_from_test': percentage,
                'void_fraction': item['void_fraction'],
                'required_weight_kg': round(required_weight, 2),
                'packing_density': item['packing_density']
            }
            
            total_weight += required_weight
        
        return {
            'formula': formula,
            'total_weight_100kg': round(total_weight, 2),
            'adjustment_factor': round(100 / total_weight, 4) if total_weight > 0 else 1
        }
    
    def get_final_recipe_100kg(self):
        """
        دستور نهایی برای تهیه 100 کیلو
        """
        formula_data = self.calculate_formula_100kg()
        final_recipe = {}
        
        adjustment = formula_data['adjustment_factor']
        
        for sieve_range, data in formula_data['formula'].items():
            adjusted_weight = data['required_weight_kg'] * adjustment
            final_recipe[sieve_range] = {
                'percentage': round(data['percentage_from_test'], 2),
                'weight_kg': round(adjusted_weight, 2)
            }
        
        return {
            'total_weight': 100.0,
            'recipe': final_recipe,
            'note': 'وزن‌ها طوری محاسبه شده‌اند که هیچ فضای خالی بین سیلیکا نماند'
        }
    
    def print_complete_report(self):
        """
        چاپ گزارش کامل
        """
        print("\n" + "="*80)
        print("📊 گزارش تجزیه تست آزمایشگاهی و فرمول بهینه")
        print("="*80)
        
        # بخش داده‌های تست
        print(f"\n🧪 داده‌های تست آزمایشگاهی:")
        print("-"*80)
        print(f"وزن کل تست: {self.test_weight} گرم")
        
        print(f"\n{'بازه الک (mm)':<20} {'وزن (g)':<15} {'درصد':<15}")
        print("-"*80)
        
        percentages = self.calculate_percentages()
        for sieve_range in self.sieve_ranges:
            name = sieve_range['name']
            weight = self.test_results.get(name, 0)
            percentage = percentages[name]
            print(f"{name:<20} {weight:<15.2f} {percentage:<15.2f}%")
        
        # بخش تجزیه فضای خالی
        print("\n" + "="*80)
        print("📐 تجزیه فضای خالی بین سیلیکا:")
        print("="*80)
        
        analysis = self.get_void_analysis()
        print(f"\n{'بازه الک':<15} {'فضای خالی %':<20} {'چگالی Packing':<20}")
        print("-"*80)
        
        for item in analysis:
            print(f"{item['sieve_range']:<15} {item['void_percentage']:<20.2f} {item['packing_density']:<20.4f}")
        
        # بخش فرمول برای 100 کیلو
        print("\n" + "="*80)
        print("🏭 فرمول برای 100 کیلو (بدون فضای خالی):")
        print("="*80)
        
        final_recipe = self.get_final_recipe_100kg()
        
        print(f"\n{'بازه الک':<20} {'درصد':<15} {'وزن مورد نیاز (kg)':<20}")
        print("-"*80)
        
        for sieve_range, data in final_recipe['recipe'].items():
            print(f"{sieve_range:<20} {data['percentage']:<15.2f} {data['weight_kg']:<20.2f}")
        
        print("-"*80)
        print(f"{'کل':<20} {'100.00':<15} {final_recipe['total_weight']:<20.2f}")
        
        print(f"\n💡 یادداشت: {final_recipe['note']}")
        
        print("\n" + "="*80)
        print("✅ پایان گزارش")
        print("="*80 + "\n")
    
    def export_to_json(self, filename=None):
        """
        صادرات نتایج به JSON
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'test_data': {
                'total_weight_grams': self.test_weight,
                'results_by_sieve': self.test_results,
                'percentages': self.calculate_percentages()
            },
            'void_analysis': self.get_void_analysis(),
            'final_recipe_100kg': self.get_final_recipe_100kg()
        }
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return f"✅ فایل ذخیره شد: {filename}"
        
        return json.dumps(data, indent=2, ensure_ascii=False)


def example_usage():
    """
    مثال استفاده
    """
    print("\n" + "="*80)
    print("🔧 مثال استفاده از محاسبه‌گر تست آزمایشگاهی")
    print("="*80)
    
    # ایجاد محاسبه‌گر
    calculator = LabTestQuartzCalculator()
    
    # مثال: تست 100 گرمی رزین
    test_results = {
        '0-0.1': 10,      # 10 گرم
        '0.1-0.2': 25,    # 25 گرم
        '0.2-0.3': 35,    # 35 گرم
        '0.3-0.4': 30     # 30 گرم
    }
    
    calculator.add_test_data(weight_grams=100, results_dict=test_results)
    
    # نمایش گزارش
    calculator.print_complete_report()
    
    # صادرات به JSON
    print("\n📁 صادرات داده‌ها:")
    json_output = calculator.export_to_json('lab_test_results.json')
    print(json_output)


if __name__ == "__main__":
    example_usage()
