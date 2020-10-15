"""PYENVCOMP
"""

import os
import sys
import argparse
import subprocess
import tableformatter as tf
from typing import List


class Colors:
    """Color listing class"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# remove all colors if the platform is not linux
if sys.platform != 'linux':
    colors = [
        var 
        for var, _ in Colors.__dict__.items() 
        if not var.startswith("__")
    ]
    for var in colors:
        setattr(Colors, var, '')

class ArgParse:
    """
    Argument parsing class
    """

    def __init__(self):
        """init function"""
        pass

    def parse_args(self):
        """Parses the commandline argument"""

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "path1",
            metavar="env path1",
            type=str,
            help="location of the first virtual environment",
        )
        parser.add_argument(
            "path2",
            metavar="env path2",
            type=str,
            help="location of the second virtual environment",
        )
        parser.add_argument(
            "-d",
            "--display",
            type=str,
            help="Compare envs based on either of these available options [all|diff|separate]",
        )

        args = parser.parse_args()
        self.path1 = args.path1
        self.path2 = args.path2
        self.display = args.display


def envs_display(env1_path, env2_path, heading, diff_or_similar_list, similar: bool):
    """Displays the table of similar or different module versions."""
    color = Colors.OKGREEN if similar else Colors.WARNING
    title = "SAME MODULE VERSIONS " if similar else "DIFFERENT MODULE VERSIONS "

    print(color + title + Colors.END)
    print(f'{env1_path.split(os.sep)[-1]} - {env1_path}')
    print(f'{env2_path.split(os.sep)[-1]} - {env2_path}')
    print(tf.generate_table(diff_or_similar_list, heading))


def env_display(env_name, env_py_version, env_path, heading, modules: list):
    """Displays the table of a single environment having extra modules."""
    print(
        "ONLY IN "
        + Colors.BOLD
        + Colors.OKGREEN
        + f"{env_name} ({env_py_version})"
        + Colors.END
    )
    print(f'({env_path})')
    print(tf.generate_table(modules, heading))


def env_map(modules: List[str]) -> dict:
    """Creates a dict of module to version for an environment"""
    mod_to_ver = {}
    for module in modules:
        try:
            mod, version, *_ = module.split("-")
            mod_to_ver[mod] = version
        except Exception:
            pass
    return mod_to_ver


def get_raw_modules(path, env_py_version=None):
    """Returns raw list of modules along with versions in an environment"""
    if sys.platform == 'linux':
        env_modules = subprocess.check_output(
            f"ls -d {str(path)}/lib/{env_py_version}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;' ",
            shell=True,
        )
        return env_modules.decode("utf-8").split("\n")
    else:
        env_modules = os.listdir(path + os.sep + "Lib" + os.sep + "site-packages")
        return [
            module[: module.rfind(".")]
            for module in env_modules
            if "dist-info" in module
        ]


def get_python_version(path):
    """Returns the python version of the environment"""
    if sys.platform == 'linux':
        return os.listdir(path + os.sep + "/lib")[0]
    else:
        py_ver_config_path = path + os.sep + 'pyvenv.cfg'
        with open(py_ver_config_path) as f:
            version = None
            for line in f:
                if line.lower().startswith('version'):
                    version = line.split('=')[-1].strip()
                    break
        return version


def main():
    """
    The main comparing function
    """
    arg_parse = ArgParse()
    arg_parse.parse_args()
    args = vars(arg_parse)

    env1_path = args["path1"]
    env2_path = args["path2"]
    display = args["display"]

    env1_name = env1_path[env1_path.rfind("/") + 1 :]
    env2_name = env2_path[env2_path.rfind("/") + 1 :]

    env1_py_version = get_python_version(env1_path)
    env2_py_version = get_python_version(env2_path)
    env1_modules = get_raw_modules(env1_path, env1_py_version)
    env2_modules = get_raw_modules(env2_path, env2_py_version)

    env1_map = {}
    env2_map = {}

    env1_map = env_map(env1_modules)
    env2_map = env_map(env2_modules)

    env1_modules = set(env1_map.keys())
    env2_modules = set(env2_map.keys())

    common_modules = env1_modules & env2_modules
    only_in_env1 = env1_modules - env2_modules
    only_in_env2 = env2_modules - env1_modules

    similar_list = []
    non_similar_list = []
    for module in common_modules:
        if env1_map[module] == env2_map[module]:
            similar_list.append([module, env1_map[module], env2_map[module]])
        else:
            non_similar_list.append([module, env1_map[module], env2_map[module]])

    only_env_1_list = []
    only_env_2_list = []

    for module in only_in_env1:
        only_env_1_list.append([module, env1_map[module]])

    for module in only_in_env2:
        only_env_2_list.append([module, env2_map[module]])

    heading = [
        "Module",
        f"{env1_name} ({env1_py_version})",
        f"{env2_name} ({env2_py_version})",
    ]
    env1_heading = [f"{env1_name}({env1_py_version})", "version"]
    env2_heading = [f"{env2_name}({env2_py_version})", "version"]
    print(
        ''' 
        ______  _________   ___    ____________  __  _______ 
       / __ \ \/ / ____/ | / / |  / / ____/ __ \/  |/  / __ \\
      / /_/ /\  / __/ /  |/ /| | / / /   / / / / /|_/ / /_/ /
     / ____/ / / /___/ /|  / | |/ / /___/ /_/ / /  / / ____/ 
    /_/     /_/_____/_/ |_/  |___/\____/\____/_/  /_/_/  
    
    '''
    )
    try:
        if display in ["all", None]:
            envs_display(env1_path, env2_path, heading, similar_list, similar=True)
            envs_display(env1_path, env2_path, heading, non_similar_list, similar=False)
            env_display(
                env1_name, env1_py_version, env1_path, env1_heading, only_env_1_list
            )
            env_display(
                env2_name, env2_py_version, env2_path, env2_heading, only_env_2_list
            )
        elif display == "diff":
            envs_display(env1_path, env2_path, heading, non_similar_list, similar=False)
        elif display == "similar":
            envs_display(env1_path, env2_path, heading, similar_list, similar=True)
        elif display == "separate":
            env_display(
                env1_name, env1_py_version, env1_path, env1_heading, only_env_1_list
            )
            env_display(
                env2_name, env2_py_version, env2_path, env2_heading, only_env_2_list
            )
    except Exception as exception:
        print(exception)
