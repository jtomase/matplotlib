"""
generate the rst files for the examples by iterating over the pylab examples
"""
import os, glob

import matplotlib.cbook as cbook


import os
import sys
fileList = []
rootdir = '../mpl_examples'

datad = {}
for root, subFolders, files in os.walk(rootdir):
    for fname in files:
        if ( fname.startswith('.') or fname.startswith('#') or fname.startswith('_') or
             fname.find('.svn')>=0 or not fname.endswith('.py') ):
            continue

        fullpath = os.path.join(root,fname)
        contents = file(fullpath).read()
        # indent
        relpath = os.path.split(root)[-1]
        datad.setdefault(relpath, []).append((fname, contents))

subdirs = datad.keys()
subdirs.sort()

fhindex = file('index.rst', 'w')
fhindex.write("""\
.. _examples-index:

####################
Matplotlib Examples
####################

.. htmlonly::

    :Release: |version|
    :Date: |today|

.. toctree::
    :maxdepth: 2

""")

for subdir in subdirs:
    if not os.path.exists(subdir):
        os.makedirs(subdir)
        
    static_dir = os.path.join('..', '_static', 'examples')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    static_dir = os.path.join(static_dir, subdir)
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)


    subdirIndexFile = os.path.join(subdir, 'index.rst')
    fhsubdirIndex = file(subdirIndexFile, 'w')
    fhindex.write('    %s\n'%subdirIndexFile)


    fhsubdirIndex.write("""\
.. _%s-examples-index:


##############################################
%s Examples
##############################################

.. htmlonly::

    :Release: |version|
    :Date: |today|

.. toctree::
    :maxdepth: 1

"""%(subdir, subdir))

    print subdir

    
    data = datad[subdir]
    data.sort()
    for fname, contents in data:

        static_file = os.path.join(static_dir, fname)
        fhstatic = file(static_file, 'w')
        fhstatic.write(contents)
        fhstatic.close()

        basename, ext = os.path.splitext(fname)
        rstfile = '%s.rst'%basename
        outfile = os.path.join(subdir, rstfile)
        fhsubdirIndex.write('    %s\n'%rstfile)
        fh = file(outfile, 'w')
        fh.write('.. _%s-%s:\n\n'%(subdir, basename))
        title = '%s example code: %s'%(subdir, fname)

        fh.write(title + '\n')
        fh.write('='*len(title) + '\n\n')
        

        print '    %s'%fname

        linkname = os.path.join('..', '..', '_static', 'examples', subdir, fname)
        fh.write('%s (`link to source <%s>`_)::\n\n'%(fname, linkname))

        # indent the contents
        contents = '\n'.join(['    %s'%row.rstrip() for row in contents.split('\n')])

        fh.write(contents)
        fh.write('\n\n')
        fh.close()

    fhsubdirIndex.close()

fhindex.close()
