#!/bin/bash

echo "Запуск калькулятора юнит-экономики..."

# Проверка и установка виртуального окружения
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python -m venv venv
fi

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source venv/Scripts/activate

# Установка основных пакетов напрямую
echo "Установка необходимых пакетов..."
pip install streamlit pandas numpy plotly fpdf streamlit-option-menu watchdog

# Запуск приложения
echo "Запуск приложения..."
python -m streamlit run app.py 