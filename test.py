import plotly.express as px
from dashforge import Dashboard

df = px.data.iris()
fig1 = px.parallel_coordinates(df, color="species_id", labels={"species_id": "Species",
                  "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                  "petal_width": "Petal Width", "petal_length": "Petal Length", },
                    color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2)

df = px.data.gapminder()
fig2 = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

df = px.data.gapminder()
fig3 = px.area(df, x="year", y="pop", color="continent", line_group="country")

data = dict(
    number=[39, 27.4, 20.6, 11, 2],
    stage=["Website visit", "Downloads", "Potential customers", "Requested price", "Invoice sent"])
fig4 = px.funnel(data, x='number', y='stage')

df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig5 = px.pie(df, values='pop', names='country', title='Population of European continent')

df = px.data.gapminder().query("year == 2007")
fig6 = px.treemap(df, path=[px.Constant('world'), 'continent', 'country'], values='pop',
                  color='lifeExp', hover_data=['iso_alpha'])

dashboard = Dashboard()
dashboard.set_bg_color(line="#FF1100DD",
                       behindchart="#DDDDDDB5",
                       outterChart="#1a1a1a",
                       innerChart="#1a1a1a",
                       ChartText="#ffffff")
dashboard.set_title("Dashboard")
dashboard.add_chart(fig1)
dashboard.add_chart(fig2)
dashboard.add_chart(fig3)
dashboard.add_chart(fig4)
dashboard.add_chart(fig5)
dashboard.add_chart(fig6)
dashboard.add_chart(fig3)
# dashboard.add_kpi("KPI 1", 100)
dashboard.add_kpi("KPI 2", 200)
dashboard.add_kpi("Total profit", 50000)
dashboard.add_kpi("KPI 3", 300213)
dashboard.set_chart_titles(["Parallel Coordinates", "Scatter Plot", "Area Chart", "Funnel Chart", "Pie Chart", "Treemap", "Area Chart 2"])
dashboard.preset("preset1")
dashboard.build_dashboard()
dashboard.run()