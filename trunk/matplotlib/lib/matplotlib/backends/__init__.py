import sys
import matplotlib

__all__ = ['backend','show','draw_if_interactive','error_msg',
           'new_figure_manager', 'backend_version']

interactive_bk     = ['GTK','GTKAgg','GTKCairo','FltkAgg','QtAgg', 'TkAgg',
                      'WX','WXAgg',]
non_interactive_bk = ['Agg','Cairo','GD','GDK','Paint','PS','SVG','Template']
all_backends       = interactive_bk + non_interactive_bk

backend = matplotlib.get_backend()
if backend not in all_backends:
    raise ValueError, 'Unrecognized backend %s' % backend

# Import the requested backend into a generic module object
backend_name = 'backend_'+backend.lower()
backend_mod = __import__('matplotlib.backends.'+backend_name,
                         globals(),locals(),[backend_name])

# Things we pull in from all backends
new_figure_manager = backend_mod.new_figure_manager

if hasattr(backend_mod,'backend_version'):
    backend_version = getattr(backend_mod,'backend_version')
else: backend_version = 'unknown'

# Now define the public API according to the kind of backend in use
if backend in interactive_bk:
    error_msg  = backend_mod.error_msg
    show       = backend_mod.show
    draw_if_interactive = backend_mod.draw_if_interactive
else:  # non-interactive backends
    def draw_if_interactive():  pass
    def show(): pass
    def error_msg(m):
        matplotlib.verbose.report_error(m)
        sys.exit()

# Additional imports which only happen for certain backends.  This section
# should probably disappear once all backends are uniform.
if backend=='Paint':
    from backend_paint import error_msg
elif backend in ['WX','WXAgg']:
    Toolbar = backend_mod.Toolbar
    __all__.append('Toolbar')

matplotlib.verbose.report('backend %s version %s' % (backend,backend_version))
