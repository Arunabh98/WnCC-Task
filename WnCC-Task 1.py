# Sorting Algorithm used Quicksort. The expected running time is O(nlog(n)).
# For QuickSort Implementation
import random
# For Exception Handling
from urllib2 import URLError
# For Google API Request
import requests
# for sys.exit
import sys

# Stores the name of the place and distance from IIT Bombay
placeDetails = []


# QuickSort Algorithm Implementation, Sorts Distances in Ascending Order
def quickSort(A):
    if len(A) == 1:
        return A
    if len(A) == 0:
        return []
    arraySortedIndex = []
    for elements in range(len(A)):
        arraySortedIndex.append((' ', 0))
    leftIndex = 0
    rightIndex = len(A) - 1
    # random selection of pivot around which next iteration would take place
    pivot = random.randint(0, len(A) - 1)
    # Sorting elements by comparing its value to pivot
    for elements in A:
        if elements[1] < A[pivot][1]:
            arraySortedIndex[leftIndex] = elements
            leftIndex += 1
        elif elements[1] > A[pivot][1]:
            arraySortedIndex[rightIndex] = elements
            rightIndex -= 1
    arraySortedIndex[leftIndex] = A[pivot]
    # Recursive Calls to quickSort()
    sortedArray = quickSort(arraySortedIndex[:leftIndex]) + [arraySortedIndex[leftIndex]] + quickSort(
        arraySortedIndex[rightIndex + 1:])

    # Returns Sorted Array
    return sortedArray


# Gets the distances of places by using Google Maps API
def getDistance():
    count = 0
    # Reads from input.txt
    f = open('input.txt', 'r+')
    for placeInput in f:
        place = placeInput.replace(' ', '+')
        try:
            # Implementation of Google Maps API
            response = requests.get(
                'https://maps.googleapis.com/maps/api/directions/json?origin=' + place + 'Mumbai' + '&' + 'destination=' + 'IIT+Bombay')
            jsonResponse = response.json()
            if jsonResponse["status"] == 'NOT_FOUND':
                print placeInput, " not found"
            elif jsonResponse["status"] == 'INVALID_REQUEST':
                # Input is Invalid
                print jsonResponse["error_message"], placeInput, ' is invalid.'
            elif jsonResponse["status"] == 'ZERO_RESULTS':
                # Not accessible by road
                placeDetails.append((placeInput, 10000000 + count))
                count += 1
            else:
                placeDetails.append((placeInput, jsonResponse["routes"][0]["legs"][0]["distance"]["value"]))
        # Exception Handling
        except requests.ConnectionError:
            sys.exit("No Internet Connection")
        # General Exceptions
        except Exception as e:
            sys.exit('Unexpected Error')


getDistance()
SortedPlaceDetails = quickSort(placeDetails)
print "RESULTS"
print "Distance(m) Name of place"
for place in SortedPlaceDetails:
    if place[1] >= 10000000:
        print 'Not accesible by road - ', place[0]
    else:
        print place[1], '     ', place[0]
raw_input()
