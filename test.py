import unittest 
from TrajectoryAnalysisModule import TrajectoryAnalysis
import yaml
import argparse

# The test based on unittest module
class TestClass(unittest.TestCase):

    def test_method1(self):
        # Read the configuration file
        with open("test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        TrajectoryAnalysisObj = TrajectoryAnalysis(config)
        TrajectoryAnalysisObj.process()
    
    def test_method2(self):
        # Read the configuration file
        with open("test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        TrajectoryAnalysisObj = TrajectoryAnalysis(config)
        result = TrajectoryAnalysisObj.compute_directed_hausdorff_distance_matrix()

    def test_method3(self):
        # Read the configuration file
        with open("test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        TrajectoryAnalysisObj = TrajectoryAnalysis(config)
        config["TRAJECTORY_SRC_PATH"] = "1234.json"
        self.assertEqual(TrajectoryAnalysisObj.read_and_preprocess_data(config["TRAJECTORY_SRC_PATH"]), "File not found")

    def test_method4(self):
        # Read the configuration file
        with open("test_config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        TrajectoryAnalysisObj = TrajectoryAnalysis(config)
        config["TRAJECTORY_SRC_PATH"] = 1234
       
        self.assertEqual(TrajectoryAnalysisObj.read_and_preprocess_data(config["TRAJECTORY_SRC_PATH"]), "The trajectory file path is not a string")

    
