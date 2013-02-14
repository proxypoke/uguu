#!/usr/bin/env python3
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

import os
import yaml
import uguu

uguu_conf_path = "./uguu_conf.yml"
flexget_conf_path = "./flexget_conf.yml"

if not os.access(uguu_conf_path, os.F_OK):
    print("uguu test config not found.")
    exit(1)
if not os.access(flexget_conf_path, os.F_OK):
    print("Flexget test config not found.")
    exit(1)

flexget_conf = yaml.load(open(flexget_conf_path))

uguu_conf = uguu.read_config(uguu_conf_path)
generated_conf = uguu.generate_config(uguu_conf)

if not flexget_conf == generated_conf:
    print("Generated and expected configs do not match.")
    print("=============== [ EXPECTED ] ===============")
    print(yaml.dump(flexget_conf))
    print("=============== [ GENERATED ] ==============")
    print(yaml.dump(generated_conf))
    exit(1)
else:
    print("Generated and expected config match. Success.")
