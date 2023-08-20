import argparse
import yaml
from TrajectoryAnalysisModule import TrajectoryAnalysis

def main():

    # Initialize argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Program to perform Trajectory Analysis")
    parser.add_argument("--config", default="config.yaml", help="Path to configuration file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")

    # Parse command-line arguments
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode is enabled.")

    
    # Read the configuration file
    with open(args.config, 'r') as config_file:
        config = yaml.safe_load(config_file)

    Analysis = TrajectoryAnalysis(config) 

    

if __name__ == "__main__":
    main()