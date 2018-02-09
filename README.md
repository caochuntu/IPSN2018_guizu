# Walkway Discovery from Large Scale Crowdsensing

Source code of IPSN 2018 paper "Walkway Discovery from Large Scale Crowdsensing" is shown here.
--------------------------------------------------

**There are three parts in our code:**
- Data Classification
- Walkway Identification
- Automatic Verification

In order to improve the readability and usability of the code. We will keep organizing the code and adding necessary comments.
Currently we just update map matching in **Data Classification** based on [kartoffel](https://github.com/juhanaka/kartoffel) version which stores the map into a postgresql database, leading to a slowing searching phase when there are billions of observations.
Thus, we design a quadtree based method, which dramatically improve the efficiency of map matching phase.
The quadtree-based code will be available by the end of 18 Februray 2018.


_We will keep updating the code continuously_.