#!/usr/bin/env python3
from jinja2 import Template, FileSystemLoader, Environment
import os
import copy


def set_variables():

    variables = {
        "suite": os.environ.get("SUITE"),
        "name": os.environ.get("NAME"),
        "okta_group": os.environ.get("OKTA_GROUP"),
        "ecr_repo": os.environ.get("ECR_REPO"),
        "gitops_repo": os.environ.get("GITOPS_REPO"),
        "kargo_project_name": os.environ.get("KARGO_PROJECT_NAME", "{{suite}}-{{name}}-project"),
    }
    return variables


def resolve_jinja_variables(variables, max_passes=10):
    resolved = copy.deepcopy(variables)
    for _ in range(max_passes):
        changed = False
        for key, value in resolved.items():
            if isinstance(value, str):
                rendered = Template(value).render(**resolved)
                if rendered != value:
                    resolved[key] = rendered
                    changed = True
        if not changed:
            break

    return resolved


resolved_variables = resolve_jinja_variables(set_variables())

os.makedirs("rendered", exist_ok=True)

env = Environment(loader=FileSystemLoader("templates"))

for template_name in env.list_templates():
    rendered_template_name = Template(template_name).render(**resolved_variables)
    template = env.get_template(template_name)
    rendered = template.render(**resolved_variables)
    output_path = os.path.join("rendered", rendered_template_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(rendered)
