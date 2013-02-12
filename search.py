import re


def _strip_matlab(line):
  # still doesn't get all the format strings right
  if '%' in line:
    ll = line[:line.find('%')]
    if 'printf' not in ll:
      return ll
  return line


def _strip_c(line):
  if '//' in line:
    return line[:line.find('//')]
  if line.lstrip().startswith('*'):
    return ''
  return line


def grep(pattern, filename):
  if filename.endswith('.m'):
    comment_strip = _strip_matlab
  elif filename.endswith('.cpp') or filename.endswith('.c'):
    comment_strip = _strip_c
  else:
    # it's unlikely to get here, due to the way find_files works now
    comment_strip = lambda line: line
  with open(filename) as fh:
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
