import json
import os
import re
import subprocess
from zipfile import ZipFile
import shutil
import matplotlib.pyplot as plt
import pathlib

import paths


def plot_incubator_data(data):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)

    ax1.plot(data["time"], data["{Plant}.p.T_bair_out"], label="Real_T_bair")
    ax1.plot(data["time"], data["{KalmanFilter}.k.T_bair_out"], label="KalmanFilter_T_bair")
    ax1.legend()

    ax2.plot(data["time"], data["{Controller}.c.heater_on_out"], label="Controller_heater_on")
    ax2.legend()

    ax3.plot(data["time"], data["{KalmanFilter}.k.T_heater_out"], label="KalmanFilter_T_heater")
    ax3.legend()

    ax4.plot(data["time"], data["{Supervisor}.s.H_out"], label="Supervisor_H")
    ax4.plot(data["time"], data["{Supervisor}.s.C_out"], label="Supervisor_C")
    ax4.legend()

def removeIfExists(fileOrDirectory):
    if os.path.exists(fileOrDirectory):
        if os.path.isfile(fileOrDirectory):
            os.remove(fileOrDirectory)
        else:
            shutil.rmtree(fileOrDirectory)

def zipdir(output_filename, path):
    zipf = ZipFile(output_filename, 'w')
    length = len(path)

    for root, dirs, files in os.walk(path):
        folder = root[length:]  # path without "parent"
        for file in files:
            zipf.write(os.path.join(root, file), os.path.join(folder, file))
    zipf.close()

def printSection(section):
    hashes = "###############################"
    print("\n" + hashes)
    print(section)
    print(hashes)

def getMaestroJarPath():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "maestro.jar"))
    if not os.path.exists(path):
        raise Exception("maestro.jar needs to be located in the same folder as utils.py")
    return path

def getCorrectedMultiModelAsPath(tempDir, multiModelPath, resultsPath):

    with open(multiModelPath) as f:
        multiModel = json.load(f)

    for fmu in multiModel["fmus"]:
        fmuNameMatch = re.match("{(\w+)}", fmu)
        assert len(fmuNameMatch.groups()) == 1, f"Problem extracting fmu name from FMU key {fmu}. Name should be { '{FMUName}' }."
        fmuName = fmuNameMatch.groups()[0]
        fmuPath = os.path.join(tempDir, f"{fmuName}.fmu")
        fmuFolderPath = os.path.join(paths.fmuDir, fmuName)
        assert os.path.isdir(fmuFolderPath), f"Problem finding fmu directory {fmuFolderPath}."
        zipdir(fmuPath, fmuFolderPath)
        multiModel["fmus"][fmu] = pathlib.Path(fmuPath).as_uri()

    correctedMultiModelPath = os.path.join(resultsPath, "multiModel.json")

    with open(correctedMultiModelPath, "w") as f:
        json.dump(multiModel, f)

    return correctedMultiModelPath


def testCliCommandWithFunc(cmd, func, cwd=None):
    print("Cmd: " + cmd)
    p = subprocess.run(cmd, shell=True, cwd=cwd)
    if p.returncode != 0:
        raise Exception(f"Error executing {cmd}")
    else:
        func()