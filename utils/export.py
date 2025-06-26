import pandas as pd
import io
from fpdf import FPDF
from datetime import datetime
from typing import Dict, Any, List
import base64

class ExportManager:
    """
    Класс для экспорта результатов расчетов в различные форматы
    """
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    def create_excel_report(self, data: Dict[str, Any]) -> bytes:
        """
        Создание Excel отчета с результатами расчетов
        """
        # Создаем Excel writer
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Основные результаты
            self._create_summary_sheet(data, writer)
            
            # Детальные расчеты
            self._create_detailed_calculations_sheet(data, writer)
            
            # Анализ сценариев
            if 'scenarios' in data:
                self._create_scenarios_sheet(data, writer)
            
            # Рекомендации
            self._create_recommendations_sheet(data, writer)
        
        output.seek(0)
        return output.read()
    
    def _create_summary_sheet(self, data: Dict[str, Any], writer):
        """Создание листа с основными результатами"""
        summary_data = {
            'Параметр': [
                'Товар',
                'Маркетплейс',
                'Категория',
                'Цена продажи (₽)',
                'Себестоимость (₽)',
                'Расходы маркетплейса (₽)',
                'Маркетинговые расходы (₽)',
                'Операционные расходы (₽)',
                'Общие затраты (₽)',
                'Прибыль с единицы (₽)',
                'Маржинальность (%)',
                'LTV (₽)',
                'CAC (₽)',
                'LTV/CAC',
                'Период окупаемости (мес.)',
                'P.R.O.F.I.T. Score',
                'Дата расчета'
            ],
            'Значение': [
                data.get('product_name', 'Не указан'),
                data.get('marketplace', 'Не указан'),
                data.get('category', 'Не указана'),
                f"{data.get('selling_price', 0):,.0f}",
                f"{data.get('total_cogs', 0):,.0f}",
                f"{data.get('marketplace_costs', 0):,.0f}",
                f"{data.get('marketing_costs', 0):,.0f}",
                f"{data.get('operational_costs', 0):,.0f}",
                f"{data.get('total_costs', 0):,.0f}",
                f"{data.get('unit_profit', 0):+,.0f}",
                f"{data.get('profit_margin', 0):.1f}%",
                f"{data.get('ltv', 0):,.0f}",
                f"{data.get('cac', 0):,.0f}",
                f"{data.get('ltv_cac_ratio', 0):.1f}",
                f"{data.get('payback_period', 0):.1f}",
                f"{data.get('profit_score', 0)}/100",
                self.timestamp
            ]
        }
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Основные результаты', index=False)
    
    def _create_detailed_calculations_sheet(self, data: Dict[str, Any], writer):
        """Создание листа с детальными расчетами"""
        detailed_data = {
            'Категория затрат': [],
            'Статья расходов': [],
            'Сумма (₽)': [],
            'Доля от цены (%)': []
        }
        
        selling_price = data.get('selling_price', 1)
        
        # Себестоимость
        cogs_items = [
            ('Закупочная стоимость', data.get('purchase_cost', 0)),
            ('Упаковка', data.get('packaging_cost', 0)),
            ('Маркировка', data.get('labeling_cost', 0)),
            ('Контроль качества', data.get('quality_control', 0)),
            ('Сертификация', data.get('certification', 0))
        ]
        
        for item_name, amount in cogs_items:
            detailed_data['Категория затрат'].append('Себестоимость')
            detailed_data['Статья расходов'].append(item_name)
            detailed_data['Сумма (₽)'].append(amount)
            detailed_data['Доля от цены (%)'].append(f"{(amount / selling_price) * 100:.1f}%")
        
        # Расходы маркетплейса
        marketplace_items = [
            ('Комиссия маркетплейса', data.get('commission_amount', 0)),
            ('Фулфилмент', data.get('fulfillment_cost', 0)),
            ('Хранение', data.get('storage_total', 0)),
            ('Эквайринг', data.get('payment_amount', 0))
        ]
        
        for item_name, amount in marketplace_items:
            detailed_data['Категория затрат'].append('Маркетплейс')
            detailed_data['Статья расходов'].append(item_name)
            detailed_data['Сумма (₽)'].append(amount)
            detailed_data['Доля от цены (%)'].append(f"{(amount / selling_price) * 100:.1f}%")
        
        # Маркетинговые расходы
        marketing_items = [
            ('PPC реклама', data.get('ppc_cost_per_unit', 0)),
            ('Внешний маркетинг', data.get('external_marketing', 0)),
            ('Инфлюенсер-маркетинг', data.get('influencer_marketing', 0)),
            ('Создание контента', data.get('content_creation', 0))
        ]
        
        for item_name, amount in marketing_items:
            detailed_data['Категория затрат'].append('Маркетинг')
            detailed_data['Статья расходов'].append(item_name)
            detailed_data['Сумма (₽)'].append(amount)
            detailed_data['Доля от цены (%)'].append(f"{(amount / selling_price) * 100:.1f}%")
        
        # Операционные расходы
        operational_items = [
            ('Постоянные расходы на единицу', data.get('fixed_cost_per_unit', 0)),
            ('Обработка заказа', data.get('customer_service', 0)),
            ('Обработка возвратов', data.get('return_cost_per_unit', 0))
        ]
        
        for item_name, amount in operational_items:
            detailed_data['Категория затрат'].append('Операционные')
            detailed_data['Статья расходов'].append(item_name)
            detailed_data['Сумма (₽)'].append(amount)
            detailed_data['Доля от цены (%)'].append(f"{(amount / selling_price) * 100:.1f}%")
        
        df_detailed = pd.DataFrame(detailed_data)
        df_detailed.to_excel(writer, sheet_name='Детальные расчеты', index=False)
    
    def _create_scenarios_sheet(self, data: Dict[str, Any], writer):
        """Создание листа с анализом сценариев"""
        scenarios = data.get('scenarios', {})
        
        scenario_data = {
            'Сценарий': [],
            'Цена продажи (₽)': [],
            'Общие затраты (₽)': [],
            'Прибыль с единицы (₽)': [],
            'Маржинальность (%)': [],
            'Месячная прибыль (₽)': []
        }
        
        monthly_volume = data.get('monthly_sales_volume', 100)
        
        for scenario_name, scenario_result in scenarios.items():
            scenario_data['Сценарий'].append(scenario_name)
            scenario_data['Цена продажи (₽)'].append(f"{scenario_result.get('selling_price', 0):,.0f}")
            scenario_data['Общие затраты (₽)'].append(f"{scenario_result.get('total_costs', 0):,.0f}")
            scenario_data['Прибыль с единицы (₽)'].append(f"{scenario_result.get('unit_profit', 0):+,.0f}")
            scenario_data['Маржинальность (%)'].append(f"{scenario_result.get('profit_margin', 0):.1f}%")
            
            monthly_profit = scenario_result.get('unit_profit', 0) * monthly_volume
            scenario_data['Месячная прибыль (₽)'].append(f"{monthly_profit:+,.0f}")
        
        df_scenarios = pd.DataFrame(scenario_data)
        df_scenarios.to_excel(writer, sheet_name='Сценарии', index=False)
    
    def _create_recommendations_sheet(self, data: Dict[str, Any], writer):
        """Создание листа с рекомендациями"""
        recommendations_data = {
            'Тип': [],
            'Рекомендация': [],
            'Приоритет': []
        }
        
        # Здесь можно добавить логику для формирования рекомендаций
        # На основе данных расчетов
        
        profit_margin = data.get('profit_margin', 0)
        
        if profit_margin < 0:
            recommendations_data['Тип'].append('Критическая проблема')
            recommendations_data['Рекомендация'].append('Товар убыточен. Необходимо повысить цену или снизить затраты.')
            recommendations_data['Приоритет'].append('Высокий')
        
        if profit_margin < 10:
            recommendations_data['Тип'].append('Область для улучшения')
            recommendations_data['Рекомендация'].append('Низкая маржинальность. Рассмотрите оптимизацию затрат.')
            recommendations_data['Приоритет'].append('Средний')
        
        marketplace_costs = data.get('marketplace_costs', 0)
        selling_price = data.get('selling_price', 1)
        
        if (marketplace_costs / selling_price) > 0.3:
            recommendations_data['Тип'].append('Область для улучшения')
            recommendations_data['Рекомендация'].append('Высокие расходы маркетплейса. Рассмотрите смену категории.')
            recommendations_data['Приоритет'].append('Средний')
        
        if profit_margin > 20:
            recommendations_data['Тип'].append('Сильная сторона')
            recommendations_data['Рекомендация'].append('Отличная маржинальность. Потенциал для масштабирования.')
            recommendations_data['Приоритет'].append('Низкий')
        
        df_recommendations = pd.DataFrame(recommendations_data)
        df_recommendations.to_excel(writer, sheet_name='Рекомендации', index=False)
    
    def create_pdf_report(self, data: Dict[str, Any]) -> bytes:
        """
        Создание PDF отчета с результатами расчетов
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Добавляем шрифт с поддержкой Unicode
        pdf.set_font('Arial', 'B', 16)
        
        # Заголовок
        pdf.cell(0, 10, 'Unit Economics Report', ln=True, align='C')
        pdf.ln(10)
        
        # Основная информация
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Product Information:', ln=True)
        pdf.set_font('Arial', '', 10)
        
        product_info = [
            f"Product: {data.get('product_name', 'Not specified')}",
            f"Marketplace: {data.get('marketplace', 'Not specified')}",
            f"Category: {data.get('category', 'Not specified')}",
            f"Selling Price: {data.get('selling_price', 0):,.0f} RUB",
            f"Calculation Date: {self.timestamp}"
        ]
        
        for info in product_info:
            pdf.cell(0, 6, info, ln=True)
        
        pdf.ln(5)
        
        # Финансовые результаты
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Financial Results:', ln=True)
        pdf.set_font('Arial', '', 10)
        
        financial_results = [
            f"Total Costs: {data.get('total_costs', 0):,.0f} RUB",
            f"Unit Profit: {data.get('unit_profit', 0):+,.0f} RUB",
            f"Profit Margin: {data.get('profit_margin', 0):.1f}%",
            f"LTV: {data.get('ltv', 0):,.0f} RUB",
            f"CAC: {data.get('cac', 0):,.0f} RUB",
            f"LTV/CAC Ratio: {data.get('ltv_cac_ratio', 0):.1f}",
            f"P.R.O.F.I.T. Score: {data.get('profit_score', 0)}/100"
        ]
        
        for result in financial_results:
            pdf.cell(0, 6, result, ln=True)
        
        pdf.ln(5)
        
        # Структура затрат
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Cost Breakdown:', ln=True)
        pdf.set_font('Arial', '', 10)
        
        cost_breakdown = [
            f"COGS: {data.get('total_cogs', 0):,.0f} RUB",
            f"Marketplace Costs: {data.get('marketplace_costs', 0):,.0f} RUB",
            f"Marketing Costs: {data.get('marketing_costs', 0):,.0f} RUB",
            f"Operational Costs: {data.get('operational_costs', 0):,.0f} RUB"
        ]
        
        for cost in cost_breakdown:
            pdf.cell(0, 6, cost, ln=True)
        
        # Возвращаем PDF как байты
        return pdf.output(dest='S').encode('latin-1')
    
    def create_json_export(self, data: Dict[str, Any]) -> str:
        """
        Создание JSON экспорта данных
        """
        export_data = {
            'metadata': {
                'export_date': self.timestamp,
                'version': '1.0',
                'calculator_type': 'unit_economics_marketplace'
            },
            'product_info': {
                'name': data.get('product_name', ''),
                'marketplace': data.get('marketplace', ''),
                'category': data.get('category', ''),
                'selling_price': data.get('selling_price', 0)
            },
            'cost_structure': {
                'cogs': data.get('total_cogs', 0),
                'marketplace_costs': data.get('marketplace_costs', 0),
                'marketing_costs': data.get('marketing_costs', 0),
                'operational_costs': data.get('operational_costs', 0),
                'total_costs': data.get('total_costs', 0)
            },
            'financial_metrics': {
                'unit_profit': data.get('unit_profit', 0),
                'profit_margin': data.get('profit_margin', 0),
                'ltv': data.get('ltv', 0),
                'cac': data.get('cac', 0),
                'ltv_cac_ratio': data.get('ltv_cac_ratio', 0),
                'payback_period': data.get('payback_period', 0),
                'profit_score': data.get('profit_score', 0)
            },
            'scenarios': data.get('scenarios', {}),
            'raw_data': data
        }
        
        import json
        return json.dumps(export_data, ensure_ascii=False, indent=2)
