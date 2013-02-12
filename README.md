# Matlab Tools #

A standalone utility for exploring a Matlab source directory.

## Requirements ##
 * Python 2.7  (uses argparse)
 * Optional dependencies (required for the `--graph` option)
   * numpy, networkx, matplotlib

## Notes ##
 * Only tested on Mac OSX. Minor modifications will probably be needed for compatibility with other platforms.
 * The arbor.js library is included, but the official source is here: https://github.com/samizdatco/arbor

## Usage ##

### Searching
 * `./matlab_tools.py DIR --grep foo` searches for foo in files under DIR
 * `./matlab_tools.py DIR --usage foo` searches for usages of the function foo in files under DIR
 * `./matlab_tools.py DIR --defn foo` searches for definitions of the function foo in files under DIR

### Visualizing

*These options require the optional dependencies listed above.*

 * `./matlab_tools.py DIR --graph` displays a dependency graph for files under DIR
 * `./matlab_tools.py DIR --graph subdir` roots the dependency graph at files under subdir
 * `./matlab_tools.py DIR --pyplot --graph` displays the dependency graph using pyplot
   * the default viewer opens up a browser window
