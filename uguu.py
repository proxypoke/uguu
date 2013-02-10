#!/usr/bin/env python3
# uguu - generate Flexget config files.
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

import yaml
import argparse
import os


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


#def generate_config(uguu_conf_path, flexget_conf_path):
def generate_config(uguu_conf_path):
    '''Generate a flexget config from an uguu config.'''
    uguu_conf = read_config(uguu_conf_path)
    presets = generate_presets(uguu_conf)
    tasks = generate_tasks(uguu_conf)
    flexget_conf = {
        'presets': presets,
        'tasks': tasks,
    }
    return yaml.dump(flexget_conf)
    #write_config(flexget_conf, flexget_conf_path)


def main():
    parser = argparse.ArgumentParser(
        description="generate Flexget config files")

    parser.add_argument('uguu', type=str, metavar='uguu_config',
                        help='the uguu configuration file to read from')

    args = parser.parse_args()

    # check if the uguu config exists
    if not os.access(args.uguu, os.F_OK):
        print("Error: uguu config {0} does not exist.".format(args.uguu))
        exit(1)

    print(generate_config(args.uguu))
    exit(0)

if __name__ == "__main__":
    main()
