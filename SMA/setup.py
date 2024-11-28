"""
Este archivo se utiliza para instalar el paquete. Se utiliza para instalar el paquete en el entorno actual.
"""

from setuptools import find_packages, setup


requires = ["mesa==2.4.0", "networkx==3.4.2", "matplotlib==3.9.2", "flask==3.0.3"]

setup(
    name="SMA - Modelo de Movilidad Urbana Equipo 6",
    version="3.0.0",
    packages=find_packages(),
    install_requires=requires,
)
