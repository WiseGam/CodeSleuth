from setuptools import setup, find_packages

setup(
    name="codesleuth",
    version="0.1.0",
    description="A Python module to analyze code complexity and dependencies.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/codesleuth",
    packages=find_packages(),
    install_requires=[
        "radon",
        "networkx",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
