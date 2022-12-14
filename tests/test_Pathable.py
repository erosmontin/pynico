
from pynico_eros_montin import pynico as me

# thestring=me.createTemporaryPosition('oo.nii.gz')
# print(f'the original file {thestring}')
A=me.createRandomTemporaryPathableFromFileName('oo.nii.gz',None)

print(A.getPosition())

print(A.isFile())
print(A.isDir())
print(A.exists())
print(A.getPath())
print(A.getBaseName())
print(A.getFileName())
print(A.getExtension())
print(A.getFileName())
print(A.getPosition())
print(A.addPrefix('ah'))

#changing
print("\n\n\nchanging",end="\n\n\n")
A.changePath('/data/t')
print(A.getPosition())

A.addPrefix('AA'), print(A.getPosition())
A.addSuffix('ZZ'), print(A.getPosition())
A.addPrefixAndSuffix(pre='BB',suf='YY'), print(A.getPosition())
A.changeExtension('.nii.gz'), print(A.getPosition())
A.changeExtension('mha'), print(A.getPosition())
A.changeFileNameRandom(), print(A.getPosition())
A.appendPath('fdd'), print(A.getPosition())
A.appendPathRandom(), print(A.getPosition())
A.removeLastPath(), print(A.getPosition())
A.renamePath('t','dededede'), print(A.getPosition())
A.changePathToOSTemporary(), print(A.getPosition())
A.changePathToOSTemporary(), print(A.getPosition())

#undoing
print("\n\n\nundoing",end="\n\n\n")
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.undo(), print(A.getPosition())
A.reset(), print(A.getPosition())


print(me.isCollection(A.getPosition()))
print(me.isCollection([A.getPosition()]))
