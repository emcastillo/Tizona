# Tizona, A tool for managing workloads in HPC environments

## What is Tizona

Tizona is a simple tool for launching experiments in HPC clusters
and collect their results creating csv files.

Tizona allows users to specify their set of experiments in a single 
json file and it automatically generates and submits the corresponding 
jobs to the cluster batch system.

Tizona is being developed at the Barcelona Supercomputing Center.

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

###Packing and batching

Multiple Experiments can be packed in one or few jobs by using the --pack-params and --pack-size options

When using --pack-params, supply a list of params name as specified in the experiments json params field
and experiments with the the same values for those params will be coalesced in the same pack.

To control the maximum number of experiments per job --pack-size is used. This argument can be use alone or in
conjunction with --pack-size

An example where we want to pack several experiments according to the number of nodes they need, and with a maximum
of 50 experiments per pack

```
$ python launch.py --file experiments/example1.json experiments/example2.json --pack-params nodes --pack-size 50
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

Complex SQL queries involving other files can be done by using the --csv-extra argument. The SQL will be able to use csv data stored in other files
by using join clausules or subqueries

```
$ python csv.py --file experiments/examples*json --csv-params nmess comp --csv-stats time --csv-out output.csv --csv-extra other_data.csv --csv-query "SELECT * from output INNER JOIN other_data ON output.param = other_data.param"
```

## Customize some Tizona aspects

### Rerunning experiments that failed

Tizona detects if an experiment was already run by looking if its stdout file was created.
Should you want to add a different functionality such as re-run if an error happened or re-run until a certain
algorithmic condition is met you can edit the models/base/model.py is_executed Job method.

You can even create a new model under the models directory

### Parsing job statistics for CSV generation

Right now Tizona can only work with time as an statistic as long as the binary run prints a line "time x" on its output
models/base/stats.py file can be modified to support user defined stats, a dictionary should be populated with the stat names
and values to be read when generating the csv results file.

Eventually we will provide a standard results output to be automatically detected by Tizona.

