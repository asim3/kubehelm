from setuptools import setup, find_packages


setup(
    name='kubehelm',
    version='0.0.7',
    license='MIT',
    # https://packaging.python.org/en/latest/single_source_version.html
    keywords='sample, setuptools, helm',
    python_requires='>=3.6, <4',
    packages=find_packages(include=['k8s', 'k8s.*']),
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
    package_data={
        'k8s': [
            'scripts/*',
            'templates/*/*/*',
            'templates/*/*',
            'templates/*', ],
    },
)
