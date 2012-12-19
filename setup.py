from setuptools import setup

setup(
    name = 'labgeeks-people',
    version = '1.0',
    license = 'Apache',
    url = 'http://github.com/abztrakt/labgeeks_people',
    description = 'User profiles and reviews app for the labgeeks suite of student staff management tools.',
    author = 'Craig Stimmel',
    packages = ['labgeeks_people',],
    install_requires = [
        'setuptools',
        'pillow',
        'South==0.7.3',
    ],
)
