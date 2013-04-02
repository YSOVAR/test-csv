import sys
import numpy as np
from numpy.random import random
import astropy.table as table


csvcols = ["ysovarid","sname","ra","de","hmjd","fname","mag1","emag1","useful","kind","note"]
coltype = [np.int, 'S23', np.float, np.float, np.float, 'S5', np.float, np.float, np.int, np.int, 'S20']

def add_source(table, time, mag, mag_error, ysovarid, fname, sname = None, ra = None, dec = None, useful = 1, kind = 0, note = ''):
    '''Add info about a fake source to the table.

    If ra or dec ad None, then look if a source with same ID exisits in the
    table already. If so, copy their value, if not, generate randomnly.
    '''
    if len(time) != len(mag):
        raise ValueError('Time and mag need to have same number of elements')
    if len(mag) != len(mag_error):
        raise ValueError('mag and mag_error need to have some number of elements')
    if ra is None:
        ind = np.nonzero(tab['ysovarid'] == ysovarid)[0]
        if len(ind) > 0:
            ra = table['ra'][ind][0]
        else:
            ra = np.random.random() * 360.
    if dec is None:
        ind = np.nonzero(tab['ysovarid'] == ysovarid)[0]
        if len(ind) > 0:
            dec = table['de'][ind][0]
        else:
           dec = (np.random.random() * 180) - 90.
    sname = sname or 'test_'+str(abs(ysovarid))
    for i in range(len(time)):
        table.add_row({"ysovarid": ysovarid,"sname": sname,"ra":ra,"de":dec,"hmjd":time[i],"fname": fname,"mag1":mag[i],"emag1":mag_error[i],"useful":useful,"kind":kind,"note":note})


tab = table.Table()
for name, dtype in zip (csvcols, coltype):
    col = table.Column(name = name, length=0, dtype = dtype)
    tab.add_column(col)

# create a few dummy times, that look OK that can be reused, when time
# does not matter
t5 = 55300.5 + np.arange(5)
t50 = 55500.2 + np.arange(50)


### check min, max, etc.
### source numbers begin with -1000
add_source(tab, t5, [12.,12.,12.,12.,12.], [.1,.1,.1,.1,.1], -1000, "IRAC1")
add_source(tab, t5, [12.,12.,12.,12.,12.], [.1,.1,.1,.1,.1], -1001, "IRAC2")

add_source(tab, t5, [13.,12.5,12.,11.5,11.], [.1,.1,.1,.1,.1], -1002, "IRAC1")
add_source(tab, t5, [13.,12.5,12.,11.5,11.], [.1,.1,.1,.1,.1], -1003, "IRAC2")

### testing periodicity finding
t100 = 55500. + np.arange(100) + random(100)
add_source(tab, t100, np.sin(t100*2*np.pi/3), 0.01+np.zeros_like(t100), -1500, "IRAC1")

add_source(tab, t100, np.sin(t100/50*2*np.pi) + random(100) * 0.01, 0.01+np.zeros_like(t100), -1501, "IRAC1")

add_source(tab, t100, 12. + np.sin(t100/5*2*np.pi)/20. + 2.*random(100), 0.5+random(100), -1502, "IRAC2")

add_source(tab, t100, np.sin(t100/3*2*np.pi) + random(100) * 0.01, 0.01+random(100), -1503, "IRAC1")
add_source(tab, t100, np.sin(t100/5*2*np.pi) + random(100)*10., 10.+np.zeros_like(t100), -1503, "IRAC2")




### testing multiband lc merging
add_source(tab, t50, 12.+ random(50), random(50), -2000, 'IRAC1')
t_2000 = t50
t_2000[:25] = t50[:25] - 0.06 - random(25)*0.4
t_2000[25:] = t50[25:] + 0.06 + random(25)*0.3
add_source(tab, t_2000, 12. + random(50), random(50), -2000, 'IRAC2')

add_source(tab, t50, 12.+ random(50), random(50), -2001, 'IRAC1')
add_source(tab, t50 + (random(50)*0.02)-0.01, 12.+ random(50), random(50), -2001, 'IRAC2')

add_source(tab, t50, 12.+ random(50), random(50), -2002, 'IRAC1')
add_source(tab, t50 + np.linspace(-0.049, +0.049), 12.+ random(50), random(50), -2002, 'IRAC2')

### testing CMDs
add_source(tab, t50, 12. + np.zeros(50), 0.1+np.zeros(50), -2500, 'IRAC1')
add_source(tab, t50, 11. + np.linspace(1,-1), 0.1+np.zeros(50), -2500, 'IRAC2')

add_source(tab, t50, 12. + random(50), 0.1+np.zeros(50), -2501, 'IRAC1')
add_source(tab, t50, 11. + random(50), 0.1+np.zeros(50), -2501, 'IRAC2')

# relative absorption coeff from Flaherty et al. (2007) ApJ, 663, 1069
add_source(tab, t50, 12. + np.linspace(0, 3) * 0.632, 0.1+np.zeros(50), -2502, 'IRAC1')
add_source(tab, t50, 11. + np.linspace(0, 3) * 0.53 , 0.1+np.zeros(50), -2502, 'IRAC2')



### testing Stetson
add_source(tab, t50, 12. + np.linspace(-1,1), 0.1+np.zeros(50), -2700, 'IRAC1')
add_source(tab, t50, 11. + np.linspace(1,-1), 0.1+np.zeros(50), -2700, 'IRAC2')

mags = np.ones(50)
mags[25:] = -1
add_source(tab, t50, 12. + mags, 0.1 + np.zeros(50), -2701, 'IRAC1')
add_source(tab, t50, 13. + mags, 0.1 + np.zeros(50), -2701, 'IRAC2')


#### output the stuff

import csv

with open(sys.argv[1], 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(tab.colnames)
    for i in range(len(tab)):
        writer.writerow(tab[i])

