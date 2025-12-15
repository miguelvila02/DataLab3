"""
Configuração da package Premier League Match Predictor.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

# Read requirements
req_file = Path(__file__).parent / "requirements.txt"
requirements = []
if req_file.exists():
    requirements = [
        line.strip()
        for line in req_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="pl-match-predictor",
    version="0.1.0",
    author="Miguel Vila",
    author_email="luismiguelvila@gmail.com",
    description="Premier League match outcome predictor using Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miguelvila02/DataLab3",
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # Python version requirement
    python_requires=">=3.8",
    # Dependencies
    install_requires=requirements,
    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
            "mkdocstrings[python]>=0.20.0",
        ],
    },
    # Package data
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.json", "*.joblib"],
    },
    # Console scripts
    entry_points={
        "console_scripts": [
            "pl-fetch-data=server.data.getdata.fetch_real_matches:main",
            "pl-train=server.model.modelbuild.predictor:main",
            "pl-predict=server.model.modelbuild.make_prediction:main",
        ],
    },
    # PyPI classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    # Keywords for discovery
    keywords="football soccer prediction machine-learning premier-league",
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/miguelvila02/pl-match-predictor/issues",
        "Source": "https://github.com/miguelvila02/pl-match-predictor",
        "Documentation": "https://miguelvila02.github.io/pl-match-predictor",
    },
)
