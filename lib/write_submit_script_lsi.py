'''
Write the submission script, given:
1. lsi_submit_template.sh
2. cluster_config.json
3. job_config.json for any type of job
4. All the job specific parameters given
'''

import json
import os

def editclusterconfig(
    jobname,
    time,
    cluster_config,
    cluster,
    # queuename,
    # querycmd,
    # keyarg,
    ):
    '''
    Edit the cluster config json file.
    '''

    cluster_config[cluster]['jobname'] = jobname
    cluster_config[cluster]['time'] = time
    # cluster_config[cluster]['queuename'] = queuename
    # cluster_config[cluster]['querycmd'] = querycmd
    # cluster_config[cluster]['keyarg'] = keyarg

    return cluster_config


def parse_config(job_config, program):
    '''
    Parse the parameters in the config file (already read as a dict) into the command form.
    '''
    command = job_config[program]['command']
    parameters = job_config[program]['parameters'].copy() # make a copy rather than modify in place.

    for key in list(parameters):
        if isinstance(parameters[key], bool):
            if parameters[key]:
                parameters[key] = ""
            else:
                parameters.pop(key)

    cmd = command + ' '.join('{} {}'.format(key, val) for key, val in parameters.items())
    return cmd


def write_submit_lsi(
    codedir,
    projdir,
    submission_script,
    template_file,
    job_config,
    program,
    jobname, time,
    cluster_config,
    cluster,
    # queuename='sb-96',
    # querycmd='squeue --noheader --long --states=completing,running,pending,configuring -j ',
    # keyarg="job_state = ",
    ):

    # projdir is the directory where the submission file is written into
    # codedir is the directory where all the template files are

    cluster_config = editclusterconfig(
                        jobname=jobname,
                        time=time,
                        cluster_config=cluster_config,
                        cluster=cluster,
                        # queuename=queuename,
                        # querycmd=querycmd,
                        # keyarg=keyarg,
                        )

    command = parse_config(job_config, program)

    # os.chdir(projdir)
    ## Below: remove the submission file if exists
    try:
        os.remove(os.path.join(projdir, submission_script))
    except OSError:
        pass

    ## Below: write the submission file
    with open(os.path.join(codedir, template_file), 'r') as f:
        with open(os.path.join(projdir, submission_script), 'w') as new_f:
            for line in f:
                # newline = line.decode('utf-8').replace('$$job_name', cluster_config[cluster]['job_name'])\
                newline = line.replace('$$jobname', cluster_config[cluster]['jobname'])\
                .replace('$$queuename', cluster_config[cluster]['queuename'])\
                .replace('$$mpinodes', str(job_config['general']['mpinodes']))\
                .replace('$$stdout', job_config['general']['stdout'])\
                .replace('$$stderr', job_config['general']['stderr'])\
                .replace('$$threads', str(job_config['general']['threads'][cluster]))\
                .replace('$$time', cluster_config[cluster]['time'])\
                .replace('$$modules', job_config[program]['module'][cluster])\
                .replace('$$command_to_run', command)
                # new_f.write(newline.encode('utf-8'))
                new_f.write(newline)
