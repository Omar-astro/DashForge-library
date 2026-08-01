from pathlib import Path

from setuptools import setup, find_packages

description = Path("README_PYPI.md").read_text(encoding="utf-8")

setup(
    name='dashforge',
    version='1.0.4',
    author="Omar Ashraf",
    author_email="omar.ashraf.hamed2017@gmail.com",
    description="Turn Plotly charts into interactive web dashboards with just a few lines of Python.",

    packages=find_packages(),
    install_requires=[
        "dash>=3.3.0",
        "flask>=2.3.0",
        "pandas>=2.3.3",
        "param>=2.4.1",
        "plotly>=6.4.0",
    ],
    long_description=description,
    long_description_content_type="text/markdown",

    url="https://github.com/Omar-astro/DashForge-library",
    project_urls={
        "Documentation": "https://omar-astro.github.io/DashForge-library/",
        "GitHub": "https://github.com/Omar-astro/DashForge-library",
        "Changelog": "https://github.com/Omar-astro/DashForge-library/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/Omar-astro/DashForge-library/issues",
    },

    license="MIT",

    keywords=[
        "dashboard",
        "plotly",
        "dash",
        "visualization",
        "data-analysis",
        "analytics",
        "python",
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries",
    ],
)
