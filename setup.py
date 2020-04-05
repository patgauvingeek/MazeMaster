'''Setup file'''
import setuptools

with open("README.md", "r") as fh:
  LONG_DESCRIPTION = fh.read()

setuptools.setup(
  name="MazeMaster",
  version="1.0.0",
  author="Patrick Gauvin",
  author_email="gauvin.patrick@gmail.com",
  description="A discord bot game",
  long_description=LONG_DESCRIPTION,
  long_description_content_type="text/markdown",
  url="https://github.com/patgauvingeek/MazeMaster",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3.5",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.5',
  test_suite="tests"
)
