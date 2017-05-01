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

"""
Loads the current host type based on the config.json host type

Does it dinamycally to avoid hardcoded classnames in factory methods
and to allow a diversity of hosts

TODO: Rename hosts to job runners
"""

def current_host(config):
    hosts={ }
    import sys
    import inspect
    import pkgutil 
    import importlib
    from host import Host
    
    # Try to get the current host as specified in the config file
    # Otherwise resort to the Default host
    h_config =  config.get_global_config()['host']
    host_class = h_config['type']
    #Iterate through all the members of this class
    module_names = [name for _, name, _ in pkgutil.iter_modules([__name__])]
    for mod in module_names:
        importlib.import_module(__name__+'.'+mod)

    for mod in module_names:
        for name, obj in inspect.getmembers(sys.modules[__name__+'.'+mod]):
            if inspect.isclass(obj):
                hosts[obj.__name__]=obj
   
    if host_class in hosts:
        return hosts[host_class](h_config) 
    else:
        host = Host(h_config)

    return host
