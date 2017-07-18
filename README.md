# Tizona, A tool for managing workloads in HPC environments

## What is Tizona

Tizona is a simple tool for launching experiments in HPC clusters
and collect their results creating csv files.

Tizona allows users to specify their set of experiments in a single 
json file and it automatically generates and submits the corresponding 
jobs to the cluster batch system.

Batches is being developed at the Barcelona Supercomputing Center.

## Using Tizona with your application

Tizona uses modules to deal with workloads unique characteristics,
the modules obbey a simple interface and implement functionality such as
writing a file configuration, or download a set of required files before launching the experiments
where simple bash scripts are not flexible enough.

## Tizona configuration

Tizona is configured using the config.json at the root dir,
in this file module specific configuration parameters are written.

## Tizona experiments

Tizona runs experiments using json files containing a "params" dict.
In this params dict the values for the parameters are specified as scalar values or lists.
If multiple parameters have a list as their value, Tizona will obtain all the possible combinations of all lists
it is up to the module code to detect valid or invalid configurations of parameters within the job factory method
look at the provided example.json provided for further information

## Hosts

The folder hosts/ contains descriptions of different hosts.
Each host class is in charge of creating the corresponding script and execute it.

The config.json file determines the host type where you want to run your job.

## Launching jobs

Launching a experiment:

```
$ python launch.py --file experiments/example.json
```

The --file admits multiple files
The following line launchs the two experiments and combines them in packs together:

```
$ python launch.py --file experiments/example1.json experiments/example2.json 
```

## Collecting Job Results

CSV files can be obtained with the stats values defined through the models/model/stats.py class
The following line reads all the files containing experiments and created a csv file organized by the nmess, comp params with the time value

```
$ python csv.py --file experiments/examples*json --csv-params nmess comp --csv-stats time --csv-out output.csv
```

SQL queries are allowed to the csv output by passing a query along

```
$ python csv.py --file experiments/examples*json --csv-params nmess comp --csv-stats time --csv-out output.csv --csv-query "SELECT * from output"
```


