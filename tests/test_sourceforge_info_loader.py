from leafhopper.descriptors.extra.sourceforge_info_loader import SourceForgeInfoLoader
from leafhopper.descriptors.extra import _extract_sourceforge_project_id


def test_extract_project_id_in_domain():
    project_id = _extract_sourceforge_project_id("http://findbugs.sourceforge.net/")
    assert project_id == "findbugs"

    project_id = _extract_sourceforge_project_id("http://findbugs.sourceforge.net")
    assert project_id == "findbugs"

    # using https
    project_id = _extract_sourceforge_project_id("https://findbugs.sourceforge.net")
    assert project_id == "findbugs"


def test_extract_project_id_in_path():
    project_id = _extract_sourceforge_project_id(
        "https://sourceforge.net/projects/findbugs/"
    )
    assert project_id == "findbugs"


def test_extract_project_id_in_path_with_domain():
    project_id = _extract_sourceforge_project_id(
        "https://www.sourceforge.net/projects/findbugs/"
    )
    assert project_id == "findbugs"


def test_extract_project_id_in_path_with_http():
    project_id = _extract_sourceforge_project_id(
        "http://www.sourceforge.net/projects/findbugs/"
    )
    assert project_id == "findbugs"

def test_load_sourceforge_project():
    loader = SourceForgeInfoLoader("findbugs")
    project = loader.load({"name": "findbugs"})
    assert project["name"] == "findbugs"
    assert "license" in project
    assert "description" in project
    assert project["license"] == "lgpl"
    assert project["description"] == "A static analysis tool to find bugs in Java programs."