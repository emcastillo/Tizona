import os
import subprocess
from hosts.host import Host

slurm_script = r"""#!/bin/bash
#SBATCH -N %(nodes)d
#SBATCH -J %(name)s
#SBATCH -t %(wall_time)s
#SBATCH -p %(partition)s
#SBATCH -o %(sim_out)s
#SBATCH -A %(account)s

%(env)s
#echo $SLURM_JOB_ID;

%(code)s
"""


class Slurm(Host):
    def run_job(self, job):
        # Check if the same job was submitted before
        # Name conflict

        batchcode = slurm_script % {
            "partition": self.config["partition"],
            "account": self.config["account"],
            "code": job.get_cmd_line(),
            "env": job.get_env(),
            "name": job.get_name(),
            "nodes": job.get_param("nodes"),
            "wall_time": job.get_wall_time(),
            "sim_out": job.get_stdout(),
        }

        f = open(job.get_job_script_path(), "w")
        f.write(batchcode)
        f.close()
        output = subprocess.check_output(
            "sleep 0.1 && sbatch %s" % job.get_job_script_path(), shell=True
        )
        # Return the job id
        return output.split()[-1]

    def is_running(self, exp):
        return False
