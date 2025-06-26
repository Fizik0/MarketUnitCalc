"""
Тесты для модуля calculations.py
"""

import unittest
from utils.calculations import UnitEconomicsCalculator


class TestUnitEconomicsCalculator(unittest.TestCase):
    """Тесты для класса UnitEconomicsCalculator"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.calculator = UnitEconomicsCalculator()
        
        # Базовый набор данных для тестов
        self.test_data = {
            'selling_price': 1000,
            'purchase_cost': 300,
            'packaging_cost': 50,
            'labeling_cost': 20,
            'quality_control': 30,
            'certification': 10,
            'commission_rate': 15,
            'fulfillment_cost': 100,
            'storage_total': 50,
            'payment_amount': 20,
            'ppc_cost_per_unit': 80,
            'external_marketing': 20,
            'influencer_marketing': 10,
            'content_creation': 30,
            'fixed_cost_per_unit': 40,
            'customer_service': 20,
            'return_cost_per_unit': 30,
            'marketplace': 'OZON',
            'repeat_purchase_rate': 20,
            'avg_purchases_per_year': 2.5,
            'customer_lifespan_months': 12
        }
        
    def test_calculate_cogs(self):
        """Тест расчета себестоимости"""
        cogs = self.calculator._calculate_cogs(self.test_data)
        expected_cogs = 410  # 300 + 50 + 20 + 30 + 10
        self.assertEqual(cogs, expected_cogs)
        
    def test_calculate_marketplace_costs(self):
        """Тест расчета расходов маркетплейса"""
        marketplace_costs = self.calculator._calculate_marketplace_costs(self.test_data)
        # 1000 * 0.15 (commission) + 100 (fulfillment) + 50 (storage) + 20 (payment) + 1000 * 0.02 (OZON fee)
        expected_costs = 150 + 100 + 50 + 20 + 20
        self.assertEqual(marketplace_costs, expected_costs)
        
    def test_calculate_marketing_costs(self):
        """Тест расчета маркетинговых затрат"""
        marketing_costs = self.calculator._calculate_marketing_costs(self.test_data)
        expected_costs = 140  # 80 + 20 + 10 + 30
        self.assertEqual(marketing_costs, expected_costs)
        
    def test_calculate_operational_costs(self):
        """Тест расчета операционных затрат"""
        operational_costs = self.calculator._calculate_operational_costs(self.test_data)
        expected_costs = 90  # 40 + 20 + 30
        self.assertEqual(operational_costs, expected_costs)
        
    def test_calculate_unit_economics(self):
        """Тест расчета общей юнит-экономики"""
        result = self.calculator.calculate_unit_economics(self.test_data)
        
        # Проверяем основные метрики
        self.assertEqual(result['selling_price'], 1000)
        self.assertEqual(result['total_cogs'], 410)
        self.assertEqual(result['total_costs'], 980)  # 410 + 340 + 140 + 90
        self.assertEqual(result['unit_profit'], 20)  # 1000 - 980
        
        # Проверка маржинальности с небольшой погрешностью из-за чисел с плавающей точкой
        self.assertAlmostEqual(result['profit_margin'], 2.0, places=1)  # (20 / 1000) * 100
        
    def test_edge_cases(self):
        """Тест обработки граничных случаев"""
        # Тест с нулевой ценой
        zero_price_data = self.test_data.copy()
        zero_price_data['selling_price'] = 0
        
        result = self.calculator.calculate_unit_economics(zero_price_data)
        self.assertEqual(result['selling_price'], 0)
        self.assertEqual(result['profit_margin'], 0)  # Нет деления на ноль
        
        # Тест с отрицательной ценой
        negative_price_data = self.test_data.copy()
        negative_price_data['selling_price'] = -100
        
        result = self.calculator.calculate_unit_economics(negative_price_data)
        self.assertEqual(result['selling_price'], -100)
        self.assertTrue(result['profit_margin'] < 0)
        
    def test_cohort_ltv(self):
        """Тест расчета LTV с учетом когортного анализа"""
        # Дополняем тестовые данные для расчета когорт
        cohort_data = self.test_data.copy()
        cohort_data['profit_margin'] = 30
        
        result = self.calculator.calculate_cohort_ltv(cohort_data)
        
        # Проверяем, что все необходимые показатели присутствуют
        self.assertIn('ltv_simple', result)
        self.assertIn('ltv_discounted', result)
        self.assertIn('retention_by_month', result)
        self.assertIn('cumulative_ltv', result)
        
        # Проверяем, что значение LTV положительное
        self.assertTrue(result['ltv_simple'] > 0)
        
        # Проверяем, что дисконтированный LTV меньше обычного
        self.assertTrue(result['ltv_discounted'] < result['ltv_simple'])
        
        # Проверяем, что длина массива соответствует количеству месяцев
        self.assertEqual(len(result['retention_by_month']), min(36, cohort_data['customer_lifespan_months']))


if __name__ == '__main__':
    unittest.main() 