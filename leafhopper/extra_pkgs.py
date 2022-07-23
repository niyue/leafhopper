import json


class ExtraPkgs(object):
    def __init__(self, extra_pkgs_file):
        self.extra_pkgs_file = extra_pkgs_file
        self.overrides = self._read_overrides()

    def _read_overrides(self):
        with open(self.extra_pkgs_file, "r") as f:
            extra_info = json.load(f)
            if "overrides" in extra_info:
                overrides = extra_info["overrides"]
                return {pkg["name"]: pkg for pkg in overrides}
            else:
                return {}

    def override_pkg_infos(self, pkg_infos):
        for pkg_info in pkg_infos:
            if pkg_info["name"] in self.overrides:
                override_pkg = self.overrides[pkg_info["name"]]
                # mark pkg_info as overridden
                self.overrides[pkg_info["name"]]["_overridden"] = True
                for attr in ["version", "license", "description"]:
                    if attr in override_pkg:
                        pkg_info[attr] = override_pkg[attr]
        return pkg_infos
