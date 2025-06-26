# Marketplace Unit Economics Calculator

## Overview

This is a comprehensive unit economics calculator specifically designed for Russian marketplaces (OZON, Wildberries, Yandex.Market, Avito). The application helps e-commerce businesses calculate real profitability by analyzing all costs associated with selling products on these platforms.

The calculator provides step-by-step guidance through the unit economics calculation process, including marketplace commissions, fulfillment costs, marketing expenses, and operational overhead. It features professional-grade analytics, benchmarking against industry standards, and export capabilities for business reporting.

## System Architecture

**Frontend Architecture:**
- Streamlit-based web application with multi-page navigation
- Interactive dashboard with Plotly visualizations
- Responsive design optimized for professional use
- Component-based architecture with modular pages

**Backend Architecture:**
- Python-based calculation engine with object-oriented design
- Modular utility classes for calculations, data models, and export functionality
- Data-driven configuration for marketplace-specific parameters
- Session state management for multi-step calculator workflow

**Data Management:**
- In-memory data storage using Streamlit session state
- Structured data models using Python dataclasses
- Configuration-driven marketplace data with real 2024 commission rates
- Export capabilities to Excel and PDF formats

## Key Components

**Core Calculation Engine (`utils/calculations.py`):**
- UnitEconomicsCalculator class handling all financial calculations
- Methods for COGS, marketplace costs, marketing expenses, and operational costs
- Benchmark comparison and profitability analysis
- Support for multiple business models (dropshipping, private label, wholesale, retail)

**Data Models (`utils/data_models.py`):**
- Structured dataclasses for product information, cost structures, and marketplace costs
- Enum definitions for marketplace types and business models
- Type-safe data handling with validation

**Export Manager (`utils/export.py`):**
- Excel report generation with multiple worksheets
- PDF report creation with professional formatting
- Summary sheets, detailed calculations, scenario analysis, and recommendations

**Page Components:**
- Multi-step calculator interface (`pages/calculator.py`)
- Analytics dashboard with interactive charts (`pages/dashboard.py`)
- Step validation and progress tracking

**Marketplace Data (`data/marketplace_data.py`):**
- Real commission rates and fee structures for 2024
- Category-specific parameters for major Russian marketplaces
- Benchmark data for performance comparison
- Hidden costs and algorithm-specific insights

## Data Flow

1. **User Input Collection:** Step-by-step wizard collects product information, costs, and business parameters
2. **Data Validation:** Each step validates required inputs before progression
3. **Calculation Processing:** UnitEconomicsCalculator processes all inputs using marketplace-specific parameters
4. **Results Analysis:** Generated metrics are compared against industry benchmarks
5. **Visualization:** Interactive charts and tables present results in dashboard format
6. **Export Generation:** Professional reports created in Excel/PDF formats for business use

## External Dependencies

**Core Libraries:**
- `streamlit` (1.46.0+): Web application framework
- `pandas` (2.3.0+): Data manipulation and analysis
- `plotly` (6.1.2+): Interactive visualizations and charts
- `streamlit-option-menu` (0.4.0+): Enhanced navigation components

**Export Libraries:**
- `fpdf2` (2.8.3+): PDF report generation
- `openpyxl` (3.1.5+): Excel file creation and manipulation

**Supporting Libraries:**
- `numpy`: Numerical computations
- `typing-extensions`: Enhanced type hints
- `datetime`: Date and time handling

## Deployment Strategy

**Replit Configuration:**
- Python 3.11 environment with Nix package management
- Streamlit server running on port 5000
- Autoscale deployment target for production use
- Workflow automation for development and deployment

**Application Settings:**
- Headless server mode for production deployment
- Custom theme with professional color scheme
- Wide layout optimization for dashboard viewing
- Expanded sidebar for navigation enhancement

**Performance Optimization:**
- Session state caching for calculation results
- Modular loading of components to reduce initial load time
- Efficient data structures for large datasets
- Lazy loading of visualization components

## Changelog

- June 26, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.