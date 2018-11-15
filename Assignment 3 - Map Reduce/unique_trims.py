import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    nucleotides = record[1]
    if len(nucleotides) > 10:
        new_nucleotides  = nucleotides[:-10]  
        mr.emit_intermediate(new_nucleotides, record[0]) 

def reducer(key, list_of_values):
    mr.emit(key)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)