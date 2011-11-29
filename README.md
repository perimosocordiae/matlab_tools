=Matlab Tools=

A standalone utility for exploring a Matlab source directory.

Requirements:
 * Python 2.7  (uses argparse)
 * numpy, networkx, matplotlib (optional if --graph is not used)

Notes:
 * Only tested on Mac OSX. Minor modifications will probably be needed for compatibility with other platforms.
 * The arbor.js library is included, but the official source is here: https://github.com/samizdatco/arbor

Usage:
 * `./matlab_tools.py -h` shows help information
 * `./matlab_tools.py DIR --grep foo` searches for foo in files under DIR
 * `./matlab_tools.py DIR --usage foo` searches for usages of the function foo in files under DIR
 * `./matlab_tools.py DIR --defn foo` searches for definitions of the function foo in files under DIR
 * `./matlab_tools.py DIR --graph` displays a dependency graph for files under DIR
 * `./matlab_tools.py DIR --graph subdir` roots the dependency graph at files under subdir
 * `./matlab_tools.py DIR --pyplot --graph` displays a dependency graph using pyplot
   * the default viewer opens up a browser window