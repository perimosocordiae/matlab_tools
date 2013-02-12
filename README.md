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

For a regex search term `foo`, i.e. `\beigs?\b`:

 * Search for `foo` in files under `DIR`
    ./matlab_tools.py DIR --grep foo
 * Search for usages of the function `foo` in files under `DIR`
    ./matlab_tools.py DIR --usage foo
 * Search for definitions of the function `foo` in files under `DIR`
    ./matlab_tools.py DIR --defn foo

### Visualizing

*These options require the optional dependencies listed above.*

 * Display a dependency graph for files under `DIR` in the default browser
    ./matlab_tools.py DIR --graph
 * Root the dependency graph at files under `subdir`
    ./matlab_tools.py DIR --graph subdir
 * Display the dependency graph using a native pyplot window
    ./matlab_tools.py DIR --pyplot --graph
