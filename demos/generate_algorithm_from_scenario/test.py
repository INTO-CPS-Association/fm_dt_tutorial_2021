import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import utils

resourcesPath = os.path.dirname(__file__)
resultsPath = os.path.join(resourcesPath, "results")
masterModelPath = os.path.join(resultsPath, "masterModel.conf")

def generateAlgorithmFromScenario(maestroJarPath):
    utils.removeIfExists(resultsPath)
    os.mkdir(resultsPath)
    utils.printSection("GENERATING ALGORITHM")

    scenarioPath = os.path.join(resourcesPath, "scenario.conf")
    cmd = "java -jar {0} sigver generate-algorithm {1} -output {2}".format(maestroJarPath, scenarioPath, resultsPath)
    func = lambda: print(f"Succesfully written algorithm to masterModel.conf in {resultsPath}") if(masterModelPath) else lambda: (Exception("Master model was not generated"))
    utils.testCliCommandWithFunc(cmd, func)


if __name__ == '__main__':
    generateAlgorithmFromScenario(utils.getMaestroJarPath())
