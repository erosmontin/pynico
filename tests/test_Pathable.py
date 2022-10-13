# import tmpme as me
import common as me


thestring='/data/tmp/4657f33d-4582-4507-8d2f-f78698563410/myfilename.json.tar.gz'
A=me.Pathable(thestring)

print(A.isFile())
print(A.isDir())
print(A.exists())
print(A.getPath())
print(A.getBaseName())
print(A.getBaseNameWithoutExtension())
print(A.getExtension())
print(A.getFileName())
print(A.getPosition())
print(A.getPositionWithPrefix('ah'))

#changing
print("\n\n\nchanging",end="\n\n\n")
A.changePath('/data/t')
print(A.getPosition())

A.addPrefix('AA'), print(A.getPosition())
A.addSuffix('ZZ'), print(A.getPosition())
A.addPrefixAndSuffix(pre='BB',suf='YY'), print(A.getPosition())
A.changeExtension('.nii.gz'), print(A.getPosition())
A.changeExtension('mha'), print(A.getPosition())
A.changeBaseNameWithoutExtensionRandom(), print(A.getPosition())
A.appendPath('fdd'), print(A.getPosition())
A.appendPathRandom(), print(A.getPosition())
A.removeLastPath(), print(A.getPosition())
A.renamePath('t','dededede'), print(A.getPosition())

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
