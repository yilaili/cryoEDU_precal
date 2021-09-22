#!/usr/bin/env python3
import json
import argparse
import os
import sys
import subprocess
import time
import shutil
import re
import string
import random

from lib.check_if_done import check_state_lsi
from lib.write_submit_script_lsi import write_submit_lsi

'''
Submit relion 3D classification job.
Inputs: 1. Path of the *particles.star file from particle extraction,
        2. Name of the 3D classification directory,
        3. Path of the reference volume,
        4. Diameter of the mask,
        5. Number of classes,
        6. tau2_fudge,
        7. Whether to do ctf (default is False),
        8. Initial low pass filter for ref (default is -1),
        9. Symmetry (default is C1),
        10. healpix_order (default is 2).
Output: 3D classification results, saved in the output directory.
'''

def setupParserOptions():
    ap = argparse.ArgumentParser()
    ## General inputs
    ap.add_argument('-i', '--input',
                    help="Provide star file of the ctf corrected micrographs.")
    ap.add_argument('-o','--output', default='Class3D',
                    help="Name of the directory where the outputs of 3D classification are stored.")
    ap.add_argument('-p', '--program', default='relion_Class3D',
                    help='The program to use to do particle extraction. Currently only supports relion_Class3D.')
    ap.add_argument('--projdir',
                    help="Provide the RELION project directory (main directory).")
    ## Program specific parameters
    ap.add_argument('-r','--ref',
                    help="Path to the reference model (mrc).")
    ap.add_argument('-d', '--diameter',
                    help="Diameter of the particle to be used in 3D classification (in Angstrom).")
    ap.add_argument('-K', '--numclass',
                    help="Number of classes to be used in 3D classification.")
    ap.add_argument('--tau2_fudge',
                    help="Regularisation parameter (values higher than 1 give more weight to the data).")
    ap.add_argument('--ctf', action='store_true',
                    help="Whether to do ctf correction. Default is FALSE.")
    ap.add_argument('--ini_high', default='-1',
                    help="Initial low pass filter for ref (default is -1).")
    ap.add_argument('--sym', default='C1',
                    help="Symmetry (default is C1).")
    ap.add_argument('--healpix_order', default='2',
                    help="Healpix order for the angular sampling (before oversampling) on the (3D) sphere: hp2=15deg, hp3=7.5deg, etc.")
    ## Cluster submission needed
    ap.add_argument('--template', default='config/lsi_submit_template.sh',
                    help="Name of the submission template.")
    ap.add_argument('--cluster', default='lsi',
                    help='The computer cluster the job will run on.')
    ap.add_argument('--jobname', default='Class3D',
                    help='Jobname on the submission script.')
    # ap.add_argument('--user_email', help='User email address to send the notification to.')
    ap.add_argument('--time', default='48:00:00',
                    help='Expected max run time of the job.')
    ap.add_argument('--mpinodes', default='10',
                    help='Number of mpi processes used in the compute cluster.')
    # ap.add_argument('--threads', default='10',
    #                 help='Number of threads used per mpi process.')

    args = vars(ap.parse_args())
    return args


def outdir_naming(length=6):

    # ctf = 1 if args['ctf'] else 0
    # ctf_intact_first_peak = 1 if args['ctf_intact_first_peak'] else 0
    # zero_mask = 1 if args['zero_mask'] else 0
    # params = [
    #     ('diam-{:s}', args['diameter']),
    #     ('K-{:s}', args['numclass']),
    #     ('tau2-{:s}', args['tau2_fudge']),
    #     ('ctf-{:01d}', ctf),
    #     ('ign1p-{:01d}', ctf_intact_first_peak),
    #     ('zerom-{:01d}', zero_mask)]
    # specs = '_'.join([t.format(v) for (t, v) in params])
    # return specs

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length)) # random string with length=length


def editjobconfig(
    job_config, save_path,
    mpinodes, stdout, stderr,
    input, output, ref,
    diameter, numclass, tau2_fudge,
    ini_high, sym, healpix_order, ctf,
    threads):

    '''
    Modify the job_config according to the parameters, and then
    save it to the save_path as job.json.
    '''

    job_config['general']['stdout'] = stdout
    job_config['general']['stderr'] = stderr
    job_config['general']['mpinodes'] = mpinodes

    if not ctf:
        assert not ctf_intact_first_peak

    parameters = job_config['relion_Class3D']['parameters']

    parameters['--i'] = input
    parameters['--o'] = output
    parameters['--ref'] = ref
    parameters['--particle_diameter'] = diameter
    parameters['--K'] = numclass
    parameters['--tau2_fudge'] = tau2_fudge
    parameters['ini_high'] = ini_high
    parameters['sym'] = sym
    parameters['healpix_order'] = healpix_order
    parameters['--j'] = threads

    if ctf:
        parameters['--ctf'] = True

    with open(os.path.join(save_path, 'job.json'), 'w') as outfile:
        json.dump(job_config, outfile)

    return job_config


def parse_config(job_config):
    '''
    Parse the parameters in the config file (already read as a dict) into the command form.
    '''
    command = job_config['relion_Class3D']['command']
    parameters = job_config['relion_Class3D']['parameters'].copy() # make a copy rather than modify in place.

    for key in list(parameters):
        if isinstance(parameters[key], bool):
            if parameters[key]:
                parameters[key] = ""
            else:
                parameters.pop(key)

    cmd = command + ' '.join('{} {}'.format(key, val) for key, val in parameters.items())

    return cmd


def save_pipeline(job_config, save_path):
    '''
    Save pipeline.json file to keep track of the input--output link of this job.
    '''
    pipeline = {
        'input': job_config['relion_Class3D']['parameters']['--i'],
        'output': job_config['relion_Class3D']['parameters']['--o']
        }

    with open(os.path.join(save_path, 'pipeline.json'), 'w') as outfile:
        json.dump(pipeline, outfile)


def check_good(class_dir):
    '''
    Currently only supports relion 3D classification.
    Check if 'run_it025_model.star' file exists.
    '''
    return os.path.isfile(os.path.join(class_dir, 'run_it025_model.star'))


def submit(**args):

    cluster = args['cluster']
    codedir = os.path.abspath(os.path.join(os.path.realpath(sys.argv[0]), os.pardir))
    projdir = args['projdir']
    cluster_config_file = 'config/cluster_config.json'
    job_config_file = 'config/config_class3d.json'

    ## mkdir to setup the job
    try:
        os.mkdir(os.path.join(projdir, args['output']))
    except OSError:
        pass

    os.chdir(codedir)
    with open(cluster_config_file, 'r') as f:
        cluster_config = json.load(f)
    with open(job_config_file, 'r') as f:
        job_config = json.load(f)

    jobname = args['jobname']
    # user_email = args['user_email']
    time = args['time']
    program = args['program']
    mpinodes = args['mpinodes']
    threads = job_config['general']['threads'][cluster]
    # threads = args['threads']

    outname = outdir_naming()
    submission_script = 'submit_%s_%s.sh' %(args['program'], outname)
    input = args['input']
    output_dir = os.path.join(args['output'], outname)
    submission_script_dir = os.path.join(projdir, output_dir)
    output = '%s/run '%output_dir
    stdout = '%s/run.out'%output_dir
    stderr = '%s/run.err'%output_dir

    # make the subdirectory under the output directory (Class3D)
    try:
        shutil.rmtree(os.path.join(projdir, output_dir))
        os.mkdir(os.path.join(projdir, output_dir))
    except OSError:
        os.mkdir(os.path.join(projdir, output_dir))

    job_config = editjobconfig(
        job_config, os.path.join(projdir, output_dir),
        mpinodes, stdout, stderr,
        input, output, args['ref'],
        args['diameter'], args['numclass'], args['tau2_fudge'],
        args['ini_high'], args['sym'], args['healpix_order'], args['ctf'],
        threads,
        )

    save_pipeline(job_config, os.path.join(projdir, output_dir))

    write_submit_lsi(
        codedir=codedir,
        projdir=projdir,
        submission_script=submission_script,
        submission_script_dir=submission_script_dir,
        template_file=args['template'],
        job_config=job_config,
        program=program,
        jobname=jobname,
        time=time,
        cluster_config=cluster_config,
        cluster=cluster,
        )

    cmd = 'sbatch ' + os.path.join(submission_script_dir, submission_script)
    jobid = subprocess.check_output(cmd, shell=True, cwd=projdir)
    jobid = jobid.decode("utf-8")
    jobid = str([int(s) for s in jobid.split() if s.isdigit()][0])

    with open(os.path.join(projdir, '%s_%s.log'%(args['program'], outname)), 'a+') as f:
        f.write('Job submitted. Job directory name is %s. Job ID is %s.\n' %(outname, jobid))
    querycmd = cluster_config[cluster]['querycmd']
    keyarg = cluster_config[cluster]['keyarg']

    return jobid, querycmd, keyarg, outname


def check_complete(jobid, querycmd, keyarg):
    ## Below: check every 2 seconds if the job has finished.
    state = check_state_lsi(querycmd, jobid, keyarg)
    start_time = time.time()
    interval = 2
    while state!='completed':
        time.sleep(interval)
        state = check_state_lsi(querycmd, jobid, keyarg)


def check_output_good(outname, **args):
    projdir = args['projdir']
    output_dir = os.path.join(args['output'], outname)
    # os.chdir(projdir)

    ## Below: check if the particle picking output is correct.
    with open(os.path.join(projdir, '%s_%s.log'%(args['program'], outname)), 'a+') as f:
        f.write('Job done. Checking outputs....\n')
    isgood = check_good(os.path.join(projdir, output_dir))
    with open(os.path.join(projdir, '%s_%s.log' %(args['program'], outname)), 'a+') as f:
        if isgood:
            f.write('3D classification for %s has finished.\n'%outname)
        else:
            f.write('Submission job %s is done but the output may not be right. Please check.\n'%outname)


if __name__ == '__main__':
    args = setupParserOptions()
    jobid, querycmd, keyarg, outname = submit(**args)
    check_complete(jobid, querycmd, keyarg)
    check_output_good(outname, **args)
