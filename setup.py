from setuptools import setup, find_packages


class PyPiSettings:
    version = '0.0.8'
    install_requires = [
        'requests',
        'kubernetes == 12.0.1',
        'Jinja2==2.11.3',
        'mysql-connector-python', ]
    package_data = {
        'k8s': [
            'scripts/*',
            'templates/*/*/*',
            'templates/*/*',
            'templates/*', ], }


setup(
    name='kubehelm',
    version=PyPiSettings.version,
    license='MIT',
    # https://packaging.python.org/en/latest/single_source_version.html
    keywords='sample, setuptools, helm',
    python_requires='>=3.6, <4',
    packages=find_packages(include=['k8s', 'k8s.*']),
    install_requires=PyPiSettings.install_requires,
    package_data=PyPiSettings.package_data,
    entry_points={
        'console_scripts': [
            'kubehelm = k8s.controller:execute_from_command_line',
        ],
    },
)
