from setuptools import find_packages, setup

setup(
    name="py-log-analyzer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich>=15.0.0",
    ],
    entry_points={
        "console_scripts": [
            "py-log-analyzer=py_log_analyzer.cli:run",
        ],
    },
    python_requires=">=3.10",
)
