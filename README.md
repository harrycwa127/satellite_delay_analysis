# satellite_delay_analysis

## Introduction

The overall objective is to analyze if the data download deadline can be met given the data on an LEO satellite can be transferred either directly to a ground station or via some other LEO satellite, given a configuration of an LEO satellite constellation and a set of ground stations. The analysis is conducted based on the simulation of the communication behavior between LEO satellites and between an LEO satellite and the ground stations.

---

## Guideline

### Setting

To Set up the parameter of the Simulator. A settings folder contains the setting file as below.

| Setting file name       | description                                                                      | format                             |
| ----------------------- | -------------------------------------------------------------------------------- | ---------------------------------- |
| main_GROUND_STATION.txt | use for simulator, contain only one ground station as the point data transfer to | Latitude(degree) Longitude(degree) |
| main_OBSERVATION.txt    | use for simulator, contain only one observation point as the point to observe   | Latitude(degree) Longitude(degree) |
| test_GROUND_STATION.txt | use for testing. contain a ground station list                                   | Latitude(degree) Longitude(degree) |
| test_OBSERVATION.txt    | use for testing, contain a observation points list as the poin to observe        | Latitude(degree) Longitude(degree) |
| TIME_INTERVAL.txt       | use for simulator and testing, define the datetime of simulator                 | yyyy MM dd hh mm ss                |

### Environment

The environment requires python3.8, if python version>=3.10, use py command instead of python, sample as below

```
py main.py
```

For install the python liburay run the following command in the project directory.

```
pip install -r "requirements.txt"
```

### Execute

At the project directory, run the main.py file to start the Simulator, comment as below.

```
python main.py
```

After starting the Simulator, a window with default value is created to set up the parameter.
![Setting Window](readme_img/settingUI.png)

After setting the parameter, click submit to start Simulator

if want to disable the Setting Window, please open the main.py and follow the step below.

1. go to line 21, comment or delete the code, as below

   ```
   Setting.display()
   ```
2. uncomment the code from line 24 to 35 as below.
   ![Setting Window](readme_img/disable_setting_UI.png)
3. If want to modify the value, just change the value in line 24 to 35.

### Result

After the Simulator is started, the result window will be popup as below.
![Setting Window](readme_img/path.png)

The detailed data will be stored as analysis result.xls in the results folder.
