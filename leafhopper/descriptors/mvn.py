from leafhopper.descriptors.descriptor import Descriptor
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

class Mvn(Descriptor):
    def __init__(self) -> None:
        super().__init__()

    # use element tree API to parse `dependencies` from maven pom file
    def parse(self, pom: str) -> list:
        # parse pom xml string into element tree
        tree = ElementTree.fromstring(pom)
        # find the `dependencies` element
        dependencies = tree.find('dependencies')
        deps = []
        # iterate through each `dependency` element
        for dependency in dependencies:
            dep_info = {}
            # get groupId, artifactId, version
            group_id = dependency.find('groupId').text
            artifact_id = dependency.find('artifactId').text
            version = dependency.find('version').text
            # create a key-value pair for the dictionary
            dep_info["name"] = group_id + ":" + artifact_id
            dep_info["version"] = version
            deps.append(dep_info)
        return deps

