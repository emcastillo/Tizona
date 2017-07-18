# Copyright (c) 2017, Barcelona Supercomputing Center
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# Authors: E. Castillo (Barcelona Supercomputing Center)

import argparse
import os
import hosts
import random
from collections import defaultdict, deque

from builder import JobBuilder

from utils.files import read_json
from results.CSVResults import Results


class Batcher(object):
    """
    Interface to Tizona main operations
    
    1. Launch Experiments
    2. Collect experiments

    This class hold all the experiments specified in the
    input files after sampling all the possible parameters combinations
    """

    def __init__(self, config):
        """
        Args:
            config (config obj) In : Holds the global configuration of Batcher

        Attributes:
            config (config obj) : Global configuration of batcher
            experiments (list of Job objects ) : List with all the jobs to launch
            global_desc (list of GDesc objects ) : Files that group other experiment files and 
                                          set parameters for csv generation, plotting etc.
        """
        self.config = config
        
        # Parse Json Files
        builder = JobBuilder(config)
        self.experiments = builder.build(config.get_args().file)
        self.global_desc = builder.get_global_desc()

    def run(self):
        """
        Will run all the experiments specified in the --file cmd_line argument
        Experiments are initialized first by calling the prepare method in the corresponding
        job module and then the already executed ones are removed to prevent
        relaunching them
        
        Multiple experiments can be packed in jobs as specified by the param list in --pack-params
        And every pack will have at most --pack-size experiments

        Packing code contributed by LLNL        

        The current host, as specified in the config.json file will execute the experiments
        """
        pack_params = self.config.get_args().pack_params
        pack_size   = self.config.get_args().pack_size

        random.shuffle(self.experiments)

        self.__prepare_experiments()
        self.__remove_executed()       
        
        jobs = self.__pack_experiments(pack_params, pack_size)
        for job in jobs:
            hosts.current_host(self.config).run_job(job)

    def results(self):            
        """ Generates a CSV file with the experiments output as described in the documentation """
        #Creates the results files
        csv_params = self.config.get_args().csv_params
        csv_stats  = self.config.get_args().csv_stats
        csv_query  = self.config.get_args().csv_query
        csv_output = self.config.get_args().csv_output
        csv_extra  = self.config.get_args().csv_extra

        # If we have global desc files process them
        for gdesc in self.global_desc:
            csv_params = global_desc['csv_params'] if 'csv_params' in global_desc else csv_params
            csv_stats  = global_desc['csv_stats']  if 'csv_stats'  in global_desc else csv_stats
            csv_output = global_desc['csv_output'] if 'csv_output' in global_desc else csv_output
            csv_query  = global_desc['csv_query']  if 'csv_query'  in global_desc else csv_query
            csv_extra  = global_desc['csv_extra']  if 'csv_extra'  in global_desc else csv_extra
            Results(self.config).process(gdesc.experiments,csv_params, csv_stats, csv_query, csv_output)

        #Only do the whole processing if there is no gdescs
        if not len(self.global_desc):
            Results(self.config).process(self.experiments,csv_params, csv_stats, csv_query, csv_extra, csv_output)

    def __prepare_experiments(self):
        """ Calls the prepare hook in the job module """
        for exp in self.experiments:
            exp.prepare()

    def __remove_executed(self):
        """ Remove already executed experiments """
        self.experiments = filter(lambda x: not x.is_executed(), self.experiments)

    def __pack_experiments(self, pack_params, pack_size):
        """
        Create Packed jobs were all the experiments within a job
        have the same value for the params specified in pack_params
        and each job has at most pack_size experiments
        
        Arguments: 
            pack_params (list of str) : name of the params as specified in the params field of the json
            pack_size (int) : maximum number of experiments per job 
        """

        if (not pack_params) and (not pack_size):
            # no pack especified
            return self.experiments

        if pack_params:
            # Create groups of experiments with that share the same pack_params value
            parts = self.__group_exps(self.experiments, pack_params)
            packs = deque([])
            if pack_size:
                for part in parts:
                    packs.extend([part[i:i+pack_size] for i in range(0, len(part), pack_size)])
        elif pack_size:
            packs = [self.experiments[i:i+pack_size] for i in range(0, len(self.experiments), pack_size)]

        return [self.config.get_job_model().PackedJob(i,pack) for i, pack in enumerate(packs)]

 
    def __group_exps(self, jobs, params):
        """
        Create sub list of experiments grouped by the params list values
        """
        parts = []
        if not len(params):
            return [jobs]

        partition = defaultdict(list)
        for job in jobs:
            partition[job.get_param(params[0])].append(job)
        
        for key in partition:
            parts += self.__group_exps(partition[key],params[1:]) 
        return parts

