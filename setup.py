import multiprocessing
from setuptools import setup, find_packages

setup(
    name='sow-generator',
    version='0.1',
    description='Create a scope of work from templates and version controlled documentation.',
    long_description = open('README.rst', 'r').read() + open('CHANGELOG.rst', 'r').read() + open('AUTHORS.rst', 'r').read(),
    author='Hedley Roos',
    author_email='hedley@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/sow-generator',
    packages = find_packages(),
    install_requires = [
        'Django<1.7',
        'South',
        'celery',
        'django-celery',
        'raven',
        'PyYAML',
        'requests',
        'github3.py',
    ],
    include_package_data=True,
    tests_require=[
        'django-setuptest>=0.1.4',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
