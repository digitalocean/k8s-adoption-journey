# Building the Documentation

A simple quick start for building the documentation for the [Kubernetes Adoption Journey](https://digitalocean.github.io/k8s-adoption-journey/) project.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Understanding MkDocs Projects](#understanding-mkdocs-projects)
- [Content Authoring](#content-authoring)
- [Extending Functionality via Plugins/Extensions](#extending-functionality-via-pluginsextensions)
- [Local Testing](#local-testing)
- [Publishing to GitHub Pages](#publishing-to-github-pages)
- [Using GitHub Actions to Automate the Process](#using-github-actions-to-automate-the-process)
- [Cleaning Up](#cleaning-up)
- [Additional Resources](#additional-resources)

## Overview

Main documentation is built using [MkDocs](https://www.mkdocs.org/). It's a powerful and yet simple static site generator tool written in [Python](https://www.python.org). Documentation generated using MkDocs is authored using Markdown files and a [mkdocs.yaml](../mkdocs.yml) file to configure the entire project.

Main theme used is called [Material for MkDocs](https://squidfunk.github.io/mkdocs-material). It's a feature rich theme offering lots of possibilities in terms of formatting and enriching documentation pages content.

For more information and available features, please visit:

- [MkDocs User Guide](https://www.mkdocs.org/user-guide/)
- [Material Theme Reference](https://squidfunk.github.io/mkdocs-material/reference/)

## Prerequisites

1. [Python3](https://www.python.org/) installed on your machine. Instructions available [here](https://docs.python-guide.org/starting/installation/), depending on your operating system.
2. [Pip3](https://pip.pypa.io/en/stable/) installed on your machine. You can check if it's installed as described [here](https://docs.python-guide.org/starting/install3/linux/#setuptools-pip).
3. [GNU Make](https://www.gnu.org/software/make/) for building [Makefile](https://www.gnu.org/software/make/manual/html_node/Introduction.html) based projects:
   - [Linux instructions](https://howtoinstall.co/en/make).
   - [MacOS instructions](https://formulae.brew.sh/formula/make) (via Homebrew).

## Understanding MkDocs Projects

Each project starts with a [mkdocs.yaml](../mkdocs.yml) file. This is the central piece of every MkDocs based project. It contains configuration describing your MkDocs project such as name, author, navigation structure, theme, etc. Whenever you build a MkDocs project, this file is read first and static html content is generated based on current configuration.

Minimal `mkdocs.yaml` configuration looks like below:

```yaml
site_name: Example Project
site_url: https://example.com

nav:
  - Home: index.md
  - About: about.md
theme:
  name: material
  logo: assets/logo.png
```

Explanation for the above configuration:

- `site_name` - This is a required setting, and should be a string that is used as the main title for the project documentation.
- `site_url` - Sets the canonical URL of the site. This will add a link tag with the canonical URL to the head section of each HTML page.
- `nav` - This setting is used to determine the format and layout of the global navigation for the site.
- `theme` - sets a theme for the whole site, and associated options (such as setting a logo, etc).

Next, comes the MkDocs project layout. In a typical setup, you will encounter this layout for each project:

```text
├── docs
│   ├── assets
│   │   └── do_logo.svg
│   ├── getting-started.md
│   └── index.md
├── mkdocs.yml
└── site
│   ├── index.html
...
```

The `docs` folder holds all your assets such as images, markdown pages, etc. Then, comes the `mkdocs.yaml` file, and finally the `site` folder, sitting at the same level as the `docs` folder. The `site` folder contains all the static assets which needs to be published. That's where the generated static content lives. This folder is not committed to Git with the rest of the files because it constantly changes based on the docs folder assets and the configuration of your MkDocs project. In other words, the `docs` folder is the `source` folder, and `site` is the `build` folder for the final artifacts to be published.

One important file from the `docs` folder is the `index.md` file. This is the first page that gets rendered and presented to the user when accessing your website (very much like the `index.html` file). The `assets` subfolder contains various images or other files that you want to embed into your final documentation site.

Markdown pages can live anywhere under the docs folder. You can even nest them in other subfolders. In the `nav` section from the `mkdocs.yaml` file you can reference each by path. Below example shows this feature:

```yaml
nav:
  - Home: index.md
  - Getting started:
      - Installing required tools: getting-started/installing-required-tools.md
      - Authentication: getting-started/authentication.md
```

In the above example, `installing-required-tools.md` and `authentication.md` markdown files live under the `getting-started` subfolder, which in turn lives in the `docs` folder. Below listing shows the project layout for the previous `nav` configuration:

```text
├── docs
│   ├── getting-started
│   │   ├── authentication.md
│   │   └── installing-required-tools.md
│   └── index.md
...
```

Bootstrapping a new project can be done via the `mkdocs` utility, as explained in the [getting started tutorial](https://www.mkdocs.org/getting-started/).

**Note:**

This project is using `make` on top of the mkdocs utility to simplify the bootstrapping process, as well as setting up a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html). How you will do that, is explained in the [Local Testing](#local-testing) section from this guide.

Choosing a theme and setting options is done via the `theme` section:

```yaml
theme:
  name: material
```

You can read more about themes [here](https://www.mkdocs.org/user-guide/choosing-your-theme/). This project is using the [Material Theme](https://squidfunk.github.io/mkdocs-material/reference/).

Please visit the [official documentation](https://www.mkdocs.org/user-guide/configuration/) for more information about all the available options.

## Content Authoring

Adding pages and more content is done via the mkdocs `configuration file` and the `docs` folder. MkDocs supports regular Markdown syntax, but it can also add extra features on top, such as tabbed views, admonitions, etc. Those extra features are provided via the main theme, or via plugins/extensions.

Content authoring goes the usual way as for every markdown file. On top of that, you will get additional features and fancy stuff via markdown extensions. MkDocs uses the [Python Markdown library](https://python-markdown.github.io/) to translate Markdown files into HTML. Python Markdown supports a variety of [extensions](https://python-markdown.github.io/extensions/) that customize how pages are formatted.

For more information about how to write your docs, please visit the official MkDocs site [documentation](https://www.mkdocs.org/user-guide/writing-your-docs/) on this topic.

## Extending Functionality via Plugins/Extensions

MkDocs is very flexible, and allows you to extend functionality via extensions and plugins. Extensions add more features to content authoring by enriching the existing ones provided by Markdown. These features are provided by [Python markdown extensions](https://python-markdown.github.io/extensions/).

Below example shows how to enable additional markdown extensions:

```yaml
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```

Plugins on the other hand, add more features to the core functionality of MkDocs. For example, the bellow snippet enables the [autolinks](https://github.com/midnightprioriem/mkdocs-autolinks-plugin) plugin:

```yaml
plugins:
  # simplifies relative linking between documents
  # https://github.com/midnightprioriem/mkdocs-autolinks-plugin
  - autolinks
```

Current project uses the [autolinks](https://github.com/midnightprioriem/mkdocs-autolinks-plugin) plugin to simplify the process of cross referencing between various sections of the documentation.

**Note:**

The `autolinks` plugin doesn't work for the `nav` section from the mkdocs.yaml file. There, you still need to reference using a valid relative path.

Please visit the [official documentation](https://www.mkdocs.org/user-guide/configuration/#markdown_extensions) page to read more about extensions. Also the [plugins page](https://www.mkdocs.org/user-guide/configuration/#plugins) offers more information about this MkDocs feature.

## Local Testing

The kubernetes adoption project offers a `Makefile` based setup to simplify the initial setup process. It also creates a `Python virtual environment` for you, so that your system is not cluttered with additional packages, or conflict with the existing ones. This is a good practice in general for each Python based project (or tool).

The only requirements is for you to have `python3`, `pip3` and `make` installed as explained in the [prerequisites](#prerequisites) section of this guide.

Please follow below steps, to start contributing to this project (assuming you have a local copy of this repo):

1. Change directory to your local copy:

    ```shell
    cd k8s-adoption-journey
    ```

2. Run the `serve` command via `make`:

    ```shell
    make serve
    ```

    The output looks similar to:

    ```text
    ...
    INFO     -  Building documentation...
    INFO     -  Cleaning site directory
    INFO     -  Documentation built in 0.22 seconds
    INFO     -  [11:56:45] Watching paths for changes: 'docs', 'mkdocs.yml'
    INFO     -  [11:56:45] Serving on http://127.0.0.1:8000/
    INFO     -  [12:01:05] Detected file changes
    ...
    ```

3. Open a web browser, and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000/).

The `make serve` command will create a Python virtual environment first. Then, it will download all project dependencies via pip3 in the virtual environment. Next, the `mkdocs serve` command runs, which will build the final MkDocs project. Finally, a local web server is started serving static content from the `site` folder.

The local web server is also watching for any changes happening in the `mkdocs.yaml` file and the `docs` folder. This way, you can see live changes to your website directly in your web browser. No need to reload pages, because the live reloading feature does this for you automatically.

You can also take a look at the [Makefile](../Makefile) used in this project to see what it does. In a nutshell, it's composed of a few targets that set up the Python virtual environment, and then call `mkdocs` commands/subcommands. In other words, it's a wrapper around `mkdocs` CLI, and the Python `virtualenv` command.

## Publishing to GitHub Pages

MkDocs is also able to publish your site to GitHub pages for your forked repository. For this to work, you need to have GitHub pages [configured](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) for your repo.

The custom [Makefile](../Makefile) provided in this project can be used for this task:

```shell
make gh-deploy 
```

Under the hood, the above command calls the `mkdocs gh-deploy` command. Then, it will create a `gh-pages` branch for your repo, and push the `site` folder contents to it. Finally, you can manually trigger the workflow provided with this repo, and publishes the site to GitHub pages (assuming you have set it up correctly, and points to the `gh-pages` branch).

You can read more about [gh-deploy command](https://www.mkdocs.org/user-guide/deploying-your-docs/) on the official documentation page for MkDocs.

## Using GitHub Actions to Automate the Process

In a real life scenario, you will want to create a PR, then commit changes to the `main` branch via a `merge` operation. Finally, the github pages documentation publish workflow kicks in automatically, and updates the live site.

To check the functionality, you can take a look at the main workflow file used in this repo, called [publish_doc](../.github/workflows/publish_doc.yaml). In a nutshell, it's triggered whenever a change is pushed to the `main` branch (which should be protected and only accepts PRs). Then, the [deploy-mkdocs](https://github.com/marketplace/actions/deploy-mkdocs) action is used to perform the actual deployment to GitHub pages.

## Cleaning Up

Cleaning up additional artifacts created via MkDocs is accomplished via:

```shell
make clean
```

The above command cleans the `site` and `venv` (Python virtual environment assets) directories. Also, the [.gitignore](../.gitignore) file is configured to not commit those folders content to remote by mistake.

## Additional Resources

To further enrich your experience, please visit the following additional links:

- [MkDocs Getting Started Guide](https://www.mkdocs.org/getting-started/)
- [MkDocs User Guide](https://www.mkdocs.org/user-guide/)
- [Additional MkDocs Plugins](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins/)
- [Material Theme Reference](https://squidfunk.github.io/mkdocs-material/reference/)
- [Diagrams Support via Mermaid.js](https://github.com/fralau/mkdocs-mermaid2-plugin)
