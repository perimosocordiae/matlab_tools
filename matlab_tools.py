#!/usr/bin/env python
import os
import re
from argparse import ArgumentParser


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
  for dir,subdirs,files in os.walk(rootdir):
    if '.svn' in subdirs:
      subdirs.remove('.svn')
    for f in files:
      if re.search('\.(m|c(pp)?|h(pp)?)$',f):
        ff[f.lower()] = os.path.join(dir,f)
  return ff


def strip_matlab(line):
  # still doesn't get all the format strings right
  if '%' in line:
    ll = line[:line.find('%')]
    if 'printf' not in ll:
      return ll
  return line


def strip_c(line):
  if '//' in line:
    return line[:line.find('//')]
  if line.lstrip().startswith('*'):
    return ''
  return line


def strip_none(line):
  return line


def grep(pattern,file):
  if file.endswith('.m'):
    comment_strip = strip_matlab
  elif file.endswith('.cpp') or file.endswith('.c'):
    comment_strip = strip_c
  elif '.mex' in file:
    return
  else:
    comment_strip = strip_none
  with open(file) as fh:
    for i,line in enumerate(fh):
      if pattern.search(comment_strip(line)):
        yield i+1,line.strip()


def search_patterns(files,args):
  strip_root = lambda s: s[len(args.project_root):]
  patterns = {
    'grep': [re.compile(patt) for patt in args.grep],
    'defn': [re.compile('function\s.*?=?\s*%s\s*(\(|;|$)' % patt, re.I) for patt in args.defn],
   'usage': [re.compile('(\W|^)%s(\(|;|$)'%patt, re.I) for patt in args.usage],
  }

  for opt, patts in patterns.iteritems():
    for i,patt in enumerate(patts):
      print '>>',opt, 'for', getattr(args,opt)[i]
      for file in files.itervalues():
        for lineno,match in grep(patt,file):
          print "%s:%d: %s" % (strip_root(file),lineno,match)


def dependency_graph(defn_files,usage_files):
  usage_files.update(defn_files)  # just in case
  functions = find_all_defns(usage_files)
  usages = find_usages(functions,usage_files,set(defn_files.itervalues()))
  # usages is an adjacency matrix
  graph = nx.from_numpy_matrix(usages,create_using=nx.DiGraph())
  graph = nx.relabel_nodes(graph,dict(enumerate(usage_files.iterkeys())))
  disconnected_files = []
  for nodes in nx.connected_components(nx.Graph(graph)):
    if len(nodes) == 1:
      if len(defn_files) == len(usage_files):  # only in full case
        disconnected_files.append(nodes[0])
      continue
    yield graph.subgraph(nodes)
  if disconnected_files:
    print 'disconnected files: (may be dead code)'
    for f in disconnected_files:
      print ' ', f


def show_graphs_pyplot(graph_iter):
  for comp in graph_iter:
    pos = nx.shell_layout(comp)
    #pos = nx.spring_layout(comp)
    pyplot.figure()
    nx.draw(comp,pos)
    nx.draw_networkx_edge_labels(comp,pos,edge_labels=dict([((u,v),d['weight']) for u,v,d in comp.edges(data=True)]))
  pyplot.show()


def show_graphs_arbor(proj_root,graph_iter,roots):
  for i,comp in enumerate(graph_iter):
    g = {'title':'%s: CC %d'%(proj_root,i+1),'nodes':{},'edges':{}}
    for node in comp.nodes():
      g['nodes'][node] = {'label': node}
      if node in roots:
        g['nodes'][node]['color'] = 'yellow'
    for u,v,d in comp.edges(data=True):
      if u not in g['edges']:
        g['edges'][u] = {v: d['weight']}
      else:
        g['edges'][u][v] = d['weight']
    arbor(g['title'],g)


def find_all_defns(files):
  patt = re.compile('function\s.*?=?\s*(\w+)\s*(?:\(|;|$)', re.I)
  functions = {}
  for fpath in files.itervalues():
    for _,match in grep(patt,fpath):
      functions[patt.search(match).groups(1)] = fpath
      break  # only the first function counts
  return functions


def find_usages(functions, files, targets):
  adj = numpy.zeros((len(files),len(files)),dtype=int)
  path_inds = dict((p,i) for i,p in enumerate(files.itervalues()))
  for fn,fpath in functions.iteritems():
    i = path_inds[fpath]
    patt = re.compile('(\W|^)%s(\(|;|$)'%fn, re.I)
    for j,fpath2 in enumerate(files.itervalues()):
      if fpath not in targets and fpath2 not in targets:
        continue
      # edge (j,i) = n means i calls j n times
      adj[j,i] = sum(1 for _ in grep(patt,fpath2))
  return adj

if __name__ == '__main__':
  args = parse_args()
  files = find_files(args.project_root)
  search_patterns(files,args)
  if args.graph is not None:
    import numpy
    import networkx as nx
    defn_files = files if args.graph == [] else dict((os.path.basename(f).lower(),f) for f in args.graph)
    graphs = dependency_graph(defn_files,files)
    if args.pyplot:
      from matplotlib import pyplot
      show_graphs_pyplot(graphs)
    else:
      from arbor import arbor
      show_graphs_arbor(args.project_root,graphs,set(defn_files.iterkeys()))
