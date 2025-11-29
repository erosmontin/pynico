from pynico import pynico as me


def test_garbagecollector_trash(tmp_path):
    G = me.GarbageCollector()
    base = tmp_path / "trashdir"
    base.mkdir()
    file_a = base / "a.json.tar.gz"
    file_a.write_text("content", encoding="utf-8")
    A = me.Pathable(str(file_a))
    for t in range(3):
        A.addSuffix(str(t))
        A.touch()
        G.throw(A.getPosition())
        A.undo()
    G.throw(A.getPath())
    G.trash()
    assert not file_a.exists()
    assert not base.exists()


def test_change_base_name_safe_and_Temporary(tmp_path):
    A = me.Pathable(str(tmp_path / "a.json.tar.gz"))
    A.addSuffix("1")
    A.touch()
    A.changeBaseNameSafe("a.txt")
    assert A.getExtension() == "txt"
    AA = me.createTemporaryPathableFromFileName("tmp.txt")
    AA.changePathToSafePath()
    AA.changeBaseNameSafe("a.txt")
    assert AA.getExtension() == "txt"
