import os
import sys
from tempfile import TemporaryDirectory
import pandas as pd
import matplotlib.pyplot as plt
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import utils


resourcesPath = os.path.dirname(__file__)
this_dir = os.path.dirname(__file__)
resultsPath = os.path.join(this_dir, "results")
executionParametersPath = os.path.join(this_dir, "executionParameters.json")
fiMablPath = os.path.join(this_dir, "FaultInject.mabl")
fiConfPath = os.path.join(this_dir, "FaultEvents.xml")
fiJarPath = os.path.join(this_dir, "faultinject-1.0.0-SNAPSHOT-jar-with-dependencies.jar")

multiModelPath = os.path.join(resourcesPath, "multimodel.json")
masterModelPath = os.path.join(resultsPath, "masterModel.conf")

def cliGenerateAlgorithmFromScenario(maestroJarPath):
    utils.printSection("GENERATING ALGORITHM")

    scenarioPath = os.path.join(resourcesPath, "scenario.conf")
    cmd = "java -jar {0} sigver generate-algorithm {1} -output {2}".format(maestroJarPath, scenarioPath, resultsPath)
    func = lambda: print("Succesfully written algorithm to masterModel.conf") if(masterModelPath) else lambda: (Exception("Master model was not generated"))
    utils.testCliCommandWithFunc(cmd, func)

def executeAlgorithm(batch_mode, maestroJarPath):
    utils.removeIfExists(resultsPath)
    os.mkdir(resultsPath)

    #bash_command = "java -jar " + coePath + " import sg1  --interpret " + fiMablPath + " " + multiModel + " " + coeJsonPath + " " + resultsPath

    cliGenerateAlgorithmFromScenario(maestroJarPath)

    utils.printSection("EXECUTING ALGORITHM")

    with TemporaryDirectory() as temp_dir:
        multiModel = utils.getCorrectedMultiModelAsPath(temp_dir, multiModelPath, resultsPath)
        with open(multiModel) as f:
            mm = json.load(f)

        mm["faultInjectConfigurationPath"] = fiConfPath.replace('\\','/')

        with open(multiModel, "w") as f:
            json.dump(mm, f)

        cmd = "java -cp {0}{1}{2} org.intocps.maestro.Main sigver execute-algorithm -ext {3} -mm {4} -ep {5} -al {6} -output {7} -di -vim FMI2".format(maestroJarPath, os.pathsep, fiJarPath, fiMablPath, multiModel, executionParametersPath, masterModelPath, resultsPath)
        func = lambda: print(f"Results of execution are located in {resultsPath}") if(os.path.exists(os.path.join(resultsPath, "outputs.csv"))) else lambda: (Exception("No output was returned from executing the algorithm"))
        utils.testCliCommandWithFunc(cmd, func)

    # Plot
    print("Plotting results...")
    results = pd.read_csv(os.path.join(resultsPath, "outputs.csv"))
    utils.plot_incubator_data(results)
    if not batch_mode:
        plt.savefig(os.path.join(resultsPath, "results.pdf"))
        plt.show()

if __name__ == '__main__':
    executeAlgorithm(False, utils.getMaestroJarPath())