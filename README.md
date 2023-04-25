# CS 330 Case Study Part 2 README
## Authors 
- Ali Thursland - akt21
- Mike Kim - bk146
- Noa Nir - nn83

## Zip Contents

Our ZIP file contains our source code and a PDF of our slides for Case Study Part 2. All of our solutions are implemented in Python. Our source code contains the following .py files:

### .py files 
- simplify.py: Contains a new version of the functions we used to simplify trajectories in Case Study Part 1, with an improved compression ratio
- import_data.py: Imports the data from 'geolife-cars-upd8.csv' for Task 4
- approach1.py: Implementation of Approach 1 from Task 4
- task4.py: Contains implementation of Approach 2 from Task 4, as well as the code needed to run the appropriate experiments / create the visualizations
- task5.py: Contains all the functions needed to implement the coded solutions to Task 5 
### .txt files
The ZIP file also contains the following .txt files, in the experimental results folder: 

#### task 4
 - approach1_avg_dists_eps_1.txt: Average distances of trajectories in trajectory-ids.txt from center trajectory computed using Approach 1, where trajectories are simplified with epsilon = 0.03
 - approach1_avg_dists_eps_2.txt: Average distances of trajectories in trajectory-ids.txt from center trajectory computed using Approach 1, where trajectories are simplified with epsilon = 0.1
 - approach1_avg_dists_eps_3.txt: Average distances of trajectories in trajectory-ids.txt from center trajectory computed using Approach 1, where trajectories are simplified with epsilon = 0.3
 - approach1_avg_dists.txt: Average distances of trajectories in trajectory-ids.txt from center trajectory computed using Approach 1. 
 - approach2_avg_dists.txt: Average distances of trajectories in trajectory-ids.txt from center trajectory computed using Approach 2. 

#### task 5
- simplify_tests.txt: Compression ratios calculated for 3 specific trajectory ids, to test our implementation of the simplification algorithm 
 - avg_costs_seed_random.txt: Average costs of clustering for random seeding method for k = [4,6,8,10,12]
 - avg_costs_seed_prop.txt: Average costs of clustering for proposed seeding method for k = [4,6,8,10,12]

### .png files
The ZIP file also contains the following .png files, in the figures folder: 

#### task 4
 - approach1_whole.png, approach1_zoom1.png, approach1_zoom2.png: The visualizations of approach 1 at varying levels of zooms for clarity 
 - approach2_whole.png, approach2_zoom1.png, approach2_zoom2.png: Visualizations for approach 2 at varying levels of zoom for clarity

#### task 5
 - avg_costs_vs_k.png: Average costs of clustering for random and proposed seeding methods vs. k = [4,6,8,10,12]
 - centers_prop_seed_k_10.png: Centers of clusters chosen using our proposed seeding method for our chosen k, k = 10.
 - avg_costs_over_iterations.png: Average cost of clustering for over iterations for both random and proposed seeding methods

To reproduce our experimental results for each task, run approach1.py, task4.py and task5.py.

 ## External Dependencies

The only external library we used is matplotlib, which we utilize for creating our visualizations. Run the following command to install matplotlib:

    pip3 install matplotlib
    
matplotlib is necessary to run task4.py and task5.py All of the other source code files can be run without any external dependencies.

