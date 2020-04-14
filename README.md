#### Given 2 airports, find the shortest route between them and alternate path
For this task, networkx library has been used, as it offers some useful APIs for path optimisation.

Additionally, a lot of data analysis has been done using numpy/pandas in Jupyter notebook.
This includes calculating distance between routes (used for network optiisation), as this takes substantial amount of time.
This data analysis is available in the notebook:

[flight_data_analysis.ipynb](flight_data_analysis.ipynb)
 
 Test cases are available in the directory:
 [tests](/tests)
 
#### Build
Run this command to build docker file:
```bash
$ docker build -t flight_networks_service . 
``` 

#### To run the app, run this command:
```bash
$ docker run -it --rm -p 5050:5050 flight_networks_service:latest
``` 

#### The app is now available at: http://localhost:5050

The endpoint for accessing routes '/paths'. It takes 3 query params: 
- source: the airport id of departure
- destination:  the airport id of arrival
- halts: max allowed halts in the journey

#### Concurrency
This app uses gunicorn as application server. It is configured to run 20 worker processes, and each worker can run 10 threads

