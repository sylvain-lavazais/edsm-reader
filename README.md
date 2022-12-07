# Project Astraeus - EDSM Reader

This Repository is a part of a bigger project called `Astraeus`.

`Astraeus` aim to guide fleet carrier commander through the galaxy and environments of Elite Dangerous.

its goals:
 - Gather intel about systems, bodies, entities... of the galaxy
 - Jump route planner for fleet carriers based on interest of mining, trading, etc...

## EDSM Reader

this service allow to load data from another existing tools of EDCD (Elite: Dangerous Community Developers), 
called EDSM (Elite: Dangerous Star Map).

this tools will browse every system and bodies available in EDSM while respecting the APIs limits of EDSM.

this should fulfill the first objective of Astraeus.

### Prerequisite

this module use python 3.10

you can install it from [python official website](https://www.python.org/)

or from [pyenv](https://github.com/pyenv/pyenv) 

### How to run it

without any parameter.

```shell
python -m esdm-reader
```
will display the help about options

```text
Usage: python -m edsm-reader [OPTIONS]

  Start the edsm reader application
  
  example: python -m edsm-reader \
  --api_key [<your api_key>] \
  --commander_name [name] \
  --init_file_path [path/to/file] \
  --log_level [CRITICAL|ERROR|WARNING|INFO|DEBUG]

Options:
  --api_key TEXT         The EDSM api key
  --commander_name TEXT  The EDSM registered commander name
  --init_file_path TEXT  The file path to the system json file for init
  --log_level TEXT       The log level for trace
  --help                 Show this message and exit.
```

### How to contribute

If you want to contribute to a project and make it better, your help is very welcome. Contributing is also a great way to learn more about social coding on Github, new technologies and and their ecosystems and how to make constructive, helpful bug reports, feature requests and the noblest of all contributions: a good, clean pull request.

#### How to make a clean pull request

1. Create a personal fork of the project on Github.
2. Clone the fork on your local machine. Your remote repo on Github is called `origin`.
3. Add the original repository as a remote called `upstream`.
4. If you created your fork a while ago be sure to pull upstream changes into your local repository.
5. Create a new branch to work on! Branch from `main`.
6. Implement/fix your feature, comment your code.
7. Follow the code style of the project, including indentation.
8. If the project has tests run them!
9. Write or adapt tests as needed.
10. Add or change the documentation as needed.
11. Squash your commits into a single commit with git's [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.
12. Push your branch to your fork on Github, the remote `origin`.
13. From your fork open a pull request in the correct branch. Target the project's `main` branch
14. Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete
  your extra branch(es).

#### Commit messages

use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

