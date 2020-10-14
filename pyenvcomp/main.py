"""
PYENVCOMP
"""

import os
import argparse
import subprocess
import tableformatter as tf


class Colors:
    """ Color listing class
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class ArgParse:
    """
    Argument parsing class
    """

    def __init__(self, path1, path2, display=None):
        """init function
        """

        self.path1 = path1
        self.path2 = path2
        self.display = display

    def parse_args(self, argv=None):
        """ Parses the commandline argument
        """

        parser = argparse.ArgumentParser()

        parser.add_argument(
            'Path1',
            metavar='env path1',
            type=str,
            help='python virtual-environment path',
        )

        parser.add_argument(
            'Path2',
            metavar='env path2',
            type=str,
            help='python virtual-environment path',
        )
        parser.add_argument('-d', '--display', type=str, help='username')

        args = parser.parse_args(argv)
        self.path1 = args.Path1
        self.path2 = args.Path2
        self.display = args.display


def main():
    """
    The main comparing function 
    """

    arg_parse = ArgParse(path1=None, path2=None)
    arg_parse.parse_args()
    args = vars(arg_parse)

    input_path = args['path1']
    comp_path = args['path2']
    display = args['display']

    env_1_name = input_path[input_path.rfind("/") + 1 :]

    env_2_name = comp_path[comp_path.rfind("/") + 1 :]

    python_version_env_1 = os.listdir(input_path + os.sep + "/lib")[0]
    path1_modules = subprocess.check_output(
        f"ls -d {str(input_path)}/lib/{python_version_env_1}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;' ",
        shell=True,
    )
    python_version_env_2 = os.listdir(comp_path + os.sep + "/lib")[0]
    path2_modules = subprocess.check_output(
        f"ls -d {str(comp_path)}/lib/{python_version_env_2}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;'",
        shell=True,
    )

    output_split1 = path1_modules.decode("utf-8").split('\n')
    output_split2 = path2_modules.decode("utf-8").split('\n')

    env_map1 = {}
    env_map2 = {}

    cols = [
        'Module',
        f"{env_1_name}({python_version_env_1})",
        f"{env_2_name}({python_version_env_2})",
    ]
    similar_list = []
    non_similar_list = []

    for i in output_split1:
        try:
            env_map1[i.split("-")[0]] = i.split("-")[1]
        except:
            pass  # TODO

    for i in output_split2:
        try:
            env_map2[i.split("-")[0]] = i.split("-")[1]
        except:
            pass  # TODO

    same_keys = lambda first, second: [k for k in first.keys() if k in second.keys()]
    result = same_keys(env_map1, env_map2)
    for key in result:
        if env_map1[key] == env_map2[key]:
            similar_list.append([key, env_map1[key], env_map2[key]])
        else:
            non_similar_list.append([key, env_map1[key], env_map2[key]])

    keys_in_env1 = env_map1.keys()
    keys_in_env2 = env_map2.keys()
    only_in_env1 = list(set(keys_in_env1) - set(keys_in_env2))
    only_in_env2 = list(set(keys_in_env2) - set(keys_in_env1))

    only_env_1_list = []
    only_env_2_list = []

    for k in only_in_env1:
        only_env_1_list.append([k, env_map1[k]])

    for k in only_in_env2:
        only_env_2_list.append([k, env_map2[k]])

    try:
        if display in ['all', None]:
            print(" SAME MODULE VERSIONS ")
            print(tf.generate_table(similar_list, cols))
            print(" DIFFERENT MODULE VERSIONS ")
            print(tf.generate_table(non_similar_list, cols))
            print(
                'ONLY IN '
                + Colors.BOLD
                + Colors.OKGREEN
                + f'{env_1_name}({python_version_env_1})'
                + Colors.END
            )

            col_1 = [f"{env_1_name}({python_version_env_1})", "version"]
            print(tf.generate_table(only_env_1_list, col_1))

            print(
                'ONLY IN '
                + Colors.BOLD
                + Colors.OKGREEN
                + f'{env_2_name}({python_version_env_2})'
                + Colors.END
            )

            col_2 = [f"{env_2_name}({python_version_env_2})", "version"]
            print(tf.generate_table(only_env_2_list, col_2))

        elif display == 'diff':
            print(" DIFFERENT MODULE VERSIONS ")
            print(tf.generate_table(non_similar_list, cols))
        elif display == 'similar':
            print(" SAME MODULE VERSIONS ")
            print(tf.generate_table(similar_list, cols))
        elif display == 'separate':
            print(
                'ONLY IN '
                + Colors.BOLD
                + Colors.OKGREEN
                + f'{env_1_name}({python_version_env_1})'
                + Colors.END
            )

            col_1 = [f"{env_1_name}({python_version_env_1})", "version"]
            print(tf.generate_table(only_env_1_list, col_1))

            print(
                'ONLY IN '
                + Colors.BOLD
                + Colors.OKGREEN
                + f'{env_2_name}({python_version_env_2})'
                + Colors.END
            )

            col_2 = [f"{env_2_name}({python_version_env_2})", "version"]
            print(tf.generate_table(only_env_2_list, col_2))

    except Exception as exception:
        print(exception)
