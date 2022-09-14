from setuptools import setup, find_packages


setup(
    name='pyasjp',
    version='1.3.0',
    license='Apache 2.0',
    description='programmatic access to ASJP',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    author='Robert Forkel',
    author_email='forkel@shh.mpg.de',
    url='',
    keywords='data',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.7',
    install_requires=[
        'attrs>=19.3',
        'csvw',
        'clldutils>=3.5',
    ],
    extras_require={
        'dev': ['flake8', 'wheel', 'twine', 'build'],
        'test': [
            'pytest>=5',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
    entry_points={
        'console_scripts': [
            'asjp=pyasjp.__main__:main',
        ]
    },
)
