DAX_SETTINGS_TEMPLATE="""; High level admin information. E.g. email address
[admin]
user_home={user_home}
admin_email={admin_email}
smtp_host={smtp_host}
smtp_from={smtp_from}
smtp_pass={smtp_pass}
xsitype_include={xsitype_include}

; Deep information about the cluster. This should include commands that are grid-specific to get job id, walltime usage etc. Additionally, there are several templates that needed to be specified. See readthedocs for a description
[cluster]
cmd_submit={cmd_submit}
prefix_jobid={prefix_jobid}
suffix_jobid={suffix_jobid}
cmd_count_nb_jobs={cmd_count_nb_jobs}
cmd_get_job_status={cmd_get_job_status}
queue_status={queue_status}
running_status={running_status}
complete_status={complete_status}
cmd_get_job_memory={cmd_get_job_memory}
cmd_get_job_walltime={cmd_get_job_walltime}
cmd_get_job_node={cmd_get_job_node}
job_extension_file={job_extension_file}
job_template={job_template}
email_opts={email_opts}
gateway={gateway}
root_job_dir={root_job_dir}
queue_limit={queue_limit}
results_dir={results_dir}
max_age={max_age}

; Information used to connect to REDCap databases if DAX_manager is used
[redcap]
api_url={api_url}
api_key_dax={api_key_dax}

; Keeping this outside of redcap so we dont have to add a prefix to all the variables
[dax_manager]
project={project}
settingsfile={settingsfile}
masimatlab={masimatlab}
tmp={tmp}
logsdir={logsdir}
user={user}
gateway={gateway}
email={email}
queue={queue}
priority={priority}
email_opts={email_opts}
dax_build_start_date={dax_build_start_date}
dax_build_end_date={dax_build_end_date}
dax_build_pid={dax_build_pid}
dax_update_tasks_start_date={dax_update_tasks_start_date}
dax_update_tasks_end_date={dax_update_tasks_end_date}
dax_update_tasks_pid={dax_update_tasks_pid}
dax_launch_start_date={dax_launch_start_date}
dax_launch_end_date={dax_launch_end_date}
dax_launch_pid={dax_launch_pid}
max_age={max_age}
admin_email={admin_email}
"""

import os
import sys
import socket

class DAX_Setup_Handler(object):

    def __init__(self):
        dax_settings_file = os.path.join(os.path.expanduser('~'), '.dax_settings.ini')
        if os.path.isfile(dax_settings_file):
            sys.stdout.write('~/.dax_settings.ini exists. Exiting')
            sys.exit(1)

        self.settings_file = dax_settings_file

        # This will map the key value pairs in the string template
        self.settings_dict = dict()

        # If using DAX Manager, users can use defaults
        self.use_redcap_defaults = False

    @staticmethod
    def _prompt(message, default=None):
        """
        Method to prompt a user for an input for each key in the template.

        :param message: A string that prompts the user for input
        :param default: Default value for value (if desired)
        :return: String of the input

        """
        if default:
            stdin = raw_input("%s default<%s> [Y/n] " % (message, default))
            if stdin.lower() == 'n':
                return stdin
            else:
                return default
        else:
            stdin = raw_input(message)
            return stdin

    def _set(self, key, value):
        """
        Update the dictionary with the key/value pair for the template
        :param key: String key name in the template
        :param value: String value associated with the key
        :return: None
        """

        self.settings_dict.__setitem__(key, value)

    def _set_null(self, key):
        """
        Update the dictionary with the value of '' for the key
        :param key: String key name in the template
        :return: None
        """

        self.settings_dict.__setitem__(key, '')

    def _get_user_home(self):
        """
        Get the default user home directory. If the user wants a different one,
         prompt for it

        :return: None

        """
        default = os.path.expanduser('~')
        value = self._prompt("Please enter your home directory", default)
        self._set('user_home', value)

    def _get_admin_email(self):
        """
        Prompt the user for the admin email address

        :return: None

        """
        value = self._prompt("Please enter email address for admin. "
                             "All emails will get sent here ")
        self._set('admin_email', value)

    def _get_smtp_from(self):
        """
        Prompt the user email address where emails should come from

        :return: String of the smtp_from value, None if emtpy

        """
        value = self._prompt("Please enter an email address where emails"
                             " should be sent from ")
        self._set('smtp_from', value)

    def _get_smtp_host(self):
        """
        Prompt the user for the smtp_host if smtp_from is not null

        :return: None

        """
        if self.settings_dict['smtp_from'] != '':
            value = self._prompt("Please enter the SMTP host associated with email"
                                 " address %s " % self.settings_dict['smtp_from'])
            self._set('smtp_host', value)
        else:
            self._set_null('smtp_host')

    def _get_smtp_pass(self):
        """
        Prompt the user for the password associated with the email if
         smtp_from is set

        :return: None

        """
        if self.settings_dict['smtp_from'] != '':
            value = self._prompt("Please enter the password associated with email"
                                 " address %s " % self.settings_dict['smtp_from'])
            self._set('smtp_pass', value)
        else:
            self._set_null('smtp_pass')

    def _get_xsitype_include(self):
        """
        Prompt the user for the xsitypes for DAX to access in the project

        :return: None

        """
        if self.settings_dict['xsitype_include'] != '':
            value = self._prompt("Please enter the xsitypes you would like DAX"
                                 " to access in your XNAT instance")
            self._set('xsitype_include', value)
        else:
            self._set_null('xsitype_include')

    # Begin cluster section
    def _get_cmd_submit(self):
        """
        Prompt the user for the command to submit a job to the grid

        :return: None

        """
        value = self._prompt("What command is used to submit your batch file? [e.g., qsub, sbatch] ")
        self._set('cmd_submit', value)

    def _get_prefix_jobid(self):
        """
        Prompt the user for a string to let them know the job was submitted before printing the job ID

        :return: None

        """
        value = self._prompt("Please enter a string to print before the job id after submission", 'Submitted batch job')
        self._set('prefix_jobid', value)

    def _get_suffix_jobid(self):
        """
        Prompt the user for the suffix of the job submission string

        :return: None

        """
        value = self._prompt("Please enter a string to print after the job id after submission", '\\n')
        self._set('suffix_jobid', value)

    def _get_cmd_count_nb_jobs(self):
        """
        Prompt the user for the path to where the template file is for the
         command to count the number of jobs

        :return: None

        """
        value = self._prompt("Please enter the full path to text file"
                             " containing the command used to count the number"
                             " of jobs in the queue ")
        self._set('cmd_count_nb_jobs', value)

    def _get_cmd_get_job_status(self):
        """
        Prompt the user for the path to where the tempalte file is for the
         command to get the status of a job by job id

        :return: None

        """
        value = self._prompt("Please enter the full path to text file"
                             " containing the command used to check the running"
                             " status of a job ")
        self._set('cmd_get_job_status', value)

    def _get_queue_status(self):
        """
        Prompt the user for the path to where the template file is for the
         command to see if a job failed

        :return: None

        """
        value = self._prompt("Please enter the full path to the text file"
                             " containing the string that will be printed"
                             " if the job ID failed to submit ")
        self._set('queue_status', value)

    def _get_running_status(self):
        """
        Prompt the user for the string indicating the running status of a job
         (Running/R etc)

        :return: None

        """
        value = self._prompt("Please enter the string the job scheduler would "
                             "use to indicate that a job is 'running' ")
        self._set('running_status', value)

    def _get_complete_status(self):
        """
        Prompt the user for the string indicating the running status of a job
         (Complete/C etc)

        :return: None

        """
        value = self._prompt("Please enter the string the job scheduler would "
                             "use to indicate that a job is 'complete' ")
        self._set('complete_status', value)

    def _get_cmd_get_job_memory(self):
        """
        Prompt the user for the full path to the file containing the command
         used to see how much memory a job used

        :return: None

        """
        value = self._prompt("Please enter the full path to the text file"
                             " containing the command used to see how munch"
                             " memory a job used ")
        self._set('cmd_get_job_memory', value)

    def _get_cmd_get_job_walltime(self):
        """
        Prompt the user for the full path to the file containing the command
         used to see how much walltime a job used

        :return: None

        """
        value = self._prompt("Please enter the full path to the text file"
                             " containing the command used to see how munch"
                             " walltime a job used ")
        self._set('cmd_get_job_walltime', value)

    def _get_cmd_get_job_node(self):
        """
        Prompt the user for the full path to the file containing the command
         used to see what node a job used

        :return: None

        """
        value = self._prompt("Please enter the full path to the text file"
                             " containing the command used to see which node"
                             " a job used. ")
        self._set('cmd_get_job_node', value)

    def _get_job_extension_file(self):
        """
        Prompt the user for a job file extension (.pbs, .slurm etc)

        :return: None

        """
        value = self._prompt("Please enter an extension for the job batch file", '.pbs')
        self._set('job_extension_file', value)

    def _get_job_template(self):
        """
        Prompt the user for the full path to the file containing the template
         used to generate the batch file

        :return: None

        """
        value = self._prompt("Please enter the full path to the text file"
                             " containing the template used to generate the"
                             " batch script. ")
        self._set('job_template', value)

    def _get_email_opts(self):
        """
        Prompt the user for when they want to be notified about a job

        :return: None

        """
        value = self._prompt("Please enter when you want to be notified about"
                             " a job as defined by your grid scheduler. ")
        self._set('email_opts', value)

    def _get_gateway(self):
        """
        Prompt the user for the hostname of the server to run on

        :return: None

        """
        default = socket.gethostname()
        value = self._prompt("Please enter when you want to be notified about"
                             " a job as defined by your grid scheduler. ", default)
        self._set('gateway', value)

    def _get_root_job_dir(self):
        """
        Prompt the user for the directory where the data should be stored on the node

        :return: None

        """
        value = self._prompt("Please enter where the data should be stored on the node", '/tmp')
        self._set('root_job_dir', value)

    def _get_queue_limit(self):
        """
        Prompt the user for the maximum number of jobs that should run at a time

        :return: None

        """
        value = self._prompt("Please enter the maximum number of jobs that should run at once", '600')
        self._set('queue_limit', value)

    def _get_results_dir(self):
        """
        Prompt the user where the data should get uploaded to when done

        :return: None

        """
        default = os.path.join(os.path.expanduser('~'), 'RESULTS_XNAT_SPIDER')
        value = self._prompt("Please enter directory where data will get copied to for upload ", default)
        self._set('results_dir', value)

    def _get_max_age(self):
        """
        Prompt the user for the number of days dax should ignore the session before re-running dax_build

        :return: None

        """
        value = self._prompt("Please max days before re-running dax_build on a session", '7')
        self._set('max_age', value)

    # redcap section
    def _get_api_url(self):
        """
        Prompt user for the REDCap API URL

        :return: None

        """
        value = self._prompt("Please enter your REDCap API URL ")
        self._set('api_url', value)

    def _get_api_key_dax(self):
        """
        Prompt the user to enter an API key to connect to REDCap for DAX Manager

        :return: None

        """
        value = self._prompt("Please enter the key to connect to the DAX Manager REDCap database ")
        self._set('api_key_dax', value)

    def _get_dax_manager_dict(self):
        """
        Set the variables for DAX_manager to be defaults to try to keep debugging easier.
        :return: None
        """
        if self.settings_dict['api_key_dax'] != '':
            self._set('project','dax_project')
            self._set('settingsfile','dax_settings_full_path')
            self._set('masimatlab','dax_masimatlab')
            self._set('tmp','dax_tmp_directory')
            self._set('logsdir','dax_logs_path')
            self._set('user','dax_cluster_user')
            self._set('gateway','dax_gateway')
            self._set('email','dax_cluster_email')
            self._set('queue','dax_queue_limit')
            self._set('priority','dax_proj_order')
            self._set('email_opts','dax_job_email_options')
            self._set('dax_build_start_date','dax_build_start_date')
            self._set('dax_build_end_date','dax_build_end_date')
            self._set('dax_build_pid','dax_build_pid')
            self._set('dax_update_tasks_start_date','dax_update_tasks_start_date')
            self._set('dax_update_tasks_end_date','dax_update_tasks_end_date')
            self._set('dax_update_tasks_pid','dax_update_tasks_pid')
            self._set('dax_launch_start_date','dax_launch_start_date')
            self._set('dax_launch_end_date','dax_launch_end_date')
            self._set('dax_launch_pid','dax_launch_pid')
            self._set('max_age','dax_max_age')
            self._set('admin_email','dax_email_address')
        else:
            self._set_null('project')
            self._set_null('settingsfile')
            self._set_null('masimatlab')
            self._set_null('tmp')
            self._set_null('logsdir')
            self._set_null('user')
            self._set_null('gateway')
            self._set_null('email')
            self._set_null('queue')
            self._set_null('priority')
            self._set_null('email_opts')
            self._set_null('dax_build_start_date')
            self._set_null('dax_build_end_date')
            self._set_null('dax_build_pid')
            self._set_null('dax_update_tasks_start_date')
            self._set_null('dax_update_tasks_end_date')
            self._set_null('dax_update_tasks_pid')
            self._set_null('dax_launch_start_date')
            self._set_null('dax_launch_end_date')
            self._set_null('dax_launch_pid')
            self._set_null('max_age')
            self._set_null('admin_email')

    def write(self):
        """
        Write the all of the config options to the ~/.dax_settings.ini file
                :return: None

        """
        with open(self.settings_file, 'w') as fid:
            fid.writelines(DAX_SETTINGS_TEMPLATE.format(**self.settings_dict))

    def config(self):
        """
        Caller for all of the _get* methods
        :return: None

        """
        self._get_user_home()
        self._get_admin_email()
        self._get_smtp_from()
        self._get_smtp_host()
        self._get_smtp_pass()
        self._get_cmd_submit()
        self._get_prefix_jobid()
        self._get_suffix_jobid()
        self._get_cmd_count_nb_jobs()
        self._get_cmd_get_job_status()
        self._get_queue_status()
        self._get_running_status()
        self._get_complete_status()
        self._get_cmd_get_job_memory()
        self._get_cmd_get_job_walltime()
        self._get_cmd_get_job_node()
        self._get_job_extension_file()
        self._get_job_template()
        self._get_email_opts()
        self._get_gateway()
        self._get_root_job_dir()
        self._get_queue_limit()
        self._get_results_dir()
        self._get_max_age()
        self._get_api_url()
        self._get_api_key_dax()
        self._get_dax_manager_dict()
