# Control Theory and applications : 
# PID control (feedforward) using Temperature Control Lab kit

## Project Overview
This project aims to analyze the impact of Disturbances on a system and develop strategies for its anticipation. We use a TCLab Arduino Leonardo board equipped with two heaters and two temperature sensors.

### Key Variables:
- **MV (Manipulated Variable) :** Represents the **first heater**, our adjustable parameter.
- **PV (Process Variable):** Denotes the **system output**, measured by the first temperature sensor.
- **DV (Disturbance Variable):** Refers to the **second heater**, which introduces *disturbances* to the system.
- **SP (Set Point):** Signifies the **target temperature** we aim to achieve.
	
### Regulation Method:
To maintain temperature stability, we employ a **PID controller** with anticipatory actions facilitated by feedforward mechanisms. This integrated approach allows for effective system regulation and mitigation of disturbances.

## PIP Requirements
```python
>> pip install pandas numpy matplotlib
```
For any permission related errors try :
```python
>> pip install pandas numpy matplotlib --user
```
Be sure to use the same python version for your kernel and on your terminal when installing with pip (ModuleNotFoundError)
Disabling pylance solves the *'import "pandas" could not be resolved from sourcePylancereportMissingModuleSource'* problem.

## Submission
- **Submission Deadline:** 04 april 2024, 4pm
