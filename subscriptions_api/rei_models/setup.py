from setuptools import setup, find_packages

setup(
    name="models",
    version="0.1.0",
    description="A brief description of your local module",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        # List your dependencies here, for example:
        # "requests>=2.25.1",
        # "pandas>=1.2.0",
    ],
    python_requires=">=3.11",
)