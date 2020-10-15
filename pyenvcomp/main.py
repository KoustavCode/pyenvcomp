"""PYENVCOMP
"""

import os
import sys
import argparse
import subprocess
import tableformatter as tf


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

    if sys.platform == 'linux':
        
        env1_py_version = os.listdir(env1_path + os.sep + "/lib")[0]
        env1_modules = subprocess.check_output(
            f"ls -d {str(env1_path)}/lib/{env1_py_version}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;' ",
            shell=True,
        )
        env2_py_version = os.listdir(env2_path + os.sep + "/lib")[0]
        env2_modules = subprocess.check_output(
            f"ls -d {str(env2_path)}/lib/{env2_py_version}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;'",
            shell=True,
        )

        output_split1 = env1_modules.decode("utf-8").split("\n")
        output_split2 = env2_modules.decode("utf-8").split("\n")

    else:

        env1_py_version = "python-3.8"
        env1_modules = os.listdir(env1_path + os.sep + "Lib" + os.sep + "site-packages")
        # subprocess.check_output(
        #     f"ls -d {str(env1_path)}/lib/{env1_py_version}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;' ",
        #     shell=True,
        # )
        env2_py_version = "python-3.8"
        env2_modules = os.listdir(env1_path + os.sep + "Lib" + os.sep + "site-packages")
        # subprocess.check_output(
        #     f"ls -d {str(env2_path)}/lib/{env2_py_version}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;'",
        #     shell=True,
        # )

        output_split1 = [module[:module.rfind(".")] for module in env1_modules if "dist-info" in module] #env1_modules.decode("utf-8").split("\n")
        output_split2 = [module[:module.rfind(".")] for module in env2_modules if "dist-info" in module] #env2_modules.decode("utf-8").split("\n")


    env1_map = {}
    env2_map = {}

    cols = [
        "Module",
        f"{env1_name} ({env1_py_version})",
        f"{env2_name} ({env2_py_version})",
    ]
    similar_list = []
    non_similar_list = []

    for i in output_split1:
        try:
            env1_map[i.split("-")[0]] = i.split("-")[1]
        except:
            pass  # TODO

    for i in output_split2:
        try:
            env2_map[i.split("-")[0]] = i.split("-")[1]
        except:
            pass  # TODO

    def same_keys(first, second):
        return [k for k in first.keys() if k in second.keys()]

    result = same_keys(env1_map, env2_map)
    for key in result:
        if env1_map[key] == env2_map[key]:
            similar_list.append([key, env1_map[key], env2_map[key]])
        else:
            non_similar_list.append([key, env1_map[key], env2_map[key]])

    keys_in_env1 = env1_map.keys()
    keys_in_env2 = env2_map.keys()
    only_in_env1 = list(set(keys_in_env1) - set(keys_in_env2))
    only_in_env2 = list(set(keys_in_env2) - set(keys_in_env1))

    only_env_1_list = []
    only_env_2_list = []

    for k in only_in_env1:
        only_env_1_list.append([k, env1_map[k]])

    for k in only_in_env2:
        only_env_2_list.append([k, env2_map[k]])

    try:
        if display in ["all", None]:
            print(Colors.OKGREEN + "SAME MODULE VERSIONS " + Colors.END)
            print(tf.generate_table(similar_list, cols))
            print(Colors.WARNING + "DIFFERENT MODULE VERSIONS " + Colors.END)
            print(tf.generate_table(non_similar_list, cols))
            print(
                "ONLY IN "
                + Colors.BOLD
                + Colors.OKGREEN
                + f"{env1_name} ({env1_py_version})"
                + Colors.END
            )
            print(f"({env1_path})")

            col_1 = [f"{env1_name}({env1_py_version})", "version"]
            print(tf.generate_table(only_env_1_list, col_1))

            print(
                "ONLY IN "
                + Colors.BOLD
                + Colors.OKGREEN
                + f"{env2_name} ({env2_py_version})"
                + Colors.END
            )
            print(f"({env2_path})")

            col_2 = [f"{env2_name}({env2_py_version})", "version"]
            print(tf.generate_table(only_env_2_list, col_2))

        elif display == "diff":
            print(Colors.WARNING + "DIFFERENT MODULE VERSIONS " + Colors.END)
            print(tf.generate_table(non_similar_list, cols))
        elif display == "similar":
            print(Colors.OKGREEN + "SAME MODULE VERSIONS " + Colors.END)
            print(tf.generate_table(similar_list, cols))
        elif display == "separate":
            print(
                "ONLY IN "
                + Colors.BOLD
                + Colors.OKGREEN
                + f"{env1_name}({env1_py_version})"
                + Colors.END
            )
            print(f"({env1_path})")

            col_1 = [f"{env1_name} ({env1_py_version})", "version"]
            print(tf.generate_table(only_env_1_list, col_1))

            print(
                "ONLY IN "
                + Colors.BOLD
                + Colors.OKGREEN
                + f"{env2_name}({env2_py_version})"
                + Colors.END
            )
            print(f"({env2_path})")

            col_2 = [f"{env2_name} ({env2_py_version})", "version"]
            print(tf.generate_table(only_env_2_list, col_2))

    except Exception as exception:
        print(exception)
