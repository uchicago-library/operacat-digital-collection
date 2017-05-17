from setuptools import setup

setup(
    name='operaCat',
    version='1.0',
    long_description=__doc__,
    packages=['operacat'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.10,<1.11',
        'wagtail>=1.9,<1.10',
        'django-contrib-comments',
        'django-comments-xtd',
        'django-registration-redux'
    ]
)
