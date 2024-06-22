# Metro Bike Station: Bike Sharing
## Table of Contents
    
  - [About the project](#contributing)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
  - [Usage](#usage)

## About the Project

This project, processes the live feed of Metro Bike Share in Los Angeles city to answer the
following questions: https://bikeshare.metro.net/about/data/.
1. Given the current location of a person and number K as input, find K-nearest bike stations based on
available bikes.
2. Given the current location of a person who has a bike and number K as input, find K nearest bike
stations where docks are available.
3. Given a source and destination location in Los Angeles, present the route on Google maps or another
mapping product of a person using Metro bike. Please remember that for traveling from source to
destination, you can only use your foot and Metro bike from live feed.
## Getting Started

Since the project needs to uses external API, it is necessary
to be connected to the internet when using it.
### Prerequisites

The following packages are required to be installed:
```
pip install PyQtWebEngine
pip install scikit-learn
```
Also install all packages which are defined in the import statements:
pandas, Enum, folium, geodesic, requests, QWebEngineView, PyQt5.QtCore, PyQt5.Widgets

For detailed version requirements check requirements.txt
## Usage

Start the project by running the main function in pyqtapp.py line 269.
This start the applications home page.

There are a total of 4 views:
Home Page - Navigate to any desired functional view
View 1 - Solves Task 1
View 2 - Solves Task 2
View 3 - Solves Task 3

Enter the desired input values in the user input fields,
press 'update view' to trigger calculation on View 1 to 3.
Press 'Return to Homepage' to return to homepage.

Optionally: You can launch the program via the main function in
trigger_calc.py. This will allow you to enter the input in 
an command line interface.
