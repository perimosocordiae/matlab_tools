import networkx as nx
import numpy
import re
import os

from arbor import arbor
from search import grep


def visualize(files, args):
  defn_files = files if args.graph == [] else dict((os.path.basename(f).lower(),f) for f in args.graph)
  graphs = dependency_graph(defn_files,files)
  if args.pyplot:
    show_graphs_pyplot(graphs)
  else:
    show_graphs_arbor(args.project_root,graphs,set(defn_files.iterkeys()))


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


def show_graphs_pyplot(graph_iter):
  from matplotlib import pyplot
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
