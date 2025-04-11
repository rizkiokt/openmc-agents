from setuptools import setup, find_packages

setup(
    name="openmc-agents",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langgraph>=0.0.10",
        "numpy>=1.24.0",
        "h5py>=3.9.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "duckduckgo-search>=4.1.1",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
    ],
) 