import os
from tempfile import TemporaryDirectory
import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import utils

resourcesPath = os.path.dirname(__file__)
multiModelPath = os.path.join(resourcesPath, "multiModel.json")
resultsPath = os.path.join(resourcesPath, "results")
masterModelPath = os.path.join(resultsPath, "masterModel.conf")
executionParametersPath = os.path.join(resourcesPath, "executionParameters.json")

def cliGenerateAlgorithmFromScenario(maestroJarPath):
    utils.printSection("GENERATING ALGORITHM")

    scenarioPath = os.path.join(resourcesPath, "scenario.conf")
    cmd = "java -jar {0} sigver generate-algorithm {1} -output {2}".format(maestroJarPath, scenarioPath, resultsPath)
    func = lambda: print("Succesfully written algorithm to masterModel.conf") if(masterModelPath) else lambda: (Exception("Master model was not generated"))
    utils.testCliCommandWithFunc(cmd, func)

def executeAlgorithm(batch_mode, maestroJarPath):
    cliGenerateAlgorithmFromScenario(maestroJarPath)

    utils.printSection("EXECUTING ALGORITHM")

    with TemporaryDirectory() as temp_dir:
        multiModel = utils.getCorrectedMultiModelAsPath(temp_dir, multiModelPath, resultsPath)

        cmd = "java -jar {0} sigver execute-algorithm -mm {1} -ep {2} -al {3} -output {4} -di -vim FMI2".format(maestroJarPath, multiModel, executionParametersPath, masterModelPath, resultsPath)
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
    utils.removeIfExists(resultsPath)
    os.mkdir(resultsPath)
    executeAlgorithm(False, utils.getMaestroJarPath())
