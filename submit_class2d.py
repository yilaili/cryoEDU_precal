#!/usr/bin/env python3
import json
import argparse
import os
import sys
import subprocess
import time
import shutil
import re

from lib.check_if_done import check_state_lsi
from lib.write_submit_script_lsi import write_submit_lsi

'''
Submit relion 2D classification job.
Inputs: 1. Path of the *particles.star file from particle extraction,
        2. Name of the 2D classification directory,
        3. Diameter of the mask,
        4. Number of classes,
        5. tau2_fudge,
        6. Whether to do ctf (default is False),
        7. Whether to ignore ctf until first peak (default is False),
        8. zero_mask (default is False).
Output: 2D classification results, saved in the output directory.
'''

def setupParserOptions():
    ap = argparse.ArgumentParser()
    ## General inputs
    ap.add_argument('-i', '--input',
                    help="Provide star file of the ctf corrected micrographs.")
    ap.add_argument('-o','--output', default='Class2D',
                    help="Name of the directory where the outputs of 2d classification are stored.")
    ap.add_argument('-p', '--program', default='relion_Class2D',
                    help='The program to use to do particle extraction. Currently only supports relion_class2d.')
    ## Program specific parameters
    ap.add_argument('-d', '--diameter',
                    help="Diameter of the particle to be used in 2D classification (in Angstrom).")
    ap.add_argument('-K', '--numclass',
                    help="Number of classes to be used in 2D classification. Default is 200 (the max allowed).")
    ap.add_argument('--tau2_fudge',
                    help="Regularisation parameter (values higher than 1 give more weight to the data).")
    ap.add_argument('--ctf', action='store_true',
                    help="Whether to do ctf correction. Default is FALSE.")
    ap.add_argument('--ctf_intact_first_peak', action='store_true',
                    help="Whether to ignore ctf until first peak. Default is FALSE.")
    ap.add_argument('--zero_mask', action='store_true',
                    help="Mask surrounding background in particles to zero. Default is FALSE.")
    ## Cluster submission needed
    ap.add_argument('--template', default='config/lsi_submit_template.sh',
                    help="Name of the submission template.")
    ap.add_argument('--cluster', default='lsi',
                    help='The computer cluster the job will run on.')
    ap.add_argument('--jobname', default='Class2D',
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


def editparameters(
    s, input, output,
    diameter, numclass, tau2_fudge, threads,
    ctf, ctf_intact_first_peak, zero_mask):

    if not ctf:
        assert not ctf_intact_first_peak

    new_s = s.replace('$$input', input)\
            .replace('$$output', output)\
            .replace('$$diameter', diameter)\
            .replace('$$numclass', numclass)\
            .replace('$$tau2_fudge', tau2_fudge)\
            .replace('$$j', threads)

    if ctf:
        new_s += '--ctf '
    if ctf_intact_first_peak:
        new_s += '--ctf_intact_first_peak '
    if zero_mask:
        new_s += '--zero_mask '

    return new_s


def check_good(class_dir):
    '''
    Currently only supports relion 2D classification.
    Check if 'run_it025_model.star' file exists.
    '''
    return os.path.isfile(os.path.join(class_dir, 'run_it025_model.star'))


def outdir_naming(**args):
    ## Output directory naming
    ctf = 1 if args['ctf'] else 0
    ctf_intact_first_peak = 1 if args['ctf_intact_first_peak'] else 0
    zero_mask = 1 if args['zero_mask'] else 0
    params = [
        ('diam-{:s}', args['diameter']),
        ('K-{:s}', args['numclass']),
        ('tau2-{:s}', args['tau2_fudge']),
        ('ctf-{:01d}', ctf),
        ('ign1p-{:01d}', ctf_intact_first_peak),
        ('zerom-{:01d}', zero_mask)]
    specs = '_'.join([t.format(v) for (t, v) in params])

    return specs


def submit(**args):

    cluster = args['cluster']
    codedir = os.path.abspath(os.path.join(os.path.realpath(sys.argv[0]), os.pardir))
    wkdir = os.path.abspath(os.path.join(os.path.dirname(args['input']), os.pardir))
    cluster_config_file = 'config/cluster_config.json'
    job_config_file = 'config/config_class2d.json'

    ## mkdir to setup the job
    os.chdir(wkdir)
    try:
        os.mkdir(args['output'])
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
    threads = job_config['general']['threads']
    # threads = args['threads']

    specs = outdir_naming(**args)
    submission_script = 'submit_%s_%s.sh' %(args['program'], specs)
    input = args['input']
    output_dir = os.path.join(args['output'], specs)
    output = '%s/run '%output_dir

    parameters = editparameters(job_config[program]['parameters'],
                                input, output,
                                args['diameter'], args['numclass'], args['tau2_fudge'], threads,
                                args['ctf'], args['ctf_intact_first_peak'], args['zero_mask'])

    write_submit_lsi(
        codedir=codedir,
        wkdir=wkdir,
        submission_script=submission_script,
        template_file=args['template'],
        job_config_file=job_config_file,
        program=program,
        mpinodes=mpinodes,
        # threads=threads,
        parameters=parameters,
        jobname=jobname,
        time=time,
        cluster_config_file=cluster_config_file,
        cluster=cluster,
        )

    os.chdir(wkdir)
    try:
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    except OSError:
        os.mkdir(output_dir) # make "specs" directory under the output directory

    cmd = 'sbatch ' + submission_script
    jobid = subprocess.check_output(cmd, shell=True)
    jobid = jobid.decode("utf-8")
    jobid = str(int(job_id))

    with open('%s_%s.log' %(args['program'], specs), 'a+') as f:
        f.write('Job submitted. Parameters is %s. Job ID is %s.\n' %(specs, jobid))
    querycmd = cluster_config[cluster]['querycmd']
    keyarg = cluster_config[cluster]['keyarg']

    return jobid, querycmd, keyarg


def check_complete(jobid, querycmd, keyarg):
    ## Below: check every 2 seconds if the job has finished.
    state = check_state_lsi(querycmd, jobid, keyarg)
    start_time = time.time()
    interval = 2
    while state!='completed':
        time.sleep(interval)
        state = check_state_lsi(querycmd, jobid, keyarg)


def check_output_good(**args):
    wkdir = os.path.abspath(os.path.join(os.path.dirname(args['input']), os.pardir))
    os.chdir(wkdir)

    specs = outdir_naming(**args)
    output_dir = os.path.join(args['output'], specs)

    ## Below: check if the particle picking output is correct.
    with open('%s_%s.log' %(args['program'], specs), 'a+') as f:
        f.write('Checking outputs....\n')
    isgood = check_good(output_dir)
    with open('%s_%s.log' %(args['program'], specs), 'a+') as f:
        if isgood:
            f.write('2D classification for %s has finished.\n'%specs)
        else:
            f.write('Submission job %s is done but the output may not be right. Please check.\n'%specs)


if __name__ == '__main__':
    args = setupParserOptions()
    jobid, querycmd, keyarg = submit(**args)
    check_complete(jobid, querycmd, keyarg)
    check_output_good(**args)
