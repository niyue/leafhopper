from jinja2 import Environment, PackageLoader, select_autoescape

class CombinedLicenseRenderer(object):
    def render(self, pkg_infos: list):
        env = Environment(
            loader=PackageLoader("leafhopper", "templates"),
            autoescape=select_autoescape()
        )
        template = env.get_template("LICENSES.txt.template")
        license_txt = template.render(pkg_infos=pkg_infos)
        return license_txt