import datetime
import os
import json
import tarfile
import tempfile
from typing import Tuple, List, Union, Any, Optional
import copy
import csv
import hashlib
import shutil
import time
import subprocess
import shlex
import stat
import uuid
import glob
import mimetypes
from pathlib import PurePath, Path
import platform
import getpass
import collections.abc
import pickle

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


def sanitize_for_json(data: Any) -> Any:
    """Recursively sanitize data to make it JSON serializable."""
    if isinstance(data, dict):
        return {k: sanitize_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_for_json(v) for v in data]
    elif isinstance(data, (int, float, str, bool, type(None))):
        return data
    else:
        return str(data)  # Convert non-serializable types to strings


def getPackageVersion(pkg: str = 'pynico') -> Optional[str]:
    try:
        return version(pkg)
    except Exception:
        return None


def getPackagesVersion(PKG: List[str] = ['cloudmrhub','pynico','cmrawspy','pygrappa','twixtools','numpy','scipy','matplotlib','pydicom','SimpleITK','PIL']) -> dict:
    return {r: getPackageVersion(r) for r in PKG}


def calculateMd5(file_path: str, chunk_size: int = 8192) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as afile:
        while chunk := afile.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def securecopy(imagefilename: str, new_imagefilename: str, max_attempts: int = 4, md5: Optional[str] = None, delete_after_copy: bool = False, follow_symlinks: bool = False) -> dict:
    """Securely copy a file with MD5 verification."""
    if md5 is None:
        md5 = calculateMd5(imagefilename)
    for attempt in range(max_attempts):
        try:
            shutil.copy2(imagefilename, new_imagefilename, follow_symlinks=follow_symlinks)
            with open(new_imagefilename, 'rb') as f:
                os.fdatasync(f.fileno())  # Ensure data is written
            if md5 == calculateMd5(new_imagefilename):
                result = {"status": "ok", "message": "file copied", "md5": md5}
                if delete_after_copy:
                    os.remove(imagefilename)
                    with open(new_imagefilename, 'rb') as f:
                        os.fdatasync(f.fileno())
                return result
        except Exception as e:
            if attempt == max_attempts - 1:
                return {"status": "error", "message": f"file not copied after {max_attempts} attempts: {str(e)}"}
    return {"status": "error", "message": "file not copied"}


def isCollection(h: Any) -> bool:
    return isinstance(h, collections.abc.Collection) and not isinstance(h, (str, bytes, bytearray))


def forkPathable(x):
    return copy.deepcopy(x)


def createTemporaryPosition(fn: str = '', tmp: Optional[str] = None) -> str:
    if not tmp:
        tmp = tempfile.gettempdir()
    return os.path.join(tmp, fn)


def createRandomTemporaryPathableFromFileName(fn: str, tmp: Optional[str] = None):
    P = Pathable(createTemporaryPosition(fn, tmp))
    P = Pathable(P.changeBaseNameSafe().getPosition())
    P.ensureDirectoryExistence()
    return P


def createTemporaryPathableFromFileName(fn: str, tmp: Optional[str] = None):
    P = Pathable(createTemporaryPosition(fn, tmp))
    P.ensureDirectoryExistence()
    return P


def createTemporaryPathableDirectory(tmp: Optional[str] = None):
    if not tmp:
        tmp = createTemporaryPosition()
    P = Pathable(tmp)
    P.appendPathRandom()
    P.ensureDirectoryExistence()
    return P


def unTarGz(fname: str, extract_path: Optional[str] = None) -> None:
    if extract_path is None:
        extract_path = tempfile.mkdtemp()
    with tarfile.open(fname, "r:gz") as tar:
        tar.extractall(extract_path)


def unTar(fname: str, extract_path: Optional[str] = None) -> None:
    if extract_path is None:
        extract_path = tempfile.mkdtemp()
    with tarfile.open(fname, "r:") as tar:
        tar.extractall(extract_path)


def readJson(filename: str) -> Any:
    with open(filename) as f:
        return json.load(f)


def writeJsonFile(filename: str, data: Any) -> None:
    _data = copy.deepcopy(data)
    _data = sanitize_for_json(_data)
    with open(filename, 'w') as outfile:
        json.dump(_data, outfile)


def readCsv(filename: str) -> List[List[str]]:
    with open(filename, 'r') as f:
        return list(csv.reader(f))


def readPkl(filename: str) -> Any:
    with open(filename, 'rb') as f:
        return pickle.load(f)


def writePkl(filename: str, data: Any) -> None:
    if not isinstance(data, (list, tuple)):
        data = [data]
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


class Node:
    def __init__(self, val) -> None:
        self.value = val
        self.next = None


class Stack:
    def __init__(self) -> None:
        self.top = None
        self.stackSize = 0
    
    def push(self, val):
        node = Node(val)
        node.next = self.top
        self.top = node
        self.stackSize += 1
    
    def pop(self):
        if self.top:
            value = self.top.value
            self.top = self.top.next
            self.stackSize -= 1
            return value
        else:
            raise IndexError('pop from empty stack')
        
    def peek(self):
        if self.top:
            return self.top.value
        else:
            raise IndexError('peek from empty stack')
    
    def size(self):
        return self.stackSize
    
    def __len__(self):
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
  
    def __init__(self,firstmessage=None,settings=None):
        """_summary_

        Args:
            firstmessage (_type_, optional): "ddd", Defaults to None.
            settings (_type_, optional): {"De":0,"De2":0}. Defaults to None.
        """
        self.format="%d/%m/%Y, %H:%M:%S"
        self.now=datetime.datetime.now()
        self.version='v0.0v'
        self.dflts='procedure'
        self.dflte='ERROR'
        if firstmessage is None:
            firstmessage="init log"
        if settings is None:
            settings={"author":"Eros Montin","mail":"eros.montin@gmail.com","motto":"Forty-six and two are just ahead of me"}
        self.log=[{"when":self.getFormattedDatetime(self.now),"what":firstmessage,"type":"start","settings":settings,"version":self.version}]
        self.fn=createRandomTemporaryPathableFromFileName('log.json').getPosition()
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
    
    def mergeLog(self, log_source, log_name=None):
        """Merge an entire log into this log with an optional namespace.
        
        Each entry from the source log will be stored with a 'log_name' field
        to allow filtering by log source later.
        
        Args:
            log_source: Either a Log object, a list of log entries, or a filename (str) containing JSON log data
            log_name (str, optional): Name/namespace for this log source. If None, no namespace is added.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Get the log entries from the source
        if isinstance(log_source, str):
            try:
                entries = readJson(log_source)
            except:
                return False
        elif isinstance(log_source, Log):
            entries = log_source.getLog()
        elif isinstance(log_source, list):
            entries = log_source
        else:
            return False
        
        # Append each entry with the log_name namespace
        for entry in entries:
            entry_copy = copy.deepcopy(entry)
            if log_name is not None:
                entry_copy['log_name'] = log_name
            self.log.append(entry_copy)
        
        return True
    
    def getLogByName(self, log_name):
        """Retrieve all log entries for a specific log name/namespace.
        
        Args:
            log_name (str): The name/namespace of the log to retrieve
        
        Returns:
            list: List of log entries matching the given log_name
        """
        return [entry for entry in self.log if entry.get('log_name') == log_name]
    
    def getLogNames(self):
        """Get all unique log names/namespaces in this log.
        
        Returns:
            list: List of unique log_name values found in the log entries
        """
        names = set()
        for entry in self.log:
            if 'log_name' in entry:
                names.add(entry['log_name'])
        return sorted(list(names))

    def getWhatHappened(self):
        self.printWhatHappened()

    def printWhatHappened(self, log_name=None):
        """Print the events logged.
        
        Args:
            log_name (str, optional): If provided, only print entries from this log name/namespace
        """
        if log_name is None:
            for l in self.log:
                print(l)
        else:
            for l in self.getLogByName(log_name):
                print(l)
    
    def getLog(self, log_name=None):
        """Get the events logged.
        
        Args:
            log_name (str, optional): If provided, only return entries from this log name/namespace
        
        Returns:
            list: List of log entries (filtered by log_name if provided)
        """
        if log_name is None:
            return self.log
        else:
            return self.getLogByName(log_name)
    
    def writeLogAs(self,fn):
        try:
            with open(fn, 'w') as fout:
                json.dump(self.getLog(), fout)
            return True
        except:
            return False
    
    def saveLogAs(self,fn):
        return self.writeLogAs(fn)
    def dump(self,fn=None):
        if fn is None:
            fn=self.fn
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
            if self.error is not None:
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
import stat
class GarbageCollector(object):
    def __init__(self) -> None:
        self.trashbin=Stack() #list of trash
        self.force=False
        self.verbose=False
    def __len__(self):
        return self.trashbin.size()

    def setVerbose(self):
        self.verbose=True
    def setNoVerbose(self):
        self.verbose=False
        
    def trash(self):
        while len(self):
            a = self.undo()
            try:
                if os.path.isfile(a):
                    os.remove(a)
                elif os.path.isdir(a):
                    shutil.rmtree(a)
                if self.verbose:
                            print(f'{a} removed')
            except FileNotFoundError:
                if self.verbose:
                    print(f'{a} does not exist')
            except PermissionError:
                if self.force:
                    try:
                        os.chmod(a, stat.S_IWUSR)  # Change the file permissions
                        shutil.rmtree(a)
                        if self.verbose:
                            print(f'{a} removed')
                    except Exception as e:
                        if self.verbose:
                            print(f'nope! {a} was not removed. Reason: {str(e)}')
                else:
                    if self.verbose:
                        print(f'nope! {a} was not removed due to insufficient permissions')


            else:
                if self.verbose:
                    print(f'{a} does not exist')                

    def __del__(self):
        self.trash()
    def undo(self):
        if len(self)>0:
            return self.trashbin.pop()
        else:
            return None
    def peek(self):
        if self.trashbin.top:
            return self.trashbin.top.value
        return None

    def throw(self,f):
        self.trashbin.push(f)
    
    def append(self,f):
        #just an alias
        self.throw(f)
    def setForce(self):
        self.force=True

    def setNoForce(self):
        self.force=False

    def isForce(self):
        return self.force



class SudoGarbageCollector(GarbageCollector):
    def __init__(self) -> None:
        super().__init__()
        self.force=True
    
import time
class Timer():  
    """
    A simple timer class.
    
    """
    def __init__(self):
        self.times = []
        self.start()
        self.hdr=None

    def start(self,message=None):
        """Start the timer."""
        self.tik = time.time()
        self.hdr=message

    def stop(self,m=None):
        """Stop the timer and record the time in a list."""
        self.times.append({"time":time.time() - self.tik,"message":m})
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

    def show(self):
        """Print the stops time."""
        for t in self.times:
            print(t)    
    def toJson(self,filename):
        O= json.dumps(self.times)
        if filename:
            A=Pathable(filename)
            A.writeJson({"hdr":self.hdr,"times":self.times})
        return O

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
    """
    extract info from a file position
    Path:/data/
    Basename:aa.txt
    FileName:aa
    Extension:txt
    """

    def __init__(self, position):
        self.positionStack =Stack()
        if position:
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
        [PT,L]=os.path.split(self.getPosition())
        return PT

    def getBaseName(self):
        return os.path.basename(self.getPosition())

    def fork(self):
        """
        fork the current pathable

        Returns:
            _type_: _description_
        """
        return forkPathable(self)

    def duplicate(self):
        """alias for fork

        Returns:
            _type_: _description_
        """
        return self.fork()
    
    def getExtension(self):
        _, extension = splitext_(self.getPosition())
        return extension

    def getFileName(self):
        l=splitext_(os.path.basename(self.getPosition()))
        return l[0]    
    
    
    def getPosition(self):
        return self.positionStack.peek()


    def setPosition(self,p):
        self.positionStack.push(p)
        return self
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
    
    def changeBaseName(self,name=None):
        if not name:
            raise Exception("no filename specified did you want to change basename randomly? use changeFileName")
        pt=self.getPath()
        self.setPosition(os.path.join(pt,name))
        return self


    
    def changeFileName(self,name=None):
        pt=self.getPath()
        E=self.getExtension()
        if not name:
            name=str(uuid.uuid4())
        if E[0]== '.':
            E=E[1:] 
        return self.setPosition(os.path.join(pt,name + '.' + E))
        

    
    def addSuffix(self,suf):
        return self.changePositionSuffixPrefix(suffix=suf)
        
    def appendPath(self,np):
        pt=self.getPath()
        return self.changePath(os.path.join(pt,np))
    
    def appendPathRandom(self):
        return self.appendPath(str(uuid.uuid4()))
    
    
    
    def changePathToSafePath(self):
        self.appendPath(str(uuid.uuid4()))
        self.ensureDirectoryExistence()
        return self

    def changeBaseNameSafe(self,f=None):
        if f:
            O=Pathable(f)
            EXT=O.getExtension()
            if EXT:
                self.changeExtension(EXT)
        return self.changeFileName()
    

    def getDirectoriesInPath(self,recursive=False):         
            """Get a list of the directories in Path

            Args:
                - mrecursive (bool): do you want to walk inside all your directories
            """        
            if self.isFile():
                rootdir = self.getPath()
            else:
                rootdir = self.getPosition()
                
            L=[]
            if not recursive:
                for d in os.listdir(rootdir):
                    F=os.path.join(rootdir,d)
                    if not (os.path.isfile(F)):
                        L.append(F)
            else:
                for rootdir, dirs, files in os.walk(rootdir):
                    for subdir in dirs:
                        F=os.path.join(rootdir, subdir)
                        if not (os.path.isfile(F)):
                            L.append(F)
                        
                
            return L


    def addBaseName(self,filename=None):
        if not filename:
                filename=str(uuid.uuid4())+'.pathable'
        if self.isDir():
            return self.setPosition(os.path.join(self.getPosition(),filename))
        elif self.isFile():
            return self.changeBaseName(filename)
        return self
    
    def reset(self):
        while (self.positionStack.size()>1):
            self.undo()

    
    def removeLastPath(self):
        pt=self.getPath()
        path_split = PurePath(pt).parts
        p=path_split[0]
        for t in path_split[1:-1]:
            p=os.path.join(p,t)
        return self.changePath(p)
    
    def getLastPath(self):
        pt=self.getPath()
        path_split = PurePath(pt).parts
        p=path_split[-1]
        return p

    def addPrefix(self,pre):
        if self.isFile():
            return self.changePositionSuffixPrefix(prefix=pre)

    def addPrefixAndSuffix(self,pre,suf):
        if self.isFile():
            return self.changePositionSuffixPrefix(prefix=pre,suffix=suf)
    
    def changePositionSuffixPrefix(self, suffix=None,prefix=None):
        if self.isFile():
            N = self.getFileName()
            E = self.getExtension()
            if E and E.startswith('.'):
                E = E[1:]
            if suffix:
                o=self.changeBaseName(N + suffix + '.' + E)
                N = self.getFileName()
            if prefix:
                o=self.changeBaseName(prefix + N +'.' + E)
            return o

    def changeExtension(self,ext):
        if self.isFile():
            N = self.getFileName()
            E = self.getExtension()
            if ext[0]== '.':
                ext=ext[1:] 
            return self.changeBaseName(N+"."+ext)
        
    def changeFileNameRandom(self):
        if self.isFile():
            return self.changeFileName()
    
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
    
    def unTarGz(self,PT=None):
        if not PT:
            PT=createTemporaryPathableDirectory().getPosition()
        unTarGz(self.getPosition())

    def unTar(self,PT=None):
        if not PT:
            PT=createTemporaryPathableDirectory().getPosition()
        unTar(self.getPosition())

    def readJson(self):
        return readJson(self.getPosition())

    def writeJson(self,data):
        return writeJsonFile(self.getPosition(),data)

    def readPkl(self):
        return readPkl(self.getPosition())

    def writePkl(self,data=[]):
        return writePkl(self.getPosition(),data)
    


import os
import platform
def checkDirEndsWithSlash(_dir):
    # Ensure image_dir ends with a separator
    if not _dir.endswith(os.path.sep):
        _dir += os.path.sep
    return _dir

def getPlatformInfo():
    return {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "user": getpass.getuser()
    }

if __name__=="__main__":

    # AA=createRandomTemporaryPathableFromFileName('a.txt')
    # AA.addBaseName()
    # print(AA.getPosition())
    # AA.changeBaseName('a.txt')
    # print(AA.getPosition())
    # AA.changePath('/data/tmp')
    # print(AA.getDirectoriesInPath())
    # AA.appendPath('last')
    # print(AA.getLastPath())

    # B=forkPathable(AA)
    # print(B.getLastPath())
    # print(B.getPosition())

    A=Pathable('/tmp/fff/a.zip')
    A.ensureDirectoryExistence()
    G=GarbageCollector()
    G.throw(A.getPosition())
    G.throw(A.getPath())
    
    import os
    sss="/tmp/aaaaaa"
    os.makedirs(sss, exist_ok=True)
    G.throw(sss)
    G.trash()

    



