# JJ-Ic-finder

A streamlit app  that extracts the  Critical current (Ic) from a given data set of I and V

## Process

We first find dV/dI from the given rows of V and I, we then find the Savgol filter (Savitzky-Golay filter) of 1s order for the dV/dI (d^2V / d^2I). Savgol filter  gives us a smooth 2nd order differential.

Corresponding to the negative and positive Ic, the 2nd order derivative will show spikes (as in fig), The I for which this peaks out is taken for both negative and positive current and then averaged out.

![samplePlot](https://github.com/iamashwin99/JJ-Ic-finder/blob/main/README.assets/samplePlot.png?raw=true)



The following are the default parameters in this process

The length of the filter window = 11

The order of the polynomial used to fit the samples. polyorder must be less than window_length = 3

sigNoiseThresh = 3

cutoff = 15 # cut off ends of dVdI which result in spurious maxima

