from dash import Dash, Input, Output, State, callback_context, dcc, html


APP_CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    background-color: #1a1a1a;
    font-family: Arial, sans-serif;
}

.app-shell {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #1a1a1a;
}

.main-wrapper {
    display: flex;
    flex: 1;
}

.sidebar {
    width: 350px;
    background-color: #2d2d2d;
    border-right: 3px solid #ff8c00;
    padding: 20px;
    overflow-y: auto;
}

.sidebar-stat {
    background-color: #1a1a1a;
    border: 2px solid #ff8c00;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.stat-label {
    color: #ff8c00;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: center;
}

.stat-value {
    color: #ffffff;
    font-size: 32px;
    font-weight: bold;
    text-align: center;
}

header {
    background-color: #2d2d2d;
    border-bottom: 3px solid #ff8c00;
    padding: 12px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}

header h1 {
    color: #ff8c00;
    font-size: 32px;
}

.header-controls {
    display: flex;
    gap: 15px;
    align-items: center;
}

.header-controls select,
.header-controls button,
.header-controls .Select-control {
    background-color: #ff8c00;
    color: #1a1a1a;
}

.control-dropdown {
    width: 135px;
    color: #1a1a1a;
    font-weight: bold;
}

.control-button,
.filter-button,
.maximize-btn,
.dataset-button {
    padding: 10px 15px;
    background-color: #ff8c00;
    color: #1a1a1a;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
}

.control-button:hover,
.filter-button:hover,
.maximize-btn:hover {
    background-color: #ffaa33;
}

main {
    flex: 1;
    padding: 20px;
    background-color: #1a1a1a;
    overflow-y: auto;
}

.dashboard-content {
    background-color: #2d2d2d;
    padding: 15px;
    border-radius: 8px;
    border-left: 5px solid #ff8c00;
    color: #e0e0e0;
}

.chart-container {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.chart-container.maximized {
    grid-template-columns: 1fr;
}

.chart-wrapper {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.chart-wrapper.hidden {
    display: none;
}

.chart-wrapper.maximized {
    grid-column: 1 / -1;
}

.chart-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    gap: 10px;
}

.chart-title-row h3 {
    color: #ff8c00;
    font-size: 18px;
    margin: 0;
}

.chart {
    background-color: #3a3a3a;
    border: 2px solid #ff8c00;
    border-radius: 8px;
    padding: 15px;
    min-height: 330px;
    max-height: 330px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.chart-wrapper.maximized .chart {
    min-height: 600px;
    max-height: none;
}

.chart-body {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px dashed #777;
    border-radius: 6px;
    color: #ffaa33;
    text-align: center;
    padding: 20px;
}

.placeholder-title {
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
}

.placeholder-note {
    color: #bdbdbd;
    font-size: 14px;
}

.chart-filters-header {
    background-color: #2d2d2d;
    border-bottom: 2px solid #ff8c00;
    padding: 15px 30px;
    gap: 40px;
    align-items: center;
    flex-wrap: wrap;
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

.filter-group label {
    color: #ff8c00;
    font-weight: bold;
    font-size: 14px;
    white-space: nowrap;
}

.filter-dropdown {
    width: 95px;
    color: #1a1a1a;
}

.filter-checkbox label {
    color: #ff8c00;
    font-weight: bold;
}

.dataset-view-container {
    padding: 40px;
}

.dataset-view-title {
    color: #ff8c00;
    margin-bottom: 15px;
}

.dataset-selector-container {
    margin-bottom: 30px;
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
}

.dataset-button {
    border: 2px solid #ff8c00;
    background-color: transparent;
    color: #ff8c00;
}

.dataset-button.active {
    background-color: #ff8c00;
    color: #1a1a1a;
}

.dataset-container {
    overflow-x: auto;
    margin-top: 20px;
}

.dataset-table {
    width: 100%;
    border-collapse: collapse;
    color: #ffffff;
}

.dataset-table thead tr {
    background-color: #ff8c00;
    color: #1a1a1a;
}

.dataset-table th,
.dataset-table td {
    padding: 10px;
    border: 1px solid #555;
    text-align: left;
}

.dataset-table tbody tr {
    border-bottom: 1px solid #333;
}

footer {
    background-color: #0f0f0f;
    border-top: 3px solid #ff8c00;
    padding: 20px;
    text-align: center;
    color: #888;
    font-size: 14px;
}

@media (max-width: 1200px) {
    .chart-container {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 850px) {
    header,
    .main-wrapper {
        flex-direction: column;
        align-items: stretch;
    }

    .sidebar {
        width: 100%;
        border-right: none;
        border-bottom: 3px solid #ff8c00;
    }

    .chart-container {
        grid-template-columns: 1fr;
    }

    .header-controls {
        flex-wrap: wrap;
    }
}
"""

YEARS = [{"label": str(year), "value": str(year)} for year in range(2021, 2026)]

SIDEBAR_STATS = [
    ("Total number of students:", "-"),
    ("Number of subjects:", "-"),
    ("Average pass rate:", "-"),
    ("Average fail rate:", "-"),
    ("Average base pay:", "-"),
    ("Highest paying role:", "-"),
]

CHART_TITLES = [
    "Total Students per Year",
    "Failed Students by Subject",
    "Passed Students by Subject",
    "Students by Delivery Mode & Year",
    "Fees by State",
    "Base Pay by Job Title",
]

DATASET_NAMES = {
    "1": "Dataset 1",
    "2": "Dataset 2",
    "3": "Dataset 3",
}


def stat_card(label, value):
    return html.Div(
        [
            html.Div(label, className="stat-label"),
            html.Div(value, className="stat-value"),
        ],
        className="sidebar-stat",
    )


def filter_group(title, checklist_id, dropdown_id, button_id):
    return html.Div(
        [
            html.Label(title),
            dcc.Checklist(
                id=checklist_id,
                options=[{"label": "Apply", "value": "apply"}],
                value=[],
                className="filter-checkbox",
            ),
            html.Label("Year:"),
            dcc.Dropdown(
                id=dropdown_id,
                options=YEARS,
                value="2021",
                clearable=False,
                className="filter-dropdown",
            ),
            html.Button("OK", id=button_id, n_clicks=0, className="filter-button"),
        ],
        className="filter-group",
    )


def chart_card(index, title):
    return html.Div(
        [
            html.Div(
                [
                    html.H3(title, id=f"chart-title-{index}"),
                    html.Button(
                        "Maximize",
                        id=f"chart-toggle-{index}",
                        n_clicks=0,
                        className="maximize-btn",
                    ),
                ],
                className="chart-title-row",
            ),
            html.Div(
                html.Div(
                    [
                        html.Div(title, className="placeholder-title"),
                        html.Div(
                            "Chart placeholder reserved for Dash/Plotly content.",
                            className="placeholder-note",
                        ),
                    ],
                    className="chart-body",
                ),
                className="chart",
            ),
        ],
        id=f"chart-wrapper-{index}",
        className="chart-wrapper",
    )


def dataset_table(dataset_number):
    return html.Div(
        html.Table(
            [
                html.Thead(html.Tr([html.Th("Column 1")])),
                html.Tbody(
                    html.Tr(
                        html.Td(
                            f"{DATASET_NAMES[dataset_number]} placeholder. "
                            "Dataset loading can be wired here later."
                        )
                    )
                ),
            ],
            className="dataset-table",
        ),
        className="dataset-container",
    )


app = Dash(__name__)
app.title = "Dashboard"
app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{APP_CSS}</style>
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

app.layout = html.Div(
    [
        dcc.Store(id="maximized-chart"),
        dcc.Store(id="active-dataset", data="1"),
        html.Header(
            [
                html.H1("Dashboard"),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="view-mode",
                            options=[
                                {"label": "Graphs", "value": "graphs"},
                                {"label": "Dataset", "value": "dataset"},
                            ],
                            value="graphs",
                            clearable=False,
                            className="control-dropdown",
                        ),
                        html.Button("Export", id="export-button", n_clicks=0, className="control-button"),
                        html.Button("v", id="filter-toggle", n_clicks=0, className="control-button"),
                    ],
                    className="header-controls",
                ),
            ]
        ),
        html.Div(
            [
                filter_group(
                    "Failed Students Filter:",
                    "failed-filter-apply",
                    "failed-filter-year",
                    "failed-filter-button",
                ),
                filter_group(
                    "Passed Students Filter:",
                    "passed-filter-apply",
                    "passed-filter-year",
                    "passed-filter-button",
                ),
            ],
            id="chart-filters-header",
            className="chart-filters-header",
            style={"display": "none"},
        ),
        html.Div(
            [
                html.Aside([stat_card(label, value) for label, value in SIDEBAR_STATS], className="sidebar"),
                html.Main(
                    html.Div(
                        html.Div(
                            [chart_card(index, title) for index, title in enumerate(CHART_TITLES, start=1)],
                            id="chart-container",
                            className="chart-container",
                        ),
                        className="dashboard-content",
                    ),
                    id="graphs-view",
                ),
            ],
            id="main-wrapper",
            className="main-wrapper",
        ),
        html.Main(
            html.Div(
                html.Div(
                    [
                        html.H2("Dataset View", className="dataset-view-title"),
                        html.Div(
                            [
                                html.Button("Dataset 1", id="dataset-button-1", n_clicks=0, className="dataset-button active"),
                                html.Button("Dataset 2", id="dataset-button-2", n_clicks=0, className="dataset-button"),
                                html.Button("Dataset 3", id="dataset-button-3", n_clicks=0, className="dataset-button"),
                            ],
                            className="dataset-selector-container",
                        ),
                        html.Div(id="dataset-content"),
                    ],
                    className="dataset-view-container",
                ),
                className="dashboard-content",
            ),
            id="dataset-view",
            style={"display": "none"},
        ),
        html.Footer("(c) 2025 Dashboard. All rights reserved. | Last updated: December 27, 2025"),
    ],
    className="app-shell",
)


@app.callback(
    Output("main-wrapper", "style"),
    Output("dataset-view", "style"),
    Output("chart-filters-header", "style"),
    Output("filter-toggle", "style"),
    Output("filter-toggle", "children"),
    Input("view-mode", "value"),
    Input("filter-toggle", "n_clicks"),
)
def switch_view_mode(view_mode, filter_clicks):
    if view_mode == "dataset":
        return (
            {"display": "none"},
            {"display": "block"},
            {"display": "none"},
            {"display": "none"},
            "v",
        )

    filters_open = bool(filter_clicks and filter_clicks % 2)
    return (
        {"display": "flex"},
        {"display": "none"},
        {"display": "flex"} if filters_open else {"display": "none"},
        {"display": "inline-block"},
        "^" if filters_open else "v",
    )


@app.callback(
    Output("maximized-chart", "data"),
    [Input(f"chart-toggle-{index}", "n_clicks") for index in range(1, 7)],
    State("maximized-chart", "data"),
)
def toggle_maximized_chart(*args):
    current_chart = args[-1]
    triggered = callback_context.triggered

    if not triggered:
        return current_chart

    button_id = triggered[0]["prop_id"].split(".")[0]
    if not button_id.startswith("chart-toggle-"):
        return current_chart

    selected_chart = button_id.replace("chart-toggle-", "")
    return None if current_chart == selected_chart else selected_chart


@app.callback(
    Output("chart-container", "className"),
    [Output(f"chart-wrapper-{index}", "className") for index in range(1, 7)],
    [Output(f"chart-toggle-{index}", "children") for index in range(1, 7)],
    Input("maximized-chart", "data"),
)
def update_chart_maximized_state(maximized_chart):
    container_class = "chart-container maximized" if maximized_chart else "chart-container"

    wrapper_classes = []
    button_labels = []
    for index in range(1, 7):
        chart_id = str(index)
        if not maximized_chart:
            wrapper_classes.append("chart-wrapper")
            button_labels.append("Maximize")
        elif maximized_chart == chart_id:
            wrapper_classes.append("chart-wrapper maximized")
            button_labels.append("Back")
        else:
            wrapper_classes.append("chart-wrapper hidden")
            button_labels.append("Maximize")

    return (container_class, *wrapper_classes, *button_labels)


@app.callback(
    Output("chart-title-2", "children"),
    Output("chart-title-3", "children"),
    Input("failed-filter-button", "n_clicks"),
    Input("passed-filter-button", "n_clicks"),
    State("failed-filter-year", "value"),
    State("passed-filter-year", "value"),
)
def update_filtered_chart_titles(_failed_clicks, _passed_clicks, failed_year, passed_year):
    return (
        f"Failed Students by Subject - {failed_year}",
        f"Passed Students by Subject - {passed_year}",
    )


@app.callback(
    Output("active-dataset", "data"),
    Input("dataset-button-1", "n_clicks"),
    Input("dataset-button-2", "n_clicks"),
    Input("dataset-button-3", "n_clicks"),
    State("active-dataset", "data"),
)
def choose_dataset(_dataset_1, _dataset_2, _dataset_3, current_dataset):
    triggered = callback_context.triggered
    if not triggered:
        return current_dataset

    button_id = triggered[0]["prop_id"].split(".")[0]
    if button_id.startswith("dataset-button-"):
        return button_id.replace("dataset-button-", "")

    return current_dataset


@app.callback(
    Output("dataset-content", "children"),
    Output("dataset-button-1", "className"),
    Output("dataset-button-2", "className"),
    Output("dataset-button-3", "className"),
    Input("active-dataset", "data"),
)
def render_dataset(active_dataset):
    button_classes = [
        "dataset-button active" if active_dataset == str(index) else "dataset-button"
        for index in range(1, 4)
    ]
    return dataset_table(active_dataset or "1"), *button_classes


if __name__ == "__main__":
    app.run(debug=False)
