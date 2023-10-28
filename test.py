#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
#from models.state import State
import sys

p1 = storage.get('Place', sys.argv[1])
print(p1.amenities)
print(p1)
print(p1.amenity_ids)
