import matplotlib.pyplot as plt
from utilities import FileReader
import csv
import numpy as np

"""def plot_trajectory(filename):
    x = []
    y = []

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            x.append(float(row[0]))
            y.append(float(row[1]))

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'o', linewidth=1.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Robot Trajectory')
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()"""


def plot_trajectory(filename):
    x = []
    y = []
    
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        
        for row in csv_reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    
    # Generate points for the sigmoid curve
    #x_ref = np.linspace(0, 2, 100)
    #y_ref = 1 / (1 + np.exp(-(x_ref - 1) * 6))

    # Generate points for the y=x^2 curve
    x_ref = np.linspace(0, 2, 100)
    y_ref = x_ref**2
    
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'o', linewidth=1.5, label='Robot Trajectory')
    plt.plot(x_ref, y_ref, '-', linewidth=2, label='Sigmoid Curve')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Robot Trajectory with Sigmoid Curve')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.tight_layout()
    plt.show()    





import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_trajectory(filename)



