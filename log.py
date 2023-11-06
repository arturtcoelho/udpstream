def log(message, file):
    if file == None:
        file = 'log.txt'
    with open(file, 'a') as f:
        f.write(message)
        f.write('\n')