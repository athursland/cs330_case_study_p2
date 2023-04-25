# CS 330 Case Study Part 2 README
## Authors 
- Ali Thursland - akt21
- Mike Kim - bk146
- Noa Nir - nn83

## Zip Contents

Our ZIP file contains our source code and a PDF of our slides for Case Study Part 2. All of our solutions are implemented in Python. Our source code contains the following .py files: 

- simplify.py: Contains a new version of the functions we used to simplify trajectories in Case Study Part 1, with an improved compression ratio
- import_data.py: Imports the data from 'geolife-cars-upd8.csv' for Task 4
- approach1.py: Implementation of Approach 1 from Task 4
- task4.py: Contains implementation of Approach 2 from Task 4, as well as the code needed to run the appropriate experiments / create the visualizations
- task5.py: Contains all the functions needed to implement the coded solutions to Task 5 

The ZIP file also contains the following .txt files, in the experimental results folder: 


The ZIP file also contains the following .png files, in the figures folder: 
- task 4 figures:
- approach1_whole.png, approach1_zoom1.png, approach1_zoom2.png: The visualizations of approach 1 at varying levels of zooms for clarity 
- approach2_whole.png, approach2_zoom1.png, approach2_zoom2.png: Visualizations for approach 2 at varying levels of zoom for clarity
- task 5 figures: 
- avg_costs_vs_k.png: 
- centers_prop_seed_prop_k.png: 
- avg_costs_over_iterations.png: 

To reproduce our experimental results for each task, uncomment the appropriate lines in the main call for task4.py and task5.py. They are labelled appropriately. 

 ## External Dependencies

The only external library we used is matplotlib, which we utilize for creating our visualizations. Run the following command to install matplotlib:

    pip3 install matplotlib
    
matplotlib is necessary to run task1.py, task2.py,and  task3_tests.py. All of the other source code files can be run without any external dependencies.

