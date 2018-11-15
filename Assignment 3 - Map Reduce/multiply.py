import MapReduce
import sys

mr = MapReduce.MapReduce()
K = 5
def mapper(record):
    matrix, row, col, val = record
    if matrix == 'a':
        for n in range(K):
            mr.emit_intermediate((record[1], n), [matrix, col, val])
    else:
        for n in range(K):
            mr.emit_intermediate((n, record[2]), [matrix, row, val])

def reducer(key, list_of_values):
    result_A, result_B = [],[]
    for val in list_of_values:
        if val[0]=='a':
            result_A.append(val)
        else:
            result_B.append(val)
    
    result = 0
    
    for a in result_A:
        for b in result_B:
            if a[1] == b[1]:
                result += a[2] * b[2]
    
    mr.emit((key[0], key[1], result))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)