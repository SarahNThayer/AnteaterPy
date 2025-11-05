# AnteaterPy
clean, readable wrapper for the Anteater API, built for exploring course and GPA data automation

Peter is a simple Python utility class for retrieving course and grade distribution data from the Anteater API (REST API providing UC Irvine course data).

It allows users to:

- Fetch all years a given course was offered

- Retrieve average GPA across years for a specific course

- Drill down to section-level GPA data for a specific year


# FEATURES

- Retrieve all years a course was offered

- Get average GPA per year for a course

- Get GPA for each section code of a course

- Automatically handles API requests and errors

# INSTALLATION

Requirements:

`Python 3.8` or higher

`requests` library

# USAGE

- Save the provided Python file as peter.py

Run directly with: `$ python peter.py`


The example at the bottom of the file document:

- Initializing a Peter object

- Fetching the years a course was offered

- Retrieving GPA data
