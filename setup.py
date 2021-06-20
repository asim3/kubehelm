from setuptools import setup, find_packages


setup(
    name='kubehelm',
    version='0.0.5',
    license='MIT',
    # https://packaging.python.org/en/latest/single_source_version.html
    keywords='sample, setuptools, helm',
    python_requires='>=3.6, <4',


    packages=find_packages(include=['k8s', 'k8s.*']),
    # packages=find_packages(include=['k8s']),
    # packages=['k8s'],
    # packages=find_packages(),



    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['peppercorn'],  # Optional

    install_requires=[
        'kubernetes == 12.0.1',
        'Jinja2==2.11.3',
        'mysql-connector-python',
        'requests',
    ],




    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={
        'console_scripts': [
            'kubehelm = k8s.controller:execute_from_command_line',
        ],
    },
)
