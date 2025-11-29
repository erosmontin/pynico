
from pynico import pynico as me
from pathlib import Path
import tempfile


def test_pathable_basic(tmp_path):
	file_path = tmp_path / "a.nii.gz"
	file_path.write_text("data", encoding="utf-8")
	A = me.Pathable(str(file_path))
	assert A.getPosition() == str(file_path)
	assert A.getExtension() == "nii.gz"
	assert A.getFileName() == "a"
	assert A.isFile()
	assert not A.isDir()
	# change extension
	A.changeExtension(".mha")
	assert A.getExtension() == "mha"


def test_append_prefix_suffix_and_undo(tmp_path):
	file_path = tmp_path / "b.txt"
	file_path.write_text("x", encoding="utf-8")
	A = me.Pathable(str(file_path))
	original = A.getPosition()
	A.addSuffix("_s")
	assert "_s" in A.getBaseName()
	A.addPrefix("pre_")
	assert "pre_" in A.getBaseName()
	# undo changes
	A.undo()
	assert A.getPosition() != original
	A.reset()
	assert A.getPosition() == original


def test_is_collection():
	assert me.isCollection([1, 2, 3])
	assert not me.isCollection("abc")
