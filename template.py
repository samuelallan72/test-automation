import argparse
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repo", type=str, help="repo name in config file", required=True)
    parser.add_argument("-p", "--path", type=str, help="path to checked out target repo", required=True)
    args = parser.parse_args()

    with open("config.yaml") as f:
        full_config = yaml.safe_load(f)["repos"]

    config = full_config[args.repo]

    for file in config["files"]:
        shutil.copy(file["src"], args.path + "/" + file["dest"])

    env = Environment(loader=FileSystemLoader("."))
    for template_config in config["templates"]:
        template = env.get_template(template_config["src"])
        output = template.render(**(template_config["vars"]))
        with open(args.path + "/" + template_config["dest"], "w") as f:
            f.write(output)


if __name__ == "__main__":
    main()
