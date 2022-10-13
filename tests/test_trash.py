# import tmpme as me
from pynico_eros_montin import pynico as me


G=me.GarbageCollector()


thestring='/tmp/g/a.json.tar.gz'
A=me.Pathable(thestring)
for t in range(5):
    A.addSuffix(str(t))
    A.touch()
    G.throw(A.getPosition())
    A.undo()
G.throw(A.getPath())
G.trash()



L=[]
for t in range(55):
    A.addSuffix(str(t))
    A.touch()
    L.append(A.getPosition())
    # G.throw(A.getPosition())
    A.undo()


