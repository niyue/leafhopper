import json


class ExtraPkgs(object):
    def __init__(self, extra_pkgs_file):
        self.extra_pkgs_file = extra_pkgs_file
        with open(self.extra_pkgs_file, "r") as f:
            extra_info = json.load(f)
            self.overrides = self._read_overrides(extra_info)
            self.hiddens = set(extra_info.get("hiddens", []))

    def _read_overrides(self, extra_info) -> dict:
        if "overrides" in extra_info:
            overrides = extra_info["overrides"]
            return {pkg["name"]: pkg for pkg in overrides}
        else:
            return {}

    def override_pkg_infos(self, pkg_infos: list) -> list:
        for pkg_info in pkg_infos:
            if pkg_info["name"] in self.overrides:
                # mark pkg_info as overridden
                self.overrides[pkg_info["name"]]["_overridden"] = True
                override_pkg = self.overrides[pkg_info["name"]]
                # get all properties from override_pkg
                attrs = set(override_pkg.keys()).union(
                    {"version", "license", "homepage", "description"}
                )
                for attr in attrs:
                    if attr in override_pkg:
                        pkg_info[attr] = override_pkg[attr]
                if "overridden_name" in override_pkg:
                    pkg_info["name"] = override_pkg["overridden_name"]

        # hide packages
        pkg_infos = [p for p in pkg_infos if p["name"] not in self.hiddens]
        return pkg_infos
