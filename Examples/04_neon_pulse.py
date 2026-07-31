"""Header-free neon telemetry board using Plotly graph objects."""

from dashforge import Dashboard
from _bootstrap import launch
import numpy as np
import plotly.graph_objects as go


def build_dashboard() -> Dashboard:
    rng = np.random.default_rng(99)
    x = np.arange(60)
    signal = np.sin(x / 5) + rng.normal(0, .12, 60)
    gauge = go.Figure(go.Indicator(mode="gauge+number+delta", value=76, delta={"reference": 68},
                                   title={"text": "System health"}, gauge={"axis": {"range": [0, 100]},
                                   "bar": {"color": "#39FFB6"}, "steps": [{"range": [0, 50], "color": "#19223B"}, {"range": [50, 80], "color": "#253A50"}]}))
    wave = go.Figure(go.Scatter(x=x, y=signal, mode="lines", line={"color": "#FF4FD8", "width": 3}, fill="tozeroy"))
    radar = go.Figure(go.Scatterpolar(r=[88, 64, 91, 73, 82], theta=["Latency", "Uptime", "Throughput", "Quality", "Coverage"], fill="toself", line={"color": "#00E5FF"}))
    dashboard = Dashboard()
    dashboard.set_theme("dark")
    dashboard.set_colors(line="#39FFB6", behindchart="#080B16", HeaderBG="#080B16", KPIBackgroundArea="#080B16",
                         ChartAreaBackground="#10172B", outterChart="#10172B", innerChart="#10172B", ChartBorder="#243553")
    dashboard.hide_Header()
    dashboard.set_title("Pulse")
    dashboard.add_kpi({"Events / min": "12,841", "Live nodes": "48", "Alert level": "LOW"})
    dashboard.add_chart([gauge, wave, radar])
    dashboard.set_chart_per_row([3])
    dashboard.set_chart_titles(["Readiness", "Live signal", "Capability profile"])
    dashboard.set_chart_subtitles([None, "A 60-second synthetic telemetry window", None])
    dashboard.set_footer_text("PULSE / SYNTHETIC TELEMETRY")
    return dashboard


if __name__ == "__main__":
    launch(build_dashboard(), 8054)
