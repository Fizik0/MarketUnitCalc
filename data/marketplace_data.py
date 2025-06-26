"""
Данные о комиссиях и бенчмарках российских маркетплейсов
Основано на реальных данных 2024 года
"""

# Структура комиссий по маркетплейсам и категориям
MARKETPLACE_COMMISSIONS = {
    "OZON": {
        "Электроника": {
            "commission_rate": 12.0,
            "fulfillment_base": 60.0,
            "storage_per_day": 2.0,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 150.0,
                "packaging": 25.0
            }
        },
        "Одежда и обувь": {
            "commission_rate": 15.0,
            "fulfillment_base": 80.0,
            "storage_per_day": 1.5,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 100.0,
                "packaging": 30.0
            }
        },
        "Товары для дома": {
            "commission_rate": 18.0,
            "fulfillment_base": 70.0,
            "storage_per_day": 2.5,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 120.0,
                "packaging": 35.0
            }
        },
        "Красота и здоровье": {
            "commission_rate": 20.0,
            "fulfillment_base": 50.0,
            "storage_per_day": 1.0,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 80.0,
                "packaging": 20.0
            }
        },
        "Детские товары": {
            "commission_rate": 16.0,
            "fulfillment_base": 65.0,
            "storage_per_day": 1.8,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 110.0,
                "packaging": 28.0
            }
        },
        "Спорт и отдых": {
            "commission_rate": 14.0,
            "fulfillment_base": 90.0,
            "storage_per_day": 3.0,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 140.0,
                "packaging": 40.0
            }
        },
        "Автотовары": {
            "commission_rate": 13.0,
            "fulfillment_base": 85.0,
            "storage_per_day": 2.8,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 160.0,
                "packaging": 45.0
            }
        },
        "Книги": {
            "commission_rate": 25.0,
            "fulfillment_base": 40.0,
            "storage_per_day": 0.8,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 60.0,
                "packaging": 15.0
            }
        },
        "Продукты питания": {
            "commission_rate": 22.0,
            "fulfillment_base": 45.0,
            "storage_per_day": 4.0,
            "mandatory_marketing": 2.0,
            "additional_fees": {
                "processing_returns": 200.0,
                "packaging": 20.0
            }
        }
    },
    "Wildberries": {
        "Электроника": {
            "commission_rate": 8.5,
            "fulfillment_base": 55.0,
            "storage_per_day": 3.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 120.0,
                "packaging": 20.0
            }
        },
        "Одежда и обувь": {
            "commission_rate": 11.0,
            "fulfillment_base": 70.0,
            "storage_per_day": 2.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 90.0,
                "packaging": 25.0
            }
        },
        "Товары для дома": {
            "commission_rate": 13.0,
            "fulfillment_base": 65.0,
            "storage_per_day": 2.8,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 100.0,
                "packaging": 30.0
            }
        },
        "Красота и здоровье": {
            "commission_rate": 15.0,
            "fulfillment_base": 45.0,
            "storage_per_day": 1.2,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 70.0,
                "packaging": 18.0
            }
        },
        "Детские товары": {
            "commission_rate": 12.0,
            "fulfillment_base": 60.0,
            "storage_per_day": 2.2,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 95.0,
                "packaging": 25.0
            }
        },
        "Спорт и отдых": {
            "commission_rate": 10.0,
            "fulfillment_base": 80.0,
            "storage_per_day": 3.5,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 130.0,
                "packaging": 35.0
            }
        },
        "Автотовары": {
            "commission_rate": 9.0,
            "fulfillment_base": 75.0,
            "storage_per_day": 3.2,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 140.0,
                "packaging": 40.0
            }
        }
    },
    "Яндекс.Маркет": {
        "Электроника": {
            "commission_rate": 5.0,
            "fulfillment_base": 45.0,
            "storage_per_day": 1.5,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 100.0,
                "packaging": 22.0
            }
        },
        "Одежда и обувь": {
            "commission_rate": 7.0,
            "fulfillment_base": 60.0,
            "storage_per_day": 1.8,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 85.0,
                "packaging": 27.0
            }
        },
        "Товары для дома": {
            "commission_rate": 8.0,
            "fulfillment_base": 55.0,
            "storage_per_day": 2.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 95.0,
                "packaging": 32.0
            }
        },
        "Красота и здоровье": {
            "commission_rate": 10.0,
            "fulfillment_base": 40.0,
            "storage_per_day": 1.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 65.0,
                "packaging": 20.0
            }
        }
    },
    "Авито": {
        "Электроника": {
            "commission_rate": 3.5,
            "fulfillment_base": 0.0,  # Самовывоз
            "storage_per_day": 0.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 0.0,
                "packaging": 0.0,
                "listing_fee": 50.0,
                "promotion_fee": 150.0
            }
        },
        "Одежда и обувь": {
            "commission_rate": 4.0,
            "fulfillment_base": 0.0,
            "storage_per_day": 0.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 0.0,
                "packaging": 0.0,
                "listing_fee": 60.0,
                "promotion_fee": 180.0
            }
        },
        "Товары для дома": {
            "commission_rate": 4.5,
            "fulfillment_base": 0.0,
            "storage_per_day": 0.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 0.0,
                "packaging": 0.0,
                "listing_fee": 70.0,
                "promotion_fee": 200.0
            }
        },
        "Автотовары": {
            "commission_rate": 3.0,
            "fulfillment_base": 0.0,
            "storage_per_day": 0.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 0.0,
                "packaging": 0.0,
                "listing_fee": 80.0,
                "promotion_fee": 250.0
            }
        }
    }
}

# Отраслевые бенчмарки по категориям и маркетплейсам
BENCHMARKS = {
    "OZON": {
        "Электроника": {
            "avg_price": 8500,
            "avg_conversion": 0.025,
            "avg_return_rate": 0.12,
            "avg_ctr": 0.035,
            "avg_margin": 0.18,
            "avg_ltv_cac": 2.8,
            "seasonal_multiplier": {
                "Q1": 0.9,
                "Q2": 1.0,
                "Q3": 0.8,
                "Q4": 1.4
            }
        },
        "Одежда и обувь": {
            "avg_price": 3200,
            "avg_conversion": 0.018,
            "avg_return_rate": 0.25,
            "avg_ctr": 0.042,
            "avg_margin": 0.35,
            "avg_ltv_cac": 2.2,
            "seasonal_multiplier": {
                "Q1": 0.7,
                "Q2": 1.1,
                "Q3": 0.9,
                "Q4": 1.6
            }
        },
        "Товары для дома": {
            "avg_price": 2800,
            "avg_conversion": 0.022,
            "avg_return_rate": 0.08,
            "avg_ctr": 0.038,
            "avg_margin": 0.28,
            "avg_ltv_cac": 3.1,
            "seasonal_multiplier": {
                "Q1": 1.2,
                "Q2": 0.9,
                "Q3": 0.8,
                "Q4": 1.3
            }
        },
        "Красота и здоровье": {
            "avg_price": 1800,
            "avg_conversion": 0.032,
            "avg_return_rate": 0.06,
            "avg_ctr": 0.048,
            "avg_margin": 0.45,
            "avg_ltv_cac": 4.2,
            "seasonal_multiplier": {
                "Q1": 0.9,
                "Q2": 1.0,
                "Q3": 1.1,
                "Q4": 1.2
            }
        },
        "Детские товары": {
            "avg_price": 2500,
            "avg_conversion": 0.028,
            "avg_return_rate": 0.10,
            "avg_ctr": 0.045,
            "avg_margin": 0.32,
            "avg_ltv_cac": 3.8,
            "seasonal_multiplier": {
                "Q1": 1.0,
                "Q2": 1.1,
                "Q3": 1.3,
                "Q4": 1.4
            }
        },
        "Спорт и отдых": {
            "avg_price": 4200,
            "avg_conversion": 0.020,
            "avg_return_rate": 0.15,
            "avg_ctr": 0.035,
            "avg_margin": 0.22,
            "avg_ltv_cac": 2.5,
            "seasonal_multiplier": {
                "Q1": 0.8,
                "Q2": 1.3,
                "Q3": 1.2,
                "Q4": 0.9
            }
        },
        "Автотовары": {
            "avg_price": 3800,
            "avg_conversion": 0.015,
            "avg_return_rate": 0.18,
            "avg_ctr": 0.028,
            "avg_margin": 0.25,
            "avg_ltv_cac": 2.3,
            "seasonal_multiplier": {
                "Q1": 0.9,
                "Q2": 1.2,
                "Q3": 1.1,
                "Q4": 1.0
            }
        }
    },
    "Wildberries": {
        "Электроника": {
            "avg_price": 7800,
            "avg_conversion": 0.030,
            "avg_return_rate": 0.10,
            "avg_ctr": 0.040,
            "avg_margin": 0.22,
            "avg_ltv_cac": 3.2,
            "seasonal_multiplier": {
                "Q1": 0.9,
                "Q2": 1.0,
                "Q3": 0.8,
                "Q4": 1.5
            }
        },
        "Одежда и обувь": {
            "avg_price": 2900,
            "avg_conversion": 0.022,
            "avg_return_rate": 0.30,
            "avg_ctr": 0.050,
            "avg_margin": 0.40,
            "avg_ltv_cac": 2.8,
            "seasonal_multiplier": {
                "Q1": 0.6,
                "Q2": 1.2,
                "Q3": 0.9,
                "Q4": 1.8
            }
        },
        "Товары для дома": {
            "avg_price": 2400,
            "avg_conversion": 0.025,
            "avg_return_rate": 0.07,
            "avg_ctr": 0.042,
            "avg_margin": 0.32,
            "avg_ltv_cac": 3.5,
            "seasonal_multiplier": {
                "Q1": 1.1,
                "Q2": 0.9,
                "Q3": 0.8,
                "Q4": 1.4
            }
        },
        "Красота и здоровье": {
            "avg_price": 1600,
            "avg_conversion": 0.035,
            "avg_return_rate": 0.05,
            "avg_ctr": 0.052,
            "avg_margin": 0.48,
            "avg_ltv_cac": 4.8,
            "seasonal_multiplier": {
                "Q1": 0.9,
                "Q2": 1.0,
                "Q3": 1.1,
                "Q4": 1.3
            }
        }
    },
    "Яндекс.Маркет": {
        "Электроника": {
            "avg_price": 9200,
            "avg_conversion": 0.028,
            "avg_return_rate": 0.08,
            "avg_ctr": 0.032,
            "avg_margin": 0.25,
            "avg_ltv_cac": 3.8,
            "seasonal_multiplier": {
                "Q1": 0.9,
                "Q2": 1.0,
                "Q3": 0.8,
                "Q4": 1.4
            }
        },
        "Одежда и обувь": {
            "avg_price": 3500,
            "avg_conversion": 0.020,
            "avg_return_rate": 0.20,
            "avg_ctr": 0.038,
            "avg_margin": 0.38,
            "avg_ltv_cac": 3.0,
            "seasonal_multiplier": {
                "Q1": 0.7,
                "Q2": 1.1,
                "Q3": 0.9,
                "Q4": 1.6
            }
        }
    }
}

# Коэффициенты алгоритмов ранжирования (на основе инсайдов из документов)
RANKING_FACTORS = {
    "OZON": {
        "sales_velocity": 0.35,  # Скорость продаж
        "customer_experience": 0.25,  # Клиентский опыт (отзывы, рейтинг, возвраты)
        "content_quality": 0.20,  # Качество контента
        "ad_investment": 0.15,  # Рекламные инвестиции
        "seller_metrics": 0.05,  # Метрики продавца
        "hidden_signals": {
            "session_time": 0.1,
            "cart_additions": 0.15,
            "wishlist_additions": 0.1,
            "cross_sell_performance": 0.08,
            "price_position_index": 0.12
        }
    },
    "Wildberries": {
        "sales_performance": 0.40,
        "customer_satisfaction": 0.30,
        "content_optimization": 0.20,
        "advertising_efficiency": 0.10
    }
}

# Штрафы и особенности платформ
PLATFORM_PENALTIES = {
    "OZON": {
        "frequent_price_changes": -0.10,  # Более 3 раз в неделю
        "price_war_participation": -0.15,
        "sudden_sales_spike": -0.20,  # Резкий рост продаж
        "review_aging": -0.25,  # Отзывы старше 6 месяцев теряют вес
        "category_cannibalization": -0.18  # Много товаров в одной категории
    },
    "Wildberries": {
        "poor_content_quality": -0.15,
        "low_stock_availability": -0.20,
        "high_return_rate": -0.25
    }
}

# Рекомендуемые KPI по фазам развития (P.R.O.F.I.T. методология)
PHASE_KPI = {
    "stabilization": {  # Месяцы 1-3
        "targets": {
            "positive_unit_economics": True,
            "roas_min": 3.0,
            "inventory_turnover_min": 6.0,
            "customer_satisfaction_min": 4.5
        },
        "actions": [
            "Аудит всех издержек",
            "Оптимизация топ-20% товаров",
            "Настройка базовой аналитики",
            "Стандартизация процессов",
            "Quality content для main SKUs"
        ]
    },
    "optimization": {  # Месяцы 4-9
        "targets": {
            "margin_improvement": 0.15,  # 10-15%
            "ltv_cac_ratio_min": 3.0,
            "automation_coverage": 0.70,
            "brand_recognition_growth": True
        },
        "actions": [
            "Advanced analytics внедрение",
            "Автоматизация pricing и inventory",
            "Premium positioning selected SKUs",
            "Brand building activities",
            "Customer retention programs"
        ]
    },
    "scaling": {  # Месяцы 10-12+
        "targets": {
            "market_share_leadership": True,
            "geographic_expansion": True,
            "innovation_pipeline": True,
            "sustainable_advantages": True
        },
        "actions": [
            "Market leadership positioning",
            "Strategic partnerships",
            "Technology platform development",
            "Talent acquisition scaling",
            "Investment in innovation"
        ]
    }
}

# Коэффициенты для расчета CAC по каналам
CAC_MULTIPLIERS = {
    "ppc_search": 1.0,  # Базовый множитель
    "ppc_display": 1.3,
    "social_media": 0.8,
    "influencer": 1.5,
    "content_marketing": 0.6,
    "email_marketing": 0.3,
    "referral": 0.4
}

# Сезонные коэффициенты по месяцам
SEASONAL_FACTORS = {
    1: 0.85,  # Январь - спад после НГ
    2: 0.90,  # Февраль
    3: 1.05,  # Март - 8 марта
    4: 0.95,  # Апрель
    5: 1.10,  # Май - майские праздники
    6: 1.00,  # Июнь
    7: 0.90,  # Июль - отпуска
    8: 0.85,  # Август - отпуска
    9: 1.15,  # Сентябрь - Back to school
    10: 1.10,  # Октябрь
    11: 1.25,  # Ноябрь - Black Friday
    12: 1.40   # Декабрь - Новый год
}

def get_marketplace_commission(marketplace: str, category: str) -> dict:
    """Получение данных о комиссиях для конкретного маркетплейса и категории"""
    if marketplace in MARKETPLACE_COMMISSIONS:
        if category in MARKETPLACE_COMMISSIONS[marketplace]:
            return MARKETPLACE_COMMISSIONS[marketplace][category]
        else:
            # Возвращаем средние значения если категория не найдена
            categories = MARKETPLACE_COMMISSIONS[marketplace]
            avg_commission = sum(cat["commission_rate"] for cat in categories.values()) / len(categories)
            avg_fulfillment = sum(cat["fulfillment_base"] for cat in categories.values()) / len(categories)
            
            return {
                "commission_rate": avg_commission,
                "fulfillment_base": avg_fulfillment,
                "storage_per_day": 2.0,
                "mandatory_marketing": 0.0,
                "additional_fees": {
                    "processing_returns": 100.0,
                    "packaging": 25.0
                }
            }
    else:
        # Данные по умолчанию для неизвестного маркетплейса
        return {
            "commission_rate": 15.0,
            "fulfillment_base": 60.0,
            "storage_per_day": 2.0,
            "mandatory_marketing": 0.0,
            "additional_fees": {
                "processing_returns": 100.0,
                "packaging": 25.0
            }
        }

def get_category_benchmark(marketplace: str, category: str) -> dict:
    """Получение бенчмарков для категории на маркетплейсе"""
    if marketplace in BENCHMARKS and category in BENCHMARKS[marketplace]:
        return BENCHMARKS[marketplace][category]
    else:
        # Возвращаем средние значения
        return {
            "avg_price": 3000,
            "avg_conversion": 0.025,
            "avg_return_rate": 0.12,
            "avg_ctr": 0.035,
            "avg_margin": 0.25,
            "avg_ltv_cac": 3.0,
            "seasonal_multiplier": {
                "Q1": 0.9,
                "Q2": 1.0,
                "Q3": 0.9,
                "Q4": 1.3
            }
        }

def calculate_seasonal_adjustment(month: int) -> float:
    """Расчет сезонного коэффициента для заданного месяца"""
    return SEASONAL_FACTORS.get(month, 1.0)

def get_ranking_impact(marketplace: str, metrics: dict) -> float:
    """Расчет влияния на ранжирование в зависимости от метрик"""
    if marketplace not in RANKING_FACTORS:
        return 1.0
    
    factors = RANKING_FACTORS[marketplace]
    impact_score = 1.0
    
    # Здесь можно добавить логику расчета влияния на основе метрик
    # Например, штрафы за частые изменения цен, низкое качество контента и т.д.
    
    return impact_score
