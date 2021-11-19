import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import utils

resourcesPath = os.path.dirname(__file__)
resultsPath = os.path.join(resourcesPath, "results")
masterModelPath = os.path.join(resourcesPath, "masterModel.conf")

def visualizeTraces(jarPath):
    utils.removeIfExists(resultsPath)
    os.mkdir(resultsPath)
    utils.printSection("VISUALIZING TRACES")
    cmd = "java -jar {0} sigver visualize-traces {1} -output {2}".format(jarPath, masterModelPath, resultsPath)
    func = lambda: True
    utils.testCliCommandWithFunc(cmd, func)

if __name__ == '__main__':
    visualizeTraces(utils.getMaestroJarPath())
