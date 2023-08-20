import unittest 
from TrajectoryAnalysisModule import TrajectoryAnalysis
import yaml
import argparse

# The test based on unittest module
class TrajectoryAnalysis(unittest.TestCase):
    def runTest1(self):
        # Read the configuration file
        with open("config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        Analysis = TrajectoryAnalysis(config)
        result = TrajectoryAnalysis.compute_hausdorff_distance_matrix()
        self.assertTrue(result)
        # self.assertEqual(TrajectoryAnalysis.compute_hausdorff_distance_matrix())
 
# run the test
unittest.main()