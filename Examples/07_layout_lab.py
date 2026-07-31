"""Exercises one-, two-, and three-column rows with exact card sizing."""

from dashforge import Dashboard
from _bootstrap import launch
import numpy as np
import pandas as pd
import plotly.express as px


def build_dashboard() -> Dashboard:
    rng = np.random.default_rng(5)
    data = pd.DataFrame({"x": np.arange(30), "a": rng.normal(20, 4, 30).cumsum(), "b": rng.normal(15, 3, 30).cumsum(), "group": rng.choice(list("ABC"), 30)})
    figures = [
        px.line(data, x="x", y=["a", "b"]),
        px.bar(data.groupby("group", as_index=False).a.mean(), x="group", y="a", color="group"),
        px.scatter(data, x="a", y="b", color="group", size="x"),
        px.histogram(data, x="a", color="group"),
        px.ecdf(data, x="b", color="group"),
        px.box(data, y="a", color="group"),
    ]
    dashboard = Dashboard()
    dashboard.set_theme("light")
    dashboard.set_colors(line="#0F766E", HeaderBG="#ECFDF5", KPIBackgroundArea="#D1FAE5", ChartAreaBackground="#F0FDFA", ChartBorder="#5EEAD4")
    dashboard.set_title("Layout Laboratory")
    dashboard.add_chart(figures)
    dashboard.set_chart_per_row([1, 2, 3])
    dashboard.set_custom_size([[[100, 125]], [[65, 90], [35, 90]], [[34, 78], [33, 78], [33, 78]]])
    dashboard.set_chart_titles(["Hero trend", "Wide comparison", "Narrow relationship", "Distribution", "Cumulative distribution", "Compact summary"])
    dashboard.set_footer_text("A sizing and layout regression scenario")
    return dashboard


if __name__ == "__main__":
    launch(build_dashboard(), 8057)
