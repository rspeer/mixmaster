from setuptools import setup

setup(
    name="mixmaster",
    version='0.5',
    maintainer='Rob Speer',
    maintainer_email='rob@luminoso.com',
    license="MIT",
    url='http://github.com/LuminosoInsight/mixmaster',
    platforms=["any"],
    description="Finds long anagrams",
    packages=['mixmaster'],
    package_data={'mixmaster': ['data/*.csv', 'data/*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
    }
)
