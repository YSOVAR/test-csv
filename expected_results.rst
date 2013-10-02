Testing our YSOVAR codes
========================
We have generated artifical csv files that have the same format (at at
least a very similar one) to the csv files extracted from the YSOVAR2
database.
The purpose of this excercise is to 

- test that our code works correctly
- compare our python code to Maria's IDL code

Just like the real data, one singe csv file contains many different
sources and each source is meant to verify one or more of the
statistics we use. Most of them are analytically generated, so we know
what the result should be exactly, some are randomly generated. They
might change between different run (I'll implement a constant seed of
the random number generator later).

Parameters that are uninteresting for the test in question (e.g. RA,
DEC or the magnitudes when we only care for the number of datapoints)
are randomly generated and will also change each time we rerun the
program. Also, I did not bother to set the number of digits for each
item, so that e.g. `ra` and `de` might have less digits and `mag1` might
have more than in the csv files. Let me know if that is a problem, I can fix that.

All sources in the csv file have negative `ysovarid` entries to set
them apart form real data. Below, we list for each source which
statistics we want to verify there.

.. Note:: All the examples below assume that no systematic error (i.e.
   no error-floor is added). If you *do* add an error floor, then
   obviously all values that depend on the error (chi^2, stetson)
   will not come out as analytically calculated.





One-color statistics
--------------------
We generated several very short and simple lightcurves for different sources,
that have entries in one band only.

Which lightcurves make the cut?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We ignore lightcurves below a certain number of datapoints. To check
that this rejection works, here are a few (constant) lightcurves with
few datapoints.

============= ====================
Source number number of datapoints  
============= ====================
-998          4
-999          5
-1000         6 
============= ====================

All other lightcurves in the simulated dataset have 6 or more
datapoints (most have 50 or 100 datapoints).


constant lightcurves
^^^^^^^^^^^^^^^^^^^^

These are two lightcurves that have identical entires, one of them tests the IRAC1 channel,
the other one the IRAC2 channel.
The followinf statistics should be compared:

- number of entries = 6 in the band chosen
- max = 12
- min = 12 
- median = 12
- weighted mean = 12
- any quantile = 12
- standard deviation = 0 
- median absolute devitation = 0
- chi^2 to mean = 0

============= ===== ===========
Source number band  lightcurve  
============= ===== ===========
-1000         IRAC1 constant 
-1001         IRAC2 constant
============= ===== ===========

simple lightcurves
^^^^^^^^^^^^^^^^^^
These two lightcurves have identical entries again.
The following statistics should be compared:

- number of entries = 6 in the band chosen for -1002 and -1003, 100 for -1004
- max = 13
- min = 11 
- median = 12
- weighted mean = 12
- standard deviation = 1./sqrt(2) = 0.7071 (taking dof = 1)  (*not for -1004*)
- median absolute devitation = 0.5  (*not for -1004*)
- reduced chi^2 to mean = 50.0 (*only approximate for -1004*)
- 10%-90% spread of the distribution = 1.6 (*only for -1004* - depending on how
  your algorithm treats the values on the boundaries, this might vary +- 0.02)

============= ===== ==================
Source number band  lightcurve  
============= ===== ==================
-1002         IRAC1 linear brightening
-1003         IRAC2 linear brightening
-1004         IRAC1 linear brightening
============= ===== ==================

lightcurve that would show if mag and error are reordered
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This lightcurve would show if errors are messed up with respect to the times.
Thus, most important is a comparison for quantities that depend on both,
magnitude and error:

- reduced chi^2 to mean = 0.9665139
- weighted mean = 12.31796

============= ===== ==================
Source number band  lightcurve  
============= ===== ==================
-1010         IRAC1 jumps up and down
============= ===== ==================


Periodicity
-----------
All lightcurves here are generated with a sin-wave, most have some
added noise, so the expected results can vary a little. We add the noise,
because some implementations of Lomb-Scargle fail, if the solution is
exact (the peak of the periodogram could be infinite).

============= ===== ====== ================================
Source number band  Noise? expected results
============= ===== ====== ================================
-1500         IRAC1 no     period = 3
-1501         IRAC1 yes    period = 50, peak is significant
-1502         IRAC2 yes    no significant peak
-1503         both  yes    period = 3 in IRAC1, =5 in IRAC2
                           IRAC1 is more significant
============= ===== ====== ================================


Merging lightcurves with data in different bands
------------------------------------------------
The following lightcurves have different observation times in IRAC1
and IRAC2 (e.g. IRAC1 before IRAC2, IRAC1 after IRAC2). The table
gives the expected number of datapoints where photometry for IRAC1 and
IRAC2 exisits within 12 minutes, 0.01 days, or 0.05 days.

============= ========= ========= =========
Source number 12 min    0.01 days 0.05 days
============= ========= ========= =========
-2000         none      none      none
-2001         50        50        50
-2002         8         10        50
============= ========= ========= =========

Two-color statistics
--------------------
Here are a few sources to check shapes in the color-magnitude-diagram.

============= ============ ===========
Source number color change CMD shape
============= ============ ===========
-2500         None         flat   
-2501         random       point cloud
-2502         reddening    line
============= ============ ===========

And now the Stetson index

============= =============
Source number Stetson index
============= =============
-2700           0.00
-2701           0.00
-2702          10.1012
-2703          10.1012
-2704         -10.1012
============= =============
