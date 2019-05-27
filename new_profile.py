# Usage: python new_profile.py [name] homeowner

import sys
import os

def main ():

    name = 'dataset/' + sys.argv[1]

    if not os.path.exists(name):
        os.makedirs(name)
        print ("[INFO] Profile ", sys.argv[1],  " created ")
        if sys.argv[2] == "homeowner":
            f = open("homeowners.txt", "a+")  
            f.write('\n')  
            f.write(sys.argv[1])
    else:    
        print ("[INFO] Profile ", sys.argv[1],  " already exists")

if __name__ == '__main__':
    main()
