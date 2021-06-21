from setuptools import setup, find_packages

import os


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


long_description = read("README.md")


setup(
    name='kubehelm',
    version=get_version("k8s/__init__.py"),
    long_description=long_description,
    license='MIT',
    keywords='kubernetes, deploy, production, helm, ingress, network',
    python_requires='>=3.6, <4',
    packages=find_packages(include=['k8s', 'k8s.*']),
    package_data={
        'k8s': [
            'scripts/*',
            'templates/*/*/*',
            'templates/*/*',
            'templates/*',
        ],
    },
    entry_points={
        'console_scripts': [
            'kubehelm = k8s.controller:execute_from_command_line',
        ],
    },
    install_requires=[
        'requests',
        'kubernetes == 12.0.1',
        'Jinja2==2.11.3',
        'mysql-connector-python',
    ],
)
