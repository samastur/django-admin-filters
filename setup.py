from setuptools import setup, find_packages

version = __import__('adminfilters').__version__

setup(
    name = 'django-admin-filters',
    version = version,
    description = 'Django Admin Filters',
    author = 'Jonas Obrist',
    author_email = 'jonas.obrist@divio.ch',
    url = 'http://github.com/ojii/django-admin-filters',
    packages = find_packages(),
    zip_safe=False,
)