"""Shared launch helper for the DashForge examples."""

from dashforge import Dashboard


def launch(dashboard: Dashboard, port: int) -> None:
    """Build and launch a predictable, development-friendly dashboard."""
    dashboard.set_port(port)
    dashboard.set_debug(False)
    dashboard.build_dashboard()
    dashboard.run()
