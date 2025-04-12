from setuptools import setup, find_packages

setup(
    name="cookbook_manager",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.11.3",
        "pick>=2.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.3",
            "pytest-mock>=3.14.0",
        ],
    },
)
