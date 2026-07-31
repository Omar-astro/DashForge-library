"""Make examples runnable directly from a source checkout."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashforge.dashforge import Dashboard


def launch(dashboard: Dashboard, port: int) -> None:
    """Build and launch a predictable, development-friendly dashboard."""
    dashboard.set_port(port)
    dashboard.set_debug(False)
    dashboard.build_dashboard()
    dashboard.run()
