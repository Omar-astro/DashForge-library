from copy import deepcopy
import plotly.express as px
from plotly.graph_objects import Figure
from dash import Dash, Input, Output, State, dcc, html
from typing import Literal
from param import Color

class Dashboard():
    '''Start by Initalizing the main variables of the dashboard'''
    def __init__(self):
        self.line_colors = "#ff8c00"
        self.Title = None
        self.charts = []
        self.kpi = {}
        self.preset_choosen = "preset1"
        self.chart_titles = []
        self._allowed_presets = {"preset1"}
        self.chartBG = "#1a1a1a"
        self.outterchart_bg = "#1a1a1a"
        self.innerChart_bg = "#1a1a1a"
        self.chat_text_color = "#ffffff"
        self.headerBG_color = "#2d2d2d"
        self.kPIBG_color = "#2d2d2d"
        self.kPICard_color = "#1a1a1a"
        self.kPItext_color = "#ffffff"
        self.chartArea_BG_color = "#2d2d2d"
        self.maxbtn_color = "#1a1a1a"
        self.ChartBorder_color = "#3a3a3a"

    def set_bg_color(self, line: Color = "#ff8c00",
                     behindchart: Color = "#1a1a1a",
                     outterChart: Color = "#1a1a1a",
                     innerChart: Color = "#1a1a1a",
                     ChartText: Color = "#ffffff",
                     HeaderBG: Color = "#2d2d2d",
                     KPIBackgroundArea: Color = "#2d2d2d",
                     KPICard: Color = "#1a1a1a",
                     KPIText: Color = "#ffffff",
                     ChartAreaBackground: Color = "#2d2d2d",
                     MaximizeButton: Color = "#1a1a1a",
                     ChartBorder: Color = "#3a3a3a"
                     ):
        '''Set the background color of the dashboard'''
        self.line_colors = line
        self.chartBG = behindchart
        self.outterchart_bg = outterChart
        self.innerChart_bg = innerChart
        self.chat_text_color = ChartText
        self.headerBG_color = HeaderBG
        self.kPIBG_color = KPIBackgroundArea
        self.kPICard_color = KPICard
        self.kPItext_color = KPIText
        self.chartArea_BG_color = ChartAreaBackground
        self.maxbtn_color = MaximizeButton
        self.ChartBorder_color = ChartBorder
        
    def set_chart_titles(self, titles: list):
        '''Set the titles for the charts'''
        self.chart_titles = titles

    def set_title(self, title:str):
        '''Set the title of the dashboard'''
        self.Title = title
    
    def add_chart(self, chart: Figure):
        '''Add a chart to the dashboard'''
        self.charts.append(chart)

    def add_kpi(self, kpi_name, kpi_value):
        '''Add a KPI to the dashboard'''
        self.kpi[kpi_name] = kpi_value
    
    def preset(self, preset_name):
        '''Choose a preset for the dashboard'''
        if preset_name not in self._allowed_presets:
            raise ValueError(f"Preset not found. Allowed presets: {', '.join(sorted(self._allowed_presets))}")
        self.preset_choosen = preset_name

    def build_dashboard(self):
        '''Build the dashboard layout'''
        if self.preset_choosen == "preset1":
            return self.__layout1()
        else:
            raise ValueError("Preset not found")
        
    def __layout1(self):
        self.app = Dash(__name__)
        self.app.title = self.Title or "Dashboard"
#"#1a1a1a"
        dashboard_color = self.chartBG
        accent_color = self.line_colors

        def chunk_charts(charts, chunk_size=3):
            return [charts[index:index + chunk_size] for index in range(0, len(charts), chunk_size)]

        self.app.index_string = f"""
        <!DOCTYPE html>
        <html>
            <head>
                {{%metas%}}
                <title>{{%title%}}</title>
                {{%favicon%}}
                {{%css%}}
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}

                    body {{
                        min-height: 100vh;
                        background-color: {dashboard_color};
                        font-family: Arial, sans-serif;
                    }}

                    .dashboard-shell {{
                        min-height: 100vh;
                        background-color: {dashboard_color};
                        color: #e0e0e0;
                    }}

                    .dashboard-header {{
                        background-color: {self.headerBG_color};
                        border-bottom: 3px solid {accent_color};
                        padding: 14px 30px;
                    }}

                    .dashboard-header h1 {{
                        color: {accent_color};
                        font-size: 32px;
                        line-height: 1.2;
                    }}

                    .dashboard-main {{
                        display: flex;
                        min-height: calc(100vh - 68px);
                    }}

                    .insights-sidebar {{
                        width: 350px;
                        background-color: {self.kPIBG_color};
                        border-right: 3px solid {accent_color};
                        padding: 20px;
                        overflow-y: auto;
                    }}

                    .insight-card {{
                        background-color: {self.kPICard_color};
                        border: 2px solid {accent_color};
                        border-radius: 8px;
                        padding: 20px;
                        margin-bottom: 20px;
                    }}

                    .insight-label {{
                        color: {accent_color};
                        font-size: 14px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        text-align: center;
                    }}

                    .insight-value {{
                        color: {self.kPItext_color};
                        font-size: 30px;
                        font-weight: bold;
                        text-align: center;
                        overflow-wrap: anywhere;
                    }}

                    .charts-main {{
                        flex: 1;
                        padding: 20px;
                        overflow-y: auto;
                    }}

                    .dashboard-content {{
                        background-color: {self.chartArea_BG_color};
                        border-left: 5px solid {accent_color};
                        border-radius: 8px;
                        padding: 15px;
                        width: 100%;
                    }}

                    .chart-grid {{
                        display: flex;
                        flex-direction: column;
                        gap: 20px;
                        width: 100%;
                    }}

                    .chart-row {{
                        display: grid;
                        gap: 20px;
                        width: 100%;
                    }}

                    .chart-row-1 {{
                        grid-template-columns: minmax(0, 1fr);
                    }}

                    .chart-row-2 {{
                        grid-template-columns: repeat(2, minmax(0, 1fr));
                    }}

                    .chart-row-3 {{
                        grid-template-columns: repeat(3, minmax(0, 1fr));
                    }}

                    .chart-wrapper {{
                        min-width: 0;
                    }}

                    .chart-wrapper.hidden {{
                        display: none;
                    }}

                    .chart-wrapper.maximized {{
                        grid-column: 1 / -1;
                    }}

                    .chart-title-row {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        gap: 10px;
                        margin-bottom: 10px;
                    }}

                    .chart-title {{
                        color: {accent_color};
                        font-size: 18px;
                        margin: 0;
                    }}

                    .maximize-btn {{
                        background-color: {accent_color};
                        color: {self.maxbtn_color};
                        border: none;
                        border-radius: 5px;
                        padding: 8px 12px;
                        cursor: pointer;
                        font-weight: bold;
                    }}

                    .maximize-btn:hover {{
                        filter: brightness(1.12);
                    }}

                    .chart-card {{
                        background-color: {self.ChartBorder_color};
                        border: 2px solid {accent_color};
                        border-radius: 8px;
                        padding: 15px;
                        min-height: 330px;
                        overflow: hidden;
                    }}

                    .chart-row-1 .chart-card {{
                        min-height: 450px;
                    }}

                    .chart-row-2 .chart-card {{
                        min-height: 375px;
                    }}

                    .chart-row-3 .chart-card {{
                        min-height: 300px;
                    }}

                    .chart-wrapper.maximized .chart-card {{
                        min-height: 640px;
                    }}

                    .chart-card .dash-graph,
                    .chart-card .js-plotly-plot {{
                        height: 100% !important;
                    }}

                    .chart-row-1 .chart-card .dash-graph,
                    .chart-row-1 .chart-card .js-plotly-plot {{
                        height: 420px !important;
                    }}

                    .chart-row-2 .chart-card .dash-graph,
                    .chart-row-2 .chart-card .js-plotly-plot {{
                        height: 345px !important;
                    }}

                    .chart-row-3 .chart-card .dash-graph,
                    .chart-row-3 .chart-card .js-plotly-plot {{
                        height: 270px !important;
                    }}

                    .chart-wrapper.maximized .chart-card .dash-graph,
                    .chart-wrapper.maximized .chart-card .js-plotly-plot {{
                        height: 610px !important;
                    }}

                    .empty-state {{
                        min-height: 300px;
                        border: 1px dashed #777;
                        border-radius: 6px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: #ff00ea;
                        font-weight: bold;
                        text-align: center;
                    }}

                    @media (max-width: 1200px) {{
                        .chart-row-3 {{
                            grid-template-columns: repeat(2, minmax(0, 1fr));
                        }}
                    }}

                    @media (max-width: 850px) {{
                        .dashboard-main {{
                            flex-direction: column;
                        }}

                        .insights-sidebar {{
                            width: 100%;
                            border-right: none;
                            border-bottom: 3px solid {accent_color};
                        }}

                        .chart-row {{
                            grid-template-columns: 1fr;
                        }}

                        .chart-row-1 .chart-card,
                        .chart-row-2 .chart-card,
                        .chart-row-3 .chart-card {{
                            min-height: 300px;
                        }}

                        .chart-row-1 .chart-card .dash-graph,
                        .chart-row-1 .chart-card .js-plotly-plot,
                        .chart-row-2 .chart-card .dash-graph,
                        .chart-row-2 .chart-card .js-plotly-plot,
                        .chart-row-3 .chart-card .dash-graph,
                        .chart-row-3 .chart-card .js-plotly-plot {{
                            height: 270px !important;
                        }}
                    }}
                </style>
            </head>
            <body>
                {{%app_entry%}}
                <footer>
                    {{%config%}}
                    {{%scripts%}}
                    {{%renderer%}}
                </footer>
            </body>
        </html>
        """

        insights = [
            html.Div(
                [
                    html.Div(kpi_name, className="insight-label"),
                    html.Div(kpi_value, className="insight-value"),
                ],
                className="insight-card",
            )
            for kpi_name, kpi_value in self.kpi.items()
        ]

        def styled_chart(chart):
            figure = deepcopy(chart)
            try:
                figure.update_layout(
                    paper_bgcolor= self.outterchart_bg, # outer chart bg color
                    plot_bgcolor= self.innerChart_bg, # inner chart bg color
                    font={"color": self.chat_text_color}, # Chart text color
                    dragmode="pan",
                    uirevision="dashforge",
                    margin={"l": 40, "r": 20, "t": 20, "b": 40},
                )
            except AttributeError:
                if isinstance(figure, dict):
                    figure.setdefault("layout", {})
                    figure["layout"].update(
                        {
                            "paper_bgcolor": self.outterchart_bg,
                            "plot_bgcolor": self.innerChart_bg,
                            "font": {"color": self.chat_text_color},
                            "dragmode": "pan",
                            "uirevision": "dashforge",
                            "margin": {"l": 40, "r": 20, "t": 20, "b": 40},
                        }
                    )
            return figure

        chart_rows = []

        if self.charts:
            for i in range(0, len(self.charts), 3):
                row_charts = self.charts[i:i + 3]
                row_cards = []

                for index, chart in enumerate(row_charts, start=i + 1):
                    row_cards.append(
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(self.chart_titles[index - 1] if index <= len(self.chart_titles) else f"Chart {index}", className="chart-title"),
                                        html.Button(
                                            "⛶",
                                            id=f"chart-toggle-{index}",
                                            n_clicks=0,
                                            className="maximize-btn",
                                            title="Maximize chart",
                                        ),
                                    ],
                                    className="chart-title-row",
                                ),
                                html.Div(
                                    dcc.Graph(
                                        figure=styled_chart(chart),
                                        config={
                                            "displayModeBar": True,
                                            "displaylogo": False,
                                            "scrollZoom": True,
                                            "responsive": True,
                                        },
                                    ),
                                    className="chart-card",
                                ),
                            ],
                            id=f"chart-wrapper-{index}",
                            className="chart-wrapper",
                        )
                    )

                chart_rows.append(
                    html.Div(
                        row_cards,
                        className=f"chart-row chart-row-{len(row_charts)}",
                    )
                )
        else:
            chart_rows = [
                html.Div(
                    [
                        html.H3("Chart", className="chart-title"),
                        html.Div("No charts added yet.", className="empty-state"),
                    ],
                    className="chart-row chart-row-1",
                )
            ]

        self.app.layout = html.Div(
            [
                dcc.Store(id="maximized-chart"),
                html.Header(html.H1(self.Title or "Dashboard"), className="dashboard-header"),
                html.Div(
                    [
                        html.Aside(insights, className="insights-sidebar") if insights else None,
                        html.Main(
                            html.Div(
                                html.Div(chart_rows, id="chart-grid", className="chart-grid"),
                                className="dashboard-content",
                            ),
                            className="charts-main",
                        ),
                    ],
                    className="dashboard-main",
                ),
            ],
            className="dashboard-shell",
        )

        if self.charts:
            chart_count = len(self.charts)

            self.app.clientside_callback(
                """
                function() {
                    const currentChart = arguments[arguments.length - 1];
                    const triggered = dash_clientside.callback_context.triggered;

                    if (!triggered.length) {
                        return currentChart;
                    }

                    const buttonId = triggered[0].prop_id.split('.')[0];
                    if (!buttonId.startsWith('chart-toggle-')) {
                        return currentChart;
                    }

                    const selectedChart = buttonId.replace('chart-toggle-', '');
                    return currentChart === selectedChart ? null : selectedChart;
                }
                """,
                Output("maximized-chart", "data"),
                [Input(f"chart-toggle-{index}", "n_clicks") for index in range(1, chart_count + 1)],
                State("maximized-chart", "data"),
                prevent_initial_call=True,
            )

            self.app.clientside_callback(
                """
                function(maximizedChart) {
                    const gridClass = maximizedChart ? 'chart-grid maximized' : 'chart-grid';
                    const wrapperClasses = [];
                    const buttonLabels = [];

                    for (let index = 1; index <= %d; index++) {
                        const chartId = String(index);
                        if (!maximizedChart) {
                            wrapperClasses.push('chart-wrapper');
                            buttonLabels.push('⛶');
                        } else if (maximizedChart === chartId) {
                            wrapperClasses.push('chart-wrapper maximized');
                            buttonLabels.push('Back');
                        } else {
                            wrapperClasses.push('chart-wrapper hidden');
                            buttonLabels.push('⛶');
                        }
                    }

                    return [gridClass, ...wrapperClasses, ...buttonLabels];
                }
                """ % chart_count,
                Output("chart-grid", "className"),
                [Output(f"chart-wrapper-{index}", "className") for index in range(1, chart_count + 1)],
                [Output(f"chart-toggle-{index}", "children") for index in range(1, chart_count + 1)],
                Input("maximized-chart", "data"),
                prevent_initial_call=True,
            )

        return self.app

    def run(self):
        '''Run the dashboard'''
        self.app.run(debug=False, port=5000)
