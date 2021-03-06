"""
This is a matlab style functional interface the matplotlib.

The following matlab compatible commands are provided by

   >>> from matplotlib.matlab import *

Plotting commands

  axes     - Create a new axes
  axis     - Set or return the current axis limits
  bar      - make a bar chart
  cla      - clear current axes
  clf      - clear a figure window
  close    - close a figure window
  cohere   - make a plot of coherence
  csd      - make a plot of cross spectral density
  errorbar - make an errorbar graph
  figure   - create or change active figure
  gca      - return the current axes
  gcf      - return the current figure
  get      - get a handle graphics property
  hist     - make a histogram
  loglog   - a log log plot
  pcolor   - make a pseudocolor plot
  plot     - make a line plot
  psd      - make a plot of power spectral density
  savefig  - save the current figure
  scatter  - make a scatter plot
  set      - set a handle graphics property
  semilogx - log x axis
  semilogy - log y axis
  show     - show the figures
  subplot  - make a subplot (numrows, numcols, axesnum)
  text     - add some text at location x,y to the current axes
  title    - add a title to the current axes
  xlabel   - add an xlabel to the current axes
  ylabel   - add a ylabel to the current axes

Matrix commands

  cumprod   - the cumulative product along a dimension
  cumsum    - the cumulative sum along a dimension
  detrend   - remove the mean or besdt fit line from an array
  diag      - the k-th diagonal of matrix 
  diff      - the n-th differnce of an array
  eig       - the eigenvalues and eigen vectors of v
  eye       - a matrix where the k-th diagonal is ones, else zero 
  find      - return the indices where a condition is nonzero  
  fliplr    - flip the rows of a matrix up/down
  flipud    - flip the columns of a matrix left/right
  linspace  - a linear spaced vector of N values from min to max inclusive
  ones      - an array of ones
  rand      - an array from the uniform distribution [0,1]
  randn     - an array from the normal distribution
  rot90     - rotate matrix k*90 degress counterclockwise
  squeeze   - squeeze an array removing any dimensions of length 1
  tri       - a triangular matrix
  tril      - a lower triangular matrix
  triu      - an upper triangular matrix
  vander    - the Vandermonde matrix of vector x
  svd       - singular value decomposition
  zeros     - a matrix of zeros
  
Probability

  levypdf   - The levy probability density function from the char. func.
  normpdf   - The Gaussian probability density function
  rand      - random numbers from the uniform distribution
  randn     - random numbers from the normal distribution

Statistics

  corrcoef  - correlation coefficient
  cov       - covariance matrix
  max       - the maximum along dimension m
  mean      - the mean along dimension m
  median    - the median along dimension m
  min       - the minimum along dimension m
  norm      - the norm of vector x
  prod      - the product along dimension m
  ptp       - the max-min along dimension m
  std       - the standard deviation along dimension m
  sum       - the sum along dimension m

Time series analysis

  bartlett  - M-point Bartlett window
  blackman  - M-point Blackman window
  cohere    - the coherence using average periodiogram
  csd       - the cross spectral density using average periodiogram
  fft       - the fast Fourier transform of vector x
  hamming   - M-point Hamming window
  hanning   - M-point Hanning window
  hist      - compute the histogram of x
  kaiser    - M length Kaiser window
  psd       - the power spectral density using average periodiogram
  sinc      - the sinc function of array x

Other

  angle     - the angle of a complex array
  polyfit   - fit x, y to an n-th order polynomial
  polyval   - evaluate an n-th order polynomial
  roots     - the roots of the polynomial coefficients in p
  trapz     - trapezoidal integration


Credits: The plotting commands were provided by
John D. Hunter <jdhunter@ace.bsd.uhicago.edu>

Most of the other commands are from the Numeric, MLab and FFT, with
the exception of those in mlab.py provided by matplotlib.
"""

__version__  = '0.63.0'
__revision__ = '$Revision$'
__date__     = '$Date$'

import sys, os
import distutils.sysconfig

def warn(s):
    'issue a warning'
    print >> sys.stderr, s


"""
Manage user customizations through a rc file.

The default file location is given in the following order

  - environment variable MATPLOTLIBRC

  - HOME/.matplotlibrc if HOME is defined

  - PATH/.matplotlibrc where PATH is the return value of
    get_data_path()
"""

import sys, os

major, minor1, minor2, s, tmp = sys.version_info
if major<2 or (major==2 and minor1<3):
    True = 1
    False = 0
else:
    True = True
    False = False



def get_home():
    """
    return the users HOME dir across platforms or None.
    
    On win32, if either HOME is not set or HOME is set but doesn't
    exist, the value of USERPROFILE will be used instead.
    """

    if os.environ.has_key('HOME'):
        path = os.environ['HOME']
        if os.path.exists(path): return path

    if sys.platform=='win32' and os.environ.has_key('USERPROFILE'):
        path = os.environ['USERPROFILE']
        if os.path.exists(path): return path

    return None

def get_data_path():

    path = os.path.join(distutils.sysconfig.PREFIX, 'share', 'matplotlib')
    if os.path.isdir(path): return path

    path = os.path.join(os.sep.join(__file__.split(os.sep)[:-1]), 
                        'share','matplotlib')
    if os.path.isdir(path): return path

    path = os.path.join(os.sep.join(__file__.split(os.sep)[:-5]), 
                        'share','matplotlib')
    if os.path.isdir(path): return path

    if os.environ.has_key('MATPLOTLIBDATA'):
        path = os.environ['MATPLOTLIBDATA']
        if os.path.isdir(path): return path

	
    # CODE ADDED TO SUPPORT PY2EXE - you will need to copy
    # C:\Python23\share\matplotlib into your dist dir.  See
    # http://starship.python.net/crew/theller/moin.cgi/MatPlotLib
    # for more info
    if sys.platform=='win32' and sys.frozen:
        path = os.path.join(os.path.split(sys.path[0])[0], 'matplotlibdata')
        return path
    raise RuntimeError('Could not find the matplotlib data files')


def validate_path_exists(s):
    'If s is a path, return s, else False'
    if os.path.exists(s): return s
    else:
        raise RuntimeError('"%s" should be a path but it does not exist'%s)

def validate_bool(b):
    'Convert b to a boolean or raise'
    bl = b.lower()
    if bl in ('f', 'no', 'false', '0', 0): return False
    elif bl in ('t', 'yes', 'true', '1', 1): return True
    else:
        raise ValueError('Could not convert "%s" to boolean' % b)

def validate_float(s):
    'convert s to float or raise'
    try: return float(s)
    except ValueError:
        raise ValueError('Could not convert "%s" to float' % s)

def validate_int(s):
    'convert s to float or raise'
    try: return int(s)
    except ValueError:
        raise ValueError('Could not convert "%s" to int' % s)
        
def validate_numerix(s):
    'return "Numeric" or "Numarray" or raise'
    sl = s.lower()
    if sl=='numeric': return 'Numeric'
    elif sl=='numarray': return 'numarray'
    else:
        raise ValueError('Numerix must be Numeric or numarray')

def validate_toolbar(s):
    """
    return toolbar string 'None', 'classic', 'toolbar2'
    """
    s = s.lower()
    if s=='none': return 'None'
    elif s=='classic': return s
    elif s=='toolbar2': return s    
    else:
        raise ValueError('toolbar must be None | classic | toolbar2')

class validate_nseq_float:
    def __init__(self, n):
        self.n = n
    def __call__(self, s):
        'return a seq of n floats or raise'
        ss = s.split(',')
        if len(ss) != self.n:
            raise ValueError('You must use exactly %d comma separated values'%self.n)
        try: return [float(val) for val in ss]
        except ValueError:
            raise ValueError('Could not convert all entries to floats')

def validate_color(s):
    'return a valid color arg'
    if s.lower() == 'none': return 'None'
    if len(s)==1 and s.isalpha(): return s
    if s.find(',')>=0: # looks like an rgb
        # get rid of grouping symbols
        s = ''.join([ c for c in s if c.isdigit() or c=='.' or c==','])
        vals = s.split(',')
        if len(vals)!=3:
            raise ValueError('Color tuples must be length 3')
        
        try: return [float(val) for val in vals]
        except ValueError:
            raise ValueError('Could not convert all entries "%s" to floats'%s)

    if s.replace('.', '').isdigit(): # looks like scalar
        try: return float(s)
        except ValueError:
            raise ValueError('Could not convert "%s" to float' % s)
        
    if len(s)==6 and s.isalnum: # looks like hex
        return '#' + s

    raise ValueError('"s" does not look like color arg')

def validate_comma_sep_str(s):
    'return a list'
    ss = s.split(',')
    try:
        return [val.strip() for val in ss]
    except ValueError:
        raise ValueError('Could not convert all entries to strings')

def validate_orientation(s):
    if s.lower() in ['landscape', 'portrait']:
        return True
    else:
        raise ValueError('orientation must be one of: portrait, landscape')

def validate_fontsize(s):
    if s.lower() in ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large',
             'xx-large', 'smaller', 'larger']:
        return s.lower()
    try:
        return float(s)
    except ValueError:
        raise ValueError('not a valid font size')


# a map from key -> value, converter
defaultParams = {
    'backend'           : ['GTK', str],
    'numerix'           : ['Numeric', validate_numerix],
    'toolbar'           : ['classic', validate_toolbar],
    'datapath'          : [get_data_path(), validate_path_exists],
    'interactive'       : [False, validate_bool],
    'timezone'          : ['UTC', str],    

    # line props    
    'lines.linewidth'   : [0.5, validate_float],     # line width in points
    'lines.linestyle'   : ['-', str],                # solid line
    'lines.color'       : ['b', validate_color],     # blue
    'lines.marker'       : ['None', str],     # black
    'lines.markeredgecolor'       : ['k', validate_color],     # black
    'lines.markerfacecolor'       : ['b', validate_color],     # blue
    'lines.markeredgewidth'       : [0.5, validate_float],     
    'lines.markersize'  : [6, validate_float],       # markersize, in points
    'lines.antialiased' : [True, validate_bool],     # antialised (no jaggies)
    'lines.data_clipping' : [False, validate_bool],  # clip data

    # patch props    
    'patch.linewidth'   : [0.5, validate_float], # line width in points
    'patch.edgecolor'   : ['k', validate_color], # black
    'patch.facecolor'   : ['b', validate_color], # blue
    'patch.antialiased' : [True, validate_bool], # antialised (no jaggies)


    # font props
    'font.family'       : ['serif', str],            # used by text object
    'font.style'        : ['normal', str],           #
    'font.variant'      : ['normal', str],           #
    'font.stretch'      : ['normal', str],           # 
    'font.weight'       : ['normal', str],           #
    'font.size'         : ['medium', validate_fontsize], #
    'font.serif'        : ['serif', validate_comma_sep_str],
    'font.sans-serif'   : ['sans-serif', validate_comma_sep_str],
    'font.cursive'      : ['cursive', validate_comma_sep_str],
    'font.fantasy'      : ['fantasy', validate_comma_sep_str],
    'font.monospace'    : ['monospace', validate_comma_sep_str],

    # text props
    'text.color'        : ['k', validate_color],     # black
    'text.fontstyle'    : ['normal', str],
    'text.fontangle'    : ['normal', str],
    'text.fontvariant'  : ['normal', str],
    'text.fontweight'   : ['normal', str],
    'text.fontsize'     : ['medium', validate_fontsize],


    'image.aspect' : ['free', str],  # free| preserve
    'image.interpolation'  : ['bilinear', str], 
    'image.cmap'   : ['gray', str],        # one of gray, jet
    'image.lut'    : [256, validate_int],  # lookup table
    'image.origin'    : ['upper', str],  # lookup table    

    # axes props
    'axes.hold'         : [True, validate_bool],    # background color; white    
    'axes.facecolor'    : ['w', validate_color],    # background color; white
    'axes.edgecolor'    : ['k', validate_color],    # edge color; black
    'axes.linewidth'    : [1.0, validate_float],    # edge linewidth
    'axes.titlesize'    : ['large', validate_fontsize], # fontsize of the axes title
    'axes.grid'         : [False, validate_bool],   # display grid or not
    'axes.labelsize'    : ['medium', validate_fontsize], # fontsize of the x any y labels
    'axes.labelcolor'   : ['k', validate_color],    # color of axis label

    # tick properties
    'tick.major.size'   : [5, validate_float],      # major tick size in points
    'tick.minor.size'   : [2, validate_float],      # minor tick size in points    
    'tick.major.pad'   : [3, validate_float],      # distance to label in points
    'tick.minor.pad'   : [3, validate_float],      # distance to label in points
    'tick.color'        : ['k', validate_color],    # color of the tick labels 
    'tick.labelsize'    : ['small', validate_fontsize], # fontsize of the tick labels

    'grid.color'       :   ['k', validate_color],       # grid color
    'grid.linestyle'   :   [':', str],       # dotted
    'grid.linewidth'   :   ['0.5', validate_float],     # in points            


    # figure props
    # figure size in inches: width by height
    'figure.figsize'    : [ (8,6), validate_nseq_float(2)], 
    'figure.dpi'        : [ 80, validate_float],   # DPI
    'figure.facecolor'  : [ 0.75, validate_color], # facecolor; scalar gray
    'figure.edgecolor'  : [ 'w', validate_color],  # edgecolor; white

    'savefig.dpi'       : [ 150, validate_float],   # DPI
    'savefig.facecolor' : [ 'w', validate_color],  # facecolor; white
    'savefig.edgecolor' : [ 'w', validate_color],  # edgecolor; white
    'savefig.orientation' : [ 'portait', validate_orientation],  # edgecolor; white

    'tk.window_focus'   : [ False, validate_bool],  # Maintain shell focus for TkAgg
    'plugins.directory' : ['.matplotlib_plugins', str], # where plugin directory is locate

    }


def matplotlib_fname():
    """
    Return the path to the rc file

    Search order:

     * current working dir
     * environ var MATPLOTLIBRC
     * HOME/.matplotlibrc
     * MATPLOTLIBDATA/.matplotlibrc
     
    """

    fname = os.path.join( os.getcwd(), '.matplotlibrc')
    if os.path.exists(fname): return fname

    if os.environ.has_key('MATPLOTLIBRC'):
        path =  os.environ['MATPLOTLIBRC']
        if os.path.exists(path):
            fname = os.path.join(path, '.matplotlibrc')
            if os.path.exists(fname):
                return fname

    home = get_home()
    if home is not None:
        fname = os.path.join(home, '.matplotlibrc')
        if os.path.exists(fname):
            return fname

    path =  get_data_path() # guaranteed to exist or raise
    fname = os.path.join(path, '.matplotlibrc')
    if not os.path.exists(fname):
        print >> sys.stderr, 'Could not find .matplotlibrc; using defaults'
    return fname

def rc_params():
    'Return the default params updated from the values in the rc file'

    deprecated_map = {
        'text.fontstyle':   'font.style',
        'text.fontangle':   'font.style',
        'text.fontvariant': 'font.variant',
        'text.fontweight':  'font.weight',
        'text.fontsize':    'font.size',
        'tick.size' :       'tick.major.size',
        }
    
    fname = matplotlib_fname()
    if not os.path.exists(fname):
        return dict([ (key, tup[0]) for key, tup in defaultParams.items()])

    cnt = 0
    for line in file(fname):
        cnt +=1
        line = line.strip()
        if not len(line): continue
        if line.startswith('#'): continue
        tup = line.split(':',1)
        if len(tup) !=2:
            print >>sys.stderr, 'Illegal line #%d\n\t%s\n\tin file "%s"' % (cnt, line, fname)
            continue

        key, val = tup
        key = key.strip()
        if key in deprecated_map.keys():
            alt = deprecated_map[key]
            warn('%s is deprecated in .matplotlibrc - use %s instead.' % (key, alt))
            key = alt
            
        if not defaultParams.has_key(key):
            print >>sys.stderr, 'Bad key "%s" on line %d in %s' % (key, cnt, fname)
            continue

        
        default, converter =  defaultParams[key]


        ind = val.find('#')
        if ind>=0: val = val[:ind]   # ignore trailing comments
        val = val.strip()
        try: cval = converter(val)   # try to convert to proper type or raise
        except Exception, msg:
            print >>sys.stderr, 'Bad val "%s" on line #%d\n\t"%s"\n\tin file "%s"\n\t%s' % (val, cnt, line, fname, msg)
            continue
        else:
            # Alles Klar, update dict
            defaultParams[key][0] = cval

    # strip the conveter funcs and return
    return dict([ (key, tup[0]) for key, tup in defaultParams.items()])

# this is the instance used by the matplotlib classes
rcParams = rc_params() 

rcParamsDefault = dict(rcParams.items()) # a copy

def rc(group, **kwargs):
    """
    Set the current rc params.  Group is the grouping for the rc, eg
    for lines.linewidth the group is 'lines', for axes.facecolor, the
    group is 'axes', and so on.  kwargs is a list of attribute
    name/value pairs, eg

      rc('lines', linewidth=2, color='r')

    sets the current rc params and is equivalent to
    
      rcParams['lines.linewidth'] = 2
      rcParams['lines.color'] = 'r'

    The following aliases are available to save typing for interactive
    users
        'lw'  : 'linewidth'
        'ls'  : 'linestyle'        
        'c'   : 'color'
        'fc'  : 'facecolor'
        'ec'  : 'edgecolor'
        'mfc' : 'markerfacecolor'
        'mec' : 'markeredgecolor'
        'mew' : 'markeredgewidth'
        'aa'  : 'antialiased'            
        'l'   : 'lines'
        'a'   : 'axes'
        'f'   : 'figure'
        'p'   : 'patches'
        'g'   : 'grid'

    Thus you could abbreviate the above rc command as

          rc('l', lw=2, c='r')


    Note you can use python's kwargs dictionary facility to store
    dictionaries of default parameters.  Eg, you can customize the
    font rc as follows

      font = {'family' : 'monospace',
              'weight' : 'bold',
              'size'   : 'larger',
             }

      rc('font', **font)  # pass in the font dict as kwargs

    This enables you to easily switch between several configurations.
    Use rcdefaults to restore the default rc params after changes.
    """

    aliases = {
        'lw'  : 'linewidth',
        'ls'  : 'linestyle',
        'c'   : 'color',                        
        'fc'  : 'facecolor',
        'ec'  : 'edgecolor',
        'mfc' : 'markerfacecolor',
        'mec' : 'markeredgecolor',
        'mew' : 'markeredgewidth',
        'aa'  : 'antialiased',                        
        'l'   : 'lines',
        'a'   : 'axes',
        'f'   : 'figure',
        'p'   : 'patches',
        'g'   : 'grid',        
        }
    
    for k,v in kwargs.items():
        name = aliases.get(k) or k
        key = '%s.%s' % (group, name)
        if not rcParams.has_key(key):
            raise KeyError('Unrecognized key "%s" for group "%s" and name "%s"' %
                           (key, group, name))
        
        rcParams[key] = v


def rcdefaults():
    """
    Restore the default rc params - the ones that were created at
    matplotlib load time
    """
    rcParams.update(rcParamsDefault)



# Now allow command line to override

# Allow command line access to the backend with -d (matlab compatible
# flag)

if hasattr(sys,'argv'):         # mod_python doesn't have argv attr
    for s in sys.argv[1:]:
        if s.startswith('-d'):  # look for a -d flag
            rcParams['backend'] = s[2:].strip()
            break

_knownBackends = {'PS':1, 'GTK':1, 'Template':1, 'GD':1,
                  'WX':1, 'Paint':1, 'Agg':1, 'GTKAgg':1, 'SVG':1,
                  'TkAgg':1, 'WXAgg':1, 'FltkAgg':1,}

def use(arg):
    """
    Set the matplotlib backend to one of the _knownBackends
    """
    
    if not _knownBackends.has_key(arg):
        print >>sys.stderr, 'unrecognized backend %s.\n' % arg +\
              'Use one of %s' % ', '.join( _knownBackends.keys() )
        sys.exit()
    rcParams['backend'] = arg

def get_backend():
    return rcParams['backend']

def interactive(b):
    """
    Set interactive mode to boolean b.

    If b is True, then draw after every plotting command, eg, after xlabel
    """
    rcParams['interactive'] = b

def is_interactive():
    'Return true if plot mode is interactive'
    b = rcParams['interactive']
    return b
    
def tk_window_focus():
    """Return true if focus maintenance under TkAgg on win32 is on.
     This currently works only for python.exe and IPython.exe.
     Both IDLE and Pythonwin.exe fail badly when tk_window_focus is on."""
    if rcParams['backend'] != 'TkAgg':
	return False    
    return rcParams['tk.window_focus']



