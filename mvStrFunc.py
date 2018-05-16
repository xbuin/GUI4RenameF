# test for main functions

import os
import sys

idlists = {'a', 'b', 'c', 'd'}

def addID2Name(filename, idset, idx):
    idlist = list(idset)
    newname = idlist[idx] + '-' + filename
    return newname

def replaceSpecStr(filename, repstr, newstr):
    print 'File name is: ', filename
    print "Str replaced: ", repstr
    print "New str: ", newstr
    if repstr not in filename:
        print "No " + repstr + " in file name, exit."
        return None

    newname = filename.replace(repstr, newstr, 1)
    return newname


def mvFileName(filename, mvfunc, *keys):
    
    if mvfunc == replaceSpecStr:
        repstr=keys[0]
        newstr=keys[1]
        if repstr == '':
            print 'No original string specified, error'
            return
        newname = mvfunc(filename, repstr, newstr)
        print newname

    elif mvfunc == addID2Name:
        idset = keys[0]
        for j in range(0, 4):
            newname = mvfunc(filename, idset, j)
            print newname

    print "CMD is DONE!!!"

    return

if __name__ == '__main__':
    mvFileName('binx_test_file.log', replaceSpecStr, 'test_', '')
    mvFileName('binx_test_file.log', addID2Name, idlists)
    
