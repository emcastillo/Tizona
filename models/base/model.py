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

import os

"""
Binary File Runner
"""

def job_factory(experiment, param_sample, job_id, config):
    """
    Instantiate one or multiple jobs depending on the
    specified parameters

    Args:
        experiment (dict)   In : contains the whole experiment.json
        param_sample (dict) In : contains a sampled params section of the 
                                 experiment, this means one of all the possible
                                 combinations
        job_id (int) In        : The id of the job
        config (dict) In       : Config values set for the module in the config.json
    Returns:
        list : list of Job objects
    """
    jobs = []
    job= Job(experiments,param_sample, job_id, config)

    return [job]

def define_args(args):
    """ 
    Add custom cmdline arguments passed

    Args:
        args (argparse obj) InOut : the argparse object where the new parameters will be added
    
    """
    pass

def process_params(experiment, args):
    """
    Reconfigure the experiment dict
    according to parsed args

    Args:
        experiment (dict) InOut : The complete json file dict, which will be altered
                    based on the args added at the defined_args function
        args (argparse obj)  In : The argparse object contained the args specified at
                    the define_args function already parsed

    """
    pass


class Job(object):
    """
    Containes and provides methods to access
    all the relevant job parameters
    """
    def __init__(self, experiment, param_sample, job_id, config):
        """
        Initializes a job based on the general experiments description
        and a parameters sample

        Args/Attributes:

            experiment (dict)   In : contains the whole experiment.json
            param_sample (dict) In : contains a sampled params section of the 
                                     experiment, this means one of all the possible
                                     combinations
            job_id (int) In        : The id of the job
            config (config obj) In : The config object with the module settings

        """
        self.experiment = experiment
        self.param_sample = param_sample
        self.job_id = job_id
        self.config = config

    def prepare(self):
        """
        Do any work required prior launching the job
        This is module specific
        """
        pass

    def __get_exp_list_as_line(self,key):
        """
        Given a key of the experiment file
        that contains a list, fuse the list
        elements in a single string with line 
        breaks.

        This does not work in params, just global experiment
        fields like the bin or the environment

        Args:
           key (str) In :  Experiment file field that
                         should be fused in one string
        Returns:
           str : all the elements in self.experiment[key]
                 fused in a single string with line breaks
        """
        line = self.experiment[key]
        if type(line) is list:
            line = '\n'.join(line)
        # Substitute all the parameters in the bins cmd 
        return (line)
    
    def get_cmd_line(self):
        """
        Returns:
            str : all the commands the script will execute
        """
        cmd_line =  self.__get_exp_list_as_line('bin')%self.param_sample
        return cmd_line
            
    def get_env(self):
        """
        Returns:
            str : all the environment variables that should be 
                  set prior running the cmd line
        """
        # Load the modules and the environment if necessary
        return self.__get_exp_list_as_line('env')

    def get_name(self):
        """
        Returns:
            str : self.experiment['name'] with the placeholders
                    replaced by the values in the param sample
        """
        return self.experiment['name'] % self.param_sample
    
    def get_working_dir(self):
        """
        Returns the working dir for the experiment
        if it does not exist create it under the
        config['base']['OUT_DIR'] directory

        The working directory can be specified using
        parameters

        Returns:
            str : path to the jobs working directory
        """

        wd_name = self.experiment['working_dir'] % self.param_sample
        wd_path = os.path.join(self.config['OUT_DIR'], wd_name)
        dir = os.path.expandvars(os.path.dirname(wd_path))
        if not os.path.exists(dir):
            os.makedirs(dir)
        return wd_path
   
    def get_graph_name(self):
        """
        Gets the name of the experiment used for represent it
        in a CSV column.

        Returns:
            str : self.experiment['graph_name'] with the placeholders
                    replaced by the values in the param sample
        """
        return self.experiment['graph_name'] % self.param_sample
    
    def get_param(self, param):
        """
        Returns:
            str : value of the param in the param_sample attr
        """
        return self.param_sample[param]

    def get_config(self):
        """
        Returns:
            config obj: The config parameters for this module as defined in 
                      config.json
        """
        return self.config

    def get_stdout(self):
        """
        Returns:
            str : path to the file where the stdout will be stored
        """
        return os.path.join(self.get_working_dir(),self.get_name()+'.out')

    def get_stderr(self):
        """
        Returns:
            str : path to the file where the stderr will be stored
        """
        return os.path.join(self.get_working_dir(),self.get_name()+'.err')

    def is_executed(self):
        """
        Returns:
            bool : True when the stdout file already exists (the Job was executed)
        """
        return os.path.isfile(self.get_stdout())

