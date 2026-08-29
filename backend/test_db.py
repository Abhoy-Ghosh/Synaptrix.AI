import os
import tempfile
import pytest

from app.storage.db import (
    init_db,
    create_project,
    get_projects,
    get_project,
    create_chat,
    get_chats,
    add_message,
    get_messages,
    delete_project
)


def test_database_crud(tmp_path, monkeypatch):
    test_db_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", test_db_dir)

    # Re-import or patch DB_PATH to use isolated test dir
    import app.storage.db as db_module
    db_module.BASE_DIR = test_db_dir
    db_module.DB_PATH = os.path.join(test_db_dir, "synaptrix.db")

    # 1. Initialize
    init_db()

    # 2. Create Project
    p = create_project("Quantum AI", "Quantum Computing", "Research on quantum ML algorithms")
    assert p is not None
    assert p["name"] == "Quantum AI"

    # 3. List Projects
    projects = get_projects()
    assert len(projects) == 1

    # 4. Create Chat
    c = create_chat(p["id"], "Quantum Error Correction", "parallel")
    assert c is not None
    assert c["title"] == "Quantum Error Correction"

    # 5. Add Messages
    m1 = add_message(c["id"], "user", "What are top quantum error correction methods?")
    m2 = add_message(c["id"], "assistant", "Here is the summary of Surface Codes...", {"papers": [{"title": "Surface code quantum computing"}]})
    assert m1 is not None
    assert m2 is not None

    # 6. Fetch Messages
    msgs = get_messages(c["id"])
    assert len(msgs) == 2
    assert msgs[1]["research_data"]["papers"][0]["title"] == "Surface code quantum computing"

    # 7. Delete Project
    delete_project(p["id"])
    assert get_project(p["id"]) is None
    assert len(get_projects()) == 0


if __name__ == "__main__":
    print("Running DB test script directly...")
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        class TmpPath:
            def __str__(self):
                return tmpdir
        class DummyMonkey:
            def setenv(self, k, v): os.environ[k] = v
        test_database_crud(tmpdir, DummyMonkey())
        print("[+] All DB tests passed successfully!")
