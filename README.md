# OVERVIEW
This repository contains 2 toy examples for the usage of the MonteScene library:  
- PolygonGame1  
- PolygonGame2  
  
Both examples use MonteScene to select a subset of proposals from a set of input proposals to best match a ground truth.  
The input proposals are polygons with labels related to scene.  
The differ in how the ground truth is provided.

## PolygonGame1
In this example the ground truth is provided in the same format as the proposals: As labeled polygons.
## PolygonGame2
In this example the polygons are rendered to what is essentially a semantic segmentation. An this is provided as the input for the code.


# DEPENDENCIES
These dependencies need to be installed in whatever python environment you are using:  
## Python Version
Works with python 3.8.10
## MonteScene
The MonteScene library.  
You can find the library and the installation instructions in this github repository:  
[MonteScene](https://github.com/vevenom/MonteScene)
## Remaining Dependencies
These are other dependencies for these specific examples.  
They are provided in the requirements.txt file.  


# RUN
## -m
The examples need to be run as a module (with the -m option).  
```console
python3 -m <example folder: PolygonGameX>
```
## VSCode: launch.json
The repository contains a .vscode folder with a launch configuration for Visual Studio Code.  


# DISPLAY OUTPUT
These examples output tensorboard logs.  
## output directory
The log files are stored in the folder PolygonGameX/output/  
## tensorboard
To view the most recent logfile use the command:  
```console
tensorboard --logdir <output directory>
```
and open the url specified in the output of the commmand.  


# DIRECTORY STRUCTURE
- .vscode: Visual Studio Code launch configuration
- input: The input data for running either example
- PolygonGame1
	- output: The output of running example 1
- PolygonGame2
	- output: The output of running example 2
- requirements.txt: for installing the required dependencies
- (Matching: depended upon by examples)
- (Proposals: depended upon by examples)


# INPUT DATA
The json input data was created by labeling objects in labelme.
### Labelme on Ubuntu
On Ubuntu labelme can be installed with:
```console
[sudo] apt install labelme
```