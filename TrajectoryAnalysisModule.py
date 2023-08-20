import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
import json 
import logging
import sys

class TrajectoryAnalysis:

    def __init__(self, config:str): 
        """ Init of all variables for processing goes here """

        self.trajectories = self.read_and_preprocess_data(config["TRAJECTORY_SRC_PATH"])
        self.hausdorff_distance_matrix = self.compute_hausdorff_distance_matrix()
        self.cluster_and_plot_figures(self.hausdorff_distance_matrix, config["PLOT_DIST_MATRIX"], 
                                      config["SAVE_DIST_MATRIX_PATH"], config["SAVE_GROUPED_TRAJECTORIES_PATH"], 
                                      config["EPS"], config["MIN_SAMPLES"])

    def read_and_preprocess_data(self, trajectory_file_path:str):
        """ 
        function_name - read_and_preprocess_data
        input - trajectory_file_path (str)
        output - trajectories (list([(x1,y1), (x2,y2) ......],...))
        process - reads the json file and pre-process the required values only for further processing
        """

        trajectories = []
        if type(trajectory_file_path) != str:
            logging.error("The trajectory file path is not a string")
            return "The trajectory file path is not a string"
            # sys.exit(1)
        try:
            with open(trajectory_file_path, "r") as json_file:
                trajectory_data = json.load(json_file)
        except FileNotFoundError:
            logging.error("File not found")
            return "File not found"
            # sys.exit(1)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format")
            return "Invalid JSON format"
            # sys.exit(1)
        except Exception as e:
            logging.error("An error occurred:", e)
            return "An error occurred:"
            # sys.exit(1)

        
        for element in trajectory_data:
    
            #Preprocess each trajectory and numpify the arrays
            res_tr = tuple(map(str, element["coordinates"].split(' ')))
            res_tr_list = [tuple(map(float, val.split(','))) for val in res_tr]

            #trajectories would contain elements as [(x1,y1), (x2,y2) ......]
            trajectories.append(np.array(res_tr_list))

        return trajectories

    def calc_directed_hausdorff_distance(self, traj1, traj2):
        """ 
        function_name - calc_directed_hausdorff_distance
        input - traj1 (numpy_array - [(x1,y1), (x2,y2) ......]), traj2 (numpy_array - [(x1,y1), (x2,y2) ......])
        output - directed_hausdorff_dist (float)
        process - calculates the directed hausdorff distance between given two trajectories
        """

        if len(traj1) < 1 or len(traj2) < 1:
            logging.error("There are not enough points in a trajectory to compute distance.")
            return "There are not enough points in a trajectory to compute distance."
            # sys.exit(1)


        #Computing directed hausdorf distance as DH(A, B) = max(max(min(d(a, b))) , max(min(d(b, a))))

        distances_1_to_2 = cdist(traj1, traj2, 'euclidean')
        max_distances_1_to_2 = np.max(np.min(distances_1_to_2, axis=1))
        
        distances_2_to_1 = cdist(traj2, traj1, 'euclidean')
        max_distances_2_to_1 = np.max(np.min(distances_2_to_1, axis=1))
        
        directed_hausdorff_dist = max(max_distances_1_to_2, max_distances_2_to_1)
        
        return directed_hausdorff_dist #hausdorff_dist

    def compute_hausdorff_distance_matrix(self):
        """ 
        function_name - compute_hausdorff_distance_matrix
        input - trajectories (list([(x1,y1), (x2,y2) ......],...))
        output - directed_hausdorff_distance_matrix (numpy_array)
        process - calculates the hausdorff distance matrix between all trajectory combinations
        """
        if len(self.trajectories) <= 1:
            logging.error("There are not enough trajectories to perform computing")
            return "There are not enough trajectories to perform computing"
            # sys.exit(1)

        directed_hausdorff_distance_matrix = np.zeros((len(self.trajectories), len(self.trajectories)))
        for i in range(len(self.trajectories)):
            for j in range(len(self.trajectories)):
                directed_hausdorff_distance_matrix[i, j] = self.calc_directed_hausdorff_distance(self.trajectories[i], self.trajectories[j])
        return directed_hausdorff_distance_matrix

    def cluster_and_plot_figures(self, directed_hausdorff_distance_matrix, plot_dist_matrix:bool, 
                                 save_dist_matrix_path:str, save_grouped_trajectories_path:str, 
                                 eps:float, min_samples:int):
        """ 
        function_name - cluster_and_plot_figures
        input - directed_hausdorff_distance_matrix (numpy_array), plot_dist_matrix (boolean), 
                save_dist_matrix_path (str), save_grouped_trajectories_path (str), 
                eps (float), min_samples (int)
        output - None (saves final figures to destination paths)
        process - cluster the trajectories based on directed hausdorf distance and 
                  plot the grouped trajectories with same colour for each group after 
                  eliminating outlier (DBSCAN is used for clustering)
        """
        #Visualise hausdorf distance matrix before clustering 
        if plot_dist_matrix == True:
            try:
                # Plot the Hausdorff distance matrix
                fig1 = plt.figure(figsize=(8, 6))
                plt.imshow(hausdorff_distance_matrix, cmap='cividis', origin='upper', interpolation='nearest')
                plt.colorbar(label='Directed Hausdorff Distance')
                plt.title('Directed Hausdorff Distance Matrix')
                plt.xlabel('Trajectories along X axis')
                plt.ylabel('Trajectories along Y axis')
                plt.xticks(range(len(hausdorff_distance_matrix[0])))
                plt.yticks(range(len(hausdorff_distance_matrix[1])))
                # plt.xticks(np.arange(len(hausdorff_distance_matrix[0])), np.arange(1, len(hausdorff_distance_matrix[0]) + 1))
                # plt.yticks(np.arange(len(hausdorff_distance_matrix[1])), np.arange(1, len(hausdorff_distance_matrix[1]) + 1))
                # plt.tight_layout()
                if save_dist_matrix_path.endswith(".png") or save_dist_matrix_path.endswith(".jpg"):
                    fig1.savefig(save_dist_matrix_path)
                else:
                    return "Invalid file path to save distance matrix figure"
                    # sys.exit(1)
            except Exception as e:
                return "An error occurred in saving hausdorff_distance_matrix:"
                # sys.exit(1)
        else:
            if plot_dist_matrix != False:
                return "Type Error! It should be a boolean value."


        try:
            # Use DBSCAN to group similar trajectories based on the Hausdorff distance matrix
            # eps = 20.0  # Maximum distance between points to be considered in the same neighborhood
            # min_samples = 6  # Minimum number of samples required for a cluster
            dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
            cluster_labels = dbscan.fit_predict(hausdorff_distance_matrix)

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
                # sys.exit(1)
        except Exception as e:
            return "An error occurred while saving grouped_trajectories:"
            # sys.exit(1)