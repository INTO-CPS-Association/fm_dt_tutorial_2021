import unittest

import utils
import execute_algorithm.test as execute_algorithm_test
from generate_algorithm_from_scenario.test import generateAlgorithmFromScenario
from verify_algorithm.test import verifyAlgorithm
from visualize_traces.test import visualizeTraces
import execute_algorithm_faultinjection.test as fault_injection_test

batch_mode = True

class TestDTTutorial(unittest.TestCase):
    jarPath = utils.getMaestroJarPath()

    def test_execute_algorithm(self):
        execute_algorithm_test.executeAlgorithm(batch_mode, self.jarPath)

    def test_generate_algorithm_from_scenario(self):
        generateAlgorithmFromScenario(self.jarPath)

    def test_verify_algorithm(self):
        verifyAlgorithm(self.jarPath)

    def test_visualize_traces(self):
        visualizeTraces(self.jarPath)

    def test_execute_algorithm_faultinjection(self):
        fault_injection_test.executeAlgorithm(batch_mode, self.jarPath)


if __name__ == '__main__':
    unittest.main()

