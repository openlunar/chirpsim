# chirpsim
A super low fidelity time simulation of a chirp signal and doppler shifting.

## Requirements
* Python 3.x
* Numpy
* Matplotlib
* Scipy

## Installation
Clone this repository:

    git clone git@github.com:openlunar/chirpsim.git
    cd chirpsim/
    pip install -r requirements.txt

Currently, this tool cannot be installed as a package. You must run it
out of the repository directory.

## Usage
Navigate to the repo's root folder, and run chirpsim.py with no arguments:

    cd chirpsim/
    python chirpsim.py

## Output
The following plots should show up:

A plot of the time domain:\
![Time Plot](https://raw.githubusercontent.com/openlunar/chirpsim/5f84682ccab8df515a7ad022e1eae25135d96141/t_plot.png)

A plot of the frequency domain:\
![Frequency Plot](https://raw.githubusercontent.com/openlunar/chirpsim/5f84682ccab8df515a7ad022e1eae25135d96141/f_plot.png)
