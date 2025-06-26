"""
Скрипт для запуска тестов проекта
"""
import unittest
import pytest
import sys
import os

if __name__ == "__main__":
    # Проверим, что рабочая директория содержит необходимые модули
    if not os.path.exists("utils") or not os.path.exists("tests"):
        print("ОШИБКА: Скрипт должен запускаться из корневой директории проекта")
        sys.exit(1)
    
    # Запускаем тесты через unittest
    print("Запуск тестов через unittest...")
    unittest_suite = unittest.defaultTestLoader.discover("tests")
    unittest_result = unittest.TextTestRunner().run(unittest_suite)
    
    # Запускаем тесты через pytest с генерацией отчета о покрытии
    print("\nЗапуск тестов через pytest с отчетом о покрытии...")
    pytest.main(["tests", "-v", "--cov=utils", "--cov-report=term"])
    
    # Возвращаем код ошибки, если тесты не прошли
    if not unittest_result.wasSuccessful():
        sys.exit(1)