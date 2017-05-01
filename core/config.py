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

#Configure according your host
from collections import defaultdict
from utils.files import read_json
from utils import loaders

class Config(object):
    """
    Holds the complete Batcher Config

    The command line args for the batcher core
    and the job module

    The config.json parameters

    And is in charge of loading the job module elements

    TODO: This class must be rethink, too many responsibilities
    """
    def __init__(self, args):
        """
        Attributes: 
            config_params (dict)   : the parsed config.json file
            args (argparse object) : parsed cmdline params 
            model_args             : unparsed remaining cmdline params
            job_model              : imported model file from the job module
        """
        self.config_params = read_json('config.json')
        self.args,self.model_args = args.parse_args()
        self.job_model = None


    def get_global_config(self):
        """ Returns the entire config.json file """
        return self.config_params
    
    def get_module_config(self, module):
        """ Returns the module section of the config.json file """
        return self.config_params[module]
   
    def get_args(self):
        """ Returns the batcher args object """
        return self.args

    def get_job_model(self):
        """ Returns the loaded file containing the Job class """
        return self.job_model
      
    #TODO: This two methods are UGLY replace this with a more elegant solution
    def get_model(self, pclass):
        """
        Imports files in the job module packages
        to get the Stats or the Model classes

        Args:
           pclass (str) In : value can be (model, stats)
        """ 
        if not pclass in ('model','stats'):
            raise UnknownModelClass('Class should be model or stats')

        model_pkg = 'models.'+self.model_name+'.'+pclass
        module=loaders.load_module(model_pkg)
        return module

    def load_model(self, experiment, model_name):
        """
        Loads the job_module.model package

        Args:
           experiment (dict) : json file of the experiment that requires this model 
        Returns:
           pkg class of job_module.model 
        """
        # Don't load twice
        if self.job_model: 
            return self.job_model

        if self.args.use_model:
            model_name = self.args.use_model

        self.model_name = model_name
        self.job_model=self.get_model('model')
        
        #Parse the module specific args
        if len(self.model_args): 
            model_parser = argparse.ArgumentParser(self.model_args)
            self.job_model.define_args(model_parser)
            self.job_model.process_params(experiment, model_parser.parse_args())

        return self.job_model 

