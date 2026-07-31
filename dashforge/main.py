"""DashForge: build interactive Dash dashboards from Plotly figures.

The :class:`Dashboard` class collects Plotly figures and presentation settings,
then builds a ready-to-run Dash application. A minimal dashboard looks like::

    from dashforge.dashforge import Dashboard
    import plotly.express as px

    dashboard = Dashboard()
    dashboard.add_chart(px.bar(x=["North", "South"], y=[18, 24]))
    dashboard.build_dashboard()
    dashboard.run()
"""

from copy import deepcopy
from plotly.graph_objects import Figure
from dash import Dash, Input, Output, State, dash_table, dcc, html
import os
from flask import send_from_directory
from typing import Literal
from param import Color
from datetime import date
import pandas as pd

class Dashboard():
    """Configure and run a dashboard made from Plotly figures.

    A dashboard starts with sensible dark-theme defaults. Add one or more
    figures with :meth:`add_chart`, optionally configure its layout and
    presentation, then call :meth:`build_dashboard` followed by :meth:`run`.

    Example:
        >>> import plotly.express as px
        >>> dashboard = Dashboard()
        >>> dashboard.set_title("Sales overview")
        >>> dashboard.add_chart(px.bar(x=["Jan", "Feb"], y=[12, 18]))
        >>> dashboard.build_dashboard()
    """

    def __init__(self):
        """Create a dashboard with default settings and no charts."""
        self.port = 5000
        self.debug = True
        self.Title = None
        self.Logo = None
        self.footer_text = None
        self.dataset = None
        self.FontFamily = "Arial, sans-serif"
        self.data_name = "Data Table"
        self.preset_choosen = "preset1"
        self.insights = False
        self.timestamp = False
        self.header_option = False
        self.chart_row_tag = False
        self.kpi = {}
        self.charts = []
        self.chart_titles = []
        self.chart_subtitles = []
        self.chart_per_row = []
        self.custom_sizes = []
        self.max_buttons = []
        self._allowed_presets = {"preset1"}
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

    def set_colors(self, line: Color | None = None,
                     behindchart: Color | None = None,
                     outterChart: Color | None = None,
                     innerChart: Color | None = None,
                     ChartText: Color | None = None,
                     HeaderBG: Color | None = None,
                     KPIBackgroundArea: Color | None = None,
                     KPICard: Color | None = None,
                     KPIText: Color | None = None,
                     ChartAreaBackground: Color | None = None,
                     MaximizeButton: Color | None = None,
                     ChartBorder: Color | None = None
                     ):
        """Update one or more dashboard colors, leaving omitted values unchanged.

        Args:
            line: Accent color used for borders and headings.
            behindchart: Page-level dashboard background color.
            outterChart: Plotly figure background color.
            innerChart: Plotting-area background color.
            ChartText: Plotly chart text color.
            HeaderBG: Header and footer background color.
            KPIBackgroundArea: KPI sidebar background color.
            KPICard: Individual KPI card background color.
            KPIText: KPI value text color.
            ChartAreaBackground: Background behind chart cards.
            MaximizeButton: Maximize button text color.
            ChartBorder: Chart card border color.

        Example:
            >>> dashboard = Dashboard()
            >>> dashboard.set_colors(line="#0EA5E9", HeaderBG="#0F172A")
        """
        colour_updates = {
            "line_colors": line,
            "chartBG": behindchart,
            "outterchart_bg": outterChart,
            "innerChart_bg": innerChart,
            "chat_text_color": ChartText,
            "headerBG_color": HeaderBG,
            "kPIBG_color": KPIBackgroundArea,
            "kPICard_color": KPICard,
            "kPItext_color": KPIText,
            "chartArea_BG_color": ChartAreaBackground,
            "maxbtn_color": MaximizeButton,
            "ChartBorder_color": ChartBorder,
        }
        for attribute, colour in colour_updates.items():
            if colour is not None:
                setattr(self, attribute, colour)
        
    def set_chart_titles(self, titles: list):
        """Set chart-card titles in the same order as added charts.

        Use ``None`` for a chart that should not render a title.
        """
        self.chart_titles = titles

    def set_port(self, port: int):
        """Set the local port used by :meth:`run`."""
        self.port = port

    def set_dataset_name(self, data_name: str):
        """Set the heading shown on the optional dataset page."""
        self.data_name = data_name

    def set_debug(self, debug: bool):
        """Enable or disable Dash debug mode for :meth:`run`."""
        self.debug = debug

    def set_chart_subtitles(self, subtitles: list):
        """Set optional chart-card subtitles in the order charts were added.

        Use ``None`` for a chart that should not render a subtitle.
        """
        self.chart_subtitles = subtitles

    def set_font_family(self, font_family: str):
        """Set the CSS font family used throughout the dashboard.

        Example:
            >>> dashboard.set_font_family("Trebuchet MS, sans-serif")
        """
        self.FontFamily = font_family

    def set_footer_text(self, footer_text: str):
        """Set the text displayed in the dashboard footer."""
        self.footer_text = footer_text

    def add_dataset(self, dataset: pd.DataFrame):
        """Add a sortable and filterable pandas dataset page.

        Adding a dataset keeps the header visible because it provides the
        navigation control between the dashboard and dataset pages.

        Raises:
            ValueError: If ``dataset`` is not a pandas DataFrame.
        """
        self.hide_Header(False)
        if not isinstance(dataset, pd.DataFrame):
            raise ValueError("Dataset must be a pandas DataFrame")
        self.dataset = dataset

    def set_theme(self, theme: Literal["dark", "light"]):
        """Apply DashForge's built-in ``"dark"`` or ``"light"`` theme.

        A theme updates the dashboard color settings. Call :meth:`set_colors`
        afterwards to override individual colors.

        Raises:
            ValueError: If ``theme`` is not ``"dark"`` or ``"light"``.
        """
        if theme not in ["dark", "light"]:
            raise ValueError("Theme must be 'dark' or 'light'")
        if theme == "dark":
            self.set_colors(line="#ff8c00",
                              behindchart="#1a1a1a",
                              outterChart="#1a1a1a",
                              innerChart="#1a1a1a",
                              HeaderBG="#2d2d2d",
                              KPIBackgroundArea="#2d2d2d",
                              KPICard="#1a1a1a",
                              KPIText="#ffffff",
                              ChartAreaBackground="#2d2d2d",
                              MaximizeButton="#1a1a1a",
                              ChartBorder="#3a3a3a",
                              ChartText="#ffffff")
        else:
            self.set_colors(
                line="#ff8c00",
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
        """Set the dashboard title shown in the browser and header."""
        self.Title = title
    
    def hide_Header(self, hide: bool = True):
        """Show or hide the dashboard header.

        The header cannot be hidden while a dataset page is configured because
        it contains the button used to switch between the two pages.

        Raises:
            ValueError: If a dataset has already been added.
        """
        if self.dataset is not None:
            raise ValueError("Cannot hide header when a dataset is added. Remove the dataset first.")
        self.header_option = hide

    def add_chart(self, chart: Figure):
        """Add one Plotly figure or a list of Plotly figures.

        Args:
            chart: A ``plotly.graph_objects.Figure`` or a list containing only
                Plotly figures.

        Raises:
            ValueError: If the input is not a figure or a list of figures.

        Example:
            >>> dashboard.add_chart([figure_one, figure_two])
        """
        if isinstance(chart, Figure):
            self.charts.append(chart)
        elif isinstance(chart, list) and all(isinstance(c, Figure) for c in chart):
            self.charts.extend(chart)
        else:
            raise ValueError("Chart must be a plotly.graph_objects.Figure or a list of Figures")

    def set_chart_per_row(self, chart_amount: list):
        """Set the number of charts in each dashboard row.

        Each row may contain one, two, or three charts, and the total must
        equal the number of figures already added. For six charts, ``[2, 3, 1]``
        creates rows containing two, three, and one card.

        Raises:
            ValueError: If the counts do not match the chart total or a count
                is outside the inclusive range from 1 to 3.
         EX: If 6 charts are added to the dashboard, and the chart_amount is set to [2, 3, 1], 
         then the first row will have 2 charts, the second row will have 3 charts, 
         and the third row will have 1 chart.
         
            Example usage:
            add_chart([fig1, fig2, fig3, fig4, fig5, fig6])
            set_chart_per_row([2, 3, 1]) # This will set the first row to have 2 charts, the second row to have 3 charts, and the third row to have 1 chart.
        """

        self.chart_row_tag = True
        no_charts = len(self.charts)
        if sum(chart_amount) != no_charts:
            raise ValueError(f"Sum of chart_amount {sum(chart_amount)} does not match the number of charts added {no_charts}.")
        elif not all(1 <= n <= 3 for n in chart_amount):
            raise ValueError("Each value in chart_amount must be between 1 and 3 (inclusive).") 
        self.chart_per_row = chart_amount

    def set_max_buttons(self, max_buttons: list):
        """Choose which chart cards display a maximize button.

        Supply one boolean per chart. If this method is not called, every
        chart displays its maximize button.

        Raises:
            ValueError: If the list length differs from the chart count or any
                value is not a boolean.
        """
        if len(max_buttons) != len(self.charts):
            raise ValueError(f"Length of max_buttons {len(max_buttons)} does not match the number of charts {len(self.charts)}.")
        elif not all(isinstance(b, bool) for b in max_buttons):
            raise ValueError("All values in max_buttons must be boolean (True or False).")
        self.max_buttons = max_buttons

    def add_timestamp(self, timestamp: bool = True):
        """Show or hide a date stamp in the dashboard footer.

        Args:
            timestamp: ``True`` records and displays today's date; ``False``
                removes the timestamp.
        """
        if timestamp:
            self.timestamp = True
            self.Time = date.today().strftime("%Y-%m-%d")
        else:
            self.timestamp = False
    
    def set_custom_size(self, sizes_list: list):
        """Set per-chart width and height values for each dashboard row.

        Each row is either ``None`` for default sizing or a list of
        ``[width, height]`` pairs. The list must contain an entry for every
        dashboard row and each configured row must contain an entry for every
        chart in that row.

        Example:
            >>> dashboard.set_chart_per_row([2, 1])
            >>> dashboard.set_custom_size([[[65, 120], [35, 120]],
                                         [[100, 90]]])

        Raises:
            ValueError: If the row structure or a size pair is invalid.
        """
        if not self.chart_row_tag:
            no_rows = len(self.charts) // 3 + (len(self.charts) % 3 > 0)
        else:
            no_rows = len(self.chart_per_row)

        if len(sizes_list) != no_rows:
            raise ValueError(f"Length of sizes_list {len(sizes_list)} does not match the number of rows {no_rows}.")
        for i in range(len(sizes_list)):
            values = sizes_list[i]
            if values is not None:
                if not isinstance(values, list):
                    raise ValueError("Each row's size specification must be a list or None.")

                if not self.chart_row_tag:
                    expected_charts_in_row = 3 if i < no_rows - 1 else len(self.charts) % 3 or 3
                else:
                    expected_charts_in_row = self.chart_per_row[i]
                if len(values) != expected_charts_in_row:
                    raise ValueError(f"Row {i + 1} expects {expected_charts_in_row} size specifications, but got {len(values)}.")
                
                for size in values:
                    if not (isinstance(size, list) and len(size) == 2 and all(isinstance(dim, (int, float)) for dim in size)):
                        raise ValueError("Each chart's size must be a list of two numbers [width, height].")
        self.custom_sizes = sizes_list
            
    def set_logo(self, logo_path:str):
        """Set the logo source displayed at the left of the dashboard header.

        A plain relative path is served from the current working directory.
        Absolute web URLs and data URLs can also be used.
        """
        self.Logo = logo_path

    def add_kpi(self, kpi_name, kpi_value = None):
        """Add one KPI card or update several KPI cards at once.

        Args:
            kpi_name: A label, numeric label, or dictionary mapping labels to
                displayed values.
            kpi_value: Displayed value when ``kpi_name`` is a single label.

        Raises:
            ValueError: If ``kpi_name`` is not a supported label or dictionary.

        Example:
            >>> dashboard.add_kpi("Monthly revenue", "$42,000")
            >>> dashboard.add_kpi({"Customers": 128, "Conversion": "4.6%"})
        """
        self.insights = True
        
        if isinstance(kpi_name, str) or isinstance(kpi_name, int) or isinstance(kpi_name, float):
            self.kpi[kpi_name] = kpi_value
        elif isinstance(kpi_name, dict):
            self.kpi.update(kpi_name)
        else:
            raise ValueError("KPI name must be a string or a dictionary")

    def preset(self, preset_name):
        """Choose a supported dashboard layout preset.

        Currently, ``"preset1"`` is the available preset.

        Raises:
            ValueError: If the preset name is not supported.
        """
        if preset_name not in self._allowed_presets:
            raise ValueError(f"Preset not found. Allowed presets: {', '.join(sorted(self._allowed_presets))}")
        self.preset_choosen = preset_name

    def build_dashboard(self):
        """Build and return the configured Dash application.

        Call this after configuring the dashboard and before :meth:`run` when
        you need direct access to the underlying Dash app.

        Returns:
            dash.Dash: The generated Dash application.
        """
        if self.preset_choosen == "preset1":
            return self.__layout1()
        else:
            raise ValueError("Preset not found")
        
    def __layout1(self):
        """Create the internal layout used by the ``preset1`` dashboard."""
        self.app = Dash(__name__)
        self.app.title = self.Title or "Dashboard"
        @self.app.server.route('/files/<path:filename>')
        def _serve_project_file(filename):
            return send_from_directory(os.getcwd(), filename)
        dashboard_color = self.chartBG
        accent_color = self.line_colors

        def chunk_charts(charts, chunk_size=3):
            return [charts[index:index + chunk_size] for index in range(0, len(charts), chunk_size)]

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

                    .page-toggle-btn {{
                        margin-left: auto;
                        background-color: {accent_color};
                        color: {self.maxbtn_color};
                        border: none;
                        border-radius: 5px;
                        padding: 9px 14px;
                        cursor: pointer;
                        font-weight: bold;
                    }}

                    .page-toggle-btn:hover {{
                        filter: brightness(1.12);
                    }}

                    .dataset-page-main {{
                        flex: 1;
                        padding: 20px;
                        overflow: auto;
                    }}

                    .dataset-card {{
                        width: 100%;
                        background-color: {self.chartArea_BG_color};
                        border-left: 5px solid {accent_color};
                        border-radius: 8px;
                        padding: 20px;
                    }}

                    .dataset-heading {{
                        display: flex;
                        align-items: baseline;
                        justify-content: space-between;
                        gap: 12px;
                        margin-bottom: 18px;
                        flex-wrap: wrap;
                    }}

                    .dataset-title {{
                        color: {accent_color};
                        font-size: 24px;
                        margin: 0;
                    }}

                    .dataset-summary {{
                        color: {self.chat_text_color};
                        font-size: 14px;
                        opacity: 0.85;
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
                        padding-right: 30px;
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

                    .maximize-btn.hidden {{
                        display: none;
                    }}
                    


                    .chart-card {{
                        background-color: {self.ChartBorder_color};
                        border: 2px solid {accent_color};
                        border-radius: 8px;
                        padding: 15px;
                        width: 100%;
                        height: calc(clamp(240px, 50.6vh, 400px) * var(--chart-height-scale, 1));
                        overflow: hidden;
                    }}



                    .chart-wrapper.maximized .chart-card {{
                        height: calc(clamp(384px, 80vh, 824px) * var(--chart-height-scale, 1));
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
                    paper_bgcolor= self.outterchart_bg,
                    plot_bgcolor= self.innerChart_bg,
                    font={"color": self.chat_text_color},
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

        def _row_sizes_for(row_index: int):
            if row_index >= len(self.custom_sizes):
                return None
            return self.custom_sizes[row_index]

        def _chart_height_style(size_spec):
            if size_spec is None:
                return {}
            return {"--chart-height-scale": str(size_spec[1] / 100)}

        def _row_grid_style(row_sizes, row_length: int):
            if row_sizes is None:
                return {"gridTemplateColumns": f"repeat({row_length}, minmax(0, 1fr))"}

            return {
                "gridTemplateColumns": " ".join(
                    f"minmax(0, {100 if size_spec is None else size_spec[0]}fr)"
                    for size_spec in row_sizes
                )
            }

        chart_rows = []
        if self.charts:
            i = 0
            j = 0
            while i < len(self.charts):
                if j < len(self.chart_per_row):
                    row_size = self.chart_per_row[j]
                else:
                    row_size = 3
                j += 1
                row_charts = self.charts[i:i + row_size]
                row_sizes = _row_sizes_for(len(chart_rows))
                row_cards = []

                for offset, chart in enumerate(row_charts):
                    MaxButton_enable = True if (not self.max_buttons) else self.max_buttons[i + offset]
                    button_class_name = "maximize-btn" if MaxButton_enable else "maximize-btn hidden"

                    index = i + offset + 1
                    if index <= len(self.chart_titles):
                        title_entry = self.chart_titles[index - 1]
                        title_text = None if title_entry is None else title_entry
                    else:
                        title_text = f"Chart {index}"

                    if index <= len(self.chart_subtitles):
                        subtitle_entry = self.chart_subtitles[index - 1]
                        subtitle_text = None if subtitle_entry is None else subtitle_entry
                    else:
                        subtitle_text = None

                    title_children = []
                    if title_text is not None:
                        title_children.append(html.H3(title_text, className="chart-title"))
                    if subtitle_text is not None:
                        title_children.append(html.Div(subtitle_text, className="chart-subtitle"))
                    if not title_children:
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
                                            className=button_class_name,
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
                                    style=_chart_height_style(
                                        row_sizes[offset] if row_sizes is not None and offset < len(row_sizes) else None
                                    ),
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
                        style=_row_grid_style(row_sizes, len(row_charts)),
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
        if self.Logo:
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
                    html.Button(
                        "Page 2",
                        id="page-toggle",
                        n_clicks=0,
                        className="page-toggle-btn",
                    ) if self.dataset is not None else None,
                ],
                className="dashboard-header",
            )
        else:
            header_comp = html.Header(
                [
                    html.H1(self.Title or "Dashboard"),
                    html.Button(
                        "Page 2",
                        id="page-toggle",
                        n_clicks=0,
                        className="page-toggle-btn",
                    ) if self.dataset is not None else None,
                ],
                className="dashboard-header",
            )
        def _retrieve_timestamp():
            if self.footer_text:
                return html.P(f"Generated on {self.Time}", className="Timestamp-with-footer")
            else:
                return html.P(f"Generated on {self.Time}", className="Timestamp-only")

        dataset_page = None
        if self.dataset is not None:
            dataset_page = html.Main(
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(self.data_name, className="dataset-title"),
                                html.Span(
                                    f"{len(self.dataset):,} rows · {len(self.dataset.columns):,} columns",
                                    className="dataset-summary",
                                ),
                            ],
                            className="dataset-heading",
                        ),
                        dash_table.DataTable(
                            id="data-table",
                            columns=[{"name": str(column), "id": str(column)} for column in self.dataset.columns],
                            data=self.dataset.rename(columns=str).to_dict("records"),
                            page_size=20,
                            sort_action="native",
                            filter_action="native",
                            style_table={"overflowX": "auto"},
                            style_header={
                                "backgroundColor": accent_color,
                                "color": self.maxbtn_color,
                                "fontWeight": "bold",
                                "border": f"1px solid {accent_color}",
                            },
                            style_data={
                                "backgroundColor": self.kPICard_color,
                                "color": self.chat_text_color,
                                "border": f"1px solid {self.ChartBorder_color}",
                            },
                            style_cell={
                                "padding": "12px",
                                "minWidth": "120px",
                                "width": "120px",
                                "maxWidth": "320px",
                                "textAlign": "left",
                                "fontFamily": safe_font_family,
                                "whiteSpace": "normal",
                                "height": "auto",
                            },
                            style_filter={
                                "backgroundColor": self.outterchart_bg,
                                "color": self.chat_text_color,
                            },
                        ),
                    ],
                    className="dataset-card",
                ),
                className="dataset-page-main",
            )

        self.app.layout = html.Div(
            [
                dcc.Store(id="maximized-chart"),
                header_comp if not self.header_option else None,
                html.Div(
                    [
                        html.Aside([
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
                    id="page-one",
                ),
                html.Div(
                    dataset_page,
                    className="dashboard-main",
                    id="page-two",
                    style={"display": "none"},
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

        if not self.header_option and self.dataset is not None:
            @self.app.callback(
                Output("page-one", "style"),
                Output("page-two", "style"),
                Output("page-toggle", "children"),
                Input("page-toggle", "n_clicks"),
            )
            def toggle_page(n_clicks):
                showing_page_two = n_clicks and n_clicks % 2 == 1

                if showing_page_two:
                    return {"display": "none"}, {"display": "flex"}, "Dashboard"

                return {"display": "flex"}, {"display": "none"}, "Page 2"

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
        """Start the configured Dash server.

        Call :meth:`build_dashboard` first. The server uses the port and debug
        values configured with :meth:`set_port` and :meth:`set_debug`.
        """
        self.app.run(debug=self.debug, port=self.port)
