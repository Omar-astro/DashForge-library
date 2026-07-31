"""Build all visual examples without starting their web servers."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def load_builder(path: Path):
    spec = spec_from_file_location(path.stem, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_dashboard


if __name__ == "__main__":
    directory = Path(__file__).parent
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))
    cases = sorted(path for path in directory.glob("[0-9][0-9]_*.py") if path.name != Path(__file__).name)
    for case in cases:
        dashboard = load_builder(case)()
        app = dashboard.build_dashboard()
        assert app.layout is not None, f"{case.name} did not create a layout"
        print(f"PASS  {case.name} ({len(dashboard.charts)} charts)")
    print(f"Built {len(cases)} DashForge showcase dashboards successfully.")
