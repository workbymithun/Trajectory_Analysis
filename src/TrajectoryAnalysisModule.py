import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import json 
import logging
import sys

class PerformTrajectoryAnalysis:

    def __init__(self, config:str): 
        """ Init of all variables for Analysis """

        self.config = config 
        self.trajectories = self.read_and_preprocess_data(self.config["TRAJECTORY_SRC_PATH"])

    def process(self): 
        """  Perform Trajectory Analysis """
        
        directed_hausdorff_distance_matrix = self.compute_directed_hausdorff_distance_matrix(self.trajectories)
        self.group_trajectories_and_plot_figures(directed_hausdorff_distance_matrix, self.config["PLOT_DIST_MATRIX"], 
                                      self.config["SAVE_DIST_MATRIX_PATH"], self.config["SAVE_GROUPED_TRAJECTORIES_PATH"], 
                                      self.config["EPS"], self.config["MIN_SAMPLES"])
        
    def plot_trajectories(self, trajectories):
        """
        function_name - plot_trajectories
        input - trajectories (list([(x1,y1), (x2,y2) ......],...))
        output - Displays the 2D tajectories
        process - Read the trajectory points and display trajectories.
        """

        for traj in trajectories:
            x_vals, y_vals = zip(*traj)  # Unzip the points into separate x and y lists
            plt.plot(x_vals, y_vals)
        # Set plot labels and title
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("2D Trajectories")
        # Show plot
        plt.show()
       
    def read_and_preprocess_data(self, trajectory_file_path:str):
        """ 
        function_name - read_and_preprocess_data
        input - trajectory_file_path (str)
        output - trajectories (list([(x1,y1), (x2,y2) ......],...))
        process - reads the json file and pre-process the required values only for further processing.
        """

        if type(trajectory_file_path) != str:
            logging.error("The trajectory file path is not a string")
            return "The trajectory file path is not a string"
        try:
            with open(trajectory_file_path, "r") as json_file:
                trajectory_data = json.load(json_file)
        except FileNotFoundError:
            logging.error("File not found")
            return "File not found"
        except json.JSONDecodeError:
            logging.error("Invalid JSON format")
            return "Invalid JSON format"
        except Exception as e:
            logging.error("An error occurred:", e)
            return "An error occurred:"
        trajectories = [np.array([tuple(map(float, val.split(','))) for val in element["coordinates"].split(' ')])
                            for element in trajectory_data]
        return trajectories

    def calculate_directed_hausdorff_distance(self, traj1, traj2):
        """ 
        function_name - calculate_directed_hausdorff_distance
        input - traj1 (numpy_array - [(x1,y1), (x2,y2) ......]), traj2 (numpy_array - [(x1,y1), (x2,y2) ......])
        output - directed_hausdorff_dist (float)
        process - calculates the directed hausdorff distance between given two trajectories.
        """

        if len(traj1) < 1 or len(traj2) < 1:
            logging.error("There are not enough points in a trajectory to compute distance.")
            return "There are not enough points in a trajectory to compute distance."

        #Computing directed hausdorf distance as DH(A, B) = max(max(min(d(a, b))) , max(min(d(b, a))))

        distances_1_to_2 = cdist(traj1, traj2, 'euclidean')
        max_distances_1_to_2 = np.max(np.min(distances_1_to_2, axis=1))
        
        distances_2_to_1 = cdist(traj2, traj1, 'euclidean')
        max_distances_2_to_1 = np.max(np.min(distances_2_to_1, axis=1))
        
        directed_hausdorff_dist = max(max_distances_1_to_2, max_distances_2_to_1)
        
        return directed_hausdorff_dist

    def compute_directed_hausdorff_distance_matrix(self, trajectory_list):
        """ 
        function_name - compute_directed_hausdorff_distance_matrix
        input - trajectory_list (list([(x1,y1), (x2,y2) ......],...))
        output - directed_hausdorff_distance_matrix (numpy_array)
        process - calculates the hausdorff distance matrix.
        """

        if len(trajectory_list) <= 1:
            logging.error("There are not enough trajectories to perform computing")
            return "There are not enough trajectories to perform computing"

        num_trajectories = len(trajectory_list)
        directed_hausdorff_distance_matrix = np.zeros((num_trajectories, num_trajectories))

        for i in range(num_trajectories):
            for j in range(i, num_trajectories):  # Use symmetry of the distance matrix
                distance = self.calculate_directed_hausdorff_distance(trajectory_list[i], trajectory_list[j])
                directed_hausdorff_distance_matrix[i, j] = distance
                directed_hausdorff_distance_matrix[j, i] = distance  # Fill symmetric value

        return directed_hausdorff_distance_matrix

    def group_trajectories_and_plot_figures(self, directed_hausdorff_distance_matrix, plot_dist_matrix:bool, 
                                 save_dist_matrix_path:str, save_grouped_trajectories_path:str, 
                                 eps:float, min_samples:int):
        """ 
        function_name - group_trajectories_and_plot_figures
        input - directed_hausdorff_distance_matrix (numpy_array), plot_dist_matrix (boolean), 
                save_dist_matrix_path (str), save_grouped_trajectories_path (str), 
                eps (float), min_samples (int)
        output - None (saves final figures to destination paths)
        process - cluster the trajectories based on directed hausdorf distance and 
                  plot the grouped trajectories with same colour for each group after 
                  eliminating outliers (DBSCAN is used for clustering).
        """

        #Visualise hausdorf distance matrix before clustering 
        if plot_dist_matrix == True:
            try:
                # Plot the Hausdorff distance matrix
                fig1 = plt.figure(figsize=(8, 6))
                plt.imshow(directed_hausdorff_distance_matrix, cmap='cividis', origin='upper', interpolation='nearest')
                plt.colorbar(label='Directed Hausdorff Distance')
                plt.title('Directed Hausdorff Distance Matrix')
                plt.xlabel('Trajectories along X axis')
                plt.ylabel('Trajectories along Y axis')
                plt.xticks(range(len(directed_hausdorff_distance_matrix[0])))
                plt.yticks(range(len(directed_hausdorff_distance_matrix[1])))
                plt.tight_layout()
                if save_dist_matrix_path.endswith(".png") or save_dist_matrix_path.endswith(".jpg"):
                    fig1.savefig(save_dist_matrix_path)
                else:
                    return "Invalid file path to save distance matrix figure"
            except Exception as e:
                return "An error occurred in saving directed_hausdorff_distance_matrix:"
        else:
            if plot_dist_matrix != False:
                return "Type Error! It should be a boolean value."

        try:
            # Use DBSCAN to group similar trajectories based on the Hausdorff distance matrix
            # eps = 20.0  # Maximum distance between points to be considered in the same neighborhood
            # min_samples = 6  # Minimum number of samples required for a cluster
            dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
            cluster_labels = dbscan.fit_predict(directed_hausdorff_distance_matrix)
            
            # Plot trajectories with distinct colors based on clusters
            fig2 = plt.figure(figsize=(10, 6))
            colormap = plt.cm.get_cmap('tab10', len(np.unique(cluster_labels)))

            for cluster_id in np.unique(cluster_labels):
                if cluster_id == -1:
                    continue  # Skip noise points (cluster_id == -1)
                color = colormap(cluster_id)
                cluster_indices = np.where(cluster_labels == cluster_id)[0]
                for index in cluster_indices:
                    traj = self.trajectories[index]
                    plt.plot(traj[:, 0], traj[:, 1], color=color, marker='o', markersize=4, linestyle='-', linewidth=1)

            plt.xlabel('X Coordinate')
            plt.ylabel('Y Coordinate')
            plt.title('Similar Trajectories Based on Directed Hausdorff Distance')
            plt.grid()
            if save_grouped_trajectories_path.endswith(".png") or save_grouped_trajectories_path.endswith(".jpg"):
                fig2.savefig(save_grouped_trajectories_path)
            else:
                return "Invalid file path to save grouped trajectories figure"
        except Exception as e:
            return "An error occurred while saving grouped_trajectories:"
            