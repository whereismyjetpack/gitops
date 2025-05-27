#!/usr/bin/env python3 
from jinja2 import Template, FileSystemLoader, Environment
import os
import shutil


def set_variables():
  suite = os.environ.get('SUITE')
  if suite is None:
    raise ValueError('SUITE environment variable is required')
  name = os.environ.get('NAME')
  if name is None:
    raise ValueError('NAME environment variable is required')
  okta_group = os.environ.get('OKTA_GROUP')
  if okta_group is None:
    raise ValueError('OKTA_GROUP environment variable is required')
  ecr_repo = os.environ.get('ECR_REPO')
  if ecr_repo is None:
    raise ValueError('ECR_REPO environment variable is required')
  gitops_repo = os.environ.get('GITOPS_REPO')
  if gitops_repo is None:
    raise ValueError('GITOPS_REPO environment variable is required')
  kargo_project_name= os.environ.get('KARGO_PROJECT_NAME')
  if kargo_project_name is None:
    kargo_project_name = f"{suite}-{name}-project"

  return {
    'suite': suite,
    'name': name,
    'okta_group': okta_group,
    'ecr_repo': ecr_repo,
    'gitops_repo': gitops_repo,
    'kargo_project_name': kargo_project_name,
  }


os.makedirs('rendered', exist_ok=True)

env = Environment(
    loader=FileSystemLoader('templates'))

for template_name in env.list_templates():
  rendered_template_name = Template(template_name).render(**set_variables())
  template = env.get_template(template_name)
  rendered = template.render(**set_variables())
  output_path = os.path.join('rendered', rendered_template_name)
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, 'w') as f:
    f.write(rendered)

# print(env.list_templates())

# project = env.get_template('project.yaml')

# rendered = project.render(**set_variables())

# with open('rendered/project.yaml', 'w') as f:
#   f.write(rendered)