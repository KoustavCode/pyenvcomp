import argparse
import subprocess
import tableformatter as tf
import os
import sys
from termcolor import colored, cprint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


my_parser = argparse.ArgumentParser(description='Compares the given python virtual environments')

my_parser.add_argument('Path1',
                       metavar='env path1',
                       type=str,
                       help='python virtual-environment path')

my_parser.add_argument('Path2',
                       metavar='env path2',
                       type=str,
                       help='python virtual-environment path')

my_parser.add_argument('--display', action='store', type=str, required=False)


args = my_parser.parse_args()
# print(args)
input_path = args.Path1
comp_path = args.Path2
print(args.display)


env_1_name = input_path[input_path.rfind("/")+1:]

env_2_name = comp_path[comp_path.rfind("/")+1:]

python_version_env_1 = os.listdir(input_path+os.sep+"/lib")[0]
path1_modules = subprocess.check_output(f"ls -d {str(input_path)}/lib/{python_version_env_1}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;' ", shell=True)
python_version_env_2 = os.listdir(comp_path+os.sep+"/lib")[0]
path2_modules = subprocess.check_output(f"ls -d {str(comp_path)}/lib/{python_version_env_2}/site-packages/*.dist-info | xargs -I% basename % | sed 's/\.dist-info//;'", shell=True)

output_split1= path1_modules.decode("utf-8") .split('\n')
output_split2= path2_modules.decode("utf-8") .split('\n')

env_map1 = {}
env_map2 = {}

cols = ['Module', f"env_1_name({python_version_env_1})", f"env_2_name({python_version_env_2})"]
similar_list = []
non_similar_list = []

for i in output_split1:
    try:
        env_map1[i.split("-")[0]] = i.split("-")[1]
    except:
        pass #TODO

for i in output_split2:
    try:
        env_map2[i.split("-")[0]] = i.split("-")[1]
    except:
        pass #TODO

same_keys = lambda first,second: [k for k in first.keys() if k in second.keys()]
result = same_keys(env_map1, env_map2)
for key in result:
    if env_map1[key] == env_map2[key]:
        similar_list.append([key, env_map1[key], env_map2[key]])
    else:
        non_similar_list.append([   key, env_map1[key], env_map2[key]])


# for k1,v1 in env_map1.iterms():
#     for k2,v2 in env_map2.items():
#         if k1==k1:
#             if v1==v2:
#                 similar_list.append(k1, v1, v2)
# if python_version_env_1 != python_version_env_2:
#     print(f"{bcolors.WARNING}Warning: Version of python is different.")
# else:
#     print(f"{bcolors.OKGREEN}Same version!")



# print(" SAME MODULES ")
# print(tf.generate_table(similar_list, cols))
# print(" DIFFERENT MODULES ")    
# print(tf.generate_table(non_similar_list, cols))

# print(f'IN --- {python_version_env_1}')
keys_in_env1 = env_map1.keys()
keys_in_env2 = env_map2.keys()
only_in_env1 = list(set(keys_in_env1) - set(keys_in_env2))
only_in_env2 = list(set(keys_in_env2) - set(keys_in_env1))
# print(only_in_env1)
# print(only_in_env2)

only_env_1_list = []
only_env_2_list = []

for k in only_in_env1:
    only_env_1_list.append([k,env_map1[k]])

for k in only_in_env2:
    only_env_2_list.append([k,env_map2[k]])



# print('ONLY IN ' + bcolors.BOLD + bcolors.OKGREEN + f'{env_1_name}({python_version_env_1})' + bcolors.END)

# col_1 = [f"env_1_name({python_version_env_1})", "version"]
# print(tf.generate_table(only_env_1_list, col_1))

# print('ONLY IN ' + bcolors.BOLD + bcolors.OKGREEN + f'{env_2_name}({python_version_env_2})' + bcolors.END)

# col_2 = [f"env_2_name({python_version_env_2})", "version"]
# print(tf.generate_table(only_env_2_list, col_2))



# print(bcolors.BOLD + bcolors.OKGREEN + 'Hello World !' + bcolors.END)

# print(only_env_2_list)

# print(env_map1)
# print(env_map2)
try:
    if args.display in ['all', None]:
        print(" SAME MODULES ")
        print(tf.generate_table(similar_list, cols))
        print(" DIFFERENT MODULES ")    
        print(tf.generate_table(non_similar_list, cols))
        print('ONLY IN ' + bcolors.BOLD + bcolors.OKGREEN + f'{env_1_name}({python_version_env_1})' + bcolors.END)

        col_1 = [f"env_1_name({python_version_env_1})", "version"]
        print(tf.generate_table(only_env_1_list, col_1))

        print('ONLY IN ' + bcolors.BOLD + bcolors.OKGREEN + f'{env_2_name}({python_version_env_2})' + bcolors.END)

        col_2 = [f"env_2_name({python_version_env_2})", "version"]
        print(tf.generate_table(only_env_2_list, col_2))


        # pass
    elif args.display == 'diff':
        print(" DIFFERENT MODULES ")    
        print(tf.generate_table(non_similar_list, cols))
        # pass
    elif args.display == 'similar':
        print(" SAME MODULES ")
        print(tf.generate_table(similar_list, cols))
    elif args.display == 'separate':
        print('ONLY IN ' + bcolors.BOLD + bcolors.OKGREEN + f'{env_1_name}({python_version_env_1})' + bcolors.END)

        col_1 = [f"env_1_name({python_version_env_1})", "version"]
        print(tf.generate_table(only_env_1_list, col_1))

        print('ONLY IN ' + bcolors.BOLD + bcolors.OKGREEN + f'{env_2_name}({python_version_env_2})' + bcolors.END)

        col_2 = [f"env_2_name({python_version_env_2})", "version"]
        print(tf.generate_table(only_env_2_list, col_2))

        # pass



# text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
# print(text)
# cprint('Hello, World!', 'green', 'on_red')
except:
    pass