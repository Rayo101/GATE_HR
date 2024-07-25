# GATE Simulation of the Siemens ECAT "EXACT3D" HR++
![This is an alt text.](/ReadmeImages/HR++SimCropped.png "This is a sample image.")
## Activate UCT VPN (If not on campus UCT eduroam)

See [this link](https://icts.uct.ac.za/services-working-remotely-virtual-private-network/install-anyconnect)

## How to connect to the server

Well you'll need an ssh client to do so.  It should be easy enough on mac and linux machines since you just need the ssh app which can be obtained easily.  For Window I reccomend using PuTTY.  Steve should've sent the login info.

## Getting started with the GATE

Don't worry you will not be compiling or installing any of these software since that will take too much time.  You will just need to know how to get your user account on the server setup with GATE.  If you want to compile Geatn4, ROOT and GATE you can do so but at your own risk since it's a nightmare if this is your first time compiling C/C++ projects.

Getting back to the setup.  We are just going to create an alias for GATE so that you don't need to reload your /.bashrc.   

The .bashrc file should be located in the folder as soon as you log into the server.  

Add the following to the end of your .bashrc.  

![This is an alt text.](/ReadmeImages/bashrc.png "This is a sample image.")

Dont change anything from my name since this is a custom version of GATE for this simulation with additional features!

## Testing if GATE is now working

In order to test if the GATE alias is now working type gate91 into the terminal.  You should see, ""Setting up Gate v9.1 with ROOT 6.22/02 and Geant4 10.07.p01".  Now type in Gate.  You should see the following.  


![This is an alt text.](/ReadmeImages/Gate.png "This is a sample image.")

## Using the GATE Simulation of the HR++

The GATE simulation of the HR++ is in the root folder of the repo.  There are two python scripts showing two examples.  These scripts look daunting but not to worry.  The simulation is already validated so all you need to do is learn how to use the simulation.  So the things you need to know about the simulation is File/Folder controls, process controls, tracer size, tracer activity, simulation times and motion.  Some additional info for your thesis on the simulation can be found in [this paper](https://www.mdpi.com/2076-3417/13/11/6690).  If there isn't anything there then you can find it in the script.  

The following explanations on the use of the script is reffering to any of the two Siemens_ECAT_HR++*.py scripts.  

### File/Folder Controls
That is from line 34 - 39.  

MACRO_FOLDER -  is a folder that will be created when you start the simulation.  This will store some macro files temporarily.  The script will clean up after itself so no need to worry about it.  Tell it to place these files wherever you want.  

ROOT_FOLDER - is a folder that will be created when you start the simulation.  This will store some root files temporarily.  The script will clean up after itself so no need to worry about it.  Tell it to place these files wherever you want.  

OUTPUT_ROOT - The output root folder.  The folder in which the output root file with all the simulation data will be placed.

OUTPUT_ROOT_FILE_NAME - The name of the output root file.  You can name it however you want.  I reccomend you give your files and folders logical names.  For exmaple if you have a bunch of ROOT files with the same sim params then add that to the folder name and add the specifics to only the file name.  But you can do whatever with the file name.  

### Process Controls
This is on line 48.  

cores - the number of processes spawned.  Ask Steve about the rules regarding the number of processes that you should spawn since other people use the server as well.  

### Tracer Size
This is on line 55.  

tracerSize - this controls the radius of the tracer in mm.  (NOTE!  Only for the layered NRW-100 tracer.)

Other tracer controls can be found from line 156 - 204.  

Note all tracers are spherical but most of the partical ones are approximately spherical.  Other are easily seen from line 156 - 204 if not using the layered NRW-100 tracer.  

### Tracer Activity
This is on line 335 and 344 (if 2nd tracer is active (could be implemented better))

sourceActivity1 - The activity of the tracer in Bq.  Note you need to compoensate for electron capture (look at the decay schemes). 

### Simulation Times
This is on lines 359 - 363.  

startTime - The simulation start time in s.   
endTime - The simulation end time in s.  
timeStep - the time step between which the geomtry will be redrawn if moved.  So if you have motion you want to make this less than the timestep of the general motion or if using generic motion then make it the temporal resolution of the path that is desired.  


### Motion
Lines 228 and 229 control if motion is active.  This is a simple boolean (True/False).  There are a bunch of motions to use.  The controls are mostly easy to understand for the simple motion except for orbitingMotionSetPoint11 and orbitingMotionSetPoint12 which is the two points that form a line about which the circular motion will occur (it's the axis about which rotation occurs).  General motion is defined by a files. 

#### How to use general motion
An easy way to create your own motion is to create the motion somewhere like python for example and save a npy file with columns t (s), x (mm), y (mm), z (mm).  You can then use createDataForSim.py script which will take this npy file and create a .placements file which will be read into GATE.  You need to place all placements files in the data folder.  You define the name of the placements file on line 234.  An example of a placements file can be seen inthe data folder.

### Running the Simulation
To run the simulation using the script first call the alias by typing gate91.  This only needs to be done once to a new terminal session.  Then type nohup python3 scriptName.py &.  nohup appends the output of the simulation (what would usually be written to the terminal) to a nohup.out file, python3 scriptName.py is just calling python and the & is to fork the written command and run the background.  For long simulations this is important since you'd like to logoff the server and sleep.  

## General Scripts

I've added some general scripts that I use quite often when analysing the simulation data.  

CreateDataForSim.py - Converts a npy file with columns t, x, y, z into a placements file that defined some arbitrary motion for the simulation.  

CreateDataForSim.py - same as CreateDataForSim.py but can convert a whole folder of npy files to placements files.  

interpolateTime.py - The time interpolation algorithm that was tested in recent time interpt paper + presented at SAIP.  Use because why not?  It produces better data and is easy to use.  

listmode_ROOT2NPY_1ms.py - This converts ROOT files to npy files to be read in when performing analysis.  ROOT folders require a more complex function and npy files are super duper fast and is a life saver when dealing with a large amount of LORs (lines-of-response).  Also performs post processing on times so that the output time minimics that of the HR++ (lors are precise to 1 ms).  Use this!

listmode_ROOT2NPY_Batch_1ms.py - same as listmode_ROOT2NPY_1ms.py but can batch conert ROOT to npy.  

listmode_ROOT2NPY_raw.py - same as listmode_ROOT2NPY_1ms.py but the only difference is that this outputs the true interaction time from the simulation (32-bit float).  

listmode_ROOT2NPY_Batch_raw.py - same as listmode_ROOT2NPY_raw.py but can batch conert ROOT to npy. 

## How to Analyse PEPT data?

Well you should've converted the ROOT file to a NPY file with listmode_ROOT2NPY_1ms.py or listmode_ROOT2NPY_Batch_1ms.py.  You are now ready to analyse the raw output of the simulation.  This can be seen in the Notebooks folder where I've added some Jupyter-Notebooks that show a basic analysis procedure.  I stopped at the plotting out the computed trajcetory since I don't really know what you guys are doing as of yet.  I'll add additional tools as is needed.    

## Output paths from analysis
This first plot is the X, Y and Z dimension of a 1.0 mCi NRW-100 layered tracer placed at (X, Y, Z) = (20.0, 20.0, 20.0) mm for 1.0 s.  
![This is an alt text.](/Notebooks/StationaryTest.png "This is a sample image.")
This is the X dimension a random walk with a timestep of 1.0 ms and a step that was sampled from a Gaussian distribution with a mean of 0.0 mm and a standard deviation of 1.0 mm.  The simulation was run for 1.0 s.  
![This is an alt text.](/Notebooks/RandomWalkTest.png "This is a sample image.")