# pyenvcomp  
## The python environment comparator tool

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

## **Future versions**

