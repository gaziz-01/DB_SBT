import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)
json_path = '/home/gaziz/dtbs_sber/file.json'


def measure_time(operation, description):
    start_time = time.time()
    result = operation()
    elapsed_time = time.time() - start_time
    print(f"{description}: {elapsed_time:.4f} секунд\n")
    return result


# hset
hash_name = "myJsonHash"

r.delete(hash_name)

def save_data():
    with open(json_path, 'r') as file:
        data = json.load(file)
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            r.hset(hash_name, key, value)
measure_time(save_data, "Время сохранения в HSET")


def read_data():
    return r.hgetall(hash_name)

measure_time(read_data, "Время чтения из HSET")

#string
string_key = "large_json_data"

def save_string():
    with open(json_path, 'r') as file:
        json_data = file.read()
        r.set(string_key, json_data)

measure_time(save_string, "Время сохранения STRING")

def read_string():
    return r.get(string_key)

measure_time(read_string, "Время чтения STRING")

#list
list_name = "myJsonList"

def save_list():
    with open(json_path, 'r') as file:
        data = json.load(file)
        for item in data:  
            r.rpush(list_name, json.dumps(item))

measure_time(save_list, "Время сохранения в LIST")

def read_list():
    list_items = r.lrange(list_name, 0, -1)
    return [json.loads(item) for item in list_items]

measure_time(read_list, "Время чтения из LIST")

#zset
zset_name = "myJsonZSet"

def save_zset():
    with open(json_path, 'r') as file:
        data = json.load(file)
        for index, item in enumerate(data):
            r.zadd(zset_name, {json.dumps(item): index})
            
measure_time(save_zset, "Время сохранения в ZSet")


def read_zset():
    return [json.loads(item) for item in r.zrange(zset_name, 0, -1)]

measure_time(read_zset, "Время чтения из ZSET")

