# Usage: python new_profile.py [name] homeowner

import sys
import os

def main ():

    name = 'dataset/' + sys.argv[1]

    if not os.path.exists(name):
        os.makedirs(name)
        print "[INFO] Profile ", sys.argv[1],  " created "
    else:    
        print "[INFO] Profile ", sys.argv[1],  " already exists"

    if sys.argv[2] == "homeowner":
         f = open("homeowners.txt", "a+")  
         f.write('\n')  
         f.write(sys.argv[1])

if __name__ == '__main__':
    main()
