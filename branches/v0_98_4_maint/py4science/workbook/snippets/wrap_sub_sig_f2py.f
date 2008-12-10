	subroutine phipol(j,mm,nodes,wei,nn,x,phi,wrk)
c
c       Lines with Cf2py in them are directives for f2py to generate a better 
c	python interface.  These must come _before_ the Fortran variable 
c       declarations so we can control the dimension of the arrays in Python.
c
c       Inputs:
Cf2py   integer check(0<=j && j<mm),depend(mm) :: j
Cf2py   real *8 dimension(mm),intent(in) :: nodes
Cf2py   real *8 dimension(mm),intent(in) :: wei
Cf2py   real *8 dimension(nn),intent(in) :: x
c
c       Outputs:
Cf2py   real *8 dimension(nn),intent(out),depend(nn) :: phi
c
c       Hidden args:
c       - scratch areas can be auto-generated by python
Cf2py   real *8 dimension(2*mm+2),intent(hide,cache),depend(mm) :: wrk
c       - array sizes can be auto-determined
Cf2py   integer intent(hide),depend(x):: nn=len(x)
Cf2py   integer intent(hide),depend(nodes) :: mm = len(nodes)
c
	implicit real *8 (a-h, o-z)
	real *8 nodes(*),wei(*),x(*),wrk(*),phi(*)
	real *8 sum, one, two, half