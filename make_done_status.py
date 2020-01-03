from collections import defaultdict
from pysnooper import snoop

class Node:
    def __init__(self,string):
        self.head = []
        self.tail = []
        self.string = string 

    def add_tail(self, other):
        self.tail.append(other)
        other.head.append(self)

    def add_head(self,other):
        self.head.append(other)
        other.tail.append(self)
    
    def result(self):
        return self.string
    
    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

def beforelist_(Node):
    list1 = []
    if  Node.head:
        for sub in Node.head:
            list1.append(sub.string)
            list1.extend(beforelist_(sub))
    return list1        

def parser_job(jobfile,NodePattern):
    stringlist = []
    TotalNodelist = []
    Nodelist = []
    for line in open(jobfile):
        if line.strip().startswith("order"):
            _,a,after,b = line.strip().split()
            
            if not a in stringlist:
                stringlist.append(a)
                TotalNodelist.append(Node(a))
            if not b in stringlist:
                stringlist.append(b)
                TotalNodelist.append(Node(b))
                        
            if after == "after":
                Node1 = TotalNodelist[stringlist.index(b)] 
                Node2 = TotalNodelist[stringlist.index(a)]
            else:
                Node1 = TotalNodelist[stringlist.index(a)] 
                Node2 = TotalNodelist[stringlist.index(b)]
            Node1.add_tail(Node2)    
            if NodePattern in Node1.string:
                Nodelist.append(Node1)
            if NodePattern in Node2.string:
                Nodelist.append(Node2)
    return Nodelist

def parser_writejob(jobfile,namelist):
    for line in open(jobfile):
        split1 = line.strip().split()
        if split1[0] == "name":
            jobname = split1[1]
            print(line.strip("\n"))
        elif split1[0] == "status":
            if jobname in namelist:
                print(line.strip("\n").replace(split1[1],"done"))
            else:
                print(line.strip("\n"))
        else:
            print(line.strip("\n"))
    
def main(jobfile,jobpattern,ifNow=False):
    Nodelist = parser_job(jobfile,jobpattern)
    nowlist = [Node.string for Node in Nodelist]
    beforelist = []
    for subNode in Nodelist:
        list1 = beforelist_(subNode)
        beforelist.extend(list1)
    if ifNow:    
        outlist = set(beforelist) | set(nowlist)    
    else:
        outlist = set(beforelist)
    parser_writejob(jobfile,outlist)

from fire import Fire            
if __name__ == "__main__":    
    Fire(main)
    
