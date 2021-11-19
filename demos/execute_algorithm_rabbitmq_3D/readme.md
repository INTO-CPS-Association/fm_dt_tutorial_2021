# Setup 
This test includes the unity fmu, and therefore has to be run on windows (at present binaries for the unity fmu are only available for this OS)
For running the same test on linux or macos, the unity fmu and its connections need to be removed from the ```multiModel.json``` file, and the ```scneario.conf```.

Before running the test:

1. Run the incubator emulator in a separate terminal. Follow the instructions at https://github.com/INTO-CPS-Association/example_digital-twin_incubator/tree/master/software.

2. Run the incubator rmqfmu bridge in a separate terminal (found in the execute_algorithm_rabbitmq_3D folder of this repo):
```bash
$ python execute_algorithm_rabbitmq_3D/rmqfmu_incubator_interface.py
```

Run the test:

3. Wait until the emulator and bridge are up and running, i.e. until the incubator state is printed continuously on the screen of the bridge terminal. 
   
4. Finally, run the rmqfmu test, from the ```scenario_verifier_test``` folder:
```bash
$ python execute_algorithm_rabbitmq_3D/test.py
```


