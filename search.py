import os

queue = []

def find(array, find):
    count = 0
    for i in array:
        if i[0] == find:
            print(i[0])
            return i, count
            count = count + 1
    return None, None

def edit_stats(array, target):
    lists, count = find(array,target)
    if lists is None:
        return False
    else:
        del array[count]
        del lists[1]
        lists.append(1)
        array.insert(0, lists)
        return True

def add_to_queue(array, var):
    lists, count = find(array, var)
    queue.append(lists)
    print('Added to Queue' + var)
    return True

def queue_pass_array(array):# Return [,] list
    queue.append(array)
    print(queue)

def access_queue():
    if not queue:
        return False
    else:
        return queue.pop()

#always return list
def search_file(konst,format):
    result = os.listdir(path = konst)
    processed = []
    if len(result) > 1:
        for file_name in result:
            if file_name.endswith(("."+str(format))):
                processed.append(file_name)
            else:
                pass
            return processed
    else:
        if not result:
            return None
        else:
            return result