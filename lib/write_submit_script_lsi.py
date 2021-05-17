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
    cluster_config_file,
    cluster,
    # queuename,
    # querycmd,
    # keyarg,
    ):
    '''
    Edit the cluster config json file.
    '''
    with open(cluster_config_file, 'r') as f:
        cluster_config = json.load(f)

    cluster_config[cluster]['jobname'] = jobname
    cluster_config[cluster]['time'] = time
    # cluster_config[cluster]['queuename'] = queuename
    # cluster_config[cluster]['querycmd'] = querycmd
    # cluster_config[cluster]['keyarg'] = keyarg

    return cluster_config


def editjobconfig(
    job_config_file,
    program,
    mpinodes,
    # threads,
    stdout, stderr,
    # input, output,
    # module,
    # command,
    parameters):
    '''
    Edit the job config file with the input information.
    '''
    with open(job_config_file, 'r') as f:
        job_config = json.load(f)

    job_config['general']['stdout'] = stdout
    job_config['general']['stderr'] = stderr
    job_config['general']['mpinodes'] = mpinodes
    # job_config['general']['threads'] = threads

    # job_config[program]['input'] = input
    # job_config[program]['output'] = output
    # job_config[program]['module'] = module
    # job_config[program]['command'] = command
    job_config[program]['parameters'] = parameters

    return job_config


def write_submit_lsi(
    codedir,
    wkdir,
    submission_script,
    template_file,
    job_config_file,
    program,
    mpinodes,
    # threads,
    stdout, stderr,
    # input, output,
    # module,
    # command,
    parameters,
    jobname, time,
    cluster_config_file,
    cluster,
    # queuename='sb-96',
    # querycmd='squeue --noheader --long --states=completing,running,pending,configuring -j ',
    # keyarg="job_state = ",
    ):

    # wkdir is the directory where the submission file is written into
    # codedir is the directory where all the template files are

    job_config = editjobconfig(
                        job_config_file=job_config_file,
                        program=program,
                        mpinodes=mpinodes,
                        # threads=threads,
                        stdout=stdout,
                        stderr=stderr,
                        # input, output,
                        # module,
                        # command,
                        parameters=parameters,
                        )

    cluster_config = editclusterconfig(
                        jobname=jobname,
                        time=time,
                        cluster_config_file=cluster_config_file,
                        cluster=cluster,
                        # queuename=queuename,
                        # querycmd=querycmd,
                        # keyarg=keyarg,
                        )

    command = job_config[program]['command'] + job_config[program]['parameters']

    os.chdir(wkdir)
    ## Below: remove the submission file if exists
    try:
        os.remove(submission_script)
    except OSError:
        pass

    ## Below: write the submission file
    with open(os.path.join(codedir, template_file), 'r') as f:
        with open(submission_script, 'w') as new_f:
            for line in f:
                # newline = line.decode('utf-8').replace('$$job_name', cluster_config[cluster]['job_name'])\
                newline = line.replace('$$jobname', cluster_config[cluster]['jobname'])\
                .replace('$$queuename', cluster_config[cluster]['queuename'])\
                .replace('$$mpinodes', job_config['general']['mpinodes'])\
                .replace('$$stdout', job_config['general']['stdout'])\
                .replace('$$stderr', job_config['general']['stderr'])\
                .replace('$$threads', job_config['general']['threads'])\
                .replace('$$time', cluster_config[cluster]['time'])\
                .replace('$$modules', job_config[program]['module'])\
                .replace('$$command_to_run', command)
                # new_f.write(newline.encode('utf-8'))
                new_f.write(newline)
