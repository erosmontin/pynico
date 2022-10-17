import datetime
import os
import json
import tarfile
import tempfile

def createTemporaryPosition(fn='',tmp=None):
    if not tmp:
        tmp = tempfile.gettempdir()
    return os.path.join(tmp,fn)
        
def unTarGz(fname):
    tar = tarfile.open(fname, "r:gz")
    tar.extractall()
    tar.close()

def unTar(fname):
    tar = tarfile.open(fname, "r:")
    tar.extractall()
    tar.close()

def readJson(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def writeJsonFile(filename,data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

import pickle

def readPkl(filename):
    with open(filename) as f:
        data = pickle.load(f)
    return data

def writePkl(filename,data=[]):
        pickle.dump(data, filename)

class Node:
    def __init__(self,val) -> None:
        self.value=val
        self.next=None

class Stack:
    def __init__(self) -> None:
        self.top =None
        self.stackSize=0
    
    def push(self,val):
        node = Node(val)
        node.next = self.top
        self.top= node
        self.stackSize+=1
    
    def pop(self):
        if self.top:
            value= self.top.value
            self.top = self.top.next
            self.stackSize-=1
            return value
        else:
            raise Exception('Stack is empty')    
        
    def peek(self):
        if self.top:
            return self.top.value
        else:
            raise Exception('stack is empty')
    def size(self):
        return self.stackSize




class Log:
    """ A Log Class.
    Just append to the log and we take care of the timing.
    You can set the format of the time.
    
    .. note::
        This function is not suitable for sending spam e-mails.

    .. todo:: 
        - Validate all post fields
        - dededede
    """    
  
    def __init__(self,init=None):
        self.format="%d/%m/%Y, %H:%M:%S"
        self.now=datetime.datetime.now()
        self.version='v0.0v'
        self.dflts='procedure'
        self.dflte='ERROR'
        if init is None:
            init="Log (" + self.version + ")"

        self.log=[{"when":self.getFormattedDatetime(self.now),"what":init,"type":"start","settings":{"author":"Eros Montin","mail":"eros.montin@gmail.com","motto":"Forty-six and two are just ahead of me"}}]
    def setTimeFormat(self,f):
        self.format=f
        #  should validate this at some point TODO
        return True

    def getFormattedDatetime(self,t):
        return t.strftime(self.format)
    def getNow(self):
        return self.getFormattedDatetime(datetime.datetime.now())
    def setDefaultType(self,f):
        if isinstance(f,str):
            self.dflts=f
            return True
        else:
            return False
    def getDefaultType(self):
        return self.dflts
    
    def setDefaultError(self,f):
        if isinstance(f,str):
            self.dflte=f
            return True
        else:
            return False
    def getDefaultError(self):
        return self.dflte

    def appendError(self,m=None):
        if m is None:
            m="ERROR"
        self.append(m,self.getDefaultError())

    def append(self,message,type=None,settings=None):
        """append the current message to the log using the time of the call

        Args:
            - message (_type_): The message to be logged.
            - type (_type_, optional): a tag good for automatic identification of type, for example ERROR or DONE. Defaults to "flow". but you can customize to set custom message
            - settings (_type_, optional): a dictoinary of options. Defaults to None.
        """        
        if type is None:
            type=self.getDefaultType()

        self.log.append({"when":self.getNow(),"what":message,"type":type,"settings":settings})
    def appendFullLog(self,fn):
        if isinstance(fn,str):
            L=readJson(fn)
        elif isinstance(fn,Log):
            L=fn.getLog()
        else:
            return False
        for l in L:
            self.log.append(l)
        return True
        

    def getWhatHappened(self):
        self.printWhatHappened()

    def printWhatHappened(self):
        """print the events logged
        """        
        for l in self.log:
            print(l)
    
    def getLog(self):
        """gett the events logged
        """
        return self.log
    
    def writeLogAs(self,fn):
        try:
            with open(fn, 'w') as fout:
                json.dump(self.getLog(), fout)
            return True
        except:
            return False
    
    def saveLogAs(self,fn):
        return self.writeLogAs(fn)
    



import subprocess

class BashIt:
    def __init__(self) -> None:
        self.bashCommand=None
        self.Log=Log('Bash')
    def setCommand(self,comm):
        self.bashCommand=comm
        self.Log.append(f'added command {comm}')
    def getCommand(self):
        return self.bashCommand
    def run(self):
        self.Log.append(f'running')
        bashCommand=self.getCommand()
        if bashCommand is not None:
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            self.Log.append(f'running {bashCommand}')
            self.output, self.error = process.communicate()
            if not self.error:
                process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE,shell=True)
                self.output, self.error = process.communicate()
            self.Log.append(f'completed {bashCommand}')
            return True
        else:
            return False


    def getBashError(self):
        return self.error
    
    def getBashOutput(self):
        return self.output





import os
class GarbageCollector(object):
    def __init__(self) -> None:
        self.trashbin=Stack() #list of trash
    def __len__(self):
        return self.trashbin.size()

    def trash(self):
        
        while len(self):
            a=self.undo()
            try:
                if os.path.isfile(a):
                    os.remove(a)
                elif os.path.isdir(a):
                    os.rmdir(a)
                else:
                    raise Exception("what's that??")
                
                print(f'{a} removed')
            except:
                print(f'nope! {a} was not removed')

    def __del__(self):
        self.trash()
    def undo(self):
        if len(self)>0:
            return self.trashbin.pop()
        else:
            return None
    def peek(self):
        return self.trashbin.pop()

    def throw(self,f):
        self.trashbin.push(f)
    
    def append(self,f):
        #just an alias
        self.throw(f)
    



import time
class Timer():  
    """_summary_
    frfrfr
    frfrfr
    frfrfr
    frfrfr
    """    
    def __init__(self):
        self.times = []
        self.start()

    def start(self):
        """Start the timer."""
        self.tik = time.time()

    def stop(self):
        """Stop the timer and record the time in a list."""
        self.times.append(time.time() - self.tik)
        return self.times[-1]

    def avg(self):
        """Return the average time."""
        return sum(self.times) / len(self.times)

    def sum(self):
        """Return the sum of time."""
        return sum(self.times)

    def getStops(self):
        """Return the stops time."""
        return self.times

def splitext_(path):
    if len(path.split('.')) > 1:
        # return path.split('.')[0],'.'.join(path.split('.')[-2:])
        S = path.split('.')
        PT = S[0]
        E = ''
        for s in range(1, len(S)):
            if s == 1:
                E = E + S[s]
            else:
                E = E + '.' + S[s]
        return PT, E
    return path, None

import uuid
import glob
import mimetypes
from pathlib import PurePath,Path
class Pathable:
    """extract info from a file position"""

    def __init__(self, position):
        self.positionStack =Stack()
        self.positionStack.push(position)

    def isDir(self):
        if self.exists():
            return os.path.isdir(self.getPosition())
        else:
            return not self.getExtension()

        
    def touch(self):
        if self.isFile():
            self.ensureDirectoryExistence()
            Path(self.getPosition()).touch()

    def isFile(self):
        if self.exists():
            return os.path.isfile(self.getPosition())
        else:
            return len(self.getExtension())>0

    def exists(self):
        pt=self.getPosition()
        return (os.path.isdir(pt) or os.path.isfile(pt))
    
    def getPath(self):
        file_name, *_= splitext_(self.getPosition())
        return os.path.dirname(file_name)

    def getBaseName(self):
        return os.path.basename(self.getPosition())
    
    def getBaseNameWithoutExtension(self):
        l=splitext_(os.path.basename(self.getPosition()))
        return l[0]

    def getExtension(self):
        _, extension = splitext_(self.getPosition())
        return extension

    def getFileName(self):
        return self.getBaseName()
    
    def getFileNameWithoutExtension(self):
        return self.getBaseNameWithoutExtension()

    def getPosition(self):
        return self.positionStack.peek()

    def getPositionWithPrefix(self, prefix):
        N = self.getBaseName()
        P = self.getPath()
        return os.path.join(P, prefix + N)
    def setPosition(self,p):
        self.positionStack.push(p)
    def undo(self):
        if self.positionStack.size()>1:
            return self.positionStack.pop()
    #change
    def changePath(self,path):
        """Change the path of the position

        Args:
            path (str): new path to join tho the name

        Returns:
            _type_: the new position
        """        
        basename=self.getBaseName()
        self.setPosition(os.path.join(path,basename))
        return self

    def changePathToOSTemporary(self):
        """Change the path of the position to os tmp

        Args:

        Returns:
            _type_: the new position
        """        
        return self.changePath(tempfile.gettempdir())
    
    def changeBaseName(self,name):
        pt=self.getPath()
        self.setPosition(os.path.join(pt,name))
        return self
    

    def changeBaseNameWithoutExtension(self,name=None):
        pt=self.getPath()
        E=self.getExtension()
        if not name:
            name=str(uuid.uuid4())
        if E[0]== '.':
            E=E[1:] 
        self.setPosition(os.path.join(pt,name + '.' + E))
        return self

    def changeFileName(self,name):
        return self.changeBaseName(name)

    def changeFileNameWithoutExtension(self,name=None):
        return self.changeBaseNameWithoutExtension(name)
    
    def addSuffix(self,suf):
        return self.changePositionSuffixPrefix(suffix=suf)
        
    def appendPath(self,np):
        pt=self.getPath()
        return self.changePath(os.path.join(pt,np))
    
    def appendPathRandom(self):

        return self.appendPath(str(uuid.uuid4()))
    
    def removeLastPath(self):
        pt=self.getPath()
        path_split = PurePath(pt).parts
        p=path_split[0]
        for t in path_split[1:-1]:
            p=os.path.join(p,t)
        return self.changePath(p)

    def addPrefix(self,pre):
        if self.isFile():
            return self.changePositionSuffixPrefix(prefix=pre)

    def addPrefixAndSuffix(self,pre,suf):
        if self.isFile():
            return self.changePositionSuffixPrefix(prefix=pre,suffix=suf)
    
    def changePositionSuffixPrefix(self, suffix=None,prefix=None):
        if self.isFile():
            N = self.getBaseNameWithoutExtension()
            E = self.getExtension()
            if E[0]== '.':
                ext=ext[1:] 
            if suffix:
                o=self.changeBaseName(N + suffix + '.' + E)
                N = self.getBaseNameWithoutExtension()
            if prefix:
                o=self.changeBaseName(prefix + N +'.' + E)
            return o

    def changeExtension(self,ext):
        if self.isFile():
            N = self.getBaseNameWithoutExtension()
            E = self.getExtension()
            if ext[0]== '.':
                ext=ext[1:] 
            return self.changeBaseName(N+"."+ext)
        
    def changeBaseNameWithoutExtensionRandom(self):
        if self.isFile():
            return self.changeBaseNameWithoutExtension()
    
    def ensureDirectoryExistence(self):
        try:
            os.makedirs(self.getPath(), exist_ok=True)
        except:
            raise Exception(f" can't write on {self.getPosition()}")
            

    def getFilesInPathByExtension(self,ext=None,sort=True):
        
        if ext:
            E=ext
        else:
            E=self.getExtension()
        if E[0]== '.':
            E=E[1:] 
        
        pt=self.getPath()

        L=glob.glob(os.path.join(pt,'*.'+E))
        if sort:
            return sorted(L)
        else:
            return L

    def getFilesInPathByExtensionAndPattern(self,pattern=None,ext=None,sort=True):
        
        if ext:
            E=ext
        else:
            E=self.getExtension()
        if E[0]== '.':
            E=E[1:] 
        
        pt=self.getPath()

        L=glob.glob(os.path.join(pt,pattern +'*.'+E))
        

        if sort:
            return sorted(L)
        else:
            return glob.glob(L)
    

    def getFilesInPathByPattern(self,pattern=None,sort=True):
        
        pt=self.getPath()

        L=glob.glob(os.path.join(pt,pattern))
        

        if sort:
            return sorted(L)
        else:
            return glob.glob(L)
    def getMiMEFileType(self):
        if self.isFile():
            return  mimetypes.guess_type(self.getPosition())
    
    def getFileType(self):
        if self.isFile():
            mime=self.getMiMEFileType()
            return mime[0].split('/')[0]
    
    def createPositionPath(self):
        return self.ensureDirectoryExistence()
    
    def renamePath(self,old,new):
        pt=self.getPath()
        path_split = PurePath(pt).parts
        p=path_split[0]
        for t in path_split[1:]:
            if t == old:
                t=new
            p=os.path.join(p,t)

        return self.changePath(p)
    
    
class PathableTemp(Pathable):
    def __init__(self,filename):
        super().__init__(createTemporaryPosition(filename))

    