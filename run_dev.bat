@echo off
echo ============================================
echo Запуск Калькулятора Юнит-Экономики в режиме разработки
echo ============================================

if not exist venv (
    echo Создание виртуального окружения...
    python -m venv venv
)

call venv\Scripts\activate

echo Установка зависимостей...
pip install -r requirements.txt

echo Установка дополнительных пакетов...
pip install watchdog streamlit streamlit-option-menu

echo Запуск приложения...
streamlit run app.py

pause