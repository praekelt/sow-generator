import os

import yaml
import pandoc

from django.conf import settings


pandoc.core.PANDOC_PATH = getattr(settings, "SOW_GENERATOR", {}).get(
    "pandoc-path", "/usr/bin/pandoc"
)

DOCUMENTS = {}

top = os.path.join(os.path.dirname(__file__), "documents")
for root, dirs, files in os.walk(top):
    for file in files:
        if file == "metadata.yaml":
            fp = open(os.path.join(root, file), "r")
            try:
                di = yaml.load(fp)
            finally:
                fp.close()
            di["template"] = ""
            template = os.path.join(root, "template.md")
            if os.path.exists(template):
                di["template"] = open(template, "r").read()
            DOCUMENTS[os.path.basename(root)] = di
