from setuptools import setup

def readme():
    with open("README.md", "r") as read_file:
        return read_file.read()

setup(
    name='operaCat',
    version='0.9.1',
    author = ['Tyler Danstrom', 'Kathy Zadrozny'],
    author_email = ['tdanstrom@uchicago.edu', 'kzadrozny@uchicago.edu'],
    description="A website developed by the authors for the Digital Library Development to present records of items collected from auction sales about five famous Italian composers",
    license = "LGPL3.0",
    long_description=readme(),
    packages=['operacat'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django', 'wagtail', 'django-contrib-comments', 'django-comments-xtd', 'django-registration-redux']
)

