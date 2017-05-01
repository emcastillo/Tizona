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

from core.batcher_args import BatcherArgs
from core.batcher import Batcher
from core.config import Config

if __name__ == '__main__':

    #Register the cmdline options
    b_args = BatcherArgs() 

    b_args.parser.add_argument('--csv-params', nargs='*', type=str,
                            help="Provide a list of files to simulate",
                            required=True)
    b_args.parser.add_argument('--csv-stats', nargs='*', type=str,
                            help="Provide a list of files to simulate",
                            required=True)
    b_args.parser.add_argument('--csv-query', type=str,
                            help="SQL query to run on the CSV file",
                            required=False, default=None)
    b_args.parser.add_argument('--csv-output', type=str,
                            help="File to save the csv output",
                            required=False, default=None)
    b_args.parser.add_argument('--csv-extra', nargs='*', type=str,
                            help="Provide a list of files tto perform complex sql queries",
                            required=False, default=[])

    # Get the benchmarks and print their current status 
    # Benchmark - Experiment - #nr of tasks - last update - STATE - last output
    cfg = Config(b_args)

    Batcher(cfg).results()
