from pathlib import Path

from setuptools import setup, find_packages

description = Path("README_PYPI.md").read_text(encoding="utf-8")

setup(
    name='dashforge',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        "dash>=3.3.0",
        "Flask>=2.3.0",
        "pandas>=2.3.3",
        "param>=2.4.1",
        "plotly>=6.4.0",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
    project_urls={
        "GitHub": "https://github.com/Omar-astro/DashForge-library",
        "Changelog": "https://github.com/Omar-astro/DashForge-library/blob/main/CHANGELOG.md",
        "Documentation": "https://omar-astro.github.io/DashForge-library/",
    },
)
