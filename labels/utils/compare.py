from pathlib import Path

import yaml
from mimesis.locales import Locale
from models.core import Definition, Designation
from providers.collection import generic_set

DEFINITIONS = Path("definitions.yaml")
OMMISSIONS = Path("utils/ommissions.yaml")
DEFINITIONS_UPDATE = Path("definitions_update.yaml")

MIMESIS_METHODS = [
    "Meta",
    "random",
    "reseed",
    "seed",
    "validate_enum",
    "get_current_locale",
    "override_locale",
    "update_dataset",
]


def valid_provider(provider):
    if "providers" in provider.__module__:
        return True
    return False


def valid_method(method):
    if method.startswith("_"):
        return False
    if method in MIMESIS_METHODS:
        return False
    return True


with DEFINITIONS.open("r", encoding="utf-8") as f:
    definition_data = yaml.load(f, Loader=yaml.FullLoader)

definitions = list(definition_data)

with OMMISSIONS.open("r", encoding="utf-8") as f:
    omitted_data = yaml.load(f, Loader=yaml.FullLoader)

omitted_methods = list(omitted_data)

generic_methods = []

generic = generic_set(Locale.DEFAULT)

for module in dir(generic):
    provider = getattr(generic, module)
    provider_name = module.lower()
    if valid_provider(provider):
        for method in dir(provider):
            if valid_method(method):
                qualified_method = f"{provider_name}.{method}"
                if qualified_method not in omitted_methods:
                    generic_methods.append(f"{provider_name}.{method}")

# Documented, not implemented
doc_not_imp = [d for d in definitions if d not in generic_methods]

print("Documented, not implemented")
print(doc_not_imp)

# Implemented, not documented
imp_not_doc = [m for m in generic_methods if m not in definitions]

# print("Implemented, not documented")
# print(imp_not_doc)


def create_default_definition(method: str) -> Definition:
    provider, method_name = method.split(".")
    return Definition(
        provider=provider,
        method=method_name,
        designation=Designation.universal,
        primitive="str",
        locales=["EN"],
        samples=["sample1", "sample2"],
        release_priority=1,
        title=f"Default title for {method}",
        description=None,
        references=[],
        aliases=[],
        notes=None,
    )


update = {}

for method in imp_not_doc:
    provider, method_name = method.split(".")
    new_definition = create_default_definition(method)
    update[method] = new_definition.model_dump(mode="json")


with DEFINITIONS_UPDATE.open("w", encoding="utf-8") as f:
    yaml.dump(update, f, Dumper=yaml.Dumper, default_flow_style=False)

print(f"New definitions written to {DEFINITIONS_UPDATE}")
