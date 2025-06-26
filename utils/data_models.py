from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class MarketplaceType(Enum):
    OZON = "OZON"
    WILDBERRIES = "Wildberries"
    YANDEX_MARKET = "Яндекс.Маркет"
    AVITO = "Авито"
    OTHER = "Другой"

class BusinessModel(Enum):
    DROPSHIPPING = "Dropshipping"
    PRIVATE_LABEL = "Private Label"
    WHOLESALE = "Wholesale"
    RETAIL = "Retail"

@dataclass
class ProductInfo:
    """Информация о товаре"""
    name: str
    category: str
    selling_price: float
    weight: float
    dimensions: str
    marketplace: MarketplaceType
    business_model: BusinessModel = BusinessModel.PRIVATE_LABEL

@dataclass
class CostStructure:
    """Структура затрат"""
    purchase_cost: float
    packaging_cost: float = 0.0
    labeling_cost: float = 0.0
    quality_control: float = 0.0
    certification: float = 0.0
    
    @property
    def total_cogs(self) -> float:
        return (self.purchase_cost + self.packaging_cost + 
                self.labeling_cost + self.quality_control + self.certification)

@dataclass
class MarketplaceCosts:
    """Расходы маркетплейса"""
    commission_rate: float
    fulfillment_cost: float
    storage_cost_per_day: float
    storage_days: int
    payment_processing_rate: float
    additional_fees: float = 0.0
    
    def calculate_total_costs(self, selling_price: float) -> float:
        commission = selling_price * (self.commission_rate / 100)
        storage_total = self.storage_cost_per_day * self.storage_days
        payment_processing = selling_price * (self.payment_processing_rate / 100)
        
        return (commission + self.fulfillment_cost + storage_total + 
                payment_processing + self.additional_fees)

@dataclass
class MarketingCosts:
    """Маркетинговые расходы"""
    ppc_budget_percent: float
    avg_cpc: float
    conversion_rate: float
    external_marketing: float = 0.0
    influencer_marketing: float = 0.0
    content_creation: float = 0.0
    
    def calculate_total_costs(self, selling_price: float) -> float:
        ppc_cost = selling_price * (self.ppc_budget_percent / 100)
        return (ppc_cost + self.external_marketing + 
                self.influencer_marketing + self.content_creation)
    
    @property
    def cac_ppc(self) -> float:
        return self.avg_cpc / (self.conversion_rate / 100) if self.conversion_rate > 0 else 0

@dataclass
class OperationalCosts:
    """Операционные расходы"""
    staff_costs_monthly: float
    office_rent_monthly: float
    software_subscriptions_monthly: float
    customer_service_per_order: float
    return_rate: float
    return_processing_cost: float
    monthly_sales_volume: int
    
    @property
    def fixed_cost_per_unit(self) -> float:
        total_fixed = self.staff_costs_monthly + self.office_rent_monthly + self.software_subscriptions_monthly
        return total_fixed / self.monthly_sales_volume if self.monthly_sales_volume > 0 else 0
    
    @property
    def return_cost_per_unit(self) -> float:
        return (self.return_rate / 100) * self.return_processing_cost
    
    @property
    def total_operational_cost_per_unit(self) -> float:
        return self.fixed_cost_per_unit + self.customer_service_per_order + self.return_cost_per_unit

@dataclass
class CustomerMetrics:
    """Метрики клиентов"""
    repeat_purchase_rate: float
    avg_purchases_per_year: float
    customer_lifespan_months: int
    cross_sell_revenue: float = 0.0
    referral_bonus: float = 0.0
    
    def calculate_ltv(self, selling_price: float) -> float:
        purchases_per_customer = (self.customer_lifespan_months / 12) * self.avg_purchases_per_year
        return (selling_price * purchases_per_customer + 
                self.cross_sell_revenue + self.referral_bonus)
    
    def calculate_payback_period(self, cac: float, selling_price: float) -> float:
        monthly_revenue = selling_price * (self.avg_purchases_per_year / 12)
        return cac / monthly_revenue if monthly_revenue > 0 else 0

@dataclass
class BusinessMetrics:
    """Бизнес-метрики"""
    unit_profit: float
    profit_margin: float
    ltv: float
    cac: float
    ltv_cac_ratio: float
    payback_period: float
    contribution_margin: float
    breakeven_price: float
    profit_score: int
    
    def get_profitability_status(self) -> str:
        if self.profit_margin >= 30:
            return "Отличная"
        elif self.profit_margin >= 20:
            return "Хорошая"
        elif self.profit_margin >= 10:
            return "Приемлемая"
        elif self.profit_margin >= 0:
            return "Низкая"
        else:
            return "Убыточная"
    
    def get_ltv_cac_status(self) -> str:
        if self.ltv_cac_ratio >= 5:
            return "Отлично"
        elif self.ltv_cac_ratio >= 3:
            return "Хорошо"
        elif self.ltv_cac_ratio >= 2:
            return "Приемлемо"
        else:
            return "Плохо"

@dataclass
class MarketplaceData:
    """Данные о маркетплейсе"""
    name: str
    commission_rates: Dict[str, float]
    fulfillment_costs: Dict[str, float]
    storage_costs: Dict[str, float]
    additional_fees: Dict[str, float]
    
    def get_commission_rate(self, category: str) -> float:
        return self.commission_rates.get(category, 15.0)
    
    def get_fulfillment_cost(self, weight: float) -> float:
        # Упрощенный расчет на основе веса
        if weight <= 0.5:
            return 50.0
        elif weight <= 1.0:
            return 80.0
        elif weight <= 2.0:
            return 120.0
        else:
            return 150.0 + (weight - 2.0) * 30

class ScenarioType(Enum):
    PESSIMISTIC = "Пессимистичный"
    REALISTIC = "Реалистичный" 
    OPTIMISTIC = "Оптимистичный"

@dataclass
class Scenario:
    """Сценарий развития бизнеса"""
    name: str
    price_change: float
    cost_change: float
    volume_change: float
    marketing_efficiency: float
    
    @classmethod
    def create_standard_scenarios(cls) -> Dict[str, 'Scenario']:
        return {
            ScenarioType.PESSIMISTIC.value: cls(
                name="Пессимистичный",
                price_change=-0.15,
                cost_change=0.10,
                volume_change=-0.30,
                marketing_efficiency=-0.20
            ),
            ScenarioType.REALISTIC.value: cls(
                name="Реалистичный",
                price_change=0.00,
                cost_change=0.05,
                volume_change=0.00,
                marketing_efficiency=0.00
            ),
            ScenarioType.OPTIMISTIC.value: cls(
                name="Оптимистичный",
                price_change=0.10,
                cost_change=-0.05,
                volume_change=0.50,
                marketing_efficiency=0.25
            )
        }

@dataclass
class Recommendation:
    """Рекомендация для оптимизации"""
    priority: str  # "high", "medium", "low"
    category: str  # "cost", "pricing", "marketing", "operations"
    title: str
    description: str
    expected_impact: str
    timeframe: str  # "immediate", "short_term", "long_term"
    
    def to_dict(self) -> Dict[str, str]:
        return {
            'priority': self.priority,
            'category': self.category,
            'title': self.title,
            'description': self.description,
            'expected_impact': self.expected_impact,
            'timeframe': self.timeframe
        }
