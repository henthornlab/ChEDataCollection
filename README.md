# ChE Data Collection Website
Flask app created by Eddie Barry (RHIT CHE class of 2022) and David Henthorn (RHIT CHE).

Allows users to query a website and pull data from an OSIsoft PI data archive.

Also exposes a /csv route for direct downloads to clients.

Server must be running the PI SDK, which means this works only on Windows machines. Clients connect from any web browser that can accept a CSV file download.

Clients for Python, Python Notebooks (Jupyter), Julia, and Matlab are included.

# UPDATED WEBSITE

The first page (/home) will have a drop-down to select the project that you want to download from.  The second page of the website loads the available instrumentation and then allows the selection of them in some way we will need to decide on. After the selection of the wanted instrumentation, you can select the date and time information in a way similar to what already exists. 