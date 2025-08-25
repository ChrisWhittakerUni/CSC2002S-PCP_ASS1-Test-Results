import os
import subprocess
import csv
import matplotlib.pyplot as plt
import pandas as pd

serial_file = "DungeonHunter"
parallel_file = "DungeonHunterParallel"



#change directory to the Testing folder so that the java scripts can run
#os.chdir("OneDrive\\Desktop\\UNI\\Courses\\CSC2002S\\Assignments\\PCP_ASS1\\Testing")

# function to do a test of the speedup with varying gridSize (and therefore grid area), and save the results to a csv file
def test(gridSize, searchDensity, seed, numTests, Spacing, firstRun, csvName):
    #convert necessary arguments to Strings
    gridSize = str(gridSize)
    searchDensity = str(searchDensity)
    seed = str(seed)

    #gridSize array
    gridSize_arr = []

    #result arrays
    serial_results = []
    parallel_results = []

    #for loop to do the runs of the java files
    for i in range(numTests):
        args = gridSize + " " + searchDensity + " " + seed

        serial_version = "java " + serial_file + " " + gridSize + " " + searchDensity + " " + seed
        parallel_version = "java " + parallel_file + " " + gridSize + " " + searchDensity + " " + seed

        #store gridSize for this run
        gridSize_arr.append(gridSize)

        # run serial:
        result = subprocess.run(serial_version, shell=True, capture_output=True, text=True, check=True)

        # Store results in array
        output = result.stdout.strip()
        time = output.split("\n")[0]
        print("serial " + args + ":")
        print(time)
        serial_results.append(time)



        # run parallel:
        result = subprocess.run(parallel_version, shell=True, capture_output=True, text=True, check=True)

        # Store results in array
        output = result.stdout.strip()
        time = output.split("\n")[0]
        print("parallel " + args + ":")
        print(time)
        parallel_results.append(time)

        
        # increment gridSize
        gridSize = str(int(gridSize) + Spacing)

    #print output to terminal
    print("gridSizes:")
    print(gridSize_arr)
    print("serial results")
    print(serial_results)
    print("parallel results")
    print(parallel_results)

    # Write to CSV
    gridArea = [int(t)*int(t) for t in gridSize_arr]
    serial_times = [int(t.replace(" ms", "")) for t in serial_results]
    parallel_times = [int(t.replace("ms", "")) for t in parallel_results]
    speedup = [int(s)/int(p) for s,p in zip(serial_times,parallel_times)]
    label = "Seed of " + str(seed) + "search Density of " + searchDensity

    mode = "w" if firstRun else "a" # overwrite and create csv if it is the first run. If it is not the first run append and do not overwrite previous runs
    with open(csvName, mode=mode, newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Header row is only put in when csv is empty (at start)
            writer.writerow(["Label", "Grid Size", "Grid Area", "Serial Time (ms)", "Parallel Time (ms)", "Speedup (Ts/Tp)"])
        for gs, ga, st, pt, su in zip(gridSize_arr, gridArea, serial_times, parallel_times, speedup):
            writer.writerow([label, gs, ga, st, pt, su])

    print("✅ CSV file '" + csvName + "' has been created.")


# function to plot results from the csv on one set of axes
def plot_all_results(graphLabel, csv_file, output_file):

    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10,6))
    labels = df["Label"].unique()

    for label in labels:
        data = df[df["Label"] == label]
        plt.plot(data["Grid Area"], data["Speedup (Ts/Tp)"], marker='o', linestyle='-', label=label)

    plt.title(graphLabel)
    plt.xlabel("Grid Area")
    plt.ylabel("Speedup (Ts/Tp)")
    plt.grid(True)
    plt.legend()
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"✅ Plot saved as {output_file}")

# run and plot speedups for different random seeds as we vary grid area
test(10, 2, 3, 20, 25, True, "results_seed.csv")
test(10, 2, 12, 20, 25, False, "results_seed.csv")
test(10, 2, 82, 20, 25, False, "results_seed.csv")
plot_all_results("Speedup vs Grid Area for Different Random Seeds", "results_seed.csv", "Speedup_vary_seeds.png")

# run and plot speedups for different search densities as we vary grid area
test(10, 0.1, 1, 20, 25, True, "results_sD.csv")
test(10, 1, 1, 20, 25, False, "results_sD.csv")
test(10, 3, 1, 20, 25, False, "results_sD.csv")
plot_all_results("Speedup vs Grid Area for Different Search Densities", "results_sD.csv", "Speedup_vary_searchDensity.png")






