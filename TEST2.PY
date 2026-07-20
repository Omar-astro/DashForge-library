from dashforge import Dashboard
import plotly.express as px

x = [1,2,3,4,5]
y = [10,20,30,40,50]

fig1 = px.line(x=x, y=y, title="Line Chart")
fig2 = px.bar(x=x, y=y, title="Bar Chart")

dash = Dashboard()

dash.set_title("My Dashboard")
dash.add_chart(fig1)
dash.add_chart(fig2)
dash.set_bg_color(line="#FF1100DD",
                   behindchart="#DDDDDDB5",)
dash.add_kpi("KPI 1", 100)
dash.add_kpi("KPI 2", 200)
dash.build_dashboard()
dash.run()