"""Dark, data-rich retail operations dashboard."""

from _bootstrap import Dashboard, launch
import plotly.express as px
import pandas as pd


def build_dashboard() -> Dashboard:
    sales = px.data.gapminder().query("year == 2007")
    regional = sales.groupby("continent", as_index=False).agg(
        population=("pop", "sum"), life_expectancy=("lifeExp", "mean"), countries=("country", "count")
    )

    figures = [
        px.scatter(sales, x="gdpPercap", y="lifeExp", size="pop", color="continent", log_x=True,
                   hover_name="country", size_max=48),
        px.bar(regional, x="continent", y="population", color="continent", text_auto=".2s"),
        px.sunburst(sales, path=["continent", "country"], values="pop", color="lifeExp",
                    color_continuous_scale="Tealgrn"),
        px.violin(sales, x="continent", y="lifeExp", color="continent", box=True, points="all"),
        px.choropleth(sales, locations="iso_alpha", color="gdpPercap", hover_name="country",
                      color_continuous_scale="Turbo"),
        px.histogram(sales, x="lifeExp", color="continent", nbins=22, barmode="overlay"),
    ]

    dashboard = Dashboard()
    dashboard.set_theme("dark")
    dashboard.set_colors(line="#00D4FF", HeaderBG="#0B132B", KPIBackgroundArea="#111C3D",
                         ChartAreaBackground="#111C3D", ChartBorder="#274060")
    dashboard.set_title("Atlas Operations Center")
    dashboard.add_kpi({"Markets": "142", "Population covered": "6.1B", "Average lifespan": "67.0", "Data freshness": "2007"})
    dashboard.add_chart(figures)
    dashboard.set_chart_per_row([2, 2, 2])
    dashboard.set_chart_titles(["Market opportunity", "Population by region", "Population hierarchy",
                                "Life expectancy spread", "GDP per capita map", "Longevity distribution"])
    dashboard.set_chart_subtitles(["Bubble size shows population", "Summed 2007 population", None,
                                  "Each dot is a country", "Hover for country detail", "Overlay by continent"])
    dashboard.set_max_buttons([True, False, True, True, True, False])
    dashboard.add_dataset(sales[["country", "continent", "lifeExp", "pop", "gdpPercap"]])
    dashboard.set_dataset_name("2007 market reference")
    dashboard.set_footer_text("Atlas / Global Intelligence")
    dashboard.add_timestamp()
    return dashboard


if __name__ == "__main__":
    launch(build_dashboard(), 8051)
