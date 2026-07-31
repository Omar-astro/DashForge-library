"""A financial analyst workspace with weighted card widths."""

from dashforge import Dashboard
from _bootstrap import launch
import numpy as np
import pandas as pd
import plotly.express as px


def build_dashboard() -> Dashboard:
    rng = np.random.default_rng(7)
    dates = pd.date_range("2024-01-01", periods=180, freq="D")
    price = 100 + np.cumsum(rng.normal(0.15, 1.7, len(dates)))
    market = pd.DataFrame({"date": dates, "close": price, "volume": rng.integers(800_000, 4_000_000, len(dates))})
    market["moving_average"] = market.close.rolling(20, min_periods=1).mean()
    market["return"] = market.close.pct_change().fillna(0)
    sectors = pd.DataFrame({"sector": ["Cloud", "AI", "Security", "Commerce", "Fintech"], "return": [24, 37, 18, 12, 29], "weight": [28, 21, 17, 19, 15]})
    figures = [
        px.line(market, x="date", y=["close", "moving_average"], template="plotly_dark"),
        px.bar(sectors, x="sector", y="return", color="return", color_continuous_scale="RdYlGn", template="plotly_dark"),
        px.area(market, x="date", y="volume", template="plotly_dark"),
        px.histogram(market, x="return", nbins=32, template="plotly_dark"),
        px.pie(sectors, values="weight", names="sector", hole=.55, template="plotly_dark"),
    ]
    dashboard = Dashboard()
    dashboard.set_theme("dark")
    dashboard.set_colors(line="#A78BFA", HeaderBG="#17152D", KPIBackgroundArea="#211D3C", ChartAreaBackground="#211D3C",
                         outterChart="#17152D", innerChart="#17152D", ChartBorder="#4C3F91")
    dashboard.set_title("Northstar Capital / Daily Brief")
    dashboard.add_kpi({"Portfolio NAV": "$24.8M", "Day change": "+1.84%", "Volatility": "18.2%", "Cash": "6.4%"})
    dashboard.add_chart(figures)
    dashboard.set_chart_per_row([2, 2, 1])
    dashboard.set_custom_size([[[68, 125], [32, 125]], [[55, 90], [45, 90]], [[100, 105]]])
    dashboard.set_chart_titles(["Price & 20-day moving average", "Sector performance", "Liquidity", "Daily-return distribution", "Portfolio allocation"])
    dashboard.set_max_buttons([True, False, True, True, False])
    dashboard.set_footer_text("Internal use only · figures simulated")
    dashboard.add_timestamp()
    return dashboard


if __name__ == "__main__":
    launch(build_dashboard(), 8053)
