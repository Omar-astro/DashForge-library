from copy import deepcopy
import plotly.express as px
from plotly.graph_objects import Figure
from dash import Dash, Input, Output, State, dcc, html
import os
from flask import send_from_directory
from typing import Literal
from param import Color
from datetime import date

class Dashboard():
    '''Start by Initalizing the main variables of the dashboard'''
    def __init__(self):
        self.Title = None
        self.Logo = None
        self.footer_text = None
        self.FontFamily = "Arial, sans-serif"
        self.preset_choosen = "preset1"
        self.insights = False
        self.timestamp = False
        self.header_option = False
        self.kpi = {}
        self.charts = []
        self.chart_titles = []
        self.chart_subtitles = []
        self.chart_per_row = []
        self._allowed_presets = {"preset1"}
        #region color initialization
        self.line_colors = "#ff8c00"
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
        #endregion

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

    def set_chart_subtitles(self, subtitles: list):
        '''Set the subtitles for the charts'''
        self.chart_subtitles = subtitles

    def set_font_family(self, font_family: str):
        '''Set the font family for the dashboard'''
        self.FontFamily = font_family

    def set_footer_text(self, footer_text: str):
        '''Set the footer text for the dashboard'''
        self.footer_text = footer_text

    def set_theme(self, theme: Literal["dark", "light"]):
        '''Set the theme of the dashboard'''
        if theme not in ["dark", "light"]:
            raise ValueError("Theme must be 'dark' or 'light'")
        if theme == "dark":
            self.set_bg_color(behindchart="#1a1a1a",
                              outterChart="#1a1a1a",
                              innerChart="#1a1a1a",
                              HeaderBG="#2d2d2d",
                              KPIBackgroundArea="#2d2d2d",
                              KPICard="#1a1a1a",
                              ChartAreaBackground="#2d2d2d",
                              MaximizeButton="#1a1a1a",
                              ChartBorder="#3a3a3a",
                              ChartText="#ffffff")
        else:
            # Light theme: contrasting/inverted colors from the dark theme
            self.set_bg_color(
                line="#ff8c00",  # keep accent color
                behindchart="#ffffff",
                outterChart="#ffffff",
                innerChart="#ffffff",
                ChartText="#000000",
                HeaderBG="#f5f5f5",
                KPIBackgroundArea="#f5f5f5",
                KPICard="#ffffff",
                KPIText="#000000",
                ChartAreaBackground="#ffffff",
                MaximizeButton="#ffffff",
                ChartBorder="#cccccc",
            )

    def set_title(self, title:str):
        '''Set the title of the dashboard'''
        self.Title = title
    
    def hide_Header(self, hide: bool = True):
        '''Hide the header of the dashboard'''
        self.header_option = hide

    def add_chart(self, chart: Figure):
        '''Add a chart to the dashboard'''
        if isinstance(chart, Figure):
            self.charts.append(chart)
        elif isinstance(chart, list) and all(isinstance(c, Figure) for c in chart):
            self.charts.extend(chart)
        else:
            raise ValueError("Chart must be a plotly.graph_objects.Figure or a list of Figures")

    def set_chart_per_row(self, chart_amount: list):
        '''Set the number of charts per row in the dashboard'''
        '''Set the chart amount per row to match the number of charts added to the dashboard
         EX: If 6 charts are added to the dashboard, and the chart_amount is set to [2, 3, 1], 
         then the first row will have 2 charts, the second row will have 3 charts, 
         and the third row will have 1 chart.
         
            Example usage:
            add_chart([fig1, fig2, fig3, fig4, fig5, fig6])
            set_chart_per_row([2, 3, 1]) # This will set the first row to have 2 charts, the second row to have 3 charts, and the third row to have 1 chart.
         '''
        no_charts = len(self.charts)
        if sum(chart_amount) != no_charts:
            raise ValueError(f"Sum of chart_amount {sum(chart_amount)} does not match the number of charts added {no_charts}.")
        elif all(1 <= n <= 3 for n in chart_amount):
            raise ValueError("Each value in chart_amount must be between 1 and 3 (inclusive).")
        self.chart_per_row = chart_amount

    def add_timestamp(self, timestamp: bool = True):
        '''Add a timestamp to the dashboard'''
        if timestamp:
            self.timestamp = True
            self.Time = date.today().strftime("%Y-%m-%d")
        else:
            self.timestamp = False
    
    def set_logo(self, logo_path:str):
        '''Set the logo of the dashboard'''
        self.Logo = logo_path

    def add_kpi(self, kpi_name, kpi_value):
        '''Add a KPI to the dashboard'''
        self.insights = True
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
# Serve project-root files at /files/<filename> so plain paths like "Logo.png" work
        @self.app.server.route('/files/<path:filename>')
        def _serve_project_file(filename):
            return send_from_directory(os.getcwd(), filename)
#"#1a1a1a"
        dashboard_color = self.chartBG
        accent_color = self.line_colors

        def chunk_charts(charts, chunk_size=3):
            return [charts[index:index + chunk_size] for index in range(0, len(charts), chunk_size)]

        # Ensure multi-word font family names are quoted for valid CSS
        def _quote_font_family(ff: str) -> str:
            parts = [p.strip() for p in ff.split(',') if p is not None]
            out = []
            for p in parts:
                if (p.startswith("'") and p.endswith("'")) or (p.startswith('"') and p.endswith('"')):
                    out.append(p)
                elif ' ' in p:
                    out.append(f"'{p}'")
                else:
                    out.append(p)
            return ", ".join(out)

        safe_font_family = _quote_font_family(self.FontFamily)

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
                        font-family: {safe_font_family};
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
                        display: flex;
                        align-items: center;
                        gap: 12px;
                    }}

                    .dashboard-logo {{
                        height: 40px;
                        width: auto;
                        display: block;
                    }}

                    .dashboard-header h1 {{
                        color: {accent_color};
                        font-size: 32px;
                        line-height: 1.2;
                    }}

                    .dashboard-footer {{
                        background-color: {self.headerBG_color};
                        border-top: 3px solid {accent_color};
                        padding: 14px 30px;
                    }}

                    .dashboard-footer-content {{
                        width: 100%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 16px;
                        flex-wrap: wrap;
                    }}

                    .dashboard-footer-content:has(.dashboard-footer-text) {{
                        justify-content: space-between;
                    }}

                    .dashboard-footer-text {{
                        color: {accent_color};
                        font-size: 28px;
                        line-height: 1.2;
                        margin: 0;
                    }}

                    .Timestamp-with-footer {{
                        color: {self.chat_text_color};
                        font-size: 14px;
                        line-height: 1.2;
                        text-align: center;
                    }}

                    .Timestamp-only {{
                        color: {self.chat_text_color};
                        font-size: 14px;
                        line-height: 1.2;
                        text-align: center;
                    }}

                    .chart-subtitle {{
                        color: {self.chat_text_color};
                        font-size: 12px;
                        margin: 0;
                        opacity: 0.9;
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
                        width: 100%;
                        height: clamp(240px, 50.6vh, 400px);
                        overflow: hidden;
                    }}

                    .chart-wrapper.maximized .chart-card {{
                        height: clamp(384px, 80vh, 824px);
                    }}

                    .chart-card .dash-graph,
                    .chart-card .js-plotly-plot {{
                        height: 100% !important;
                    }}

                    .chart-wrapper.maximized .chart-card .dash-graph,
                    .chart-wrapper.maximized .chart-card .js-plotly-plot {{
                        height: 100% !important;
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
                        .chart-row {{
                            gap: 16px;
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
            i = 0
            j = 0
            while i < len(self.charts):
                if j < len(self.chart_per_row):
                    row_size = self.chart_per_row[j]
                else:
                    row_size = 3  # Default to 3 if not enough entries in chart_per_row
                j += 1
                row_charts = self.charts[i:i + row_size]
                row_cards = []

                for index, chart in enumerate(row_charts, start=i + 1):
                    # Determine title and optional subtitle for this chart.
                    # If an entry exists but is explicitly None, skip rendering for that entry.
                    if index <= len(self.chart_titles):
                        title_entry = self.chart_titles[index - 1]
                        title_text = None if title_entry is None else title_entry
                    else:
                        # no explicit title provided -> use default
                        title_text = f"Chart {index}"

                    if index <= len(self.chart_subtitles):
                        subtitle_entry = self.chart_subtitles[index - 1]
                        subtitle_text = None if subtitle_entry is None else subtitle_entry
                    else:
                        subtitle_text = None

                    # Build title block, omitting elements when None
                    title_children = []
                    if title_text is not None:
                        title_children.append(html.H3(title_text, className="chart-title"))
                    if subtitle_text is not None:
                        title_children.append(html.Div(subtitle_text, className="chart-subtitle"))
                    if not title_children:
                        # maintain layout spacing when both omitted
                        title_children = [html.Div()]

                    title_block = html.Div(title_children)

                    row_cards.append(
                        html.Div(
                            [
                                html.Div(
                                    [
                                        title_block,
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

                i += row_size
                chart_rows.append(
                    html.Div(
                        row_cards,
                        className="chart-row",
                        style={"gridTemplateColumns": f"repeat({len(row_charts)}, minmax(0, 1fr))"},
                    )
                )
        else:
            chart_rows = [
                html.Div(
                    [
                        html.H3("Chart", className="chart-title"),
                        html.Div("No charts added yet.", className="empty-state"),
                    ],
                    className="chart-row",
                    style={"gridTemplateColumns": "minmax(0, 1fr)"},
                )
            ]

        # Build header with optional logo on the top-left
        if self.Logo:
            # Use provided path, but map plain filenames to the /files/ route
            logo_src = self.Logo
            if not (
                logo_src.startswith("http://")
                or logo_src.startswith("https://")
                or logo_src.startswith("/")
                or logo_src.startswith("data:")
            ):
                logo_src = f"/files/{logo_src}"

            header_comp = html.Header(
                [
                    html.Img(src=logo_src, alt="Logo", className="dashboard-logo"),
                    html.H1(self.Title or "Dashboard"),
                ],
                className="dashboard-header",
            )
        else:
            header_comp = html.Header(html.H1(self.Title or "Dashboard"), className="dashboard-header")

        def _retrieve_timestamp():
            if self.footer_text:
                return html.P(f"Generated on {self.Time}", className="Timestamp-with-footer")
            else:
                return html.P(f"Generated on {self.Time}", className="Timestamp-only")

        self.app.layout = html.Div(
            [
                dcc.Store(id="maximized-chart"),
                header_comp if not self.header_option else None,
                html.Div(
                    [
                        html.Aside([ #KPI cards
                                    html.Div(
                                        [
                                            html.Div(kpi_name, className="insight-label"),
                                            html.Div(kpi_value, className="insight-value"),
                                        ],
                                        className="insight-card",
                                    )
                                    for kpi_name, kpi_value in self.kpi.items()
                                ]
                                   , className="insights-sidebar") if self.insights else None,
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
                html.Footer(
                    html.Div([
                        html.Div(self.footer_text, className="dashboard-footer-text") if self.footer_text else None,
                        _retrieve_timestamp() if self.timestamp else None
                    ], className="dashboard-footer-content"),
                    className="dashboard-footer",
                ) if self.footer_text or self.timestamp else None,
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
                    window.requestAnimationFrame(() => window.dispatchEvent(new Event('resize')));
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

                    window.requestAnimationFrame(() => window.dispatchEvent(new Event('resize')));
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
        self.app.run(debug=True, port=5000)
