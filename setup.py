"""
Setup script for Email Security Analysis Engine
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme = Path(__file__).parent / "README.md"
long_description = readme.read_text() if readme.exists() else ""

setup(
    name="email-security-engine",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Email security analysis engine for spam and phishing detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/email-security-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "email-validator>=2.0.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "advanced": [
            "transformers>=4.30.0",
            "torch>=2.0.0",
            "spacy>=3.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "email-sleuth=cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)