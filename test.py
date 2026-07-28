import plotly.express as px
from dashforge import Dashboard
import pandas as pd
import numpy as np

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

np.random.seed(42)

names = ["Ava", "Noah", "Mia", "Liam", "Zoe", "Ethan", "Ivy", "Leo"]
cities = ["Dallas", "Paris", "Tokyo", "Cairo", "Berlin", "Lima", "Oslo", "Seoul"]

df = pd.DataFrame({
    "Name": np.random.choice(names, 50),
    "Age": np.random.randint(18, 70, 50),
    "City": np.random.choice(cities, 50),
    "Score": np.random.randint(0, 101, 50),
    "Height_cm": np.random.randint(140, 201, 50),
    "Salary": np.random.randint(30000, 120000, 50),
    "Name2": np.random.choice(names, 50),
    "Name3": np.random.choice(names, 50),
    "Name4": np.random.choice(names, 50),
    "Name5": np.random.choice(names, 50),
    'name6': np.random.choice(names, 50),
    'name7': np.random.choice(names, 50),
    'name8': np.random.choice(names, 50),
    'name9': np.random.choice(names, 50),
    'name10': np.random.choice(names, 50),
    'name11': np.random.choice(names, 50),
    'name12': np.random.choice(names, 50),
    'name13': np.random.choice(names, 50),
    'name14': np.random.choice(names, 50),
    'name15': np.random.choice(names, 50),
    'name16': np.random.choice(names, 50),
    'name17': np.random.choice(names, 50),
    'name18': np.random.choice(names, 50),
    'name19': np.random.choice(names, 50),
    'name20': np.random.choice(names, 50),
    'name21': np.random.choice(names, 50),
})

dashboard = Dashboard()
dashboard.set_theme("light")
dashboard.set_colors(line="#FF1100DD",
                       ChartText="#040731")
dashboard.set_logo("Logo23.png")
# dashboard.set_theme("dark")
dashboard.set_title("Dashboard charts")
dashboard.add_chart([fig1, fig2, fig3, fig4, fig5, fig6, fig3])
# dashboard.add_kpi("KPI 1", 100)
# dashboard.add_kpi("KPI 2", 500)
dashboard.add_kpi("Total profit", 50000)
dashboard.add_kpi({"KPI 1": 100, "KPI 2": 500, "Total profit 2": 40000})
dashboard.add_kpi("KPI 3", 300213)
dashboard.set_font_family("Bodoni MT")
dashboard.set_footer_text("@Astronial")
dashboard.set_chart_per_row([3,2,1,1])
dashboard.set_custom_size([[[130, 100], [110, 130], [100, 100]], 
                           [[70, 120], [100, 150]],
                           [[100, 250]],
                           None])
dashboard.set_dataset_name("Iris Dataset")
dashboard.set_chart_titles([None, "Scatter Plot", "Area Chart", "Funnel Chart", "Pie Chart", "Treemap", "Area Chart 2"])
dashboard.set_chart_subtitles(["This is a parallel coordinates chart", 
                               None,
                               None,
                               "This is an area chart", 
                               "This is a funnel chart", 
                               "This is a pie chart", 
                               "This is a treemap chart", 
                               "This is an area chart 2"])

dashboard.add_timestamp()
# dashboard.hide_Header(True)
dashboard.add_dataset(df)
dashboard.set_max_buttons([False, True, True, False, False, False, True])
dashboard.preset("preset1")
dashboard.set_debug(True)
dashboard.build_dashboard()
# dashboard.set_port(8050)
dashboard.run()