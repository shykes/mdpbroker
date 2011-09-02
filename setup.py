from setuptools import setup

setup(
        name        = "mdpbroker",
        version     = "0.0.1",
        author      = "Solomon Hykes <solomon@dotcloud.com>",
        package_dir = {
            "mdpbroker":    "."
        },
        packages    = [
            "mdpbroker"
        ],
        scripts     = [
            "mdpbroker",
            "http-to-zmq.py",
            "zmq-to-http.py"
        ],
        zip_safe    = False # Damn you setuptools, now and forever
)
