import argparse
import subprocess
import tableformatter as tf
import os

# my_parser = argparse.ArgumentParser(allow_abbrev=False)

my_parser = argparse.ArgumentParser(description="List the content of a folder")

# my_parser.add_argument('--env', action='store', type=string, required=True)
my_parser.add_argument("Path1", metavar="env path1", type=str, help="the path to list")

my_parser.add_argument("Path2", metavar="env path2", type=str, help="the path to list")

args = my_parser.parse_args()
# print(args)
input_path = args.Path1
comp_path = args.Path2

env_1_name = input_path[input_path.rfind("/") + 1 : input_path.rfind(".")]

env_2_name = comp_path[comp_path.rfind("/") + 1 : comp_path.rfind(".")]

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

output_split1 = path1_modules.decode("utf-8").split("\n")
output_split2 = path2_modules.decode("utf-8").split("\n")

env_map1 = {}
env_map2 = {}

cols = [
    "Module",
    f"env_1_name({python_version_env_1})",
    f"env_2_name({python_version_env_2})",
]
similar_list = []
non_similar_list = []

for i in output_split1:
    try:
        env_map1[i.split("-")[0]] = i.split("-")[1]
    except:
        pass

for i in output_split2:
    try:
        env_map2[i.split("-")[0]] = i.split("-")[1]
    except:
        pass

same_keys = lambda first, second: [k for k in first.keys() if k in second.keys()]
result = same_keys(env_map1, env_map2)
for key in result:
    if env_map1[key] == env_map2[key]:
        similar_list.append([key, env_map1[key], env_map2[key]])
    else:
        non_similar_list.append([key, env_map1[key], env_map2[key]])


# for k1,v1 in env_map1.iterms():
#     for k2,v2 in env_map2.items():
#         if k1==k1:
#             if v1==v2:
#                 similar_list.append(k1, v1, v2)
print(" SAME MODULES ")
print(tf.generate_table(similar_list, cols))
print(" DIFFERENT MODULES ")
print(tf.generate_table(non_similar_list, cols))

# print(env_map1)
# print(env_map2)
