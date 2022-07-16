def has_no_license(pkg_dict):
    return "license" not in pkg_dict or not pkg_dict["license"]


def has_github_homepage(pkg_dict):
    return "homepage" in pkg_dict and pkg_dict["homepage"].startswith(
        "https://github.com"
    )