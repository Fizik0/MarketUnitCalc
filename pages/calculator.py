"""
Модуль для пошагового калькулятора юнит-экономики
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data.marketplace_data import (
    MARKETPLACE_COMMISSIONS, 
    BENCHMARKS, 
    get_marketplace_commission,
    get_category_benchmark
)

def validate_current_step() -> bool:
    """Валидация текущего этапа"""
    current_step = st.session_state.current_step
    data = st.session_state.calculator_data
    
    # Валидация для каждого этапа
    if current_step == 1:
        return bool(data.get('marketplace') and data.get('category'))
    elif current_step == 2:
        return bool(data.get('product_name') and data.get('selling_price', 0) > 0)
    elif current_step == 3:
        return data.get('purchase_cost', 0) > 0
    elif current_step == 4:
        return data.get('commission_rate', 0) > 0
    elif current_step == 5:
        return data.get('ppc_budget_percent', 0) >= 0
    elif current_step == 6:
        return data.get('monthly_sales_volume', 0) > 0
    elif current_step == 7:
        return data.get('customer_lifespan_months', 0) > 0
    elif current_step == 8:
        return True  # Этап расчетов, всегда валиден
    elif current_step == 9:
        return True  # Сценарии, всегда валидны
    elif current_step == 10:
        return True  # Рекомендации, всегда валидны
    
    return True

def show_step_progress():
    """Отображение прогресса выполнения этапов"""
    progress = (st.session_state.current_step - 1) / 10
    st.progress(progress)
    
    # Цветовые индикаторы этапов
    cols = st.columns(10)
    for i in range(10):
        with cols[i]:
            step_num = i + 1
            if step_num in st.session_state.completed_steps:
                st.success(f"✅ {step_num}")
            elif step_num == st.session_state.current_step:
                st.info(f"▶️ {step_num}")
            else:
                st.write(f"⭕ {step_num}")

def step_1_marketplace_selection():
    """Этап 1: Выбор маркетплейса и категории"""
    st.subheader("🛒 Этап 1: Выбор маркетплейса и категории")
    
    col1, col2 = st.columns(2)
    
    with col1:
        marketplace = st.selectbox(
            "Выберите маркетплейс:",
            ["OZON", "Wildberries", "Яндекс.Маркет", "Авито", "Другой"],
            key="marketplace",
            help="Каждый маркетплейс имеет уникальную структуру комиссий и алгоритмы ранжирования"
        )
        
        if marketplace in MARKETPLACE_COMMISSIONS:
            categories = list(MARKETPLACE_COMMISSIONS[marketplace].keys())
            category = st.selectbox(
                "Выберите категорию товара:",
                categories,
                key="category",
                help="Комиссии сильно различаются в зависимости от категории"
            )
        else:
            category = st.text_input(
                "Введите категорию товара:", 
                key="category",
                help="Укажите категорию для более точных расчетов"
            )
    
    with col2:
        st.info("💡 **Почему это важно?**")
        st.write("• Каждый маркетплейс имеет уникальную структуру комиссий")
        st.write("• Алгоритмы ранжирования различаются")
        st.write("• Аудитория и поведение покупателей отличаются")
        
        if marketplace == "OZON":
            commission_data = get_marketplace_commission(marketplace, category)
            st.warning("📊 **Особенности OZON:**")
            st.write(f"• Комиссия: {commission_data['commission_rate']:.1f}%")
            st.write(f"• Обязательная маркетинговая комиссия: {commission_data.get('mandatory_marketing', 2):.1f}%")
            st.write("• Интеграция с Озон Премиум влияет на конверсию")
            st.write("• Алгоритм наказывает за частые изменения цен")
        elif marketplace == "Wildberries":
            st.success("📊 **Особенности Wildberries:**")
            st.write("• Более низкие комиссии")
            st.write("• Высокая конкуренция")
            st.write("• Больший процент возвратов в одежде")
        elif marketplace == "Яндекс.Маркет":
            st.info("📊 **Особенности Яндекс.Маркет:**")
            st.write("• Самые низкие комиссии")
            st.write("• Фокус на качество и сервис")
            st.write("• Интеграция с экосистемой Яндекса")
    
    # Показать бенчмарки категории
    if marketplace in BENCHMARKS and category in BENCHMARKS[marketplace]:
        benchmark = get_category_benchmark(marketplace, category)
        
        st.subheader("📈 Бенчмарки категории")
        col3, col4, col5, col6 = st.columns(4)
        
        with col3:
            st.metric("Средняя цена", f"{benchmark['avg_price']:,.0f} ₽")
        with col4:
            st.metric("Конверсия", f"{benchmark['avg_conversion']:.1%}")
        with col5:
            st.metric("Возвраты", f"{benchmark['avg_return_rate']:.1%}")
        with col6:
            st.metric("Маржа", f"{benchmark['avg_margin']:.1%}")
    
    # Сохранение данных
    st.session_state.calculator_data.update({
        'marketplace': marketplace,
        'category': category
    })

def step_2_product_info():
    """Этап 2: Информация о товаре"""
    st.subheader("📦 Этап 2: Информация о товаре")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input(
            "Название товара:", 
            key="product_name",
            help="Укажите точное название для отчетов"
        )
        
        selling_price = st.number_input(
            "Цена продажи (₽):", 
            min_value=0.0, 
            step=1.0, 
            key="selling_price",
            help="Цена, по которой товар продается покупателю"
        )
        
        weight = st.number_input(
            "Вес товара (кг):", 
            min_value=0.0, 
            step=0.1, 
            key="weight",
            help="Влияет на стоимость логистики"
        )
        
        dimensions = st.text_input(
            "Габариты (Д×Ш×В, см):", 
            key="dimensions",
            help="Например: 30×20×10"
        )
        
        # Дополнительные характеристики
        with st.expander("🔧 Дополнительные характеристики"):
            product_type = st.selectbox(
                "Тип товара:",
                ["Готовый товар", "Private Label", "Dropshipping", "Handmade"],
                key="product_type"
            )
            
            target_audience = st.selectbox(
                "Целевая аудитория:",
                ["Массмаркет", "Премиум", "Luxury", "B2B"],
                key="target_audience"
            )
            
            seasonality = st.selectbox(
                "Сезонность:",
                ["Несезонный", "Весна-лето", "Осень-зима", "Новогодний"],
                key="seasonality"
            )
    
    with col2:
        st.info("📊 **Анализ по категории**")
        
        marketplace = st.session_state.calculator_data.get('marketplace', 'OZON')
        category = st.session_state.calculator_data.get('category', 'Электроника')
        
        if marketplace in BENCHMARKS and category in BENCHMARKS[marketplace]:
            benchmarks = BENCHMARKS[marketplace][category]
            
            # Показать бенчмарки
            st.metric("Средняя цена в категории", f"{benchmarks['avg_price']:,.0f} ₽")
            st.metric("Средняя конверсия", f"{benchmarks['avg_conversion']:.1%}")
            st.metric("Средний возврат", f"{benchmarks['avg_return_rate']:.1%}")
            
            # Анализ цены
            if selling_price > 0:
                price_ratio = selling_price / benchmarks['avg_price']
                
                if price_ratio > 1.5:
                    st.warning("⚠️ Цена значительно выше средней по категории")
                    st.write("💡 Убедитесь в уникальности предложения")
                elif price_ratio < 0.7:
                    st.error("🔴 Цена может быть слишком низкой")
                    st.write("💡 Проверьте расчет себестоимости")
                else:
                    st.success("✅ Цена в пределах рыночного диапазона")
        
        # Калькулятор логистических расходов
        if weight > 0:
            st.write("#### 📦 Предварительная логистика")
            
            commission_data = get_marketplace_commission(marketplace, category)
            estimated_fulfillment = commission_data['fulfillment_base']
            
            if weight > 1.0:
                estimated_fulfillment += (weight - 1.0) * 30
            
            st.metric("Ориентировочный фулфилмент", f"{estimated_fulfillment:.0f} ₽")
            
            # Расчет габаритного веса для некоторых маркетплейсов
            if dimensions:
                try:
                    dims = [float(x.strip()) for x in dimensions.replace('×', 'x').split('x')]
                    if len(dims) == 3:
                        volume_weight = (dims[0] * dims[1] * dims[2]) / 5000  # Стандартный коэффициент
                        actual_weight = max(weight, volume_weight)
                        
                        if actual_weight > weight:
                            st.warning(f"⚠️ Габаритный вес: {actual_weight:.1f} кг")
                            st.write("Товар будет тарифицироваться по габаритному весу")
                except:
                    pass
    
    # Сохранение данных
    st.session_state.calculator_data.update({
        'product_name': product_name,
        'selling_price': selling_price,
        'weight': weight,
        'dimensions': dimensions,
        'product_type': st.session_state.get('product_type', 'Готовый товар'),
        'target_audience': st.session_state.get('target_audience', 'Массмаркет'),
        'seasonality': st.session_state.get('seasonality', 'Несезонный')
    })

def step_3_cost_structure():
    """Этап 3: Структура себестоимости"""
    st.subheader("💰 Этап 3: Структура себестоимости")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Прямые затраты")
        
        purchase_cost = st.number_input(
            "Закупочная стоимость (₽):", 
            min_value=0.0, 
            step=1.0, 
            key="purchase_cost",
            help="Стоимость товара от поставщика"
        )
        
        packaging_cost = st.number_input(
            "Упаковка (₽):", 
            min_value=0.0, 
            step=1.0, 
            value=25.0, 
            key="packaging_cost",
            help="Коробка, пленка, защитные материалы"
        )
        
        labeling_cost = st.number_input(
            "Маркировка/этикетки (₽):", 
            min_value=0.0, 
            step=1.0, 
            key="labeling_cost",
            help="Честный ЗНАК, штрих-коды, этикетки"
        )
        
        st.write("#### Дополнительные расходы")
        
        quality_control = st.number_input(
            "Контроль качества (₽):", 
            min_value=0.0, 
            step=1.0, 
            key="quality_control",
            help="Проверка товара перед отправкой"
        )
        
        certification = st.number_input(
            "Сертификация (₽ на единицу):", 
            min_value=0.0, 
            step=1.0, 
            key="certification",
            help="Распределенная стоимость сертификатов"
        )
        
        # Дополнительные расходы в зависимости от типа товара
        product_type = st.session_state.calculator_data.get('product_type', 'Готовый товар')
        
        if product_type == "Private Label":
            st.write("#### Private Label расходы")
            
            design_cost = st.number_input(
                "Дизайн и разработка (₽ на единицу):", 
                min_value=0.0, 
                step=1.0, 
                key="design_cost",
                help="Распределенная стоимость разработки"
            )
            
            tooling_cost = st.number_input(
                "Оснастка и инструменты (₽ на единицу):", 
                min_value=0.0, 
                step=1.0, 
                key="tooling_cost",
                help="Распределенная стоимость оснастки"
            )
        else:
            design_cost = 0
            tooling_cost = 0
    
    with col2:
        # Расчет общей себестоимости
        total_cost = (purchase_cost + packaging_cost + labeling_cost + 
                     quality_control + certification + design_cost + tooling_cost)
        
        selling_price = st.session_state.calculator_data.get('selling_price', 0)
        
        st.metric("💰 Общая себестоимость", f"{total_cost:,.0f} ₽")
        
        if selling_price > 0:
            gross_margin = ((selling_price - total_cost) / selling_price) * 100
            st.metric("📊 Валовая маржа", f"{gross_margin:.1f}%")
            
            # Цветовые индикаторы
            margin_container = st.container()
            with margin_container:
                if gross_margin < 30:
                    st.error("🔴 Низкая валовая маржа (< 30%)")
                    st.write("💡 **Рекомендации:**")
                    st.write("• Пересмотрите поставщиков")
                    st.write("• Оптимизируйте упаковку")
                    st.write("• Рассмотрите повышение цены")
                elif gross_margin < 50:
                    st.warning("⚠️ Умеренная валовая маржа (30-50%)")
                    st.write("💡 **Рекомендации:**")
                    st.write("• Ищите способы снижения COGS")
                    st.write("• Работайте над добавленной стоимостью")
                else:
                    st.success("✅ Хорошая валовая маржа (> 50%)")
                    st.write("💡 **Отлично!**")
                    st.write("• Есть запас для маркетинга")
                    st.write("• Возможность конкурировать по цене")
        
        # Бенчмарки по валовой марже
        st.info("📊 **Бенчмарки по валовой марже:**")
        category = st.session_state.calculator_data.get('category', 'Электроника')
        
        category_benchmarks = {
            'Электроника': "20-40%",
            'Одежда и обувь': "50-70%",
            'Товары для дома': "40-60%",
            'Красота и здоровье': "60-80%",
            'Детские товары': "40-65%",
            'Спорт и отдых': "35-55%",
            'Автотовары': "30-50%",
            'Книги': "40-60%"
        }
        
        benchmark = category_benchmarks.get(category, "30-50%")
        st.write(f"• {category}: {benchmark}")
        
        # Анализ структуры затрат
        if total_cost > 0:
            st.write("#### 📊 Структура затрат")
            
            cost_breakdown = {
                'Закупочная стоимость': purchase_cost,
                'Упаковка': packaging_cost,
                'Маркировка': labeling_cost,
                'Контроль качества': quality_control,
                'Сертификация': certification
            }
            
            if product_type == "Private Label":
                cost_breakdown['Дизайн'] = design_cost
                cost_breakdown['Оснастка'] = tooling_cost
            
            # Фильтруем нулевые значения
            cost_breakdown = {k: v for k, v in cost_breakdown.items() if v > 0}
            
            if cost_breakdown:
                fig_costs = px.pie(
                    values=list(cost_breakdown.values()),
                    names=list(cost_breakdown.keys()),
                    title="Структура себестоимости"
                )
                st.plotly_chart(fig_costs, use_container_width=True)
    
    # Сохранение данных
    st.session_state.calculator_data.update({
        'purchase_cost': purchase_cost,
        'packaging_cost': packaging_cost,
        'labeling_cost': labeling_cost,
        'quality_control': quality_control,
        'certification': certification,
        'design_cost': design_cost,
        'tooling_cost': tooling_cost,
        'total_cost': total_cost
    })

# Остальные функции этапов можно добавить аналогичным образом...
