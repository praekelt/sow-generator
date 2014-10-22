from sow_generator import DOCUMENTS

from sow_generator.models import Repository


def unpack_document_by_key(key):
    document = DOCUMENTS[key]

    # Split template into parts
    # todo: regex for more leniency
    header, footer = document["template"].split(
        "<!--- modules - do not remove or alter this line -->"
    )

    repos = []
    modules = document.get("required_modules", []) \
        + document.get("optional_modules", [])
    for module in modules:
        try:
            repo = Repository.objects.get(name=module)
        except Repository.DoesNotExist:
            continue
        repos.append(repo)

    return document, header, footer, repos
