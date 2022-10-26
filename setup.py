from setuptools import setup

REQUIREMENTS = ['requests', 'bioblend', 'setuptools']

setup(
    name='ghevaluator',
    version='1.0.0',
    packages=['ghevaluator'],
    entry_points={'console_scripts': ['ghevaluator = ghevaluator.ghevaluator_main:main']},
    url='https://github.com/chensy96/Galaxy-History-Evaluator',
    install_requires=REQUIREMENTS,
    license='LICENSE',
    author='Siyu Chen',
    author_email='chensy96@gmail.com',
    description='A CLI tool for evaluating Galaxy History'
)
