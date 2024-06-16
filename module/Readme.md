# Metro Bike Station: Bike Sharing
## Table of Contents
    
  - [About the project](#contributing)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
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

[Instructions on setting up the project locally. Include prerequisites, installation instructions, and any additional setup steps needed to get the project up and running.]

### Prerequisites

The following packages are required to be installed:
```
pip install PyQt5WebEngine
# Pip:
python -m venv sklearn-env
sklearn-env\Scripts\activate  # activate
pip install -U scikit-learn
# Conda:
conda create -n sklearn-env -c conda-forge scikit-learn
conda activate sklearn-env
```
### Installation

[Step-by-step guide on how to install and configure the project. Use clear and concise instructions to guide users through the setup process.]

## Usage

[Provide examples and instructions on how to use the project. Show common usage scenarios and explain features.]

