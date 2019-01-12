# bimug_drone
BIMUG_DRONE is a Python libray to process and analyse data recorded from a flying drone using an electronic set of devices called BIMUG, standing for Barometric, IMU, Gps.
This project is part of the subject Aerospace Laboratories developed during the Master's Degree in Space and Aeronautical
Engineering that I'm studiying at ESEIAAT - UPC (Univesitat Politécnica de Catalunya) in Terassa (Barcelona).

The source code of this library is hosted in my GitHub account:
https://github.com/cmolinaord/bimug_drone

## Usage
To use this code you have just to follow some simple steps:

### Data parsing
To parse the data from the raw files recorded from the BIMUG firmware you
just have to run with python the script *parse_data.py* inside the src folder:
```
cd src/
python parse_data.py <filename> <optional_comment>
```

The optional comment should be something to help identifying the filename,
because it would write a series of CSV files into one new directory named output_data
which will have the following name convention:
```
<comment>_S1_GPS_POS.csv
<comment>_S2_GPS_FIX.csv
...
```
One file per type of line read from the input data file.
Each file would include the parsed data by columns separated by TABs, with an indication
in the first row the name of the measurements. The first column will always be the
real time (in seconds) from the device power on.

### Data plotting
After having parsed the data to the files you would be able to do with them whatever
you want. You can export this files to another program or just read it with Python
or another language.

For our laboratory practice we needed to plot and calculate some things. So, what
I did is post-process this data with two scripts: ```plot1.py``` and ```plot2.py```.

You can run these scripts just with:
```
cd src/
python plot1.py
python plot2.py
```

And they would show you some interesting graphs. For the second flight it will
also print some calculations for the glide ratio, because in this flight, we tried
to perform an uniform and soft gliding descending, in order to calculate the glide
ratio of the plane.

## Libraries

### sensor.py
Inside this library there are some functions and definitions directly related with
the sensors itself and how they are codified in the raw data files.

The function **check_data** would check if the checksum written within each line
of raw data match with the actual checksum of the written line, to be able to
warn the user or discard the wrong lines.

The function **parse** is in charge of separating each raw data line in a vector
of strings with each measurement, that could be parsed then with the *parse_data.py*
script.

The function **coordinates** will transform the coordinates written in the raw data
file from a format DDMM.mmmm (degrees, minutes and decimals), to degrees with
decimals.

The dictionary **modes** will store the names of each filename and the names of
the measurements in them.

### process_data.py
In order to plot the graphs and compute the data, it was needed some post-processing
of the output data written in the output files.

Inside the library *process_data.py* there are some function definitions that
would do some processing.

The function **resample** would take the parsed data, from its original time scheme,
and would transform it using a new time vector by linearly interpolating the
values of the required sensor. The function will be called this way:
```
time_new, y_new = resample(comment, mode, column, t0, tf, dt)
T, lat          = resample(comment, 1, 'lat', 20, 45, 0.5)
```

* **comment**: the comment used in the output_data filename.
* **mode**: The number identifying the sensor read (and the file where it's stored)
* **column**: a string identifying the name of the measurement you want to access,
written in the top row of each file.
* **t0**: initial time (in seconds) from you want to read values
* **tf**: final time (in seconds) until you want to read values
* **dt**: the new time interval you want for the interpolated data.

This function will give you the two vectors:
* **time_new**: The new time base, from *t0* to *tf*, with increments of *dt*.
* **y_new**: The new interpolated values for the measurement required.

In this example, it would give you the data from latitude stored in "S1_GPS_POS"
file from 20s to 45s resampled with a time delta of 0.5s.
