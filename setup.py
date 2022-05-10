
import re
from setuptools import setup


versio = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('Backups_clientAPI/__main__.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(name='Backups_clientAPI-NPP',
      version=versio,
      description='API Basica diversos tipus de backups, pensat per a EIO',
      long_description=long_descr,
      long_description_content_type='text/markdown',
      url='https://github.com/NilPujolPorta/Backups_clientAPI-NPP',
      author='Nil Pujol Porta',
      author_email='nilpujolporta@gmail.com',
      license='GNU',
      packages=['Backups_clientAPI'],
      install_requires=[
          'argparse',
          "setuptools>=42",
          "wheel",
          "openpyxl",
          "pyyaml",
          "requests",
          "mysql-connector-python",
          "tqdm",
          "selenium>=4.1.0",
          "pytesseract>=0.3.8",
          "pyotp>=2.6.0",
          "opencv-python>=4.5.4.60"
      ],
	entry_points = {
        "console_scripts": ['Backups_clientAPI-NPP = Backups_clientAPI.__main__:main']
        },
      zip_safe=False)
