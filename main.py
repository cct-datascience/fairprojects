"""Generate a static website from configuration file."""
import asyncio
import os
from pathlib import Path

import toml
from jinja2 import Environment, FileSystemLoader

from ghrepo import get_org_repos

# First, load the github PAT
GH_PAT = os.environ.get("GH_PAT")

# find out if the token is valid
PAT_MSG = None

# First, load the configuration file
with Path("config.toml").open("r", encoding="UTF-8") as f:
    config = toml.load(f)

# Then get the organisation repos
repos = asyncio.run(get_org_repos(config["organization"], token=GH_PAT))

# Then, create the static website
env = Environment(loader=FileSystemLoader("web"))
template = env.get_template("page.jinja2")

var_dict = {
    "metrics": config["metrics"],
    "repos": repos,
    "page": config["page"],
    #"patmsg": PAT_MSG,
}

out = template.render(var_dict)

with Path("public/index.html").open("w", encoding="UTF-8") as f:
    f.write(out)
