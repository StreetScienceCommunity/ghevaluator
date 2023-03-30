from setuptools import setup

REQUIREMENTS = [
    'bioblend',
    'requests',
    'setuptools',
    'flake8',
    'pytest',
    'Sphinx']

setup(
    name='ghevaluator',
    version='1.0.0',
    author='Siyu Chen, Teresa Müller, Bérénice Batut',
    author_email='chensy96@gmail.com, berenice.batut@gmail.com',
    description='A CLI tool for evaluating Galaxy History',
    license='MIT',
    url='https://github.com/SteetScienceCommunity/Galaxy-History-Evaluator',
    packages=['ghevaluator'],
    entry_points={
        'console_scripts': [
            'ghevaluator = ghevaluator.__main__:main'
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering"
    ],
    install_requires=REQUIREMENTS
)
