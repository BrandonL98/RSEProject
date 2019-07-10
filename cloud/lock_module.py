def open_lock():
    f = open("lock.txt","w+")
    f.write("Unlocked")

def lock_lock():
    f = open("lock.txt","w+")
    f.write("Locked")

def check_lock_status():
    f = open("lock.txt","r")
    return f.readline()
