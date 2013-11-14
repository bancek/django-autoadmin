from distutils.core import setup

setup(
    name='django-autoadmin',
    version='0.1',
    author=u'bancek',
    packages=['autoadmin'],
    url='http://github.com/bancek/django-autoadmin',
    description="Django Autoadmin is Django application that let's you have "
                "quick administration over your Django models.",
    long_description=open('README.rst').read(),
)
