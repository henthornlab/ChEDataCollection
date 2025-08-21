# ChE Data Collection Website
Flask app created by Eddie Barry (RHIT CHE class of 2022) and David Henthorn (RHIT CHE).

Allows users to query a website and pull data from an OSIsoft PI data archive.

Also exposes a /csv route for direct downloads to clients.

Server must be running the PI SDK, which means this works only on Windows machines. Clients connect from any web browser that can accept a CSV file download.

Clients for Python, Python Notebooks (Jupyter), Julia, and Matlab are included.

# UPDATED WEBSITE

A button on the top ribbon was added that takes you to the new website address.
![UOLab_ribbon](https://github.com/sandera1-RHIT/ChEDataCollection/blob/Main/static/UOLab_ribbon.png?raw=true)

The new address allows the selection of the available projects in Unit Operations Lab.
When you press the button "Get Instruments" it sends a request to the UOLab server to return the available instruments for the selected unit.
The user is transferred to the next webpage which lists the returned instruments. 
![UOLab_project_webpage](https://github.com/sandera1-RHIT/ChEDataCollection/blob/Main/static/UOLab_Project.png?raw=true)

Individual instruments can be selected for data collection.
Alternatively, there is a "checkall" button that will select all available instruments.
A similar input process for the time information is used to finalize the data request form.
The "Download Data" button is then selected, which will connect to the server and return a .csv file containing the requested data of the selected instruments.
![UOLab_instrumentation_webpage](https://github.com/sandera1-RHIT/ChEDataCollection/blob/Main/static/UOLab_Intrumentation.png?raw=true)

Additionally, the buttons used to request data were reprogrammed.
Instead of only requiring a valid "time of day" range, the validation was updated to check for all inputs.
Each input is required before the button becomes available on every webpage.



# DO NOT TOUCH MAIN
## How To Merge
1. make changes on the testing branch
2. check if changed work on testing branch
3. switch back to main branch
4. merge testing into main
5. push main
6. check github repo for completion

# IF YOU TOUCH MAIN YOU MESSED UP
