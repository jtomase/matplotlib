from matplotlib.matlab import *

def f(t):
    s1 = cos(2*pi*t)
    e1 = exp(-t)
    return multiply(s1,e1)

t1 = arange(0.0, 5.0, 0.1)
t2 = arange(0.0, 5.0, 0.02)
t3 = arange(0.0, 2.0, 0.01)
figure(1, figsize=(7,5)) # small
#figure(1, figsize=(8,6), dpi=100) # large
subplot(211)
plot(t1, f(t1), 'bo', t2, f(t2), 'k')
grid('on')
title('A tale of 2 subplots')
ylabel('Damped')

subplot(212)
plot(t3, cos(2*pi*t3), 'r--')
grid('on')
xlabel('time (s)')
ylabel('Undamped')

#savefig('subplot_demo_small.png', dpi=60)
#savefig('subplot_demo_large.png', dpi=120)

show()

