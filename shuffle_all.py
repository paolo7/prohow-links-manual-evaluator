import random, os

def shuffle_single(source,target, target_name):
    target_file = target+target_name
    listing = os.listdir(source)
    data = []
    for infile in listing:
        with open(source+infile, 'r') as source_f:
            data = data+[(random.random(), line) for line in source_f]
    data.sort()
    with open(target_file, 'w') as target_f:
        for _, line in data:
            target_f.write(line)

def shuffle_all(dirs,target_name):
    for pair in dirs:
        shuffle_single(pair[0],pair[1],target_name)
