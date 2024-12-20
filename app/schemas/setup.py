from setuptools import setup, find_packages

setup(
    name="rei_models",
    version="0.1.0",
    packages=find_packages(include=['rei_models'], exclude=['tests*']),
    install_requires=[
        "pydantic[email]~=2.3.0",
        "python-dateutil~=2.9.0.post0"
    ],
    author="Zimba Developers",
    author_email="rei-api-dev@zimbasolutions.io",
    description="This module contains the Pydantic migrations that will be reused by other modules.",
    python_requires=">=3.11",
)
