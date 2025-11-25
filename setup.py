#!/usr/bin/env python3
"""
Setup script for the Art Institute of Chicago MCP Server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chicago-art-museum-mcp-server",
    version="1.0.0",
    author="Art Institute of Chicago MCP Contributors",
    description="MCP server for the Art Institute of Chicago API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chicago-art-museum-mcp-server",
    packages=find_packages(),
    py_modules=["server"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.10",
    install_requires=[
        "mcp>=1.1.2",
        "httpx>=0.27.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "black>=24.0.0",
            "ruff>=0.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "chicago-art-museum-mcp-server=server:main",
        ],
    },
)
