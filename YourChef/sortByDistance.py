
def getDistance(A, B):
    distance = (A['salt'] - B['salt']) ** 2 + (A['sour'] - B['sour']) ** 2 + (A['sweet'] - B['sweet']) ** 2\
               + (A['spicy'] - B['spicy']) ** 2
    return distance


def sort_restaurant(query, origin, core):
    scores = dict()
    for item in query:
        scores[item['userid']] = getDistance(item, core)
        # item['score'] = getDistance(item, core)

    for item in origin:
        item['score'] = scores.get(item['userid'], 400)
    return sorted(origin, key=lambda item: item['score'])


if __name__ == '__main__':
    query = {'salt': 1, 'sour': 1, 'sweet': 1, 'spicy': 1}
    store = [{'salt': 1, 'sour': 1, 'sweet': 1, 'spicy': 1, 'userid': 'a', 'username': 'Uncle Luoyang'},
             {'salt': 2, 'sour': 2, 'sweet': 2, 'spicy': 2, 'userid': 'asdfmmm', 'username': 'asdfmmm'},
             {'salt': 1, 'sour': 1, 'sweet': 2, 'spicy': 2, 'userid': 'xxxxxx', 'username': 'sun chan'},
             {'salt': 1, 'sour': 1, 'sweet': 2, 'spicy': 1, 'userid': 'kk', 'username': 'kkkk chan'}]
    print(sort_restaurant(store, query, store))
