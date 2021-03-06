import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    value = record[1]
    words = value.split()
    for w in words:
        mr.emit_intermediate(w,record[0])

def reducer(key, list_of_values):
    mr.emit((key,list(set(list_of_values))))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)