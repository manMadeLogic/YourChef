from math import sqrt
def getDistance(A,B):
    distance = sqrt(abs(A['salt'] - B['salt'])**2+abs(A['sour'] - B['sour'])**2+abs(A['sweet'] - B['sweet'])**2+abs(A['spicy'] - B['spicy'])**2)
    return distance

def sort(query,core):
    for item in query:
        item['score'] = getDistance(item,core)
    return sorted(query, key = lambda item:item['score'])

if __name__ == '__main__':
    query = [{'salt':1,'sour':1,'sweet':1,'spicy':1},{'salt':2,'sour':2,'sweet':2,'spicy':2}]
    print(sort(query,query[1]))