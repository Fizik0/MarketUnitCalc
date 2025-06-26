#!/bin/bash

echo "============================================"
echo "Запуск Калькулятора Юнит-Экономики"
echo "============================================"

# Создание виртуального окружения, если его нет
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python -m venv venv
fi

# Активация виртуального окружения
source venv/Scripts/activate || source venv/bin/activate

echo "Установка базовых зависимостей..."
pip install streamlit pandas plotly fpdf streamlit-option-menu watchdog

echo "Проверка порта 5000..."
# Проверяем, занят ли порт 5000
if command -v netstat &> /dev/null; then
    if netstat -ano | grep -q ":5000"; then
        echo "ВНИМАНИЕ: Порт 5000 уже используется. Используем другой порт."
        echo "Запуск приложения на порту 8501 (по умолчанию)..."
        python -m streamlit run app.py
    else
        echo "Запуск приложения..."
        python -m streamlit run app.py
    fi
else
    echo "Запуск приложения..."
    python -m streamlit run app.py
fi 