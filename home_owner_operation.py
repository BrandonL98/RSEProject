def print_owners():
    f = open("homeowners.txt", "r")
    output_string = ""
    for line in f:
        line = line.rstrip()  
        output_string = output_string + line + "\n"
    
    return output_string
    

def delete_owner(name):
    with open("homeowners.txt", "r") as f:
        lines = f.readlines()
        print(lines)

    with open("homeowners.txt", "w") as f:
        for line in lines:
            if line.strip("\r\n") != name:
                f.write(line)