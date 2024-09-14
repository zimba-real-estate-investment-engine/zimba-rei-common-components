from setuptools import setup, find_packages

setup(
    name="zimba-rei-common-components",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0.0,<4.0.0",
        # Add other dependencies here
    ],
    author="Zimba team",
    author_email="zimba@zimba.com",
    description="Zimba Real Estate Investment Engine",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zimba-real-estate-investment-engine/zimba-rei-common-components",
)
