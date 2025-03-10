# Metro Bike Station: Bike Sharing

Uni-Project

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

Since the project needs to use external API, it is necessary
to be connected to the internet when using it.

## Prerequisites
To successfully run this project, unzip pyqtapp.zip
and open it in the terminal. To run the program smoothly it is 
advised to create a virtual environment and install the specified packages
in the requirements.txt file:
windows:
```
cd pyqtapp
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python pyqtapp.py
```
linux / macOS:
```
cd pyqtapp
python -m venv venv
source venv/bin/activate 
python -r install requirements.txt
python pyqtapp.py
```

To exit the virtual environment type 'deactivate'.

## Usage
There are a total of 4 views:
Home Page - Navigate to any desired functional view
View 1 - Solves Task 1
View 2 - Solves Task 2
View 3 - Solves Task 3

Enter the desired input values in the user input fields,
press 'update view' to trigger calculation on View 1 to 3.
Press 'Return to Homepage' to return to homepage.

Optionally:
You can also run the program in its home directory with:
```
python trigger_calc.py
```
This will allow you to enter the input in 
an command line interface. Note that you will have to open the 
result images manually if started that way.
