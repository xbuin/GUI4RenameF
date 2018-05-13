# -*- coding: GB2312 -*-

'''
@author: xbuin
'''
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from time import sleep
import random

class MvFileGUI(object):
    '''
    classdocs
    '''

    def __init__(self, gui_title, vwidth, vheight):
        '''
        Constructor
        '''
        self.root_w = vwidth
        self.root_h = vheight
        self.rtitle = gui_title
        
        self.dirpath = ''
        
        self.v_rb = 0
        
        self.root = Tk()
        self.lb1 = Label(self.root, text='TargetDir: ')
        
        self.e1 = Entry(self.root, width=55)
        
        self.dirButton = Button(self.root, text='BROWSE', width=10, height=1, relief='groove', command=self.select_dirpath)
        
        self.verlb = Label(self.root, text="    Version 0.1\n")
        
        self.actButton = Button(self.root, text='DO IT', width=10, relief='groove', bg='green', command=self.button_act)
        
        self.quitButton = Button(self.root, text='EXIT', command=self.root.quit, width=10, height=1)
        
    def construct_rootfrm(self):
        self.root.title(self.rtitle)
        self.root.geometry('%dx%d+300+100' %(self.root_w, self.root_h))
        self.root.minsize(self.root_w, self.root_h)
        self.root.maxsize(self.root_w, self.root_h)
     
    def construct_radiobutton(self):
        self.lfm = LabelFrame(height=20, width=50, text='Select Function')
        self.lfm.grid(row=1, column=1)
        
        self.v_rb = StringVar()
        self.v_rb.set('v_listfile')
        self.listRB1 = Radiobutton(self.lfm, variable=self.v_rb, text='JustListFile', value='v_listfile')
        self.listRB1.grid(row=1, column=0)
        self.listRB2 = Radiobutton(self.lfm, variable=self.v_rb, text='RemoveDash', value='v_rmvdash')
        self.listRB2.grid(row=1, column=1)
        self.listRB3 = Radiobutton(self.lfm, variable=self.v_rb, text='AddRandKey', value='v_randkey')
        self.listRB3.grid(row=1, column=2)
        
    def construct_outbox(self):
        self.outfm = LabelFrame(text=' Output ')
        self.outfm.grid(row=2, column=0, columnspan=3, pady=6)
    
        self.outText = Text(self.outfm)
        self.outText.grid(padx=2)
        # outText.config(font=("arial", 9))
        self.outText.bind("<KeyPress>", lambda e : "break")
    
        self.scrollb = Scrollbar(self.outfm, command=self.outText.yview)
        self.scrollb.grid(row=0, column=1, sticky='nsew')
        self.outText['yscrollcommand'] = self.scrollb.set
           
        
    def construct_wgt(self):
        self.construct_rootfrm()
        
        self.lb1.grid(row=0, column=0, pady=10, padx=5)
        
        self.e1.grid(row=0, column=1, padx=10, pady=10)
        
        self.dirButton.grid(row=0, column=2, padx=10, pady=10)
        
        self.verlb.grid(row=1, column=0, pady=0)
        
        self.construct_radiobutton()
        
        self.actButton.grid(row=1, column=2, pady=10)
        
        self.construct_outbox()
        
        self.quitButton.grid(row=4, column=1)
        
        
    def launch_gui(self):
        self.construct_wgt()
        mainloop()
        
    def button_act(self):
        if self.dirpath == '':
            self.errorDiag()
            
        r_dirpath = self.dirpath.replace('/', '\\\\')
        
        if self.v_rb.get() == 'v_listfile':
            self.listfiles(r_dirpath)
        elif self.v_rb.get() == 'v_rmvdash':
            self.rmvdash(r_dirpath)
        elif self.v_rb.get() == 'v_randkey':
            self.addrandkey(r_dirpath)
        else:
            print 'Please select a value, %d' % self.v_rb.get()
        pass
        
    def select_dirpath(self):
        self.dirpath = tkFileDialog.askdirectory(parent=self.root, initialdir="F:/", title="Select a Directory")
        self.e1.delete(0, END)
        self.e1.insert(0, self.dirpath)
        
    def listfiles(self, d_path):
        f_num = 0
        d_num = 0
        os.chdir(d_path)
        contentlist = os.listdir('.')
        
        self.prt2obox('******************************************************')
        self.prt2obox('INFO: [%d] ITEMS TO BE LISTED', len(contentlist))
        self.prt2obox('******************************************************')
        
        for filei in contentlist:
            if os.path.isdir(filei):
                d_num += 1
                msg = "[D]: " + filei
            else:
                f_num += 1
                msg = "[F]: " + filei
             
            self.prt2obox(msg)   
            sleep(0.1)

        self.prt2obox("\n****** [%d] FILES & [%d] DIRECTORIES ARE LISTED ******\n", f_num, d_num)
        
    
    def rmvdash(self, d_path):
        os.chdir(d_path)
        contentlist = os.listdir('.')

        self.prt2obox('******************************************************')
        self.prt2obox('INFO: [%d] ITEMS TO BE PROCESSED', len(contentlist))
        self.prt2obox('******************************************************')

        exnamelist = []
        duplist = []
        j = 0
        file_named_num = 0

        for fname in contentlist:
            j = j + 1
            if os.path.isdir(fname):
                # print 'WARNING: [%s] is directory, not supported, continue' %fname
                self.prt2obox("*** WARNING: [%s] is directory, not supported, continue", fname)
                exnamelist.append(fname)
                continue
    
            newname = rename_str_after_dash(fname)    
    
            if newname == None:
                #print 'WARNING: Can NOT change [%s], key word is not found.' %fname
                self.prt2obox("*** WARNING: Can NOT change [%s], key word is not found.", fname)
                exnamelist.append(fname)
                continue

            if newname not in exnamelist:
                #print '%d: SUCCEED: [%s] -->> [%s]' %(j, fname, newname)
                self.prt2obox("%d: SUCCEED: [%s] ==>> [%s]", j, fname, newname)
                os.rename(fname, newname)
                exnamelist.append(newname)
                file_named_num += 1
            else:
                #print '!!!WARNING: %s can\'t be renamed due to duplication.' %newname
                self.prt2obox("*** WARNING: %s can\'t be renamed due to duplication.", newname)
                duplist.append(fname)

            sleep(0.2)
    
        # print '\n ----- %d files are not renamed due to duplicate name -----' %len(duplist)
        if len(duplist) == 0:
            self.prt2obox("\n****** [%d] FILES ARE RENAMED SUCCESSFULLY ******\n", file_named_num)
        else:
            self.prt2obox("\n****** [%d] FILES ARE NOT RENAMED DUE TO DUPLICATED NAME ******\n", len(duplist))
            
        for df in duplist:
            rname = rename_remove_dash(df)
            if rname == None:
                continue
    
            if rname in exnamelist:
                #print 'can not change again'
                self.prt2obox("*** WARNING: %s can't be used any more.", rname)
            else:
                # print 'INFO: Try to rename [%s] to [%s].' %(df, rname)
                self.prt2obox("DUP_NAME: please try renaming [%s] to [%s].", df, rname)
                exnamelist.append(df)
    
            sleep(0.2)
    
    def addrandkey(self, d_path):
        os.chdir(d_path)
        contentlist = os.listdir('.')

        self.prt2obox('******************************************************')
        self.prt2obox("INFO: %d ITEMS TO BE PROCESSED", len(contentlist))
        self.prt2obox('******************************************************')

        idlist = []
        exnamelist = []
        duplist = []
        j = 0
        file_named_num = 0

        genidlist(4, len(contentlist), idlist)

        for fname in contentlist:
            j += 1
    
            if os.path.isdir(fname):
                self.prt2obox("*** WARNING: [%s] is directory, not supported, continue", fname)
                exnamelist.append(fname)
                continue

            ####################################################
            # Replace the correct rename function here         #
            ####################################################
    
            newname = idlist[j-1] + ' - ' + fname

            if newname not in exnamelist:
                self.prt2obox("%d: SUCCEED: [%s] ==>> [%s]", j, fname, newname)
                os.rename(fname, newname)
                file_named_num += 1
                exnamelist.append(newname)
            else:
                self.prt2obox("*** WARNING: %s can\'t be renamed due to duplication.", newname)
                duplist.append(fname)

    
            sleep(0.2)
    
        if len(duplist) == 0:
            self.prt2obox("\n****** [%d] FILES ARE RENAMED SUCCESSFULLY ******\n", file_named_num)
        else:
            self.prt2obox("\n****** [%d] FILES ARE NOT RENAMED DUE TO DUPLICATED NAME ******\n", len(duplist))

        for df in duplist:
            rname = rename_remove_dash(df)
            if rname == None:
                continue
    
            if rname in exnamelist:
                self.prt2obox("*** WARNING: %s can't be used any more.", rname)
            else:
                self.prt2obox("DUP_NAME: please try renaming [%s] to [%s].", df, rname)
                exnamelist.append(df)
    
            sleep(0.2)
    
    def errorDiag(self):        
        tkMessageBox.showerror("Invalid Directory", "Please select a valid directory first!")
        
    def prt2obox(self, basestr, *vargs):
        if len(vargs) != 0:
            fmtstr = basestr % vargs
        else:
            fmtstr = basestr
            
        fmtstr = fmtstr + '\n'
        fmtstr = fmtstr.decode('gbk')
        self.outText.insert(END, fmtstr)
        self.outText.update()
        self.outText.see(END)
        
def rename_str_after_dash(origname):
    i = origname.find('-')
    if i < 0:
        return None
    
    i = i + 1
    newname = origname[i:].strip()
    return newname
        
def rename_remove_dash(origname):
    i = origname.find('-')
    if i < 0:
        return None
    
    retstr = origname.split('-')
    newname = ''
    
    for s in retstr:
        newname = newname + ' ' + s.strip()
    
    newname = newname.strip()
    
    return newname        

def gen1char():
    
    i = random.randint(1, 26)
    ch = chr(64+i)
    return ch

def genidlist(nbit, num, idlist):
    
    j = 0
    dn = 0
    while(j < num):
        id4b = ''
        for i in range(nbit):
            id4b = id4b + gen1char()
        
        if idlist.count(id4b) == 0:
            idlist.append(id4b)
            j += 1
        else:
            dn += 1
            continue

        
if __name__ == '__main__':
    
    rn_gui = MvFileGUI('XBUIN', 595, 487)
    rn_gui.launch_gui()
    
    
