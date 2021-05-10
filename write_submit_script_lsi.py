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
    jobname, walltime,
    cluster_config_file='cluster_config.json',
    cluster='lsi',
    queue_name='sb-96',
    query_cmd='squeue --noheader --long --states=completing,running,pending,configuring -j ',
    keyarg='job_state = '):

    '''
    Edit the cluster config json file.
    '''

    with open(cluster_config_file, 'r') as f:
        cluster_config = json.load(f)

    cluster_config[cluster]['jobname'] = jobname
    cluster_config[cluster]['time'] = walltime
    cluster_config[cluster]['queuename'] = queue_name
    cluster_config[cluster]['querycmd'] = query_cmd
    cluster_config[cluster]['keyarg'] = keyarg

    return cluster_config

def editjobconfig(
    job_config_file,
    program,
    stdout, stderr,
    input, output,
    module,
    command,
    parameters):

    '''
    Edit the job config file with the input information.
    '''

    with open(job_config_file, 'r') as f:
        job_config = json.load(f)

    job_config['general']['stdout'] = stdout
    job_config['general']['stderr'] = stderr
    job_config['general']['mpinodes'] = nodes
    job_config['general']['threads'] = threads

    job_config[program]['input'] = input
    job_config[program]['output'] = output
    job_config[program]['module'] = module
    job_config[program]['command'] = command
    job_config[program]['parameters'] = parameters

    return job_config

def write_submit_lsi(codedir, wkdir, submit_name,
                        jobname, walltime, nodes,
                        job_config_file, program,
                        input, output, stdout, stderr,
                        module, conda_env, command, parameters,
                        template_file,
                        cluster,
                        cluster_config_file='cluster_config.json',
                        ):
    # wkdir is the directory where the submission file is written into
    # codedir is the directory where all the template files are

    cluster_config = editclusterconfig(jobname, walltime, cluster=cluster)

    job_config = editjobconfig(job_config_file, \
                                program, \
                                input, output, stdout, stderr, \
                                module, \
                                conda_env, \
                                command, \
                                parameters, \
                                extra='', \
                                tail='')

    command = job_config[program]['command'] + \
                job_config['general']['input'] + \
                job_config['general']['output'] + \
                job_config[program]['parameters'] + \
                job_config['general']['stdout'] + \
                job_config['general']['stderr'] + \
                job_config[program]['tail']

    os.chdir(wkdir)
    ## Below: remove the submission file if exists
    try:
        os.remove(submit_name)
    except OSError:
        pass
    ## Below: write the submission file
    with open(os.path.join(codedir, template_file), 'r') as f:
        with open(submit_name, 'w') as new_f:
            for line in f:
                # newline = line.decode('utf-8').replace('$$job_name', cluster_config[cluster]['job_name'])\
                newline = line.replace('$$job_name', cluster_config[cluster]['job_name'])\
                .replace('$$walltime', cluster_config[cluster]['walltime'])\
                .replace('$$queue_name', cluster_config[cluster]['queue_name'])\
                .replace('$$nodes', cluster_config[cluster]['nodes'])\
                .replace('$$modules', job_config[program]['module'])\
                .replace('$$extra', job_config[program]['extra'])\
                .replace('$$conda_env', job_config[program]['conda_env'])\
                .replace('$$command_to_run', command)
                # new_f.write(newline.encode('utf-8'))
                new_f.write(newline)
