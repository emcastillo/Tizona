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

from collections import deque
from samplers import GridSampler
from utils.files import read_json


class GlobDesc(object):
    """
    Tracks the Json with the parameters
    And the list of associated jobs
    Very useful when generating results
    of several global descriptions
    """
    def __init__(self, json, exps):
        """
        Args / Attributes:
            json (dict) In : Json with the global desc file parameters
            exps (list of Job) : The experiments associated to this gdesc
        """
        self.json = json
        self.exps = exps

class JobBuilder(object): 
    """
    This class is in charge of parsing the input json files and
    obtain all the possible parameter combinations in order to
    create the needed Job objects of the corresponding module.
    """
    def __init__(self, config):
        """
        Attributes :
            config (config obj) : Contains batcher global config
            experiments (list of Job)   : Holds all the jobs
            global_desc (list of GDesc) : Holds all the global description files
        """
        self.config = config
        self.experiments = deque([])
        self.global_desc = deque([])

    def build(self, files):
        """ 
        Args:
            files (list of str) In : files to read the experiments from
        Returns:
            (list of experiments)
        """
        if not len(self.experiments):
            self.__parse_exp_files(files)
        return self.experiments

    def get_global_desc(self):
        """ Returns the list of global description files """
        return self.global_desc

    def __parse_exp_files(self, files): 
        """
        Reads all the json files and populates the self.experiments list
        with Job objects

        Args:
            files (list of str) In : files to read the experiments from
        """
        for json_file_path in files:
            print 'Reading ',json_file_path
            exp_json = read_json(json_file_path)
            # This is a global exps json
            if ('sim_files' in exp_json):
                # For results collections we want to know which jobs 
                # where obtained through global descriptions
                exps = self.__parse_exp_files(exp_json['sim_files'])
                if exps:
                    self.global_desc.append(GlobDesc(exp_json, exps))
            else:
                self.__configure_experiment(exp_json)

    def __configure_experiment(self, json):
        """
        Gets all the parameter samples for a experiment and adds them to the experiments list
        It queries the config module to get the corresponding Job Module to build the jobs

        Args:
           json (dict) In : one of the files specified in --files cmd arg already parsed as a json file
        """
        # The load model will process the parameters and 
        # tune the json dict accordingly
        job_module = self.config.load_model(json, json['model'])
        sampler = GridSampler(json, job_module, self.config.get_module_config(json['model']))
        exps = sampler.build()
        self.experiments.extend(exps)
        return exps


