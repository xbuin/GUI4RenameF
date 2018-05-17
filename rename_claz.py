# -*- coding: UTF-8 -*-

'''
@author: xbuin
'''
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from time import sleep
import random


# Rename files with specified suffix
# If the file name has extension, add the suffix before extension.
def rename_suffix_str(origname, *keys):
    sufixstr = keys[0]
    idx = origname.rindex('.')

    if idx < 0:
        newname = origname + sufixstr
    else:
        p1 = origname[0:idx]
        p2 = origname[idx:]
        newname = p1 + sufixstr + p2

    return newname

# add prefix to the file name
def rename_prefix_str(origname, *keys):
    prefixstr = keys[0]
    newname = prefixstr + origname
    return newname

# replace specified string in the file name with new string.
def rename_replace_spec_str(origname, *keys):
    repstr = keys[0]
    newstr = keys[1]
    if repstr not in origname:
        return None

    newname = origname.replace(repstr, newstr, 1)
    return newname

# Rename the file with the string after '-'.
def rename_str_after_dash(origname, *keys):
    i = origname.find('-')
    if i < 0:
        return None

    i = i + 1
    newname = origname[i:].strip()
    return newname

# Add random key to the original file name
def rename_rand_key(origname, randkey):
    newname = randkey + ' - ' + origname
    return newname

# Only remove the '-' in the file name
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

# Generate one random character
def gen1char():

    i = random.randint(1, 26)
    ch = chr(64+i)
    return ch

# Generate random keys with num bytes.
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

############################################################
# Class of GUI for renaming files in specified ways.
############################################################
class MvFileGUI(object):
    '''
    classdocs
    '''

    def __init__(self, gui_title, vwidth, vheight):
        '''
        Constructor
        '''
        # root frame properties
        self.root_w = vwidth
        self.root_h = vheight
        self.rtitle = gui_title

        # The directory path to operate
        self.dirpath = ''
        self.v_func = ''        

    # construct the root frame per width and height
    def construct_rootfrm(self):
        self.root = Tk()
        self.root.title(self.rtitle)
        self.root.geometry('%dx%d+300+100' % (self.root_w, self.root_h))
        self.root.minsize(self.root_w, self.root_h)
        self.root.maxsize(self.root_w, self.root_h)

    # construct the function group with radiobutton
    def construct_radiobutton(self):
        self.lfm = LabelFrame(height=20, width=50, text='操作选项')
        self.lfm.grid(row=1, column=1)

        # Pre-set the default function to listfile
        self.v_func = StringVar()
        self.v_func.set('v_listfile')

        # Construct the first function line
        self.listRB1 = Radiobutton(
            self.lfm, variable=self.v_func, text='仅列出文件', value='v_listfile')
        self.listRB1.grid(row=1, column=0)
        self.listRB2 = Radiobutton(
            self.lfm, variable=self.v_func, text='去除破折号', value='v_rmvdash')
        self.listRB2.grid(row=1, column=1)
        self.listRB3 = Radiobutton(
            self.lfm, variable=self.v_func, text='添加随机值', value='v_randkey')
        self.listRB3.grid(row=1, column=2, padx=7)

        # construct the name string replacement line
        self.replaceRB4 = Radiobutton(
            self.lfm, variable=self.v_func, text='替换旧字符', value='v_replacestr')
        self.replaceRB4.grid(row=2, column=0, sticky=W)
        self.repRawEntry = Entry(self.lfm, width=12)
        self.repRawEntry.grid(row=2, column=1, sticky=W)
        self.withstr = Label(self.lfm, text="新值")
        self.withstr.grid(row=2, column=2, sticky=W)
        self.repNewEntry = Entry(self.lfm, width=10)
        self.repNewEntry.grid(row=2, column=2, sticky=E, padx=6)

        # construct the prefix and suffix line
        self.prefixRB5 = Radiobutton(
            self.lfm, variable=self.v_func, text='添加前缀', value='v_addprefix')
        self.prefixRB5.grid(row=3, column=0, sticky=W)
        self.suffixRB6 = Radiobutton(
            self.lfm, variable=self.v_func, text='添加后缀', value='v_addsuffix')
        self.suffixRB6.grid(row=3, column=1, sticky=W)
        self.withfix = Label(self.lfm, text="字符")
        self.withfix.grid(row=3, column=2, sticky=W)
        self.fixstrEntry = Entry(self.lfm, width=10)
        self.fixstrEntry.grid(row=3, column=2, sticky=E, padx=6)

    # Construct the output box
    def construct_outbox(self):
        self.outfm = LabelFrame(text=' 操作日志 ')
        self.outfm.grid(row=2, column=0, columnspan=3, pady=6)

        self.outText = Text(self.outfm)
        self.outText.grid(padx=2)
        # outText.config(font=("arial", 9))
        self.outText.bind("<KeyPress>", lambda e: "break")

        self.scrollb = Scrollbar(self.outfm, command=self.outText.yview)
        self.scrollb.grid(row=0, column=1, sticky='nsew')
        self.outText['yscrollcommand'] = self.scrollb.set

    # Construct the main user GUI
    def construct_wgt(self):
        self.construct_rootfrm()

        # widget for select directory
        self.dirLable = Label(self.root, text='操作目录: ')
        self.dirLable.grid(row=0, column=0, pady=10, padx=5)

        self.dirEntry = Entry(self.root, width=55)
        self.dirEntry.grid(row=0, column=1, padx=10, pady=10)

        self.dirButton = Button(self.root, text='浏览...', width=10,
                                height=1, relief='groove', command=self.select_dirpath)
        self.dirButton.grid(row=0, column=2, padx=10, pady=10)

        # version information
        self.verionLabel = Label(self.root, text="    Version 0.1\n    2018.05.17")
        self.verionLabel.grid(row=1, column=0, pady=0)

        # function group
        self.construct_radiobutton()

        # work button
        self.actButton = Button(self.root, text='执行', width=10,
                                relief='groove', bg='orange', command=self.button_act)
        self.actButton.grid(row=1, column=2, pady=10)

        # output box
        self.construct_outbox()

        # exit button
        self.quitButton = Button(
            self.root, text='EXIT', command=self.root.quit, width=10, height=1)
        self.quitButton.grid(row=4, column=1)

    # Bring up the main GUI
    def launch_gui(self):
        self.construct_wgt()
        mainloop()

    # Processing function for work button
    def button_act(self):
        if self.dirpath == '':
            self.errorDiag("Invalid Directory",
                           "Please select a valid directory first!")
            return

        r_dirpath = self.dirpath.replace('/', '\\\\')

        if self.v_func.get() == 'v_listfile':
            self.listfiles(r_dirpath)

        elif self.v_func.get() == 'v_rmvdash':
            self.mvFileName(r_dirpath, rename_str_after_dash, '', '')

        elif self.v_func.get() == 'v_randkey':
            self.mvFileName(r_dirpath, rename_rand_key, '', '')

        elif self.v_func.get() == 'v_replacestr':
            ostr = self.repRawEntry.get().encode('gbk')
            nstr = self.repNewEntry.get().encode('gbk')
            self.mvFileName(r_dirpath, rename_replace_spec_str, ostr, nstr)

        elif self.v_func.get() == 'v_addprefix':
            prestr = self.fixstrEntry.get().encode('gbk')
            self.mvFileName(r_dirpath, rename_prefix_str, prestr, '')

        elif self.v_func.get() == 'v_addsuffix':
            sufstr = self.fixstrEntry.get().encode('gbk')
            self.mvFileName(r_dirpath, rename_suffix_str, sufstr, '')

        else:
            print 'Please select a value, %d' % self.v_func.get()

        pass

    # get the directory path and fill it in dir entry
    def select_dirpath(self):
        self.dirpath = tkFileDialog.askdirectory(
            parent=self.root, initialdir="F:/", title="Select a Directory")

        # replace char / for display in dir entry
        dirStr = self.dirpath.replace('/', '\\')

        self.dirEntry.delete(0, END)
        self.dirEntry.insert(0, dirStr)

    # List the files in the specified directory
    def listfiles(self, d_path):
        f_num = 0
        d_num = 0
        os.chdir(d_path)
        contentlist = os.listdir('.')

        self.prtHeadInfo('listing', len(contentlist))

        for filei in contentlist:
            if os.path.isdir(filei):
                d_num += 1
                msg = "[D]: " + filei
            else:
                f_num += 1
                msg = "[F]: " + filei

            self.prt2obox(msg)
            sleep(0.1)

        self.prt2obox(
            "\n------ [%d] FILES & [%d] FOLDERS LISTED ------\n", f_num, d_num)

    # The entry point to invoke real renaming functions.
    def mvFileName(self, d_path, mvFunc, *keys):
        os.chdir(d_path)
        contentlist = os.listdir('.')

        # Pre-check for special renaming functions
        if mvFunc == rename_replace_spec_str:
            oldstr = keys[0]
            if oldstr == '':
                self.errorDiag(
                    "Null String", "The string to be replaced can not be none!")
                return

        elif mvFunc == rename_prefix_str:
            prefixstr = keys[0]
            if prefixstr == '':
                self.errorDiag(
                    "Null String", "The prefix string must not be none!")
                return

        elif mvFunc == rename_rand_key:
            idlist = []
            genidlist(4, len(contentlist), idlist)
            if len(idlist) != len(contentlist):
                self.errorDiag(
                    "Invalid Keys", "Failed to generate random key!")
                return

        self.prtHeadInfo('process', len(contentlist))

        exnamelist = []
        duplist = []
        j = 0
        file_named_num = 0

        for fname in contentlist:
            j = j + 1
            if os.path.isdir(fname):
                self.prt2obox(
                    "*** WARNING: [%s] is directory, not supported, continue", fname)
                exnamelist.append(fname)
                continue

            # Get new file name per specified function
            if mvFunc == rename_rand_key:
                newname = mvFunc(fname, idlist[j-1])
            else:
                newname = mvFunc(fname, keys[0], keys[1])

            if newname == None:
                self.prt2obox(
                    "*** WARNING: Can NOT change [%s], key word is not found.", fname)
                exnamelist.append(fname)
                continue

            if newname not in exnamelist:
                self.prt2obox("%d: SUCCEED: [%s] ==>> [%s]", j, fname, newname)
                os.rename(fname, newname)
                exnamelist.append(newname)
                file_named_num += 1
            else:
                self.prt2obox(
                    "*** WARNING: %s can\'t be renamed due to duplication.", newname)
                duplist.append(fname)

            sleep(0.2)

        if len(duplist) == 0:
            self.prt2obox(
                "\n------ [%d] FILES ARE RENAMED SUCCESSFULLY ------\n", file_named_num)
        else:
            self.prt2obox(
                "\n------ [%d] FILES ARE NOT RENAMED DUE TO DUPLICATED NAME ------\n", len(duplist))

        for df in duplist:
            rname = rename_remove_dash(df)
            if rname == None:
                continue

            if rname in exnamelist:
                self.prt2obox("*** WARNING: %s can't be used any more.", rname)
            else:
                self.prt2obox(
                    "*** DUP_NAME: please try renaming [%s] to [%s].", df, rname)
                exnamelist.append(df)

            sleep(0.2)

    # show up error diaglog
    def errorDiag(self, hinfo, msg):
        tkMessageBox.showerror(hinfo, msg)

    # print information in out box
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

    # Print header information
    def prtHeadInfo(self, type, num):
        self.prt2obox('============================================')

        if type == 'process':
            self.prt2obox('INFO: [%d] ITEMS TO BE PROCESSED', num)
        elif type == 'listing':
            self.prt2obox('INFO: [%d] ITEMS TO BE LISTED', num)

        self.prt2obox('--------------------------------------------')

# test func
if __name__ == '__main__':
    rn_gui = MvFileGUI('RenameGUI', 595, 525)
    rn_gui.launch_gui()