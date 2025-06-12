#!/usr/bin/env python3
"""
Setup configuration for vnstock-mcp-server NPX package
Hybrid Node.js/Python package for Vietnamese stock market data access
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="vnstock-mcp-server-python",
    version="1.0.0",
    author="Viet Nguyen",
    author_email="vietnh@example.com",
    description="Python backend for vnstock MCP server - Vietnamese stock market data access",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vietnh/vnstock-mcp-server",
    packages=find_packages(),
    package_dir={'': 'python'},
    py_modules=["vnstock_mcp_server"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "vnstock>=3.2.0",
        "mcp>=0.1.0",
        "pandas>=1.5.0",
        "asyncio-compat>=0.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vnstock-mcp-server-python=vnstock_mcp_server:main",
        ],
    },
    keywords="vietnam stock market mcp server claude ai vnstock financial data",
    project_urls={
        "Bug Reports": "https://github.com/vietnh/vnstock-mcp-server/issues",
        "Source": "https://github.com/vietnh/vnstock-mcp-server",
        "Documentation": "https://github.com/vietnh/vnstock-mcp-server/blob/main/README.md",
    },
    include_package_data=True,
    package_data={
        "": ["*.py", "*.md", "*.txt"],
    },
)
