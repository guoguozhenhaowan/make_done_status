from collections import defaultdict
#from pysnooper import snoop

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

def afterlist_(Node):
    list1 = []
    if Node.tail:
        for sub in Node.tail:
            list1.append(sub.string)
            list1.extend(afterlist_(sub))
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
            for sub in NodePattern.split("|"):
                if sub in Node1.string:
                    Nodelist.append(Node1)
                if sub in Node2.string:
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

from itertools import groupby

def groupby_job(line):
    if line.startswith((" ","\t")):
        return "job"
    elif line.startswith("job"):
        return "job_mark"
    elif line.startswith("log"):
        return "dir"
    elif line.startswith("order"):
        return "order"
    else:
        return "other"

def parser_writeafterjob(jobfile,outlist):
    for groupname,group in groupby(open(jobfile),key=groupby_job):
        grouplist = list(group)
        #print(groupname,grouplist)
        if groupname in ["other","dir"]:
            for line in grouplist:
                print(line.strip("\n"))
        elif groupname=="job":
            name = grouplist[0].strip().split()[1]
            if name in outlist:
                print("job_begin")
                for line in grouplist:
                    if "status" == line.strip()[:6]:
                        split1 = line.strip().split()
                        line = line.strip("\n").replace(split1[1],"waiting")
                    print(line.strip("\n"))
                print("job_end")
        elif groupname=="order":
            for line in grouplist:
                name1 = line.strip().split()[1]
                name2 = line.strip().split()[3]
                if name1 in outlist and name2 in outlist:
                    print(line.strip())

def main(jobfile,jobpattern,ifNow=False, OnlyAfter=False,before_out=True):
    # ifNow contains the current cmd
    # OnlyAfter running for after or make done for before cmds
    # before_out only output before cmds when OnlyAfter is False
    Nodelist = parser_job(jobfile,jobpattern)
    nowlist = [Node.string for Node in Nodelist]
    beforelist = []
    afterlist = []
    for subNode in Nodelist:
        list1 = beforelist_(subNode)
        beforelist.extend(list1)
    for subNode in Nodelist:
        list1 = afterlist_(subNode)
        afterlist.extend(list1)
    if ifNow:
        outlist = set(beforelist) | set(nowlist)
        #print(outlist)
    else:
        outlist = set(beforelist)
    if OnlyAfter:
        if ifNow:
            outlist = set(afterlist) | set(nowlist)
        else:
            outlist = set(afterlist)
    # __import__('pdb').set_trace()
    if not OnlyAfter:
        #print(outlist)
        if before_out:
            parser_writeafterjob(jobfile,outlist)
        else:
            parser_writejob(jobfile,outlist)
    else:
        parser_writeafterjob(jobfile,outlist)

from fire import Fire
if __name__ == "__main__":
    Fire(main)
