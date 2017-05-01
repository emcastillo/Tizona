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

from __future__ import print_function
from utils import files
from collections import OrderedDict
import operator
import os


class NestedDict(OrderedDict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]

class Results(object):
    """
    Interface to manage results
    """
    def __init__(self, config):
        self.config = config

    def process(self, experiments, params, stats, query, extra_files, output):
        self.__create_csv(experiments, params, stats, output)
        if query:
            self.__run_sql(output, query, extra_files)

    def __create_csv(self, experiments, params, stats, output):
        csv = CSV(self.config, experiments=experiments,params_list = params, stats_list = stats)
        if output:
            with open(output,'w') as out:
                csv.print_csv(out)
        else:
            csv.print_csv()

    def __run_sql(self, output, query, extra_files):
        if type(query) is list:
            query = ''.join(query)
        os.system('sed "s/+/_/g" -i %s'%output)
        os.system('sed "s/ /_/g" -i %s'%output)
        extra_files = ''.join(['-i %s'%file for file in extra_files])
        qcsv_cmdline ='querycsv.py -i %s %s -o %s "%s"'%(output,extra_files,output,query)
        os.system('%s'%qcsv_cmdline)
        os.system('sed "s/\\"//g" -i %s'%output)


class CSV(object):
    """
    Iterate through all the experiments folders getting the results
    """
    def __init__(self, config, experiments, params_list, stats_list):
        self.config = config
        self.experiments =  experiments
        self.params_list = params_list
        self.stats_list  = stats_list
        self.names = []
        self.data = self.read_data(params_list, stats_list)

    def read_data(self, params_list, stats_list):
        """
        Given a params list creates a dictionary
        that obbeys the params_list hierachy in order
        The param list should contain the parameters for the simulation
        The stats the statistics for the simulation
        """
        results = NestedDict()
        for sim in self.experiments:
            cur_level = results
            for i,param in enumerate(params_list):
                param_value = sim.get_param(param)
                if i == (len(params_list)-1):
                    #Last level for this simulation, populate with stats
                    if not (sim.get_graph_name() in self.names):
                        self.names.append(sim.get_graph_name())
                    if param_value in cur_level:
                        cur_level[param_value] += self.__populate_stats(sim,stats_list)
                    else:
                        cur_level[param_value] = self.__populate_stats(sim,stats_list)
                else:
                    #advance one level
                    cur_level = cur_level[param_value] 

        return results 

    def __populate_stats(self, sim, stats_list):
        """
        Given the dictionary, it populates with the stats
        """
        sim_stats = self.config.get_model('stats').Stats(sim)
        st = [str(sim_stats.get_stat(stat)) for stat in stats_list]
        return st
    
    def __print_headers(self,output):
        if(len(self.stats_list) == 1):
            print(','.join((self.params_list+self.names)), file=output)
        else:
            print(','.join((self.params_list+self.stats_list)), file=output)
        

    def print_csv(self,output=None):
        cur_level = self.data
        self.__print_headers(output)
        for key in cur_level:
            self.__print_csv_aux(cur_level[key],[key],output)

    def __print_csv_aux(self, cur_level, csv_line=[],output=None):

        if type(cur_level) is list:
            print(','.join(map(str,csv_line) + map(str,cur_level)), file=output)
            return 
        
        for key in cur_level:
            self.__print_csv_aux(cur_level[key],csv_line+[key],output)
        

        
 

