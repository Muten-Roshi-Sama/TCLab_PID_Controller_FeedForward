# Control Theory and applications : 
# PID control (feedforward) using Temperature Control Lab kit

## Project Overview
This project aims to analyze the impact of Disturbances on a system and develop strategies for its anticipation. We use a TCLab Arduino Leonardo board equipped with two heaters and two temperature sensors.
![TCLAB_intro](https://github.com/Muten-Roshi-Sama/TCLab_PID_Controller_FeedForward/assets/131618669/7a138c37-1e18-4afe-8e71-24ae20b8bee1)
### Key Variables:
- **MV (Manipulated Variable) :** Represents the **first heater**, our adjustable parameter.
- **PV (Process Variable):** Denotes the **system output**, measured by the first temperature sensor.
- **DV (Disturbance Variable):** Refers to the **second heater**, which introduces *disturbances* to the system.
- **SP (Set Point):** Signifies the **target temperature** we aim to achieve.
	


### Graphical Approximations
![approx_model_comparison](https://github.com/Muten-Roshi-Sama/TCLab_PID_Controller_FeedForward/assets/131618669/4a4c2cd9-d6c6-4f89-9637-15d416511669)
This graph compares the differences between several approximation models, namely Broida's 1st and 2d models, Van Der Grinten and Strejc's models.

### Regulation Method:
To maintain temperature stability, we employ a **PID controller** with anticipatory actions facilitated by **feedforward** mechanisms. This integrated approach allows for effective system regulation and mitigation of disturbances.
![PIDCLPFF_normal4](https://github.com/Muten-Roshi-Sama/TCLab_PID_Controller_FeedForward/assets/131618669/61413db2-817a-4e7b-8826-074bc609ab20)
The best model will always be the Closed-Loop PID with Feedforward model. Even in presence of severe disturbances (last graph in red.)

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
