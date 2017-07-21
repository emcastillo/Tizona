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

from utils import files
import subprocess
from collections import defaultdict
import numpy as np
import os.path

class Stats(object):
    """
    Parses and stores the relevant stats of the job

    This moduel right now supports the time stat.
    The executed job should have print a line with
    the format 'Time xxx' in the stdout file
    
    If multiple lines are defined, the stat value will be the average
    """

    def __init__(self, job):
        """
        Args:
            job (job object) In : The job to get the stats from
        Attributes:
            stats (dict) : holds the readed values from the job stdout
        """
        self.stats = self.__read_stats(job)

    def __read_stats(self, job):
        """
        Parses the job stdout and stores the stats
        in a dict of lists

        Args:
            job (job object) In : The job to get the stats from
        Returns:
            dict : contains the parsed stats for the job
        """
        stats = defaultdict(list)
        file_path = os.path.expanduser(job.get_stdout())
        file_path = os.path.expandvars(file_path)
        try:
            with open(file_path,'r') as f:
                for line in f:
                    tokens = line.split()
                    if 'Time' in line:
                        stats['time'].append(tokens[-1])
        except:
            stats['time'].append('0.0')
        return stats

    def get_stat(self, stat):
        """
        Args:
            stat (str) In : stat to get the AVG value from
        Returns:
            float : Average value for stat
        """
        try:
            return np.average(map(float,self.stats[stat]))
        except:
            return None

