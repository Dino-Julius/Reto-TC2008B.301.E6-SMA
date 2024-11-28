"""
Este archivo se utiliza para instalar el paquete. Se utiliza para instalar el paquete en el entorno actual.
"""

from setuptools import find_packages, setup


requires = ["mesa", "networkx", "matplotlib", "flask"]

setup(
    name="SMA - Modelo de Movilidad Urbana Equipo 6",
    version="2.0.0",
    packages=find_packages(),
    install_requires=requires,
)
