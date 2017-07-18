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
import sys

class BatcherArgs :
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f','--file', nargs='+', type=str,
                            help="Provide a list of files to simulate",
                            required=True)

        parser.add_argument('-m','--use-model', type=str, 
                            help="Override the model defined in the json file", required = False, 
                            default = None)

        parser.add_argument('-r','--remote', type=str, 
                            help="launch the files remotely", required = False, 
                            default = None)

        parser.add_argument('-n','--prefix', type=str,
                            help="Add a prefix to the experiments name",
                            default = None)

        parser.add_argument('-ns', '--no-sync',
                            help='dont sync files when calling remote', required = False,
                            action='store_true')

        parser.add_argument('-pp','--pack-params', nargs='+', type=str, 
                            help="Pack experiments in a job file by this list of params values", required = False, 
                            default = None)

        parser.add_argument('-ps','--pack-size', type=int, 
                            help="Number of experiments PER job file", required = False, 
                            default = None)

        self.parser = parser

    def parse_args(self):
        args,model_args = self.parser.parse_known_args()
        if args.remote != None:
            from remote import remote
            remote.launch_remote(' '.join(sys.argv),args.remote, args.no_sync)
            sys.exit(0)
        return args, model_args
