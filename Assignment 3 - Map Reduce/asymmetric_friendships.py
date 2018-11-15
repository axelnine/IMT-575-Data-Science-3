import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    pair = [record[0], record[1]]
    pair.sort()
    mr.emit_intermediate((pair[0],pair[1]),1)

def reducer(key, list_of_values):
    if len(list_of_values)<2:
        mr.emit(key)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)