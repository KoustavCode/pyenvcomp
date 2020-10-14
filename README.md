# pyenvcomp  
## The python environment comparator tool :snake:

## **Installation**

```
pip install pyenvcomp
```

## **Usage**

```
➜  compare  Path1 Path2  --display <value>
```
**Path1** -  path to one environment.

**Path2** -  path to another environment. 

**List of diplay types available:**

1. ```all``` - displays all the difference, similarity and extra modules in each virual environments.
2. ```diff``` - displays just the list of modules which are present in both the virtual environments but differs in version.
3. ```separate``` - displays two different tables of extra modules in each virual environments.

*default* - similar to     ```all```  value of  ```display```  argument.


## **Example** :man_technologist:


### **Input**

```
$ compare /home/koustav/Documents/test_env_1 /home/koustav/Documents/test_env_2 --display all
```
where, `test_env_1` and `test_env_2` are my two python virtual environments .

### **Output**

```
SIMILAR MODULES 
╔═════════════════╤═══════════════════════╤═══════════════════════╗
║ Module          │ test_env_1(python3.8) │ test_env_2(python3.8) ║
╠═════════════════╪═══════════════════════╪═══════════════════════╣
║ appdirs         │ 1.4.3                 │ 1.4.3                 ║
║ CacheControl    │ 0.12.6                │ 0.12.6                ║
║ certifi         │ 2019.11.28            │ 2019.11.28            ║
║ chardet         │ 3.0.4                 │ 3.0.4                 ║
║ colorama        │ 0.4.3                 │ 0.4.3                 ║
║ contextlib2     │ 0.6.0                 │ 0.6.0                 ║
║ distlib         │ 0.3.0                 │ 0.3.0                 ║
║ distro          │ 1.4.0                 │ 1.4.0                 ║
║ html5lib        │ 1.0.1                 │ 1.0.1                 ║
║ idna            │ 2.8                   │ 2.8                   ║
║ ipaddr          │ 2.2.0                 │ 2.2.0                 ║
║ lockfile        │ 0.12.2                │ 0.12.2                ║
║ msgpack         │ 0.6.2                 │ 0.6.2                 ║
║ packaging       │ 20.3                  │ 20.3                  ║
║ pep517          │ 0.8.2                 │ 0.8.2                 ║
║ pip             │ 20.0.2                │ 20.0.2                ║
║ pkg_resources   │ 0.0.0                 │ 0.0.0                 ║
║ progress        │ 1.5                   │ 1.5                   ║
║ pyparsing       │ 2.4.6                 │ 2.4.6                 ║
║ python_dateutil │ 2.8.1                 │ 2.8.1                 ║
║ pytoml          │ 0.1.21                │ 0.1.21                ║
║ pytz            │ 2020.1                │ 2020.1                ║
║ requests        │ 2.22.0                │ 2.22.0                ║
║ retrying        │ 1.3.3                 │ 1.3.3                 ║
║ setuptools      │ 44.0.0                │ 44.0.0                ║
║ six             │ 1.14.0                │ 1.14.0                ║
║ urllib3         │ 1.25.8                │ 1.25.8                ║
║ webencodings    │ 0.5.1                 │ 0.5.1                 ║
║ wheel           │ 0.34.2                │ 0.34.2                ║
╚═════════════════╧═══════════════════════╧═══════════════════════╝

 DIFFERENT MODULES 
╔════════╤═══════════════════════╤═══════════════════════╗
║ Module │ test_env_1(python3.8) │ test_env_2(python3.8) ║
╠════════╪═══════════════════════╪═══════════════════════╣
║ numpy  │ 1.19.2                │ 1.19.1                ║
║ pandas │ 1.1.2                 │ 1.1.3                 ║
╚════════╧═══════════════════════╧═══════════════════════╝

ONLY IN test_env_1(python3.8)
╔═══════════════════════╤═════════╗
║ test_env_1(python3.8) │ version ║
╠═══════════════════════╪═════════╣
║ wrapt                 │ 1.12.1  ║
║ pikepdf               │ 1.19.3  ║
║ lazy_object_proxy     │ 1.4.3   ║
║ pylint                │ 2.6.0   ║
║ toml                  │ 0.10.1  ║
║ Pillow                │ 7.2.0   ║
║ lxml                  │ 4.5.2   ║
║ astroid               │ 2.4.2   ║
║ isort                 │ 5.6.4   ║
║ mccabe                │ 0.6.1   ║
╚═══════════════════════╧═════════╝

ONLY IN test_env_2(python3.8)
╔═══════════════════════╤═════════╗
║ test_env_2(python3.8) │ version ║
╠═══════════════════════╪═════════╣
║ Werkzeug              │ 1.0.1   ║
║ MarkupSafe            │ 1.1.1   ║
║ tornado               │ 6.0.4   ║
║ itsdangerous          │ 1.1.0   ║
║ click                 │ 7.1.2   ║
║ Flask                 │ 1.1.2   ║
║ Jinja2                │ 2.11.2  ║
╚═══════════════════════╧═════════╝
```
Visuals in actual terminal would look a bit different than the above output visual.

## **Future versions**

In the upcoming versions following features will be added:

1. Compare directly from ```Requirements.txt``` file
2. Warning messages will be provided if any depricated version of any module is being used.

Inspired by problems faced while doing r&d at my workplace :nerd_face: