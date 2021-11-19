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

Each subfolder includes both `test.py` which can be executed to run the concrete test and a `scenario.conf` representing the co-simulation scenario.

During test execution relevant test information is displayed in the console.

### Demo execute_algorithm

Shows the ability to execute an algorithm generated from a [scenario](./demos/execute_algorithm/scenario.conf)

First the test generates a mastermodel (defining the scenario and algorithm) by calling the Maestro CLI with the scenario file and places the master model in the results folder. The test then passes the resulting master model, the [multi model](./demos/execute_algorithm/multiModel.json) and execution parameters in its call to the Maestro CLI to execute the algorithm.

Any resulting execution artifacts are placed in a results folder, this includes a MaBL spec, output values and fmu logs. Lastly the output is plotted and a graph is displayed.

The file [executionParameters](./demos/execute_algorithm/executionParameters.json) can be configured as needed (e.g. step size and start and stop time for the execution).
The file [multiModel](./demos/execute_algorithm/multiModel.json) should not be changed as the test ensures that the correct FMU paths are inserted into the file as needed.
The file [scenario](./demos/execute_algorithm/scenario.conf) defines the incubator scenario with a name. The scenario, but no initialization or cosim-step instructions are present as these are part of the algorithm which is being generated as part of the test.

__NOTE: This test requires the fmus Controller, KalmanFilter, Plant, Room, Supervisor (as folders) to be located in the folder fmus with the exact names__.

### Demo execute_algorithm_3D

Same as [Demo execute_algorithm](#demo-execute_algorithm), except it also loads the Incubator3D FMU.
This demo only works on windows.

### Demo generate_algorithm_from_scenario

Shows the ability to generate an algorithm from a [scenario](./demos/generate_algorithm_from_scenario/scenario.conf).

The test calls the Maestro CLI with the scenario file.

The resulting master model which contains both the scenario and algorithm is placed in a results folder.

The scenario.conf file can be changed as needed.


### Demo verify_algorithm

Shows the ability to verify an algorithm.

The test calls the Maestro CLI with the [master model file](./demos/verify_algorithm/masterModel.conf).

This prints a message in the shell indicating if the master model is sucessfully verified or not.

In this test there is introduced an error in the algorithm in the mater model file, so it should not verify successfully.

### Test visualize_traces

Shows the ability to visualize possible traces generated from verification.

The test calls the Maestro CLI with the[master model file](./demos/visualize_traces/masterModel.conf).

As there is introduced an error in the algorithm in the mater model file, this call returns a video file that visualizes the traces.
