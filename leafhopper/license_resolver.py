from urllib.request import urlopen
from leafhopper.logger import logger

class LicenseResolver(object):
    def resolve(self, pkg_infos: list):
        for pkg_info in pkg_infos:
            if "license_text" in pkg_info:
                return
            if "license_url" in pkg_info:
                license_url = pkg_info["license_url"]
                logger.info(f"loading license text from url name={pkg_info['name']} url={license_url}")
                try:
                    license_text = urlopen(license_url).read().decode("utf-8")
                    pkg_info["license_text"] = license_text
                    return
                except Exception as e:
                    logger.error(f"failed to load license text from url name={pkg_info['name']} url={license_url} error={e}")
