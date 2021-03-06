# uguu - generate flexget config files.
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/uguu
# (Shortlink: https://git.io/uguu)
#
# Format options for vim. Please adhere to them.
# vim: set et ts=4 sw=4 tw=80:

__version__ = "1.1.2"

import os
import subprocess
import tempfile
import yaml


def read_config(path):
    cfg = open(path, mode='r')
    return yaml.load(cfg)


def write_config(config, path):
    cfg_file = open(path, mode='w')
    yml = yaml.dump(config)
    cfg_file.write(yml)
    cfg_file.close()


def generate_presets(config):
    '''Generate the presets.'''
    opts = config.get('options')
    if opts is None:
        return
    presets = dict()
    glb = presets.setdefault('global', dict())
    _generate_global(glb, opts)
    return presets


def _generate_global(global_preset, opts):
    '''Generate the global part of the presets.'''
    regexp = dict()

    if 'reject' in opts:
        regexp['reject'] = opts['reject']
    if 'accept' in opts:
        regexp['accept'] = opts['accept']

    if len(regexp) > 0:
        global_preset['regexp'] = regexp

    set = dict()

    if 'path' in opts:
        set['path'] = opts['path']
    if 'movedone' in opts:
        set['movedone'] = opts['movedone']

    if len(set) > 0:
        global_preset['set'] = set
        # NOTE: 'download' is an implied setting.
        global_preset['download'] = True

    if 'deluge' in opts:
        global_preset['deluge'] = opts['deluge']

    return


def generate_tasks(config):
    '''Generate the tasks from the configured series.'''
    series = config.get('series')
    if series is None:
        raise KeyError('No series found. This is not a valid config.')
    tasks = dict()
    for s in series:
        tasks[s] = dict()
        _generate_task(s, tasks[s], series[s])
    return tasks


def _generate_task(name, task, series):
    task['rss'] = series['rss']
    if len(series) > 1:
        # there are more options than just the RSS feed
        options = dict(series.items())
        del options['rss']
        task['series'] = [{name: options}]
    else:
        task['series'] = [name]


def generate_config(uguu_conf):
    '''Generate a flexget config from an uguu config.'''
    presets = generate_presets(uguu_conf)
    tasks = generate_tasks(uguu_conf)
    flexget_conf = {
        'presets': presets,
        'tasks': tasks,
    }
    return flexget_conf


def check_flexget():
    '''Check if flexget is available.'''
    try:
        devnull = open(os.devnull)
        subprocess.Popen(
            ['flexget', '-h'], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def download_series(name, feed, path='.', movedone='.', output='deluge',
                    series_opts=None, output_opts=None):
    '''Download a series using a temporary flexget config.'''
    output_opts = {} if output_opts is None else output_opts
    series_opts = {} if series_opts is None else series_opts
    series_opts['rss'] = feed
    cfg = {
        'options': {
            'path': path,
            'movedone': movedone,
            output: output_opts,
        },
        'series': {
            name: series_opts,
        }
    }
    flexget_conf = generate_config(cfg)
    file_ = tempfile.NamedTemporaryFile(mode='w', delete=False)
    file_.write(yaml.dump(flexget_conf))
    file_.close()
    subprocess.Popen(['flexget', '-c', file_.name]).communicate()
