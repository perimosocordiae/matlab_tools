import tempfile
import subprocess
import json
import os,os.path

def arbor(title,json_graph):
  home = os.path.expanduser('~')
  fh,fname = tempfile.mkstemp(suffix='.html',text=True)
  fh = os.fdopen(fh,'w')
  print >>fh, '<head><title>%s</title>' % title
  print >>fh, '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>'
  print >>fh, '<script src="%s/Dropbox/pyutils/arbor.js"></script>'%home
  print >>fh, '<script> var graph =', json.dumps(json_graph), ';</script>'
  print >>fh, '<script src="%s/Dropbox/pyutils/show_graph.js"></script>'%home
  print >>fh, '</head><body><canvas id=viewport width=600 height=600></body>'
  fh.close()
  subprocess.check_call('open '+fname,shell=True)

