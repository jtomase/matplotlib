#!/usr/bin/env python
# Thanks to Charles Twardy for this example
from matplotlib.matlab import *

a = arange(0,3,.02)
b = arange(0,3,.02)
c=exp(a)
d=c.tolist()
d.reverse()
d = array(d)

ax = subplot(111)
plot(a,c,'k--',a,d,'k:',a,c+d,'k')
legend(('Model length', 'Data length', 'Total message length'),
       'upper center')
ax.set_ylim([-1,20])
ax.grid(0)
xlabel('Model complexity --->')
ylabel('Message length --->')
title('Minimum Message Length')
set(gca(), 'yticklabels', [])
set(gca(), 'xticklabels', [])

# set some legend properties.  All the code below is optional.  The
# defaults are usually sensible but if you need more control, this
# shows you how
leg = gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
llines = leg.get_lines()  # all the lines.Line2D instance in the legend
frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend

# see text.Text, lines.Line2D, and patches.Rectangle for more info on
# the settable properties of lines, text, and rectangles
frame.set_facecolor(0.80)     # set the frame face color to light gray
set(ltext, 'fontsize', 10)    # the legend text fontsize
set(llines, 'linewidth', 1.5) # the legend linewidth
#leg.draw_frame(False)         # don't draw the legend frame
#savefig('legend_demo')
show()



