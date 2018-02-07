from __future__ import print_function
import numpy as np
import math
from db_wrapper import query_ways_within_radius
import utils

GPS_SIGMA = 6.7
W_DIST = 0.8
W_TANG = 0.2

# SUMMARY
#--------------------
# The main datastructure in this file is the ways array, which contains all the
# OSM ways within a certain distance of the observation. A way in the ways array
# is a dict: ways[0] = {'osm_id': 264056469L, 'points': [(x1,y1), (x2,y2) ... ] 
# With each function, the ways dictionary is extended with different attributes.


# A segment is the line between two consecutive nodes
# it is stored as a tuple containing its endpoints
def _add_segments(ways):
    for way in ways:
        way['segments'] = []
            
        for i, point in enumerate(way['points']):
            if i != 0:
                way['segments'].append((way['points'][i-1], point))
    return ways

# Add distances from each segment to base_point
def _add_distances(ways, base_point):
    for way in ways:
        way['distances'] = [utils.point_to_lineseg_dist(segment, base_point) for segment in way['segments']]
    return ways


# Distance score = Probability that observation came from a road segment
# given that GPS error is Gaussian around the road segment with stdev sigma
def _add_distance_scores(ways, sigma):
    # Gaussian
    p = lambda dist: (1/(math.sqrt(2*math.pi)*sigma))*math.exp(-0.5*(dist/sigma)**2)
    # Rayleigh
    # p = lambda dist: (dist / sigma**2) * math.exp(-(dist**2) / (2 * (sigma**2)))
    for way in ways:
        way['distance_scores'] = [p(dist) for dist in way['distances']]
    return ways

def _add_emission_probabilities(ways):
    for way in ways:
        way['emission_probabilities'] = [way['distance_scores'][i] for i in range(len(way['segments']))]
    return ways

# Return n segments with highest emission probabilities
def _get_top_n(ways, n):
    segments = []
    probabilities = []
    for way in ways:
        for i, p in enumerate(way['emission_probabilities']):
            segments.append({'way_osm_id': way['osm_id'], 'index_in_way': i, 'endpoints': way['segments'][i], 'direction': None, 'distance_score': way['distance_scores'][i],
                             'distance': way['distances'][i]})
            probabilities.append(p)
    combined = zip(segments, probabilities)
    combined.sort(key=lambda el: -el[1])
    segments = [x[0] for x in combined]
    probabilities = [x[1] for x in combined]
    return segments[:n], probabilities[:n]


# Radius in meters
# n is the number of segments returned with the top emission probabilities
def compute_emission_probabilities(observation, radius, n):
    lat, lon = observation
    point, ways = query_ways_within_radius(lat, lon, radius)
    if ways is None or point is None:
        return 1,2,3
    ways = _add_segments(ways)
    ways = _add_distances(ways, point)
    ways = _add_distance_scores(ways, GPS_SIGMA)
    ways = _add_emission_probabilities(ways)
    segments, probabilities = _get_top_n(ways, n)
    print ('complete emission probability')
    return segments, probabilities, point
