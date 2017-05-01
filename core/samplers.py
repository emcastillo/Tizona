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


try:
    from sklearn import model_selection
    from sklearn.model_selection import ParameterGrid
except ImportError:
    #Rely on an older sklearn version
    from sklearn import grid_search
    from sklearn.grid_search import  ParameterGrid

from collections import defaultdict, deque


class Sampler(object):
    """
    Base abstract class for
    implement parameter searchers
    """
    def __init__(self, experiment, job_module, job_module_config):
        """
        Args / Attributes :
            experiment (dict) : one of the --file cmd args json files already parsed
            job_module (Module pkg Class) : The Job module pkg class object used to instantiate Jobs
            job_module_config     (dict) : The config parameters (config.json) for the job_module
        """
        #global dataset
        self.experiment = defaultdict(str)
        self.experiment.update(experiment)
        self.jobs = deque([])
        self.job_module = job_module
        self.job_module_config = job_module_config

    def sample(self):
        """
        Get one combination of all the experiment[params] dict possible ones 
        """
        for param_set in self.searcher:
            yield param_set

    def build(self):
        """
        Sample all the combinations and build all the Job objects (one per params combination)

        Returns:
           list of module.Job objects
        """
        job_id = 0
        for param_set in self.sample():
            self.jobs.extend(self.job_module.job_factory(self.experiment, param_set, job_id, self.job_module_config))
        return self.jobs

class GridSampler(Sampler):
    """
    Create a series of jobs based on SKLEARN Grid Search
    It will do a combinatory search of all the params
    defined as an array in the params section of the experiments
    json
    """
    def __init__(self, experiment, args, job_module_config):
        super(self.__class__, self).__init__(experiment, args, job_module_config)
        # pre-format the experiment dict
        # Sklearn needs all the params to be in a  list for the grid to work
        # properly
        for param in experiment['params']:
            if type(experiment['params'][param]) is not list:
                experiment['params'][param] = [experiment['params'][param] ]

        self.searcher = ParameterGrid(experiment['params'])
