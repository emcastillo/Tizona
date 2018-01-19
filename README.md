# Tizona, A tool for managing workloads in HPC environments

## What is Tizona

Tizona is a tool for launching experiments in HPC clusters
and collect their results.

Tizona allows users to specify their set of experiments in a single 
json file and automatically generates and submits the corresponding 
jobs to the cluster batch system.

Tizona is being developed at the Barcelona Supercomputing Center.

## Using Tizona with your application

Tizona can use custom models to deal with workloads unique characteristics.
Models obbey a simple interface and can implement functionality such as
writing a file configuration, or download a set of required files before launching the experiments.

## Tizona configuration

Tizona is configured using the config.json at the root dir.
in this file models and hosts specific configuration parameters are written.

## Tizona experiments

Tizona runs experiments using json files containing a "params" dict.
Within this params dict, the values for the parameters are specified as scalar values or lists.
If multiple parameters have a list as their value, Tizona will obtain all the possible combinations of all lists.
It is up to the module code to detect valid or invalid configurations of parameters within the job factory method.
The example.json file shows how to create experiments.

## Hosts

The folder hosts/ contains descriptions of different hosts.
Each host class is in charge of creating the corresponding job script and execute it.

The config.json file determines the host type where you want to run your job.

## Launching jobs

Launching a experiment:

```
$ python launch.py --file experiments/example.json
```

The --file admits multiple files at once:

```
$ python launch.py --file experiments/example1.json experiments/example2.json 
```

###Packing and batching

Multiple Experiments can be packed in one or few jobs by using the --pack-params and --pack-size options

When using --pack-params, supply a list of params as specified in the experiments json params field.
Experiments with the the same values for those params will be coalesced in the same pack.

To control the maximum number of experiments per job --pack-size is used. This argument can be used alone or 
together with --pack-size

Pack several experiments according to the number of nodes they need, and with a maximum
of 50 experiments per pack:

```
$ python launch.py --file experiments/example1.json experiments/example2.json --pack-params nodes --pack-size 50
```

## Collecting Job Results

CSV files can be created with the stats values defined through the models/model/stats.py class.
The following line reads all the files containing experiments and creates a csv file organized by the nmess, comp params with the stat time values:

```
$ python csv.py --file experiments/examples*json --csv-params nmess comp --csv-stats time --csv-out output.csv
```

It is also possible to use SQL to process the csv files:

```
$ python csv.py --file experiments/examples*json --csv-params nmess comp --csv-stats time --csv-out output.csv --csv-query "SELECT * from output"
```

Complex SQL queries involving other files can be done by using the --csv-extra argument. The SQL query will be able to use csv data stored in other files
with join clausules or subqueries

```
$ python csv.py --file experiments/examples*json --csv-params nmess comp --csv-stats time --csv-out output.csv --csv-extra other_data.csv --csv-query "SELECT * from output INNER JOIN other_data ON output.param = other_data.param"
```

## Customize some Tizona aspects

### Rerunning experiments that failed

Tizona detects if an experiment was already run by looking if its stdout file was created.
It is possible to add a different functionality such as re-run if an error happened or re-run until a certain
algorithmic condition is met you can edit the models/base/model.py is_executed Job method.

### Parsing job statistics for CSV generation

The stats field on the experiment configuration allows to specify bash commands to retrieve metrics from the
output files.

```
    "stats" : {
        "time" : "grep Time %(stdout)s | rev | cut -d' ' -f1 | rev"
    }
```

Here we add a stat called time whose value is retrieved from the stdout of each experiment using that bash command.

The following placeholders will be replaced with the experiment specific values:

*stdout
*working_dir
*name
*app_name

