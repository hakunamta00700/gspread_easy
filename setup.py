from distutils.core import setup

setup(name='gspread_easy',
      version='0.2',
      description='Google SpreadSheet Convenient  Usage Util',
      author='David Cho',
      author_email='davidcho@rookiest.co.kr',
      packages=['gspread_easy'],
      install_requires=[
          "gspread",
          "oauth2client",
      ],
      )
