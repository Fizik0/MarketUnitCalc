Write-Host "Запуск калькулятора юнит-экономики..." -ForegroundColor Green

# Проверка и установка виртуального окружения
if (-not (Test-Path -Path "venv")) {
    Write-Host "Создание виртуального окружения..." -ForegroundColor Yellow
    python -m venv venv
}

# Активация виртуального окружения
Write-Host "Активация виртуального окружения..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Установка основных пакетов напрямую
Write-Host "Установка необходимых пакетов..." -ForegroundColor Yellow
pip install streamlit pandas numpy plotly fpdf streamlit-option-menu watchdog

# Запуск приложения
Write-Host "Запуск приложения..." -ForegroundColor Green
python -m streamlit run app.py 