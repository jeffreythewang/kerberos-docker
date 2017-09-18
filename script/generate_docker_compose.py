#!/usr/bin/env python3
#
# generate_docker_compose.py
#
# Generate configuration from Jinja template.
#
# usage: python3 ./script/generate_docker_compose.py
# (call only from root repository)
#
# Generate docker-compose.yml configuration from:
# - .env.values (shell environment)
# - docker-compose.yml.template (Jinja template)


import sys
import os
import configparser

import jinja2

def read_context(file_path):
    """Read a configuration file (bash compatible with source).

    Parameters
    ----------
    file_path : string
        Configuration file (bash compatible with source).

    Returns
    -------
    dict
        Configuration under the shape of dictionnary (key, value).
    """
    with open(file_path, "r") as desc:
        _buffer = "[section]\n"
        _buffer += desc.read()
    config = configparser.RawConfigParser()
    # preserve case
    config.optionxform = str
    config.read_string(_buffer)
    return dict(config.items("section"))

def render(template_path, context, generate_file=True, comment="#"):
    """From a template Jinja (with extension .template) and a context
    generate a configuration and create a file (without extension .template)
    if precised. Add a header to this configuration to mark the file as
    generated.

    Parameters
    ----------
    template_path : string
        Path file to Jinja template (with extension .template).

    context : dict
       (key, value) parameters to feed to JinJa template.

    generate_file : bool (optional, by default True)
        If true, persist generated configuration to a file in same directory
        than Jinja template (without extension .template).

    comment : string (optional, by default #)
        token for inline comment in generated configuration

    Returns
    -------
    string
        Content of generated configuration file
    """
    path, filename = os.path.split(template_path)
    content = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)
    # delete .template extension
    conf_filename, _ = os.path.splitext(filename)
    conf_path = os.path.join(path, conf_filename)
    content = "{} {}\n{} {}\n\n{}".format(
        comment,
        "Generated from Jinja template",
        comment,
        "DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN",
        content)
    if generate_file:
        with open(conf_path, "w") as desc:
            desc.write(content)
    return content

if __name__ == "__main__":
    print("=== generate docker compose configuration ===")
    if not os.path.isfile(".env.values"):
        print("ERROR: .env.values doesn't exist!", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile("docker-compose.yml.template"):
        print("ERROR: docker-compose.yml.template doesn't exist!", file=sys.stderr)
        sys.exit(1)
    context = read_context(".env.values")
    result = render("docker-compose.yml.template", context)
    print("...OK")

