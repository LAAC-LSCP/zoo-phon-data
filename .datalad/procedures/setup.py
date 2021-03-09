#!/usr/bin/env python3

import sys
import os

import datalad.api
from datalad.distribution.dataset import require_dataset

ds = require_dataset(
    sys.argv[1],
    check_installed=True,
    purpose = 'configuration'
)

url = open(os.path.join(sys.argv[1], '.datalad/path')).read().strip()
if len(sys.argv) > 2:
    url = "{}:{}".format(sys.argv[2], url)

datalad.api.siblings(
    dataset = ds,
    action = 'configure',
    name = 'cluster',
    annex_wanted = 'include=*',
    annex_required = 'include=*',
    url = url
)

datalad.api.siblings(
    dataset = ds,
    action = 'configure',
    name = 'origin',
    publish_depends = 'cluster'
)