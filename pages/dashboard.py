"""
Модуль дашборда с аналитикой и визуализацией
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from utils.calculations import UnitEconomicsCalculator
from data.marketplace_data import BENCHMARKS, get_category_benchmark

def create_dashboard():
    """Создание дашборда с аналитикой"""
    st.header("📊 Дашборд аналитики")
    
    if not st.session_state.calculator_data:
        st.warning("⚠️ Сначала выполните расчет в калькуляторе")
        return
    
    data = st.session_state.calculator_data
    
    # Основные метрики
    show_key_metrics(data)
    
    # Детальная аналитика
    col1, col2 = st.columns(2)
    
    with col1:
        show_cost_breakdown(data)
        show_profitability_analysis(data)
    
    with col2:
        show_scenario_comparison(data)
        show_benchmark_comparison(data)
    
    # Дополнительные аналитические блоки
    show_ltv_cac_analysis(data)
    show_profit_matrix(data)
    show_recommendations_summary(data)

def show_key_metrics(data):
    """Отображение ключевых метрик"""
    st.subheader("🎯 Ключевые метрики")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "💰 Выручка",
            f"{data.get('selling_price', 0):,.0f} ₽",
            help="Цена продажи товара"
        )
    
    with col2:
        st.metric(
            "💸 Затраты",
            f"{data.get('total_costs', 0):,.0f} ₽",
            help="Общие затраты на единицу"
        )
    
    with col3:
        unit_profit = data.get('unit_profit', 0)
        profit_color = "normal" if unit_profit >= 0 else "inverse"
        st.metric(
            "💎 Прибыль",
            f"{unit_profit:+,.0f} ₽",
            f"{data.get('profit_margin', 0):.1f}%"
        )
    
    with col4:
        ltv_cac = data.get('ltv_cac_ratio', 0)
        st.metric(
            "📈 LTV/CAC",
            f"{ltv_cac:.1f}",
            help="Соотношение жизненной ценности клиента к стоимости привлечения"
        )
    
    with col5:
        profit_score = data.get('profit_score', 0)
        st.metric(
            "🎯 P.R.O.F.I.T.",
            f"{profit_score}/100",
            help="Общая оценка прибыльности бизнеса"
        )

def show_cost_breakdown(data):
    """Детализация структуры затрат"""
    st.subheader("💰 Структура затрат")
    
    if 'total_cogs' in data:
        costs = {
            'Себестоимость': data.get('total_cogs', 0),
            'Маркетплейс': data.get('marketplace_costs', 0),
            'Маркетинг': data.get('marketing_costs', 0),
            'Операционные': data.get('operational_costs', 0)
        }
        
        # Убираем нулевые значения
        costs = {k: v for k, v in costs.items() if v > 0}
        
        if costs:
            fig_costs = px.pie(
                values=list(costs.values()),
                names=list(costs.keys()),
                title="Распределение затрат",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_costs.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Сумма: %{value:,.0f} ₽<br>Доля: %{percent}<extra></extra>'
            )
            
            st.plotly_chart(fig_costs, use_container_width=True)
            
            # Таблица с детализацией
            selling_price = data.get('selling_price', 1)
            cost_table = []
            
            for category, amount in costs.items():
                percentage = (amount / selling_price) * 100
                cost_table.append({
                    'Категория': category,
                    'Сумма (₽)': f"{amount:,.0f}",
                    'Доля от цены (%)': f"{percentage:.1f}%"
                })
            
            df_costs = pd.DataFrame(cost_table)
            st.dataframe(df_costs, use_container_width=True, hide_index=True)

def show_profitability_analysis(data):
    """Анализ прибыльности"""
    st.subheader("📊 Анализ прибыльности")
    
    selling_price = data.get('selling_price', 0)
    total_costs = data.get('total_costs', 0)
    unit_profit = data.get('unit_profit', 0)
    
    # Водопадная диаграмма
    categories = ['Выручка', 'Себестоимость', 'Маркетплейс', 'Маркетинг', 'Операционные', 'Прибыль']
    values = [
        selling_price,
        -data.get('total_cogs', 0),
        -data.get('marketplace_costs', 0),
        -data.get('marketing_costs', 0),
        -data.get('operational_costs', 0),
        unit_profit
    ]
    
    fig_waterfall = go.Figure(go.Waterfall(
        name="Структура прибыли",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"{v:+,.0f}" for v in values],
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig_waterfall.update_layout(
        title="Формирование прибыли с единицы товара",
        showlegend=False,
        xaxis_title="Компоненты",
        yaxis_title="Сумма (₽)"
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True)

def show_scenario_comparison(data):
    """Сравнение сценариев"""
    st.subheader("🎯 Сравнение сценариев")
    
    if 'scenarios' in data:
        scenarios = data['scenarios']
        
        # Создаем данные для сравнения
        scenario_names = list(scenarios.keys())
        profits = [scenarios[name]['unit_profit'] for name in scenario_names]
        margins = [scenarios[name]['profit_margin'] for name in scenario_names]
        
        # Столбчатая диаграмма прибыли
        fig_scenarios = go.Figure()
        
        colors = ['red', 'blue', 'green']  # Пессимистичный, реалистичный, оптимистичный
        
        for i, (name, profit) in enumerate(zip(scenario_names, profits)):
            fig_scenarios.add_trace(go.Bar(
                name=name,
                x=[name],
                y=[profit],
                text=[f"{profit:+,.0f} ₽"],
                textposition='auto',
                marker_color=colors[i % len(colors)],
                hovertemplate=f'<b>{name}</b><br>Прибыль: %{{y:+,.0f}} ₽<br>Маржа: {margins[i]:.1f}%<extra></extra>'
            ))
        
        fig_scenarios.update_layout(
            title="Прибыль по сценариям",
            xaxis_title="Сценарий",
            yaxis_title="Прибыль (₽)",
            showlegend=False
        )
        
        st.plotly_chart(fig_scenarios, use_container_width=True)
        
        # Таблица сравнения
        monthly_volume = data.get('monthly_sales_volume', 100)
        
        comparison_data = []
        for name, result in scenarios.items():
            monthly_profit = result['unit_profit'] * monthly_volume
            comparison_data.append({
                'Сценарий': name,
                'Прибыль/ед. (₽)': f"{result['unit_profit']:+,.0f}",
                'Маржа (%)': f"{result['profit_margin']:.1f}%",
                'Месячная прибыль (₽)': f"{monthly_profit:+,.0f}"
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    else:
        st.info("Сравнение сценариев будет доступно после завершения всех этапов калькулятора")

def show_benchmark_comparison(data):
    """Сравнение с отраслевыми бенчмарками"""
    st.subheader("📈 Сравнение с рынком")
    
    marketplace = data.get('marketplace', 'OZON')
    category = data.get('category', 'Электроника')
    
    if marketplace in BENCHMARKS and category in BENCHMARKS[marketplace]:
        benchmark = get_category_benchmark(marketplace, category)
        
        # Сравнение ключевых метрик
        current_margin = data.get('profit_margin', 0) / 100
        benchmark_margin = benchmark.get('avg_margin', 0.25)
        
        current_ltv_cac = data.get('ltv_cac_ratio', 0)
        benchmark_ltv_cac = benchmark.get('avg_ltv_cac', 3.0)
        
        # Радарная диаграмма
        categories = ['Маржинальность', 'LTV/CAC', 'Конверсия*', 'Возвраты*']
        
        current_values = [
            min(100, current_margin * 100),
            min(100, current_ltv_cac * 20),  # Нормализация для визуализации
            data.get('conversion_rate', benchmark.get('avg_conversion', 0.025)) * 4000,  # Нормализация
            100 - (data.get('return_rate', benchmark.get('avg_return_rate', 0.12)) * 100)  # Инвертируем для лучшей визуализации
        ]
        
        benchmark_values = [
            benchmark_margin * 100,
            benchmark_ltv_cac * 20,
            benchmark.get('avg_conversion', 0.025) * 4000,
            100 - (benchmark.get('avg_return_rate', 0.12) * 100)
        ]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=current_values,
            theta=categories,
            fill='toself',
            name='Ваши показатели',
            line_color='blue'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=benchmark_values,
            theta=categories,
            fill='toself',
            name='Рыночные бенчмарки',
            line_color='red',
            opacity=0.6
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Сравнение с рыночными показателями"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.caption("*Конверсия и возвраты нормализованы для визуализации")
        
        # Текстовое сравнение
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Ваши показатели:**")
            st.write(f"• Маржинальность: {current_margin:.1%}")
            st.write(f"• LTV/CAC: {current_ltv_cac:.1f}")
        
        with col2:
            st.write("**Рыночные бенчмарки:**")
            st.write(f"• Маржинальность: {benchmark_margin:.1%}")
            st.write(f"• LTV/CAC: {benchmark_ltv_cac:.1f}")
    else:
        st.info("Бенчмарки недоступны для выбранной комбинации маркетплейса и категории")

def show_ltv_cac_analysis(data):
    """Анализ LTV/CAC"""
    st.subheader("👥 Анализ LTV/CAC")
    
    ltv = data.get('ltv', 0)
    cac = data.get('cac', 0)
    ltv_cac_ratio = data.get('ltv_cac_ratio', 0)
    payback_period = data.get('payback_period', 0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Визуализация LTV vs CAC
        fig_ltv_cac = go.Figure()
        
        # Добавляем точку текущих значений
        fig_ltv_cac.add_trace(go.Scatter(
            x=[cac],
            y=[ltv],
            mode='markers',
            marker=dict(size=20, color='blue'),
            name='Ваш товар',
            text=[f'LTV: {ltv:,.0f}₽<br>CAC: {cac:,.0f}₽<br>Ratio: {ltv_cac_ratio:.1f}'],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        # Добавляем зоны эффективности
        x_range = np.linspace(0, max(cac * 1.5, 1000), 100)
        
        # Зона убыточности (LTV < CAC)
        fig_ltv_cac.add_trace(go.Scatter(
            x=x_range,
            y=x_range,
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Зона убыточности (LTV=CAC)',
            hoverinfo='skip'
        ))
        
        # Зона минимальной эффективности (LTV = 2*CAC)
        fig_ltv_cac.add_trace(go.Scatter(
            x=x_range,
            y=x_range * 2,
            mode='lines',
            line=dict(color='orange', dash='dash'),
            name='Минимальная эффективность (2:1)',
            hoverinfo='skip'
        ))
        
        # Зона хорошей эффективности (LTV = 3*CAC)
        fig_ltv_cac.add_trace(go.Scatter(
            x=x_range,
            y=x_range * 3,
            mode='lines',
            line=dict(color='green', dash='dash'),
            name='Хорошая эффективность (3:1)',
            hoverinfo='skip'
        ))
        
        fig_ltv_cac.update_layout(
            title='Позиционирование LTV vs CAC',
            xaxis_title='CAC (₽)',
            yaxis_title='LTV (₽)',
            showlegend=True
        )
        
        st.plotly_chart(fig_ltv_cac, use_container_width=True)
    
    with col2:
        # Метрики и рекомендации
        st.write("#### 📊 Оценка эффективности")
        
        if ltv_cac_ratio >= 5:
            st.success("🎯 Отличная эффективность (≥5:1)")
            st.write("• Высокий потенциал для масштабирования")
            st.write("• Можно увеличивать маркетинговый бюджет")
        elif ltv_cac_ratio >= 3:
            st.success("✅ Хорошая эффективность (3-5:1)")
            st.write("• Здоровые показатели приобретения")
            st.write("• Умеренное масштабирование")
        elif ltv_cac_ratio >= 2:
            st.warning("⚠️ Приемлемая эффективность (2-3:1)")
            st.write("• Требует оптимизации")
            st.write("• Ограниченное масштабирование")
        else:
            st.error("🔴 Низкая эффективность (<2:1)")
            st.write("• Критическая ситуация")
            st.write("• Необходима срочная оптимизация")
        
        st.metric("Период окупаемости", f"{payback_period:.1f} мес.")
        
        if payback_period <= 6:
            st.success("✅ Быстрая окупаемость")
        elif payback_period <= 12:
            st.warning("⚠️ Умеренная окупаемость")
        else:
            st.error("🔴 Медленная окупаемость")

def show_profit_matrix(data):
    """P.R.O.F.I.T. матрица"""
    st.subheader("🎯 P.R.O.F.I.T. Матрица")
    
    calculator = UnitEconomicsCalculator()
    recommendations = calculator.generate_recommendations(data)
    profit_matrix = recommendations.get('profit_matrix', {})
    
    if profit_matrix:
        # Создаем радарную диаграмму P.R.O.F.I.T.
        categories = list(profit_matrix.keys())
        values = list(profit_matrix.values())
        
        fig_profit = go.Figure()
        
        fig_profit.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Текущее состояние',
            line_color='blue'
        ))
        
        # Добавляем целевые показатели
        target_values = [85, 80, 75, 80, 70, 75]  # Целевые бенчмарки
        fig_profit.add_trace(go.Scatterpolar(
            r=target_values,
            theta=categories,
            fill='toself',
            name='Целевые показатели',
            line_color='green',
            opacity=0.3
        ))
        
        fig_profit.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="P.R.O.F.I.T. Анализ эффективности бизнеса"
        )
        
        st.plotly_chart(fig_profit, use_container_width=True)
        
        # Детализация по каждому компоненту
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**P** - Profitability:")
            st.write(f"• Оценка: {profit_matrix.get('Profitability', 0):.0f}/100")
            
            st.write("**R** - Resource Optimization:")
            st.write(f"• Оценка: {profit_matrix.get('Resource Optimization', 0):.0f}/100")
        
        with col2:
            st.write("**O** - Operations Excellence:")
            st.write(f"• Оценка: {profit_matrix.get('Operations Excellence', 0):.0f}/100")
            
            st.write("**F** - Financial Intelligence:")
            st.write(f"• Оценка: {profit_matrix.get('Financial Intelligence', 0):.0f}/100")
        
        with col3:
            st.write("**I** - Intelligence Automation:")
            st.write(f"• Оценка: {profit_matrix.get('Intelligence Automation', 0):.0f}/100")
            
            st.write("**T** - Transformation Strategy:")
            st.write(f"• Оценка: {profit_matrix.get('Transformation Strategy', 0):.0f}/100")

def show_recommendations_summary(data):
    """Краткое резюме рекомендаций"""
    st.subheader("💡 Ключевые рекомендации")
    
    calculator = UnitEconomicsCalculator()
    recommendations = calculator.generate_recommendations(data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("#### 🚨 Критические проблемы")
        critical_issues = recommendations.get('critical_issues', [])
        if critical_issues:
            for issue in critical_issues[:3]:  # Показываем только первые 3
                st.error(f"• {issue}")
        else:
            st.success("✅ Критических проблем не выявлено")
    
    with col2:
        st.write("#### ⚠️ Области улучшения")
        improvements = recommendations.get('improvements', [])
        if improvements:
            for improvement in improvements[:3]:
                st.warning(f"• {improvement}")
        else:
            st.info("ℹ️ Основные проблемы решены")
    
    with col3:
        st.write("#### ✅ Сильные стороны")
        strengths = recommendations.get('strengths', [])
        if strengths:
            for strength in strengths[:3]:
                st.success(f"• {strength}")
        else:
            st.info("ℹ️ Завершите расчеты для анализа")
    
    # Общий скор
    total_score = recommendations.get('total_score', 0)
    
    score_container = st.container()
    with score_container:
        st.write("#### 🎯 Общая оценка бизнеса")
        
        progress_col1, progress_col2 = st.columns([3, 1])
        
        with progress_col1:
            st.progress(total_score / 100)
        
        with progress_col2:
            st.metric("Скор", f"{total_score}/100")
        
        if total_score >= 80:
            st.success("🎯 Отличный бизнес! Готов к масштабированию")
        elif total_score >= 60:
            st.warning("⚠️ Хороший потенциал, требует оптимизации")
        elif total_score >= 40:
            st.warning("⚠️ Средние показатели, нужны улучшения")
        else:
            st.error("🔴 Критические проблемы, требует пересмотра стратегии")
