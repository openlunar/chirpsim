# chirpsim
A super low fidelity time simulation of a chirp signal and doppler shifting.
This tool was originally to help me ([Aaron](https://github.com/a3ng7n)) gain a better
understanding of signal mixing, by showing what a significant bandwidth signal 
([chirp](https://wikipedia.org/wiki/Chirp)) looks like: 
- When [mixed](https://wikipedia.org/wiki/Frequency_mixer)
- When [doppler shifted](https://wikipedia.org/wiki/Doppler_effect)
- When de-mixed with an [LO](https://wikipedia.org/wiki/Local_oscillator)
that's corrected and uncorrected for the doppler shift/distortion

The following is a color-coded diagram of what the script simulates, corresponding to
the [outputs](#output) below.\
![Overview Diagram](https://raw.githubusercontent.com/openlunar/chirpsim/master/overview.png)

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
Navigate to the repo's root folder, and run chirpsim.py with arguments:

    cd chirpsim/
    python chirpsim.py

Or with arguments as desired:

    python chirpsim.py [-h] [-t T_MAX] [-s SIZE] [-d DOPPLER] [-bw BW]
                       [-fc F_CENTER] [-fr F_RATE] [-lf LO_F] [-lp PHASE]

Or for help, do the usual:

    python chirpsim.py --help

### Command Line Arguments
There are unfortunately quite a few args, but hey, what can you do:
    
    optional arguments:
      -h, --help            show this help message and exit
      -t T_MAX, --t-maxx T_MAX
                            total simulation time, in seconds
      -s SIZE, --time-steps SIZE
                            number of timesteps
      -d DOPPLER, --doppler DOPPLER
                            amount of doppler shifting to apply to the chirp
                            signal, in percent
    
    chirp_chars:
      chirp signal characteristics
    
      -bw BW, --bandwidth BW
                            bandwidth of the chirp signal, in hz
      -fc F_CENTER, --center-frequency F_CENTER
                            center frequency of the chirp signal, in hz
      -fr F_RATE, --frequency-rate F_RATE
                            rate that the chirp spans its bandwidth, in hz/s
    
    lo_chars:
      lo signal characteristics
    
      -lf LO_F, --lo-frequency LO_F
                            frequency of the lo signal, in hz
      -lp PHASE, --lo-phase PHASE
                            phase shift of the demixing lo, from the mixing lo, in
                            deg

## Output
The following plots should show up, which are both color coded to the [overview diagram](#chirpsim) above.

A plot of the time domain:\
![Time Plot](https://raw.githubusercontent.com/openlunar/chirpsim/master/t_plot.png)

A plot of the frequency domain:\
![Frequency Plot](https://raw.githubusercontent.com/openlunar/chirpsim/master/f_plot.png)
