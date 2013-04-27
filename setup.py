from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'

install_requires = [
    'Celery',
    'Django',
]


setup(name='async_signals',
      version=version,
      description="",
      long_description=README + '\n\n' + NEWS,
      keywords='',
      author='Nathan Yergler',
      author_email='nathan@yergler.net',
      url='https://www.github.com/nyergler/async-signals',
      license='BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
)
