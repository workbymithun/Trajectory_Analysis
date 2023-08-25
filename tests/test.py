import unittest 
from src.TrajectoryAnalysisModule import PerformTrajectoryAnalysis
import yaml
import argparse

# The test based on unittest module
class TestClass(unittest.TestCase):

    def test_method1(self):
        """ Function to perform test 1."""
        # Read the configuration file
        with open("tests/test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        PerformTrajectoryAnalysisObj = PerformTrajectoryAnalysis(config)
        PerformTrajectoryAnalysisObj.process()
    
    def test_method2(self):
        """ Function to perform test 2."""
        # Read the configuration file
        with open("tests/test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        PerformTrajectoryAnalysisObj = PerformTrajectoryAnalysis(config)
        result = PerformTrajectoryAnalysisObj.compute_directed_hausdorff_distance_matrix(PerformTrajectoryAnalysisObj.trajectories)

    def test_method3(self):
        """ Function to perform test 3."""
        # Read the configuration file
        with open("tests/test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        PerformTrajectoryAnalysisObj = PerformTrajectoryAnalysis(config)
        config["TRAJECTORY_SRC_PATH"] = "1234.json"
        self.assertEqual(PerformTrajectoryAnalysisObj.read_and_preprocess_data(config["TRAJECTORY_SRC_PATH"]), "File not found")

    def test_method4(self):
        """ Function to perform test 4."""
        # Read the configuration file
        with open("tests/test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        PerformTrajectoryAnalysisObj = PerformTrajectoryAnalysis(config)
        config["TRAJECTORY_SRC_PATH"] = 1234
        self.assertEqual(PerformTrajectoryAnalysisObj.read_and_preprocess_data(config["TRAJECTORY_SRC_PATH"]), "The trajectory file path is not a string")

    
