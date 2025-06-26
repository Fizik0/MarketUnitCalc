import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
from datetime import datetime
import os

# Import custom modules
from utils.calculations import UnitEconomicsCalculator
from utils.data_models import MarketplaceData, BusinessMetrics
from utils.export import ExportManager
from data.marketplace_data import MARKETPLACE_COMMISSIONS, BENCHMARKS

# Configure page
st.set_page_config(
    page_title="Калькулятор Юнит-Экономики Маркетплейсов",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'calculator_data' not in st.session_state:
    st.session_state.calculator_data = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'completed_steps' not in st.session_state:
    st.session_state.completed_steps = set()

def main():
    st.title("🎯 Калькулятор Юнит-Экономики для Российских Маркетплейсов")
    st.markdown("### Профессиональный инструмент для расчета реальной прибыльности бизнеса")
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["Калькулятор", "Дашборд", "Методология", "Экспорт"],
        icons=["calculator", "graph-up", "book", "download"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#FF6B6B", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#FF6B6B"},
        },
    )
    
    if selected == "Калькулятор":
        calculator_page()
    elif selected == "Дашборд":
        dashboard_page()
    elif selected == "Методология":
        methodology_page()
    elif selected == "Экспорт":
        export_page()

def calculator_page():
    st.header("📋 10-этапный расчет юнит-экономики")
    
    # Progress bar
    progress = (st.session_state.current_step - 1) / 10
    st.progress(progress)
    st.write(f"Этап {st.session_state.current_step} из 10")
    
    # Step navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("← Назад", disabled=st.session_state.current_step == 1):
            st.session_state.current_step = max(1, st.session_state.current_step - 1)
            st.rerun()
    
    with col3:
        if st.button("Далее →", disabled=st.session_state.current_step == 10):
            if validate_current_step():
                st.session_state.completed_steps.add(st.session_state.current_step)
                st.session_state.current_step = min(10, st.session_state.current_step + 1)
                st.rerun()
    
    # Current step content
    if st.session_state.current_step == 1:
        step_1_marketplace_selection()
    elif st.session_state.current_step == 2:
        step_2_product_info()
    elif st.session_state.current_step == 3:
        step_3_cost_structure()
    elif st.session_state.current_step == 4:
        step_4_marketplace_costs()
    elif st.session_state.current_step == 5:
        step_5_marketing_costs()
    elif st.session_state.current_step == 6:
        step_6_operational_costs()
    elif st.session_state.current_step == 7:
        step_7_ltv_cac_analysis()
    elif st.session_state.current_step == 8:
        step_8_profit_analysis()
    elif st.session_state.current_step == 9:
        step_9_scenario_planning()
    elif st.session_state.current_step == 10:
        step_10_recommendations()

def step_1_marketplace_selection():
    st.subheader("🛒 Этап 1: Выбор маркетплейса и категории")
    
    col1, col2 = st.columns(2)
    
    with col1:
        marketplace = st.selectbox(
            "Выберите маркетплейс:",
            ["OZON", "Wildberries", "Яндекс.Маркет", "Авито", "Другой"],
            key="marketplace"
        )
        
        if marketplace in MARKETPLACE_COMMISSIONS:
            categories = list(MARKETPLACE_COMMISSIONS[marketplace].keys())
            category = st.selectbox(
                "Выберите категорию товара:",
                categories,
                key="category"
            )
        else:
            category = st.text_input("Введите категорию товара:", key="category")
    
    with col2:
        st.info("💡 **Почему это важно?**")
        st.write("• Каждый маркетплейс имеет уникальную структуру комиссий")
        st.write("• Алгоритмы ранжирования различаются")
        st.write("• Аудитория и поведение покупателей отличаются")
        
        if marketplace == "OZON":
            st.warning("📊 **Особенности OZON:**")
            st.write("• Комиссия: 8-45% в зависимости от категории")
            st.write("• Обязательная маркетинговая комиссия: 1-3%")
            st.write("• Интеграция с Озон Премиум влияет на конверсию")
    
    # Save data
    st.session_state.calculator_data.update({
        'marketplace': marketplace,
        'category': category
    })

def step_2_product_info():
    st.subheader("📦 Этап 2: Информация о товаре")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Название товара:", key="product_name")
        selling_price = st.number_input("Цена продажи (₽):", min_value=0.0, step=1.0, key="selling_price")
        weight = st.number_input("Вес товара (кг):", min_value=0.0, step=0.1, key="weight")
        dimensions = st.text_input("Габариты (Д×Ш×В, см):", key="dimensions")
    
    with col2:
        st.info("📊 **Аналитика по категории**")
        
        marketplace = st.session_state.calculator_data.get('marketplace', 'OZON')
        category = st.session_state.calculator_data.get('category', 'Электроника')
        
        if marketplace in BENCHMARKS and category in BENCHMARKS[marketplace]:
            benchmarks = BENCHMARKS[marketplace][category]
            st.metric("Средняя цена в категории", f"{benchmarks['avg_price']:,.0f} ₽")
            st.metric("Средняя конверсия", f"{benchmarks['avg_conversion']:.1%}")
            st.metric("Средний возврат", f"{benchmarks['avg_return_rate']:.1%}")
        
        # Price analysis
        if selling_price > 0:
            if marketplace in BENCHMARKS and category in BENCHMARKS[marketplace]:
                avg_price = BENCHMARKS[marketplace][category]['avg_price']
                if selling_price > avg_price * 1.5:
                    st.warning("⚠️ Цена значительно выше средней по категории")
                elif selling_price < avg_price * 0.7:
                    st.error("🔴 Цена может быть слишком низкой")
                else:
                    st.success("✅ Цена в пределах рыночного диапазона")
    
    # Save data
    st.session_state.calculator_data.update({
        'product_name': product_name,
        'selling_price': selling_price,
        'weight': weight,
        'dimensions': dimensions
    })

def step_3_cost_structure():
    st.subheader("💰 Этап 3: Структура себестоимости")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Прямые затраты")
        purchase_cost = st.number_input("Закупочная стоимость (₽):", min_value=0.0, step=1.0, key="purchase_cost")
        packaging_cost = st.number_input("Упаковка (₽):", min_value=0.0, step=1.0, value=25.0, key="packaging_cost")
        labeling_cost = st.number_input("Маркировка/этикетки (₽):", min_value=0.0, step=1.0, key="labeling_cost")
        
        st.write("#### Дополнительные расходы")
        quality_control = st.number_input("Контроль качества (₽):", min_value=0.0, step=1.0, key="quality_control")
        certification = st.number_input("Сертификация (₽ на единицу):", min_value=0.0, step=1.0, key="certification")
    
    with col2:
        total_cost = purchase_cost + packaging_cost + labeling_cost + quality_control + certification
        selling_price = st.session_state.calculator_data.get('selling_price', 0)
        
        st.metric("Общая себестоимость", f"{total_cost:,.0f} ₽")
        
        if selling_price > 0:
            gross_margin = ((selling_price - total_cost) / selling_price) * 100
            st.metric("Валовая маржа", f"{gross_margin:.1f}%")
            
            if gross_margin < 30:
                st.error("🔴 Низкая валовая маржа (< 30%)")
            elif gross_margin < 50:
                st.warning("⚠️ Умеренная валовая маржа (30-50%)")
            else:
                st.success("✅ Хорошая валовая маржа (> 50%)")
        
        st.info("💡 **Бенчмарки по валовой марже:**")
        st.write("• Электроника: 20-40%")
        st.write("• Одежда: 50-70%")
        st.write("• Товары для дома: 40-60%")
        st.write("• Красота и здоровье: 60-80%")
    
    # Save data
    st.session_state.calculator_data.update({
        'purchase_cost': purchase_cost,
        'packaging_cost': packaging_cost,
        'labeling_cost': labeling_cost,
        'quality_control': quality_control,
        'certification': certification,
        'total_cost': total_cost
    })

def step_4_marketplace_costs():
    st.subheader("🏪 Этап 4: Расходы маркетплейса")
    
    marketplace = st.session_state.calculator_data.get('marketplace', 'OZON')
    category = st.session_state.calculator_data.get('category', 'Электроника')
    selling_price = st.session_state.calculator_data.get('selling_price', 0)
    weight = st.session_state.calculator_data.get('weight', 0.5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Комиссии маркетплейса")
        
        # Get default commission rate
        default_commission = 15.0
        if marketplace in MARKETPLACE_COMMISSIONS and category in MARKETPLACE_COMMISSIONS[marketplace]:
            default_commission = MARKETPLACE_COMMISSIONS[marketplace][category]['commission_rate']
        
        commission_rate = st.slider(
            "Комиссия маркетплейса (%)", 
            min_value=5.0, 
            max_value=50.0, 
            value=default_commission,
            step=0.5,
            key="commission_rate"
        )
        
        fulfillment_cost = st.number_input(
            "Стоимость фулфилмента (₽):", 
            min_value=0.0, 
            step=1.0, 
            value=max(50.0, weight * 30),
            key="fulfillment_cost"
        )
        
        storage_days = st.slider("Среднее время хранения (дней):", min_value=1, max_value=365, value=30, key="storage_days")
        storage_cost_per_day = st.number_input("Стоимость хранения (₽/день):", min_value=0.0, step=0.1, value=2.0, key="storage_cost_per_day")
        
        payment_processing = st.slider("Эквайринг (%)", min_value=1.0, max_value=5.0, value=2.5, step=0.1, key="payment_processing")
    
    with col2:
        st.write("#### Расчет общих расходов")
        
        commission_amount = selling_price * (commission_rate / 100)
        storage_total = storage_days * storage_cost_per_day
        payment_amount = selling_price * (payment_processing / 100)
        
        st.metric("Комиссия маркетплейса", f"{commission_amount:,.0f} ₽")
        st.metric("Фулфилмент", f"{fulfillment_cost:,.0f} ₽")
        st.metric("Хранение", f"{storage_total:,.0f} ₽")
        st.metric("Эквайринг", f"{payment_amount:,.0f} ₽")
        
        total_marketplace_costs = commission_amount + fulfillment_cost + storage_total + payment_amount
        st.metric("**Всего расходов МП**", f"{total_marketplace_costs:,.0f} ₽")
        
        if marketplace == "OZON":
            st.warning("⚠️ **Дополнительные расходы OZON:**")
            mandatory_marketing = selling_price * 0.02  # 2% обязательная маркетинговая комиссия
            st.write(f"• Обязательная маркетинговая комиссия: {mandatory_marketing:,.0f} ₽")
            total_marketplace_costs += mandatory_marketing
        
        # Calculate percentage of selling price
        if selling_price > 0:
            percentage = (total_marketplace_costs / selling_price) * 100
            st.metric("% от цены продажи", f"{percentage:.1f}%")
    
    # Save data
    st.session_state.calculator_data.update({
        'commission_rate': commission_rate,
        'commission_amount': commission_amount,
        'fulfillment_cost': fulfillment_cost,
        'storage_days': storage_days,
        'storage_total': storage_total,
        'payment_processing': payment_processing,
        'payment_amount': payment_amount,
        'total_marketplace_costs': total_marketplace_costs
    })

def step_5_marketing_costs():
    st.subheader("📈 Этап 5: Маркетинговые расходы")
    
    selling_price = st.session_state.calculator_data.get('selling_price', 0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Реклама на маркетплейсе")
        
        ppc_budget_percent = st.slider(
            "Бюджет на PPC рекламу (% от оборота):", 
            min_value=0.0, 
            max_value=50.0, 
            value=15.0, 
            step=1.0,
            key="ppc_budget_percent"
        )
        
        avg_cpc = st.number_input("Средний CPC (₽):", min_value=0.0, step=1.0, value=25.0, key="avg_cpc")
        conversion_rate = st.slider("Конверсия рекламы (%):", min_value=0.1, max_value=20.0, value=2.5, step=0.1, key="conversion_rate")
        
        st.write("#### Внешний маркетинг")
        external_marketing = st.number_input("Внешний маркетинг (₽ на единицу):", min_value=0.0, step=1.0, key="external_marketing")
        influencer_marketing = st.number_input("Инфлюенсер-маркетинг (₽ на единицу):", min_value=0.0, step=1.0, key="influencer_marketing")
        content_creation = st.number_input("Создание контента (₽ на единицу):", min_value=0.0, step=1.0, value=50.0, key="content_creation")
    
    with col2:
        st.write("#### Анализ эффективности")
        
        ppc_cost_per_unit = selling_price * (ppc_budget_percent / 100)
        cac_ppc = avg_cpc / (conversion_rate / 100) if conversion_rate > 0 else 0
        
        st.metric("PPC расходы на единицу", f"{ppc_cost_per_unit:,.0f} ₽")
        st.metric("CAC (только PPC)", f"{cac_ppc:,.0f} ₽")
        
        total_marketing_costs = ppc_cost_per_unit + external_marketing + influencer_marketing + content_creation
        st.metric("**Общие маркетинговые расходы**", f"{total_marketing_costs:,.0f} ₽")
        
        if selling_price > 0:
            marketing_percentage = (total_marketing_costs / selling_price) * 100
            st.metric("% от цены продажи", f"{marketing_percentage:.1f}%")
            
            if marketing_percentage > 30:
                st.error("🔴 Высокие маркетинговые расходы (>30%)")
            elif marketing_percentage > 20:
                st.warning("⚠️ Умеренные маркетинговые расходы (20-30%)")
            else:
                st.success("✅ Оптимальные маркетинговые расходы (<20%)")
        
        st.info("💡 **Бенчмарки по маркетингу:**")
        st.write("• Новый продукт: 20-35% от оборота")
        st.write("• Зрелый продукт: 10-20% от оборота")
        st.write("• Премиум сегмент: 15-25% от оборота")
    
    # Save data
    st.session_state.calculator_data.update({
        'ppc_budget_percent': ppc_budget_percent,
        'ppc_cost_per_unit': ppc_cost_per_unit,
        'avg_cpc': avg_cpc,
        'conversion_rate': conversion_rate,
        'cac_ppc': cac_ppc,
        'external_marketing': external_marketing,
        'influencer_marketing': influencer_marketing,
        'content_creation': content_creation,
        'total_marketing_costs': total_marketing_costs
    })

def step_6_operational_costs():
    st.subheader("⚙️ Этап 6: Операционные расходы")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Постоянные расходы")
        staff_costs = st.number_input("Зарплатные расходы (₽/месяц):", min_value=0.0, step=1000.0, key="staff_costs")
        office_rent = st.number_input("Аренда офиса (₽/месяц):", min_value=0.0, step=1000.0, key="office_rent")
        software_subscriptions = st.number_input("Подписки на ПО (₽/месяц):", min_value=0.0, step=100.0, value=5000.0, key="software_subscriptions")
        
        st.write("#### Переменные расходы")
        customer_service = st.number_input("Обработка заказов (₽ за заказ):", min_value=0.0, step=1.0, value=15.0, key="customer_service")
        return_processing = st.slider("Процент возвратов (%):", min_value=0.0, max_value=50.0, value=8.0, step=1.0, key="return_rate")
        return_cost = st.number_input("Стоимость обработки возврата (₽):", min_value=0.0, step=1.0, value=100.0, key="return_cost")
        
        monthly_sales_volume = st.number_input("Плановый объем продаж (шт/месяц):", min_value=1, step=1, value=100, key="monthly_sales_volume")
    
    with col2:
        st.write("#### Расчет операционных расходов на единицу")
        
        # Fixed costs per unit
        total_fixed_monthly = staff_costs + office_rent + software_subscriptions
        fixed_cost_per_unit = total_fixed_monthly / monthly_sales_volume if monthly_sales_volume > 0 else 0
        
        # Variable costs per unit
        return_cost_per_unit = (return_rate / 100) * return_cost
        
        total_operational_costs = fixed_cost_per_unit + customer_service + return_cost_per_unit
        
        st.metric("Постоянные расходы на единицу", f"{fixed_cost_per_unit:,.0f} ₽")
        st.metric("Обработка заказа", f"{customer_service:,.0f} ₽")
        st.metric("Расходы на возвраты", f"{return_cost_per_unit:,.0f} ₽")
        st.metric("**Общие операционные расходы**", f"{total_operational_costs:,.0f} ₽")
        
        selling_price = st.session_state.calculator_data.get('selling_price', 0)
        if selling_price > 0:
            operational_percentage = (total_operational_costs / selling_price) * 100
            st.metric("% от цены продажи", f"{operational_percentage:.1f}%")
        
        st.info("💡 **Оптимизация операций:**")
        st.write("• Автоматизация обработки заказов")
        st.write("• Улучшение качества товара для снижения возвратов")
        st.write("• Эффективное планирование персонала")
        
        if return_rate > 15:
            st.warning("⚠️ Высокий процент возвратов требует внимания")
    
    # Save data
    st.session_state.calculator_data.update({
        'staff_costs': staff_costs,
        'office_rent': office_rent,
        'software_subscriptions': software_subscriptions,
        'customer_service': customer_service,
        'return_rate': return_rate,
        'return_cost': return_cost,
        'monthly_sales_volume': monthly_sales_volume,
        'fixed_cost_per_unit': fixed_cost_per_unit,
        'return_cost_per_unit': return_cost_per_unit,
        'total_operational_costs': total_operational_costs
    })

def step_7_ltv_cac_analysis():
    st.subheader("👥 Этап 7: Анализ LTV/CAC")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Параметры клиентов")
        
        repeat_purchase_rate = st.slider("Процент повторных покупок (%):", min_value=0.0, max_value=100.0, value=25.0, step=1.0, key="repeat_purchase_rate")
        avg_purchases_per_year = st.slider("Среднее количество покупок в год:", min_value=0.1, max_value=12.0, value=1.5, step=0.1, key="avg_purchases_per_year")
        customer_lifespan_months = st.slider("Жизненный цикл клиента (месяцы):", min_value=1, max_value=60, value=18, key="customer_lifespan_months")
        
        st.write("#### Дополнительные доходы")
        cross_sell_revenue = st.number_input("Доход от кросс-продаж (₽ за клиента):", min_value=0.0, step=10.0, key="cross_sell_revenue")
        referral_bonus = st.number_input("Доход от рефералов (₽ за клиента):", min_value=0.0, step=10.0, key="referral_bonus")
    
    with col2:
        st.write("#### Расчет LTV и CAC")
        
        selling_price = st.session_state.calculator_data.get('selling_price', 0)
        total_marketing_costs = st.session_state.calculator_data.get('total_marketing_costs', 0)
        
        # LTV calculation
        purchases_per_customer = (customer_lifespan_months / 12) * avg_purchases_per_year
        repeat_customers = repeat_purchase_rate / 100
        
        ltv = (selling_price * purchases_per_customer + cross_sell_revenue + referral_bonus)
        
        # CAC calculation (simplified - should include all acquisition costs)
        cac = total_marketing_costs  # This is a simplified version
        
        st.metric("LTV (Customer Lifetime Value)", f"{ltv:,.0f} ₽")
        st.metric("CAC (Customer Acquisition Cost)", f"{cac:,.0f} ₽")
        
        if cac > 0:
            ltv_cac_ratio = ltv / cac
            st.metric("LTV/CAC соотношение", f"{ltv_cac_ratio:.1f}")
            
            if ltv_cac_ratio >= 3:
                st.success("✅ Отличное соотношение LTV/CAC (≥3)")
            elif ltv_cac_ratio >= 2:
                st.warning("⚠️ Приемлемое соотношение LTV/CAC (2-3)")
            else:
                st.error("🔴 Низкое соотношение LTV/CAC (<2)")
        
        payback_period = cac / (selling_price * avg_purchases_per_year / 12) if selling_price > 0 and avg_purchases_per_year > 0 else 0
        st.metric("Период окупаемости", f"{payback_period:.1f} мес.")
        
        st.info("💡 **Бенчмарки LTV/CAC:**")
        st.write("• Отлично: >5")
        st.write("• Хорошо: 3-5")
        st.write("• Приемлемо: 2-3")
        st.write("• Плохо: <2")
    
    # Save data
    st.session_state.calculator_data.update({
        'repeat_purchase_rate': repeat_purchase_rate,
        'avg_purchases_per_year': avg_purchases_per_year,
        'customer_lifespan_months': customer_lifespan_months,
        'cross_sell_revenue': cross_sell_revenue,
        'referral_bonus': referral_bonus,
        'ltv': ltv,
        'cac': cac,
        'ltv_cac_ratio': ltv_cac_ratio if cac > 0 else 0,
        'payback_period': payback_period
    })

def step_8_profit_analysis():
    st.subheader("💎 Этап 8: Анализ прибыльности")
    
    # Calculate unit economics
    calculator = UnitEconomicsCalculator()
    result = calculator.calculate_unit_economics(st.session_state.calculator_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Структура затрат")
        
        # Create breakdown chart
        costs_data = {
            'Себестоимость': result['total_cogs'],
            'Маркетплейс': result['marketplace_costs'],
            'Маркетинг': result['marketing_costs'],
            'Операционные': result['operational_costs']
        }
        
        fig_costs = px.pie(
            values=list(costs_data.values()),
            names=list(costs_data.keys()),
            title="Структура затрат на единицу товара"
        )
        st.plotly_chart(fig_costs, use_container_width=True)
        
        st.write("#### Детализация расходов")
        for cost_type, amount in costs_data.items():
            percentage = (amount / result['selling_price']) * 100 if result['selling_price'] > 0 else 0
            st.write(f"• {cost_type}: {amount:,.0f} ₽ ({percentage:.1f}%)")
    
    with col2:
        st.write("#### Ключевые метрики")
        
        st.metric("Цена продажи", f"{result['selling_price']:,.0f} ₽")
        st.metric("Общие затраты", f"{result['total_costs']:,.0f} ₽")
        st.metric(
            "Прибыль с единицы", 
            f"{result['unit_profit']:+,.0f} ₽",
            delta=f"{result['profit_margin']:.1f}%"
        )
        
        if result['profit_margin'] >= 20:
            st.success(f"✅ Хорошая маржинальность ({result['profit_margin']:.1f}%)")
        elif result['profit_margin'] >= 10:
            st.warning(f"⚠️ Низкая маржинальность ({result['profit_margin']:.1f}%)")
        else:
            st.error(f"🔴 Убыточность ({result['profit_margin']:.1f}%)")
        
        st.write("#### P.R.O.F.I.T. Анализ")
        profit_score = calculator.calculate_profit_score(result)
        
        st.metric("P.R.O.F.I.T. Score", f"{profit_score}/100")
        
        if profit_score >= 80:
            st.success("🎯 Отличная прибыльность")
        elif profit_score >= 60:
            st.warning("⚠️ Требует оптимизации")
        else:
            st.error("🔴 Критические проблемы")
        
        breakeven_price = result['total_costs'] / 0.8  # 20% минимальная маржа
        st.metric("Точка безубыточности", f"{breakeven_price:,.0f} ₽")
    
    # Save results
    st.session_state.calculator_data.update(result)

def step_9_scenario_planning():
    st.subheader("🎯 Этап 9: Сценарное планирование")
    
    base_data = st.session_state.calculator_data
    calculator = UnitEconomicsCalculator()
    
    # Scenario definitions
    scenarios = {
        'Пессимистичный': {
            'price_change': -0.15,
            'cost_change': 0.10,
            'volume_change': -0.30,
            'marketing_efficiency': -0.20
        },
        'Реалистичный': {
            'price_change': 0.00,
            'cost_change': 0.05,
            'volume_change': 0.00,
            'marketing_efficiency': 0.00
        },
        'Оптимистичный': {
            'price_change': 0.10,
            'cost_change': -0.05,
            'volume_change': 0.50,
            'marketing_efficiency': 0.25
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Параметры сценариев")
        
        selected_scenario = st.selectbox(
            "Выберите сценарий для детального анализа:",
            list(scenarios.keys()),
            index=1,
            key="selected_scenario"
        )
        
        scenario_params = scenarios[selected_scenario]
        
        st.write(f"**{selected_scenario} сценарий:**")
        st.write(f"• Изменение цены: {scenario_params['price_change']:+.0%}")
        st.write(f"• Изменение затрат: {scenario_params['cost_change']:+.0%}")
        st.write(f"• Изменение объема: {scenario_params['volume_change']:+.0%}")
        st.write(f"• Эффективность маркетинга: {scenario_params['marketing_efficiency']:+.0%}")
        
        # Custom scenario inputs
        st.write("#### Кастомный сценарий")
        custom_price_change = st.slider("Изменение цены (%):", -50, 50, 0, key="custom_price")
        custom_cost_change = st.slider("Изменение затрат (%):", -30, 30, 0, key="custom_cost")
        custom_volume_change = st.slider("Изменение объема (%):", -50, 100, 0, key="custom_volume")
    
    with col2:
        st.write("#### Сравнение сценариев")
        
        # Calculate scenarios
        scenario_results = {}
        for name, params in scenarios.items():
            scenario_data = base_data.copy()
            scenario_data['selling_price'] *= (1 + params['price_change'])
            scenario_data['total_cost'] *= (1 + params['cost_change'])
            scenario_data['monthly_sales_volume'] *= (1 + params['volume_change'])
            
            result = calculator.calculate_unit_economics(scenario_data)
            scenario_results[name] = result
        
        # Create comparison table
        comparison_df = pd.DataFrame({
            name: {
                'Цена (₽)': f"{result['selling_price']:,.0f}",
                'Прибыль (₽)': f"{result['unit_profit']:+,.0f}",
                'Маржа (%)': f"{result['profit_margin']:.1f}%",
                'Месячная прибыль (₽)': f"{result['unit_profit'] * base_data.get('monthly_sales_volume', 100) * (1 + scenarios[name]['volume_change']):+,.0f}"
            }
            for name, result in scenario_results.items()
        })
        
        st.dataframe(comparison_df)
        
        # Visualization
        fig_scenarios = go.Figure()
        
        for name, result in scenario_results.items():
            fig_scenarios.add_trace(go.Bar(
                name=name,
                x=['Прибыль на единицу'],
                y=[result['unit_profit']],
                text=[f"{result['unit_profit']:+,.0f} ₽"],
                textposition='auto'
            ))
        
        fig_scenarios.update_layout(
            title="Сравнение прибыли по сценариям",
            yaxis_title="Прибыль (₽)",
            showlegend=True
        )
        
        st.plotly_chart(fig_scenarios, use_container_width=True)
    
    # Risk analysis
    st.write("#### Анализ рисков")
    
    worst_case = scenario_results['Пессимистичный']
    best_case = scenario_results['Оптимистичный']
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric(
            "Худший случай",
            f"{worst_case['unit_profit']:+,.0f} ₽",
            f"{worst_case['profit_margin']:.1f}%"
        )
    
    with col4:
        st.metric(
            "Базовый случай",
            f"{scenario_results['Реалистичный']['unit_profit']:+,.0f} ₽",
            f"{scenario_results['Реалистичный']['profit_margin']:.1f}%"
        )
    
    with col5:
        st.metric(
            "Лучший случай",
            f"{best_case['unit_profit']:+,.0f} ₽",
            f"{best_case['profit_margin']:.1f}%"
        )
    
    # Save scenario data
    st.session_state.calculator_data.update({
        'scenarios': scenario_results,
        'selected_scenario': selected_scenario
    })

def step_10_recommendations():
    st.subheader("🎯 Этап 10: Рекомендации и план действий")
    
    data = st.session_state.calculator_data
    calculator = UnitEconomicsCalculator()
    recommendations = calculator.generate_recommendations(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 🚨 Критические проблемы")
        for issue in recommendations.get('critical_issues', []):
            st.error(f"🔴 {issue}")
        
        st.write("#### ⚠️ Области для улучшения")
        for improvement in recommendations.get('improvements', []):
            st.warning(f"⚠️ {improvement}")
        
        st.write("#### ✅ Сильные стороны")
        for strength in recommendations.get('strengths', []):
            st.success(f"✅ {strength}")
    
    with col2:
        st.write("#### 📋 План действий")
        
        action_plan = recommendations.get('action_plan', {})
        
        if 'immediate' in action_plan:
            st.write("**Немедленные действия (1-2 недели):**")
            for action in action_plan['immediate']:
                st.write(f"• {action}")
        
        if 'short_term' in action_plan:
            st.write("**Краткосрочные (1-3 месяца):**")
            for action in action_plan['short_term']:
                st.write(f"• {action}")
        
        if 'long_term' in action_plan:
            st.write("**Долгосрочные (3-12 месяцев):**")
            for action in action_plan['long_term']:
                st.write(f"• {action}")
    
    st.write("#### 📊 P.R.O.F.I.T. Матрица развития")
    
    profit_analysis = recommendations.get('profit_matrix', {})
    
    # Create P.R.O.F.I.T. visualization
    profit_categories = ['Profitability', 'Resource Optimization', 'Operations Excellence', 
                        'Financial Intelligence', 'Intelligence Automation', 'Transformation Strategy']
    profit_scores = [profit_analysis.get(cat, 50) for cat in profit_categories]
    
    fig_profit = go.Figure()
    
    fig_profit.add_trace(go.Scatterpolar(
        r=profit_scores,
        theta=profit_categories,
        fill='toself',
        name='Текущее состояние'
    ))
    
    # Add target scores
    target_scores = [85, 80, 75, 80, 70, 75]  # Target benchmarks
    fig_profit.add_trace(go.Scatterpolar(
        r=target_scores,
        theta=profit_categories,
        fill='toself',
        name='Целевые показатели',
        opacity=0.3
    ))
    
    fig_profit.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="P.R.O.F.I.T. Анализ"
    )
    
    st.plotly_chart(fig_profit, use_container_width=True)
    
    # Final summary
    st.write("#### 📈 Итоговые метрики")
    
    col3, col4, col5, col6 = st.columns(4)
    
    with col3:
        st.metric(
            "Прибыль на единицу",
            f"{data.get('unit_profit', 0):+,.0f} ₽"
        )
    
    with col4:
        st.metric(
            "Маржинальность",
            f"{data.get('profit_margin', 0):.1f}%"
        )
    
    with col5:
        st.metric(
            "LTV/CAC",
            f"{data.get('ltv_cac_ratio', 0):.1f}"
        )
    
    with col6:
        st.metric(
            "P.R.O.F.I.T. Score",
            f"{recommendations.get('total_score', 0)}/100"
        )

def dashboard_page():
    st.header("📊 Дашборд аналитики")
    
    if not st.session_state.calculator_data:
        st.warning("⚠️ Сначала выполните расчет в калькуляторе")
        return
    
    data = st.session_state.calculator_data
    
    # Key metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Выручка",
            f"{data.get('selling_price', 0):,.0f} ₽",
            help="Цена продажи товара"
        )
    
    with col2:
        st.metric(
            "Затраты",
            f"{data.get('total_costs', 0):,.0f} ₽",
            help="Общие затраты на единицу"
        )
    
    with col3:
        profit_color = "normal" if data.get('unit_profit', 0) >= 0 else "inverse"
        st.metric(
            "Прибыль",
            f"{data.get('unit_profit', 0):+,.0f} ₽",
            f"{data.get('profit_margin', 0):.1f}%"
        )
    
    with col4:
        st.metric(
            "LTV/CAC",
            f"{data.get('ltv_cac_ratio', 0):.1f}",
            help="Соотношение жизненной ценности клиента к стоимости привлечения"
        )
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost breakdown
        if 'total_cogs' in data:
            costs = {
                'Себестоимость': data.get('total_cogs', 0),
                'Маркетплейс': data.get('marketplace_costs', 0),
                'Маркетинг': data.get('marketing_costs', 0),
                'Операционные': data.get('operational_costs', 0)
            }
            
            fig_costs = px.pie(
                values=list(costs.values()),
                names=list(costs.keys()),
                title="Структура затрат"
            )
            st.plotly_chart(fig_costs, use_container_width=True)
    
    with col2:
        # Scenario comparison
        if 'scenarios' in data:
            scenarios = data['scenarios']
            scenario_names = list(scenarios.keys())
            profits = [scenarios[name]['unit_profit'] for name in scenario_names]
            
            fig_scenarios = px.bar(
                x=scenario_names,
                y=profits,
                title="Сравнение сценариев",
                labels={'x': 'Сценарий', 'y': 'Прибыль (₽)'}
            )
            st.plotly_chart(fig_scenarios, use_container_width=True)
    
    # Detailed analysis
    st.subheader("📋 Детальный анализ")
    
    # Create analysis table
    if data:
        analysis_data = {
            'Метрика': [
                'Цена продажи',
                'Себестоимость',
                'Комиссия маркетплейса',
                'Маркетинговые расходы',
                'Операционные расходы',
                'Общие затраты',
                'Прибыль с единицы',
                'Маржинальность',
                'LTV',
                'CAC',
                'Период окупаемости'
            ],
            'Значение (₽)': [
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
                f"{data.get('payback_period', 0):.1f} мес."
            ],
            'Доля от выручки (%)': [
                "100.0%",
                f"{(data.get('total_cogs', 0) / data.get('selling_price', 1)) * 100:.1f}%",
                f"{(data.get('marketplace_costs', 0) / data.get('selling_price', 1)) * 100:.1f}%",
                f"{(data.get('marketing_costs', 0) / data.get('selling_price', 1)) * 100:.1f}%",
                f"{(data.get('operational_costs', 0) / data.get('selling_price', 1)) * 100:.1f}%",
                f"{(data.get('total_costs', 0) / data.get('selling_price', 1)) * 100:.1f}%",
                f"{data.get('profit_margin', 0):.1f}%",
                "-",
                "-",
                "-",
                "-"
            ]
        }
        
        df_analysis = pd.DataFrame(analysis_data)
        st.dataframe(df_analysis, use_container_width=True)

def methodology_page():
    st.header("📚 Методология расчетов")
    
    st.markdown("""
    ## 🎯 Что такое юнит-экономика на маркетплейсах
    
    Юнит-экономика - это анализ прибыли и убытков на уровне одной единицы товара или одного клиента. 
    На маркетплейсах это означает понимание того, сколько вы зарабатываете или теряете с каждой продажи 
    после вычета всех связанных расходов.
    
    ### Ключевая формула:
    