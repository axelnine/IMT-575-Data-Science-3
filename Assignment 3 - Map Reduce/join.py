import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    mr.emit_intermediate(record[1],record)

def reducer(key, list_of_values):
    list_of_items = []
    for value in list_of_values:
        if value[0] == 'order':
            order = value
        elif value[0] == 'line_item':
            list_of_items.append(value)
    
    for item in list_of_items:
        mr.emit(order + item)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)