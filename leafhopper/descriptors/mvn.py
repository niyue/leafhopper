from leafhopper.descriptors.descriptor import Descriptor
from leafhopper.descriptors.extra.extra_info_loader import load_extra_info

from io import BytesIO, StringIO
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree
import json
from urllib.request import urlopen
from leafhopper.logger import logger

NS = "http://maven.apache.org/POM/4.0.0"

def _parse_ignoring_namespace(pom):
    if isinstance(pom, str):
        xml = StringIO(pom)
    else:
        xml = BytesIO(pom)
    it = ElementTree.iterparse(xml)
    for _, el in it:
        _, _, el.tag = el.tag.rpartition('}') # strip ns
    return it.root

def _get_pom_path(pkg_info: dict) -> str:
    group_id = pkg_info["group_id"].replace(".", "/")
    artifact_id = pkg_info["artifact_id"]
    version = pkg_info["version"]
    return "/".join([group_id, artifact_id, version, f"{artifact_id}-{version}.pom"])


def _fill_homepage(pkg_info: dict, tree) -> dict:
    homepage = tree.find(f"url")
    if homepage is not None:
        pkg_info["homepage"] = homepage.text
    else:
        scm_url = tree.find(f"scm/url")
        if scm_url is not None:
            pkg_info["homepage"] = scm_url.text

def _load_pkg_info_with_version(pkg_info: dict) -> dict:
    pom_path = _get_pom_path(pkg_info)
    pom_url = f"https://search.maven.org/remotecontent?filepath={pom_path}"
    # get pom via http request
    try:
        logger.debug(f"loading pom url={pom_url}")
        pom = urlopen(pom_url).read()
        tree = _parse_ignoring_namespace(pom)
        _fill_homepage(pkg_info, tree)
        
        description = tree.find(f"description")
        if description is not None:
            pkg_info["description"] = description.text
        licenses = tree.findall(f"licenses/license/name")
        if licenses:
            license_texts = [license.text for license in licenses]
            pkg_info["license"] = ", ".join(license_texts)
        load_extra_info(pkg_info)
    except Exception as e:
        logger.debug(f"failed to load pom url={pom_url} error={e}")
    return pkg_info


def _load_pkg_version(pkg_info: dict) -> dict:
    artifact_url = f"https://search.maven.org/solrsearch/select?q=g:{pkg_info['group_id']}+AND+a:{pkg_info['artifact_id']}&core=gav&rows=10&wt=json"
    logger.debug(f"loading artifact version url={artifact_url}")
    artifact_versions_content = urlopen(artifact_url).read()
    artifact_versions = json.loads(artifact_versions_content)
    if "response" in artifact_versions and "docs" in artifact_versions["response"]:
        docs = artifact_versions["response"]["docs"]
        if len(docs) > 0:
            pkg_info["version"] = docs[0]["v"]
    return pkg_info


def _load_pkg_info(pkg_info: dict) -> dict:
    pkg_name = pkg_info["name"]
    logger.info(f"processing maven package name={pkg_name}")
    if not pkg_info["version"]:
        _load_pkg_version(pkg_info)
        if not pkg_info["version"]:
            return pkg_info
    return _load_pkg_info_with_version(pkg_info)


class MvnDescriptor(Descriptor):
    def __init__(self) -> None:
        super().__init__()

    # use element tree API to parse `dependencies` from maven pom file
    def parse(self, pom: str) -> list:
        # parse pom xml string into element tree
        tree = _parse_ignoring_namespace(pom)
        # find the `dependencies` element
        dependencies = tree.find(f"dependencies")
        deps = []
        # iterate through each `dependency` element
        for dependency in dependencies:
            pkg_info = {}
            # get groupId, artifactId, version
            group_id = dependency.find(f"groupId").text
            artifact_id = dependency.find(f"artifactId").text
            version_element = dependency.find(f"version")
            if version_element:
                version = version_element.text
            else:
                version = None
            # create a key-value pair for the dictionary
            pkg_info["name"] = group_id + "." + artifact_id
            pkg_info["group_id"] = group_id
            pkg_info["artifact_id"] = artifact_id
            pkg_info["version"] = version

            _load_pkg_info(pkg_info)
            deps.append(pkg_info)
        return deps
