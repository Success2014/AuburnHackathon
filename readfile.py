from os import listdir

def readfile(directory):
    l = listdir(directory)
    l.sort()
    return l[l.len()-1]


    

    
