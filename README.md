# Setup Environment

To run the tests, you need (see also script [setup_dev.ps1](demos/setup_dev.ps1)):
- Python Version 3.9.x
- Python packages: see [requirements.txt](./demos/requirements.txt)
- Java 11
- Verification and trace visualization requires UPPAAL Version 4.1 with bin in PATH.

To create new FMUs (unlikely), you need:
- UniFMU (https://github.com/into-cps-association/unifmu)

# FMUS
 - Located in `fmus` folder.
 - They have been exported using UniFMU

# Demos

The folder `demos` contains the Maestro jar and subfolders with the individual demos.

There are two ways to run the demos: 
- run all demos as batch -- ideal for checking that everything is working as it should. Plotting, printing, etc... are disabled.
- run individual demos -- ideal for development

## Running all Demos as Batch

In the `demos` folder, run:
```
python run_tests.py
```

## Running Individual Demos

Tests should be executed from the [demos](./demos) folder.

Each subfolder includes both `test.py` which can be executed to run the concrete test and either a `scenario.conf` representing the co-simulation scenario.

During test execution relevant test information is displayed in the console.

### Demo execute_algorithm

Shows the ability to execute an algorithm generated from a scenario.

First the test generates a mastermodel (representing the scenario and algorithm) by calling the Maestro web API with the scenario file. 
The test then merges the resulting mastermodel with the existing executableModel file which is then passed to Maestro to execute the algorithm.

If successful, the zip file 'zip_result.zip' is generated in the folder with the execution artifacts.

The parameter 'executionParameters' in executableModel.json can be configured as needed (e.g. step size).

Likewise also the scenario.conf file can be changed as needed.

__NOTE: This test requires the fmus Controller, KalmanFilter, Plant, Room, Supervisor (as folders) to be located in the folder fmus with the exact names__.

### Demo execute_algorithm_3D

Same as [Demo execute_algorithm](#demo-execute_algorithm), except it also loads the Incubator3D FMU.
This demo only works on windows.

### Demo execute_algorithm_faultinjection
file `faultEvents.xml` changed to `FaultEvents.xml`.  

### Demo execute_algorithm_rabbitmq_3D
This demo only works on windows.  

### Demo generate_algorithm_from_scenario

Shows the ability to generate an algorithm from a scenario.

If successful the conf file 'result_masterModel.conf' is generated in the folder containing both the scenario and algorithm.

The scenario.conf file can be changed as needed.

### Demo verify_algorithm

Shows the ability to verify an algorithm.

### Test visualize_traces

Shows the ability to visualize possible traces generated from verification.
