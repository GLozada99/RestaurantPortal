from setuptools import setup, find_packages

setup(
    name="portal",
    author="Mauricio Pacheco & Gustavo Lozada",
    version="1.0.0",
    description="Restaurant management API",
    packages=find_packages(exclude=['*tests']),
)
