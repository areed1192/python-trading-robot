from setuptools import setup, find_packages

# load the README file.
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyrobot',
    author='Alex Reed',
    author_email='coding.sigma@gmail.com',
    version='0.1.0',
    description='A trading robot built for Python that uses the TD Ameritrade API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/areed1192/python-trading-robot',
    install_requires=[
        'td-ameritrade-python-api',
        'pandas',
        'numpy'
    ],
    keywords='finance, td ameritrade, api, trading robot',
    packages=find_packages(include=['pyrobot'], exclude=['*config.py']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.7'
)
