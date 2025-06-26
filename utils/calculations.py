import pandas as pd
import numpy as np
from typing import Dict, List, Any

class UnitEconomicsCalculator:
    """
    Класс для расчета юнит-экономики товаров на маркетплейсах
    """
    
    def __init__(self):
        self.benchmarks = {
            'margin_excellent': 30,
            'margin_good': 20,
            'margin_acceptable': 10,
            'ltv_cac_excellent': 5,
            'ltv_cac_good': 3,
            'ltv_cac_acceptable': 2,
            'profit_weight': 25,
            'resource_weight': 15,
            'operations_weight': 15,
            'financial_weight': 15,
            'intelligence_weight': 15,
            'transformation_weight': 15
        }
    
    def calculate_unit_economics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основной метод расчета юнит-экономики
        """
        # Базовые данные с проверкой на None
        selling_price = data.get('selling_price', 0) or 0
        
        # Расчет себестоимости (COGS)
        total_cogs = self._calculate_cogs(data)
        
        # Расчет расходов маркетплейса
        marketplace_costs = self._calculate_marketplace_costs(data)
        
        # Расчет маркетинговых расходов
        marketing_costs = self._calculate_marketing_costs(data)
        
        # Расчет операционных расходов
        operational_costs = self._calculate_operational_costs(data)
        
        # Общие затраты
        total_costs = total_cogs + marketplace_costs + marketing_costs + operational_costs
        
        # Прибыль с единицы
        unit_profit = selling_price - total_costs
        
        # Маржинальность (с защитой от деления на ноль)
        profit_margin = (unit_profit / selling_price * 100) if selling_price > 0 else 0
        
        # Вклад в маржу (с защитой от деления на ноль)
        contribution_margin = selling_price - total_cogs - marketplace_costs
        
        # Безубыточная цена (с защитой от деления на ноль)
        breakeven_price = total_costs if total_costs <= 0 else total_costs / 0.8  # Цена для 20% маржи
        
        return {
            'selling_price': selling_price,
            'total_cogs': total_cogs,
            'marketplace_costs': marketplace_costs,
            'marketing_costs': marketing_costs,
            'operational_costs': operational_costs,
            'total_costs': total_costs,
            'unit_profit': unit_profit,
            'profit_margin': profit_margin,
            'contribution_margin': contribution_margin,
            'breakeven_price': breakeven_price
        }
    
    def _calculate_cogs(self, data: Dict[str, Any]) -> float:
        """
        Расчет себестоимости товара (Cost of Goods Sold)
        
        Включает:
        - Закупочную стоимость
        - Стоимость упаковки
        - Стоимость маркировки
        - Расходы на контроль качества
        - Расходы на сертификацию
        """
        purchase_cost = data.get('purchase_cost', 0) or 0
        packaging_cost = data.get('packaging_cost', 0) or 0
        labeling_cost = data.get('labeling_cost', 0) or 0
        quality_control = data.get('quality_control', 0) or 0
        certification = data.get('certification', 0) or 0
        
        return purchase_cost + packaging_cost + labeling_cost + quality_control + certification
    
    def _calculate_marketplace_costs(self, data: Dict[str, Any]) -> float:
        """
        Расчет расходов маркетплейса
        
        Включает:
        - Комиссию маркетплейса
        - Стоимость фулфилмента
        - Стоимость хранения
        - Стоимость обработки платежа
        - Дополнительные комиссии (например, маркетинговая комиссия OZON)
        """
        selling_price = data.get('selling_price', 0) or 0
        commission_rate = (data.get('commission_rate', 15) or 15) / 100  # Защита от None
        fulfillment_cost = data.get('fulfillment_cost', 0) or 0
        storage_total = data.get('storage_total', 0) or 0
        payment_amount = data.get('payment_amount', 0) or 0
        
        commission_amount = selling_price * commission_rate
        
        # Дополнительные расходы для OZON
        marketplace = data.get('marketplace', '')
        additional_costs = 0
        if marketplace == 'OZON':
            additional_costs = selling_price * 0.02  # Обязательная маркетинговая комиссия
        
        return commission_amount + fulfillment_cost + storage_total + payment_amount + additional_costs
    
    def _calculate_marketing_costs(self, data: Dict[str, Any]) -> float:
        """
        Расчет маркетинговых расходов
        
        Включает:
        - Стоимость PPC рекламы на единицу
        - Стоимость внешнего маркетинга на единицу
        - Расходы на инфлюенсеров на единицу
        - Затраты на создание контента на единицу
        """
        ppc_cost_per_unit = data.get('ppc_cost_per_unit', 0) or 0
        external_marketing = data.get('external_marketing', 0) or 0
        influencer_marketing = data.get('influencer_marketing', 0) or 0
        content_creation = data.get('content_creation', 0) or 0
        
        return ppc_cost_per_unit + external_marketing + influencer_marketing + content_creation
    
    def _calculate_operational_costs(self, data: Dict[str, Any]) -> float:
        """
        Расчет операционных расходов
        
        Включает:
        - Фиксированные расходы на единицу товара
        - Расходы на обслуживание клиентов
        - Расходы на обработку возвратов
        """
        fixed_cost_per_unit = data.get('fixed_cost_per_unit', 0) or 0
        customer_service = data.get('customer_service', 0) or 0
        return_cost_per_unit = data.get('return_cost_per_unit', 0) or 0
        
        return fixed_cost_per_unit + customer_service + return_cost_per_unit
    
    def calculate_profit_score(self, result: Dict[str, Any]) -> int:
        """
        Расчет P.R.O.F.I.T. Score (0-100)
        """
        score = 0
        
        # P - Profitability (0-25 points)
        profit_margin = result.get('profit_margin', 0)
        if profit_margin >= self.benchmarks['margin_excellent']:
            score += 25
        elif profit_margin >= self.benchmarks['margin_good']:
            score += 20
        elif profit_margin >= self.benchmarks['margin_acceptable']:
            score += 15
        elif profit_margin >= 0:
            score += 10
        
        # R - Resource Optimization (0-15 points)
        selling_price = result.get('selling_price', 0)
        total_costs = result.get('total_costs', 0)
        if selling_price > 0:
            cost_efficiency = (total_costs / selling_price) * 100
            if cost_efficiency <= 70:
                score += 15
            elif cost_efficiency <= 80:
                score += 12
            elif cost_efficiency <= 90:
                score += 8
        
        # O - Operations Excellence (0-15 points)
        operational_costs = result.get('operational_costs', 0)
        if selling_price > 0:
            operational_efficiency = (operational_costs / selling_price) * 100
            if operational_efficiency <= 5:
                score += 15
            elif operational_efficiency <= 10:
                score += 12
            elif operational_efficiency <= 15:
                score += 8
        
        # F - Financial Intelligence (0-15 points)
        # Базируется на соотношении маржинальности и оборачиваемости
        if profit_margin > 0:
            score += 15
        elif profit_margin >= -5:
            score += 10
        elif profit_margin >= -10:
            score += 5
        
        # I - Intelligence (0-15 points)
        # Оценка автоматизации и аналитики (упрощенная версия)
        marketplace_costs = result.get('marketplace_costs', 0)
        if selling_price > 0:
            marketplace_efficiency = (marketplace_costs / selling_price) * 100
            if marketplace_efficiency <= 20:
                score += 15
            elif marketplace_efficiency <= 30:
                score += 12
            elif marketplace_efficiency <= 40:
                score += 8
        
        # T - Transformation (0-15 points)
        # Потенциал роста и масштабирования
        contribution_margin = result.get('contribution_margin', 0)
        if contribution_margin > selling_price * 0.5:
            score += 15
        elif contribution_margin > selling_price * 0.3:
            score += 12
        elif contribution_margin > selling_price * 0.1:
            score += 8
        elif contribution_margin > 0:
            score += 5
        
        return min(100, score)
    
    def generate_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация рекомендаций на основе анализа данных
        """
        result = self.calculate_unit_economics(data)
        profit_score = self.calculate_profit_score(result)
        
        recommendations = {
            'critical_issues': [],
            'improvements': [],
            'strengths': [],
            'action_plan': {
                'immediate': [],
                'short_term': [],
                'long_term': []
            },
            'profit_matrix': {},
            'total_score': profit_score
        }
        
        # Анализ критических проблем
        if result['profit_margin'] < 0:
            recommendations['critical_issues'].append(
                f"Убыточность товара: {result['profit_margin']:.1f}%. Необходима срочная корректировка цены или затрат."
            )
            recommendations['action_plan']['immediate'].append(
                "Повысить цену или найти способы снижения затрат"
            )
        
        if result['profit_margin'] < 10:
            recommendations['critical_issues'].append(
                "Крайне низкая маржинальность. Бизнес нестабилен при колебаниях затрат."
            )
        
        # Анализ областей для улучшения
        marketplace_percentage = (result['marketplace_costs'] / result['selling_price']) * 100
        if marketplace_percentage > 30:
            recommendations['improvements'].append(
                f"Высокие расходы маркетплейса ({marketplace_percentage:.1f}%). Рассмотрите смену категории или платформы."
            )
        
        marketing_percentage = (result['marketing_costs'] / result['selling_price']) * 100
        if marketing_percentage > 25:
            recommendations['improvements'].append(
                f"Высокие маркетинговые расходы ({marketing_percentage:.1f}%). Оптимизируйте рекламные кампании."
            )
            recommendations['action_plan']['short_term'].append(
                "Провести аудит рекламных кампаний и оптимизировать ставки"
            )
        
        # Определение сильных сторон
        if result['profit_margin'] > 20:
            recommendations['strengths'].append(
                f"Отличная маржинальность ({result['profit_margin']:.1f}%). Потенциал для масштабирования."
            )
        
        cogs_percentage = (result['total_cogs'] / result['selling_price']) * 100
        if cogs_percentage < 40:
            recommendations['strengths'].append(
                f"Эффективная структура себестоимости ({cogs_percentage:.1f}%)."
            )
        
        # P.R.O.F.I.T. Matrix
        recommendations['profit_matrix'] = {
            'Profitability': min(100, max(0, result['profit_margin'] * 3)),
            'Resource Optimization': min(100, max(0, 100 - cogs_percentage)),
            'Operations Excellence': min(100, max(0, 100 - (result['operational_costs'] / result['selling_price']) * 1000)),
            'Financial Intelligence': min(100, max(0, profit_score)),
            'Intelligence Automation': 60,  # Базовое значение
            'Transformation Strategy': min(100, max(0, result['profit_margin'] * 2))
        }
        
        # Долгосрочные рекомендации
        if profit_score >= 70:
            recommendations['action_plan']['long_term'].append(
                "Рассмотреть расширение ассортимента в данной категории"
            )
            recommendations['action_plan']['long_term'].append(
                "Изучить возможности выхода на новые маркетплейсы"
            )
        
        return recommendations
    
    def calculate_scenarios(self, base_data: Dict[str, Any], scenarios: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, Any]]:
        """
        Расчет различных сценариев развития
        """
        results = {}
        
        for scenario_name, modifications in scenarios.items():
            scenario_data = base_data.copy()
            
            # Применяем модификации
            if 'price_change' in modifications:
                scenario_data['selling_price'] *= (1 + modifications['price_change'])
            
            if 'cost_change' in modifications:
                cost_fields = ['purchase_cost', 'packaging_cost', 'labeling_cost', 
                              'quality_control', 'certification']
                for field in cost_fields:
                    if field in scenario_data:
                        scenario_data[field] *= (1 + modifications['cost_change'])
            
            if 'volume_change' in modifications:
                scenario_data['monthly_sales_volume'] *= (1 + modifications['volume_change'])
            
            if 'marketing_efficiency' in modifications:
                marketing_fields = ['ppc_cost_per_unit', 'external_marketing', 
                                  'influencer_marketing', 'content_creation']
                for field in marketing_fields:
                    if field in scenario_data:
                        scenario_data[field] *= (1 + modifications['marketing_efficiency'])
            
            # Пересчитываем метрики
            results[scenario_name] = self.calculate_unit_economics(scenario_data)
        
        return results
    
    def calculate_cohort_ltv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Расширенный расчет LTV с учетом когортного анализа
        
        Учитывает снижение удержания клиентов по месяцам и позволяет
        более точно прогнозировать долгосрочную ценность клиента.
        """
        # Получаем базовые параметры
        selling_price = data.get('selling_price', 0) or 0
        gross_margin = data.get('profit_margin', 0) or 0
        repeat_purchase_rate = data.get('repeat_purchase_rate', 0) or 0
        customer_lifespan_months = data.get('customer_lifespan_months', 0) or 0
        churn_rate = 1 - (repeat_purchase_rate / 100)
        
        # Защита от деления на ноль и некорректных значений
        if churn_rate <= 0 or churn_rate >= 1:
            churn_rate = 0.5  # Значение по умолчанию, если данные некорректны
        
        # Рассчитываем удержание по месяцам
        months = min(36, customer_lifespan_months)  # Ограничиваем период для стабильности расчетов
        retention_by_month = [repeat_purchase_rate/100 * (1 - churn_rate)**(i) for i in range(months)]
        
        # Рассчитываем доход по месяцам с учетом удержания и маржи
        revenue_by_month = [selling_price * retention * (gross_margin/100) for retention in retention_by_month]
        
        # Рассчитываем накопительный LTV
        cumulative_ltv = np.cumsum(revenue_by_month).tolist()
        
        # Дисконтированный LTV (с учетом временной стоимости денег)
        discount_rate = 0.1/12  # Месячная ставка дисконтирования (примерно 10% годовых)
        discounted_revenue = [rev / ((1 + discount_rate)**i) for i, rev in enumerate(revenue_by_month)]
        discounted_ltv = np.cumsum(discounted_revenue).tolist()
        
        return {
            'ltv_simple': sum(revenue_by_month),  # Старый метод расчета
            'ltv_discounted': sum(discounted_revenue),  # LTV с учетом дисконтирования
            'retention_by_month': retention_by_month,
            'revenue_by_month': revenue_by_month,
            'cumulative_ltv': cumulative_ltv,
            'discounted_ltv': discounted_ltv
        }
    
    def calculate_inventory_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Расчет метрик оборачиваемости запасов и денежного цикла
        """
        avg_inventory = data.get('avg_inventory', 0) or 0
        monthly_cogs = data.get('monthly_cogs', 0) or 0
        payment_terms_days = data.get('payment_terms_days', 30) or 30
        supplier_terms_days = data.get('supplier_terms_days', 0) or 0
        
        # Защита от деления на ноль
        if monthly_cogs <= 0:
            return {
                'inventory_turnover': 0,
                'days_inventory': 0,
                'cash_conversion_cycle': 0
            }
        
        # Расчет оборачиваемости запасов (месячной)
        inventory_turnover = monthly_cogs / avg_inventory if avg_inventory > 0 else 0
        
        # Дни хранения запасов
        days_inventory = 30 / inventory_turnover if inventory_turnover > 0 else 0
        
        # Денежный цикл
        cash_conversion_cycle = days_inventory + payment_terms_days - supplier_terms_days
        
        return {
            'inventory_turnover': inventory_turnover,
            'days_inventory': days_inventory,
            'cash_conversion_cycle': cash_conversion_cycle
        }
    
    def perform_sensitivity_analysis(self, base_data: Dict[str, Any], 
                                   variables: List[str], 
                                   percent_changes: List[float]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Анализ чувствительности модели к изменению ключевых переменных
        
        Args:
            base_data: Исходные данные для расчета
            variables: Список переменных для анализа чувствительности
            percent_changes: Список процентных изменений для каждой переменной
            
        Returns:
            Словарь с результатами по каждой переменной
        """
        results = {}
        
        for var in variables:
            var_results = []
            original_value = base_data.get(var, 0)
            
            if original_value == 0:
                continue
                
            for change in percent_changes:
                # Копируем исходные данные
                modified_data = base_data.copy()
                
                # Модифицируем переменную
                modified_data[var] = original_value * (1 + change/100)
                
                # Рассчитываем юнит-экономику с измененным значением
                result = self.calculate_unit_economics(modified_data)
                
                # Добавляем информацию об изменении
                result['variable'] = var
                result['percent_change'] = change
                result['modified_value'] = modified_data[var]
                
                var_results.append(result)
            
            results[var] = var_results
                
        return results
