from setuptools import setup, find_packages


tests_require = [
    'diff-cover',
    'pytest',
    'pytest-cov',
    'pytest-django',
    'pytest_factoryboy',
    'pyquery',
    'factory-boy',
]
linting_require = ['flake8']

setup(
    name="senslarge",
    version="0.1.0.dev0",
    package=find_packages(),

    install_requires=[
        'Django',
        'django-braces',
        'django-bootstrap3',
        'django-bootstrap-static < 4',
        'django-fontawesome',
        'django-healthchecks',
        'django-mailgun',
        'django-redis',
        'django-weasyprint',
        'djangorestframework',
        'psycopg2',
        'pygal',
        'raven',
        'django-ordered-model',
    ],
    extras_require={
        'test': tests_require,
        'linting': linting_require,
    },
    tests_require=tests_require,
)
