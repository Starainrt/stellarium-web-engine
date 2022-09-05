#!/usr/bin/python3

# Stellarium Web Engine - Copyright (c) 2022 - Stellarium Labs SRL
#
# This program is licensed under the terms of the GNU AGPL v3, or
# alternatively under a commercial licence.
#
# The terms of the AGPL v3 license can be found in the main directory of this
# repository.

import subprocess

# Get list of otypes directly from src/otypes.c
names = []
for line in open('src/otypes.c'):
    line = line.strip()
    if not line.startswith('T('): continue
    fields = line[2:].split(',')
    name = fields[4].strip()[1:-1]
    names.append(name)

names = '\n'.join('%s, %d' % (x, i) for i, x in enumerate(names))

input_file = \
'''
%struct-type
%readonly-tables
%global-table
%7bit
%includes
%define lookup-function-name otypes_in_word_set

%{
/*
 * This file was generated by:
 * mobile/tools/make-synonyms.py
 */

%}

struct otype_hash {
    const char *name;
    int index;
}

%%
#
# otypes list.
#
{names}
%%

static int otypes_hash_search(const char *str, int len)
{
    const struct otype_hash* s;
    s = otypes_in_word_set(str, len);
    return s ? s->index : -1;
}
'''

input_file = input_file.replace('{names}', names)

subprocess.call('gperf --output-file ./src/otypes.inl <<FILE_END\n' +
                input_file + '\nFILE_END', shell=True)
