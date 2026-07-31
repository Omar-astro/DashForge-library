"""People analytics scenario that emphasizes the second data-table page."""

from dashforge import Dashboard
from _bootstrap import launch
import numpy as np
import pandas as pd
import plotly.express as px


def build_dashboard() -> Dashboard:
    rng = np.random.default_rng(24)
    teams = ["Design", "Engineering", "Marketing", "Operations"]
    people = pd.DataFrame({
        "employee": [f"Team member {number:02}" for number in range(1, 61)],
        "team": rng.choice(teams, 60),
        "tenure_years": rng.integers(0, 12, 60),
        "engagement": rng.integers(55, 100, 60),
        "salary": rng.integers(45_000, 155_000, 60),
        "work_mode": rng.choice(["Hybrid", "Remote", "Office"], 60),
    })
    figures = [
        px.box(people, x="team", y="salary", color="team", points="all"),
        px.scatter(people, x="tenure_years", y="engagement", color="team", symbol="work_mode", hover_name="employee"),
        px.histogram(people, x="work_mode", color="team", barmode="group"),
    ]
    dashboard = Dashboard()
    dashboard.set_theme("light")
    dashboard.set_colors(line="#1D4ED8", HeaderBG="#EFF6FF", KPIBackgroundArea="#DBEAFE", ChartAreaBackground="#EFF6FF", ChartBorder="#93C5FD")
    # The logo is relative to the repository root; DashForge serves it at /files/.
    dashboard.set_logo("Logo23.png")
    dashboard.set_title("People Signals")
    dashboard.set_font_family("Trebuchet MS, sans-serif")
    dashboard.add_kpi({"Headcount": len(people), "Average engagement": f"{people.engagement.mean():.0f}%", "Hybrid share": f"{(people.work_mode == 'Hybrid').mean():.0%}"})
    dashboard.add_chart(figures)
    dashboard.set_chart_per_row([1, 2])
    dashboard.set_chart_titles(["Compensation by team", "Engagement over tenure", "Work-mode mix"])
    dashboard.set_chart_subtitles(["Each point is an employee", "Color denotes team; shape denotes workplace", None])
    dashboard.add_dataset(people)
    dashboard.set_dataset_name("Employee experience sample")
    dashboard.set_footer_text("People & Culture / illustrative data")
    dashboard.add_timestamp()
    return dashboard


if __name__ == "__main__":
    launch(build_dashboard(), 8055)
