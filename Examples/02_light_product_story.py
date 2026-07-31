"""A bright product-performance dashboard with an editorial feel."""

from _bootstrap import Dashboard, launch
import numpy as np
import pandas as pd
import plotly.express as px


def build_dashboard() -> Dashboard:
    rng = np.random.default_rng(12)
    months = pd.date_range("2025-01-01", periods=12, freq="MS")
    products = ["Orbit", "Lumen", "Northstar"]
    data = pd.DataFrame([
        {"month": month, "product": product, "revenue": rng.integers(45, 150) * 1000,
         "orders": rng.integers(250, 900), "satisfaction": rng.uniform(4.0, 4.9)}
        for month in months for product in products
    ])
    latest = data[data.month == data.month.max()]
    figures = [
        px.line(data, x="month", y="revenue", color="product", markers=True, template="simple_white"),
        px.bar(latest, x="product", y="orders", color="product", text_auto=True, template="simple_white"),
        px.area(data, x="month", y="orders", color="product", template="simple_white"),
        px.scatter(data, x="orders", y="satisfaction", color="product", size="revenue", template="simple_white"),
    ]
    dashboard = Dashboard()
    dashboard.set_theme("light")
    dashboard.set_colors(line="#E8505B", HeaderBG="#FFF7ED", KPIBackgroundArea="#FFF1E6",
                         ChartAreaBackground="#FFF9F5", outterChart="#FFFFFF", innerChart="#FFFFFF",
                         ChartBorder="#F3C6B9", ChartText="#362B2B", KPICard="#FFFFFF", KPIText="#362B2B")
    dashboard.set_font_family("Georgia, serif")
    dashboard.set_title("Product Garden")
    dashboard.add_kpi("Quarterly revenue", "$1.1M")
    dashboard.add_kpi({"Active products": 3, "Average rating": "4.5 / 5", "Orders this month": f"{latest.orders.sum():,}"})
    dashboard.add_chart(figures)
    dashboard.set_chart_per_row([1, 3])
    dashboard.set_chart_titles(["Revenue has momentum", "Latest-month orders", "Order mix", "Satisfaction signal"])
    dashboard.set_chart_subtitles(["12 months of product revenue", None, "A stacked view of demand", "Larger bubbles mean higher revenue"])
    dashboard.set_footer_text("A bright DashForge product story")
    return dashboard


if __name__ == "__main__":
    launch(build_dashboard(), 8052)
