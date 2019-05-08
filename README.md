A collection of utility scripts for typical MD stuff to ease my life.

# Install
Install anaconda for python from here: https://conda.io/miniconda.html

Create a conda environment for the utilities:
```sh
conda create -n mdutilities pip python=3.6.6
conda activate mdutilities
```

Install this repository:
```sh
pip install -e git+https://github.com/stefdoerr/utilities#egg=stefanutils
```

# Usage

## vmdall
Visualizes all simulations or structures in all subfolders to a given depth

```sh
vmdall  #This will visualize all simulations in subfolders
vmdall -nf  # Will keep the water. By default I remove them to speed up stuff
vmdall -d 10  # Will recurse into 10 depths of subdirectories to search for files
vmdall -li "resname GTP"  # Will represent GTP with licorice
```

## pm
A manager for HPC projects. Practically just a database of local/remote paths which does `rsync` for you.

```
stefan:~/Work$ pm init # Only necessary once to initialize the database
stefan:~/Work$ pm list # Lists all your projects
Name: local path <-> remote path
--------------------------------
proj1: /local/path/of/project/ <-> hpc:/remote/path/of/project/
stefan:~/Work$ pm add proj2 /local/path/of/project2/ hpc:/remote/path/of/project2/  # Adds a new project
stefan:~/Work$ pm list
Name: local path <-> remote path
--------------------------------
proj1: /local/path/of/project/ <-> hpc:/remote/path/of/project/
proj2: /local/path/of/project2/ <-> hpc:/remote/path/of/project2/
stefan:~/Work$ pm send proj2  # Upload your project files
Are you sure you want to send files? This might overwrite remote results! [Y/n]y
rsync -rav --info=progress2 /local/path/of/project2/ hpc:/remote/path/of/project2/
stefan:~/Work$ pm retrieve proj2 # Download remote project files
```
