# DashForge visual test cases

Each script is a self-contained dashboard scenario.  Run one from the project
root, for example:

```powershell
python TestCases/01_dark_command_center.py
```

Every case uses a different port so it is convenient to compare several
designs. Stop a running dashboard with `Ctrl+C`.

| File | Focus |
| --- | --- |
| `01_dark_command_center.py` | Dark operations dashboard, KPIs, mixed charts, data page |
| `02_light_product_story.py` | Light editorial product dashboard and custom colors |
| `03_finance_analyst.py` | Dense financial layout, custom row widths and selective maximize buttons |
| `04_neon_pulse.py` | Header-free neon dashboard and Plotly graph objects |
| `05_people_analytics.py` | Data-table page, logo, titles, subtitles, and timestamp |
| `06_chart_gallery.py` | Seven Plotly chart types and a three-row responsive layout |
| `07_layout_lab.py` | Explicit chart sizing and one/two/three-chart row combinations |
| `08_api_smoke_test.py` | Non-server build checks for all showcase configurations |

These are visual integration examples, not unit tests: launch the dashboards
and use the chart toolbar, maximize controls, and (where present) the data-page
button to inspect the experience.
