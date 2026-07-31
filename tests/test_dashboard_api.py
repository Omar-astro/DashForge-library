"""API-level tests for the documented DashForge dashboard configuration."""

from pathlib import Path
import inspect
import sys
import unittest

import pandas as pd
from plotly.graph_objects import Figure


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dashforge.dashforge import Dashboard


class DashboardApiTests(unittest.TestCase):
    """Verify documented configuration methods without running a web server."""

    def setUp(self):
        self.figures = [Figure(), Figure(), Figure()]
        self.dashboard = Dashboard()

    def test_documented_public_methods_have_docstrings(self):
        public_methods = [
            "set_colors", "set_chart_titles", "set_port", "set_dataset_name",
            "set_debug", "set_chart_subtitles", "set_font_family",
            "set_footer_text", "add_dataset", "set_theme", "set_title",
            "hide_Header", "add_chart", "set_chart_per_row", "set_max_buttons",
            "add_timestamp", "set_custom_size", "set_logo", "add_kpi",
            "preset", "build_dashboard", "run",
        ]
        for method_name in public_methods:
            self.assertTrue(inspect.getdoc(getattr(Dashboard, method_name)))

    def test_common_dashboard_configuration_builds_an_app(self):
        self.dashboard.set_title("API test dashboard")
        self.dashboard.set_theme("light")
        self.dashboard.set_colors(line="#0EA5E9")
        self.dashboard.set_font_family("Arial, sans-serif")
        self.dashboard.set_footer_text("DashForge tests")
        self.dashboard.add_timestamp()
        self.dashboard.add_kpi({"Revenue": "$42,000", "Orders": 128})
        self.dashboard.add_chart(self.figures)
        self.dashboard.set_chart_per_row([2, 1])
        self.dashboard.set_chart_titles(["Overview", "Trend", "Details"])
        self.dashboard.set_chart_subtitles([None, "Latest period", None])
        self.dashboard.set_max_buttons([True, False, True])
        self.dashboard.set_custom_size([[[60, 100], [40, 100]], [[100, 90]]])
        self.dashboard.add_dataset(pd.DataFrame({"region": ["North", "South"], "sales": [18, 24]}))
        self.dashboard.set_dataset_name("Sales data")

        app = self.dashboard.build_dashboard()

        self.assertEqual(app.title, "API test dashboard")
        self.assertIsNotNone(app.layout)
        self.assertEqual(len(self.dashboard.charts), 3)

    def test_validation_examples_raise_clear_errors(self):
        with self.assertRaises(ValueError):
            self.dashboard.set_theme("blue")
        with self.assertRaises(ValueError):
            self.dashboard.add_chart("not a Plotly figure")
        with self.assertRaises(ValueError):
            self.dashboard.add_dataset(["not", "a", "dataframe"])

        self.dashboard.add_chart(self.figures)
        with self.assertRaises(ValueError):
            self.dashboard.set_chart_per_row([4])
        with self.assertRaises(ValueError):
            self.dashboard.set_max_buttons([True])


if __name__ == "__main__":
    unittest.main()
