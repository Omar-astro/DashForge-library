"""Seven chart families in one playful, colorful gallery."""

from _bootstrap import Dashboard, launch
import plotly.express as px


def build_dashboard() -> Dashboard:
    iris = px.data.iris()
    tips = px.data.tips()
    gap = px.data.gapminder().query("year == 2007")
    figures = [
        px.scatter_matrix(iris, dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"], color="species"),
        px.density_contour(iris, x="sepal_width", y="petal_width", color="species"),
        px.strip(tips, x="day", y="total_bill", color="sex"),
        px.funnel(dict(number=[950, 620, 370, 190, 74], stage=["Visited", "Signed up", "Trial", "Proposal", "Won"]), x="number", y="stage"),
        px.treemap(gap, path=[px.Constant("World"), "continent", "country"], values="pop", color="lifeExp", color_continuous_scale="Viridis"),
        px.pie(gap.groupby("continent", as_index=False).pop.sum(), values="pop", names="continent", hole=.4),
        px.parallel_coordinates(iris, color="species_id", dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"], color_continuous_scale="Plasma"),
    ]
    dashboard = Dashboard()
    dashboard.set_theme("dark")
    dashboard.set_colors(line="#FBBF24", HeaderBG="#2A183B", KPIBackgroundArea="#2A183B", ChartAreaBackground="#302044", ChartBorder="#6B3E93")
    dashboard.set_title("The Plotly Playground")
    dashboard.add_kpi({"Chart varieties": 7, "Datasets": 3, "Palette": "Electric"})
    dashboard.add_chart(figures)
    dashboard.set_chart_per_row([2, 3, 2])
    dashboard.set_chart_titles(["Scatter matrix", "Density contours", "Strip plot", "Conversion funnel", "World treemap", "Population donut", "Parallel coordinates"])
    dashboard.set_max_buttons([True, True, False, True, True, False, True])
    dashboard.set_footer_text("Pick a chart, maximize it, and explore")
    return dashboard


if __name__ == "__main__":
    launch(build_dashboard(), 8056)
