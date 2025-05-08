"""
Rose-Hulman Chemical Engineering Data server web API
David Henthorn, Chemical Engineering, 2022
"""

CONST_NAME = "CHE PI Data Portal"
CONST_VER = "0.10"
CONST_AUTHORS = "Eddie Barry (RHIT ChE, class of 2022) and David Henthorn, RHIT Professor"

# Requires the PIconnect package be installed. This package will install under various OS's, but
# it only functions on Windows machines with the PI SDK installed and properly setup
import PIconnect as PI

from flask import Flask, request, make_response, render_template
from datarequest import DataRequest
import pandas as pd
import numpy as np
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)


app = Flask(__name__)
print("hello world")

@app.route('/')
@app.route('/home')
def home():
    logging.info("New request for /home from %s", request.remote_addr)
    return render_template('home.html')


@app.route('/download', methods=["POST"])
def download():
    project = request.form.get("project")
    logging.info("Received download request for project %s from IP %s", project, request.remote_addr)
    date = request.form.get("start")
    start_time = request.form.get("starttime")
    end_time = request.form.get("endtime")
    interval = request.form.get("interval")

    project_num = "*" + project + "*"
    project_start = date + " " + start_time
    project_end = date + " " + end_time

    logging.info("Requested dataset with start time of %s, end time of %s, and interval of %s",
                 project_start, project_end, interval)

    if project_num == "*300*":
        search_term = "*-3*"
    else:
        search_term = project_num

    points = server.search(search_term)

    if len(points) == 0:
        logging.error("Found no PI datapoints for search term %s", search_term)
        return 'Found no PI datapoints for search term' + search_term
    else:
        logging.info("Found %s PI points for project %s", len(points), project)
        logging.info("Concatenating")
        df = pd.concat([
            point.interpolated_values(project_start, project_end, interval).to_frame(
                point.name + ' ' + point.units_of_measurement)
            for point in points], axis=1)

        logging.info("Cleaning and sorting scolumns")
        df.index.rename('Timestamp', inplace=True)
        df.sort_index(axis=1, inplace=True)

        # The encoding is off. Temporary workaround is to write the dataframe as a CSV, which fixes the encoding. Then read it in.
        df.to_csv("temp.csv")
        df = pd.read_csv("temp.csv")

        # We frequently see columns returned full of "Shutdown" comments because na instrument no longer works.
        # If the entire column is full of those, delete the whole column.

        #df.replace("Shutdown", np.nan, inplace=True)
        logging.info("Replacing non-numeric entries") 
        df.replace("Shutdown", float(np.NaN), inplace=True)
        df.dropna(how='all', axis=1, inplace=True)

        response = make_response(df.to_csv(date_format='%H:%M:%S'))
        csvname = 'AREA' + project + '-' + date + '.csv'
        response.headers['Content-Disposition'] = 'attachment; filename=' + csvname
        response.mimetype = 'text/csv'
        logging.info("Sending CSV file %s over http with response info %s", csvname, response)
        return response
    

@app.route('/csv', methods=['GET'])
def csv():
    """
    /csv route takes in a query string. Example is:
    /csv?startdate=2022-05-01&starttime=18:00&enddate=2022-05-02&endtime=4:00&interval=30s&area=150
    where area is the Unit Ops prefix... e.g. all Instrumentation and Control items are numbered 400
    and interval is time in seconds
    """

    logging.info('New request for /csv from %s', request.remote_addr)
    if request.args:
        req1 = DataRequest(request.args)
        req1.validate()
        if req1.is_valid:
            logging.info('Valid request %s', req1)
            points = server.search(req1.labarea.search_term)

            if len(points) == 0:
                logging.error("Found no PI datapoints for search term %s", req1.labarea.search_term)
                return 'Found no PI datapoints for search term'
            else:
                logging.info("Found %s PI points for project %s", len(points), req1.area)
                df = pd.concat([point.interpolated_values(req1.date1, req1.date2, req1.interval).to_frame(point.name + ' '
                    + point.units_of_measurement) for point in points], axis=1)

                df.index.rename('Timestamp', inplace=True)

                response = make_response(df.to_csv(date_format='%H:%M:%S'))
                csvname = 'AREA' + req1.area + '-' + req1.startdate + '.csv'
                response.headers['Content-Disposition'] = 'attachment; filename=' + csvname
                response.mimetype = 'text/csv'
                logging.info("Sending CSV file %s over http with response info %s", csvname, response)
                return response
        else:
            logging.error('Error in /csv route: %s', req1.errors_to_text())
            return req1.errors_to_text()
    else:
        logging.info('Received empty request to /csv endpoint. Sending instructions.')
        response = '<html><body>'
        response += 'Empty request:<br><br><br>'
        response += ('Example usage: http://hostname:port/csv?startdate=2022-05-01&starttime=18:00' +
                     '&enddate=2022-05-02&endtime=4:00&interval=10s&area=150 <br>')
        response += '</body></html>'
        return response


@app.route('/excel', methods=['GET'])
def excel():
    """
    /excel route takes in a query string. Example is:
    /excel?startdate=2022-05-01&starttime=18:00&enddate=2022-05-02&endtime=4:00&interval=30s&area=150
    where area is the Unit Ops prefix... e.g. all Instrumentation and Control items are numbered 400
    and interval is time in seconds
    """

    logging.info('New request for /excel from %s', request.remote_addr)
    if request.args:
        req1 = DataRequest(request.args)
        req1.validate()
        if req1.is_valid:
            logging.info('Valid request %s', req1)
            points = server.search(req1.labarea.search_term)

            if len(points) == 0:
                logging.error("Found no PI datapoints for search term %s", req1.labarea.search_term)
                response = 'Found no PI datapoints for search term'
            else:
                logging.info("Found %s PI points for project %s", len(points), req1.area)
                df = pd.concat([point.interpolated_values(req1.date1, req1.date2, req1.interval).to_frame(point.name + ' '
                    + point.units_of_measurement) for point in points], axis=1)

                df.index.rename('Timestamp', inplace=True)

                response = make_response(df.to_excel(date_format='%H:%M:%S'))
                excelname = 'AREA' + req1.area + '-' + req1.startdate + '.xls'
                response.headers['Content-Disposition'] = 'attachment; filename=' + excelname
                response.mimetype = 'application/vnd.ms-excel'
                logging.info("Sending excel file %s over http with response info %s", excelname, response)
                return response
        else:
            logging.error('Error in /excel route: %s', req1.errors_to_text())
            return req1.errors_to_text()
    else:
        logging.info('Received empty request to /excel endpoint. Sending instructions.')
        response = '<html><body>'
        response += 'Empty request:<br><br><br>'
        response += ('Example usage: http://hostname:port/excel?startdate=2022-05-01&starttime=18:00' +
                     '&enddate=2022-05-02&endtime=4:00&interval=10s&area=150 <br>')
        response += '</body></html>'
        return response


@app.route('/tester', methods=['GET'])
def tester():
    """
    This is a route used for testing. Sends a CSV file filled with zeros to the client.
    """
    logging.info('In /tester route. Sending CSV of zeroes for testing.')
    df = pd.DataFrame(np.zeros((10, 5)))
    response = make_response(df.to_csv())
    csvname = 'tester.csv'
    response.headers['Content-Disposition'] = 'attachment; filename=' + csvname
    response.mimetype = 'text/csv'
    return response


if __name__ == '__main__':
    logging.info("Starting %s version %s", CONST_NAME, CONST_VER)
    logging.info("Written by %s", CONST_AUTHORS)

    # Let's attempt to keep the PI server connection open here in main. Otherwise, we need to connect each time
    # we enter the /download route, which results in much longer wait times

    logging.info("Attempting to connect to PI Server using the PI SDK")
    PI.PIConfig.DEFAULT_TIMEZONE = 'America/Indianapolis'
    try:
        with PI.PIServer() as server:
            logging.info("Connected to PI Server %s which is running version %s", server.server_name, server.version)
            app.run(host="0.0.0.0")
    except Exception as e:
        logging.error('PI Server or WSGI server failed. Exception %s', e)
