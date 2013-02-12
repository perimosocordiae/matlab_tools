#!/usr/bin/env python
import os
import re
from argparse import ArgumentParser

from search import search_patterns
from visualize import visualize


def parse_args():
  p = ArgumentParser()
  p.add_argument('project_root', type=str, help='the root of your Matlab project')
  p.add_argument('--grep', nargs='+', default=[], help='search for a (regex) pattern in all project files')
  p.add_argument('--defn', nargs='+', default=[], help='search for definitons in all project files')
  p.add_argument('--usage', nargs='+', default=[],help='search for usages in all project files')
  p.add_argument('--graph', nargs='*', default=None, help='generate a project dependency graph')
  p.add_argument('--pyplot', action='store_true', help='use pyplot for the project dependency graph')
  args = p.parse_args()
  if not (args.grep or args.defn or args.usage) and args.graph is None:
    p.error('None of the options specified, nothing to do.')
  if args.pyplot and not args.graph:
    p.error('--pyplot specified without --graph')
  return args


def find_files(rootdir):
  ff = {}
  for dirname,subdirs,files in os.walk(rootdir):
    # TODO: have a directory blacklist argument
    if '.svn' in subdirs:
      subdirs.remove('.svn')
    for f in files:
      # TODO: have a filename criteria argument
      if re.search('\.(m|c(pp)?|h(pp)?)$',f):
        ff[f.lower()] = os.path.join(dirname,f)
  return ff


if __name__ == '__main__':
  args = parse_args()
  files = find_files(args.project_root)
  search_patterns(files, args)
  if args.graph is not None:
    visualize(files, args)
