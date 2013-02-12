import tempfile
import subprocess
import json
import os


def arbor(title,json_graph):
  pwd = os.path.dirname(os.path.abspath(__file__))
  fh,fname = tempfile.mkstemp(suffix='.html',text=True)
  fh = os.fdopen(fh,'w')
  print >>fh, '<head><title>%s</title>' % title
  print >>fh, '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>'
  print >>fh, '<script src="%s"></script>'%os.path.join(pwd,'arbor.js')
  print >>fh, '<script> var graph =', json.dumps(json_graph), ';</script>'
  print >>fh, '<script src="%s"></script>'%os.path.join(pwd,'show_graph.js')
  print >>fh, '<style>body {background-color: #EEE;}</style>'
  print >>fh, '</head><body><h1>%s</h1><canvas id=viewport width=600 height=600></body>' % title
  fh.close()
  subprocess.check_call('open '+fname,shell=True)
