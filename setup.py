from setuptools import setup
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='pyEPVis',
    version='0.0.2',
    description='A Expression and Particle movement visualizer package',
    author= 'Abhijith Ajith',
    url = 'https://github.com/AAbhijithA/pyEPVis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['particle', 'expression', 'expression visualizer','particle movement','visualizer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.0',
    py_modules=['pyEPVis'],
    package_dir={'':'src'},
    install_requires = [
        'numpy',
        'plotly',
    ]
)