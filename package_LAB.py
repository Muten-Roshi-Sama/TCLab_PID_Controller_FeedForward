import numpy as np

import matplotlib.pyplot as plt
from IPython.display import display, clear_output

#-----------------------------------


#-----------------------------------
def LL_RT(MV, Kp, TLead, TLag, Ts, PV, PVInit=0, method='EBD'):
    """
    The function "LL_RT" needs to be included in a "for or while loop".
    :param MV: input vector
    :param Kp: process gain
    :param T1: lead time constant (positive value) [s]
    :param T2: lag time constant (positive value) [s]
    :param Ts: sampling period [s]
    :param PV: output vector
    :param PVInit: (optional: default value is 0)
    :param method: discretisation method (optional: default value is 'EBD')
        EBD: Euler Backward difference
        EFD: Euler Forward difference
        TRAP: Trapezoïdal method
    The function "LL_RT" appends a value to the output vector "PV".
    The appended value is obtained from a recurrent equation that considers
    both lead and lag time constants.
    """
    if (TLag != 0):
        K = Ts/TLag
        if len(PV) == 0:     #if we are at the beginning
            PV.append(PVInit)
        else: 
            if method == 'EBD':
                PV.append(((1/(1+K))*PV[-1]) + ((K*Kp/(1+K))*(((1+(TLead/Ts))*MV[-1])-((TLead/Ts)*MV[-2]))))
            elif method == 'EFD':
                PV.append((1-K)*PV[-1] + Kp*K*((TLead/Ts) *MV[-1] + (1-TLead/Ts)*MV[-2]) )
            # elif method == 'TRAP':
            #     PV.append(PV[-1]*((2-K)/(2+K)) + ((Kp*K)/(2+K)) * ((2*(TLead/Ts)+1)*MV[-1] - 2*(TLead/Ts)*MV[-2] + MV[-2] ))            
            else:      #default:EBD
                PV.append(((1/(1+K))*PV[-1]) + ((K*Kp/(1+K))*(((1+(TLead/Ts))*MV[-1])-((TLead/Ts)*MV[-2]))))
            
    else:
        PV.append(Kp*MV[-1])
    
    return PV  # Returning the updated PV list

#-----------------------------------

def PID_RT(SP, PV, Man, MVMan, MVFF, KC, Ti, Td, alpha, Ts, MVMin, MVMax, MV, MVP, MVI, MVD, E, ManFF=False, PVInit=0, method='EBD-EBD'):
    """
    The function "PID_RT" needs to be included in a "for or while loop".
    SP: (or SetPoint) vector
    PV: (or Process Value) vector
    Man: (or Manual controller mode) vector (True or False)
    MVMan:(or Manual value for MV) vector
    MVFF: (or Feedforward) vector
    KC: controller gain
    Ti: integral time constant [s]
    Td: derivative time constant [s]
    alpha: TFD = alpha*Td where TFD is the derivative filter time constant [s]
    Ts: sampling period [s]
    MVMin: minimum value for MV (used for saturation and anti wind-up) :MVMax: maximum value for MV (used for saturation and anti wind-up)
    MV: MV (or Manipulated Value) vector
    MVP: MVP (or Propotional part of MV) vector
    MVI: MVI (or Integral part of MV) vector
    MVD: MVD (or Derivative part of MV) vector
    E: E (or control Error) vector
    ManFF: Activated FF in manual mode (optional: default boolean value is False)
    PVInit: Init value for PV (optional: default value is 0): used if PID_RT is ran first in the squence and no value of PV available yet.
    method: discretisation method (optional: default value is 'EBD')
    EBD-EBD: EBD for integral action and EBD for derivative action 
    EBD-TRAP: EBD for integral action and TRAP for derivative action 
    TRAP-EBD: TRAP for integral action and EBD for derivative action 
    TRAP-TRAP: TRAP for integral action and TRAP for derivative action
    The function "PID_RT" appends new values to the vectors "MV", "MVP", "MVI", and "MVD".
    The appended values are based on the PID algorithm, the controller mode, and feedforward.
    Note that saturation of "MV" within the limits [MVMin MVMax] is implemented with anti wind-up.
"""
    #Initialiwation
    TFD = Td * alpha
    #-----------------ERROR----------------
    if len(PV) ==0 :
        E.append(SP[-1] - PVInit)
    else:
        E.append(SP[-1] - PV[-1])

    if len(MVP)==0 :
        MVP.append((KC*E[-1]))
    else:
        if method == 'EBD-EBD':
            MVP.append(KC*E[-1])
        # elif method == 'TRAP-TRAP':  
        #     MVP.append(KC*E[-1])        
        else: 
            MVP.append(KC*E[-1])
    
    #-----------------Integral Action---------
    if len(MVI) == 0 :      
        MVI.append((KC*Ts/Ti)*E[-1])    # MV[k] is MV[-1] and MV[k-1] is MV[-2]
    else:
        if method == 'EBD-EBD':
            MVI.append(MVI[-1] + ((KC*Ts)/Ti)*(E[-1]))
        elif method == 'TRAP':
            MVI.append(MVI[-1] + (0.5*KC*Ts/Ti)*(E[-1] + E[-2]))
        else:      #default :EBD
            MVI.append(MVI[-1] + (KC*Ts/Ti)*E[-1])

    #------------------Derivative Action-------------
    if len(MVD)==0:
        MVD.append(((KC*Td)/(TFD+Ts))*(E[-1]))
    else:
        if method == 'EBD-EBD':
            MVD.append((TFD/(TFD+Ts))*MVD[-1] + ((KC*Td)/(TFD+Ts))*(E[-1] - E[-2])) 
        elif method =='TRAP-TRAP':
            MVD.append((((TFD-(Ts/2))/(TFD+(Ts/2)))*MVD[-1] + ((KC*Td)/(TFD+(Ts/2)))*(E[-1] - E[-2])))     
        else:  # EBD
            MVD.append((TFD/(TFD+Ts))*MVD[-1] + ((KC*Td)/(TFD+Ts))*(E[-1] - E[-2]))



    #------------Mode manuel + anti-wind up (integrator help)----------
    if Man[-1] == True:
        if ManFF:
            MVI[-1] = MVMan[-1] - MVP[-1] - MVD[-1] 
        else:
            MVI[-1] = MVMan[-1] - MVP[-1] - MVD[-1] - MVFF[-1]

    # -----------------Saturation----------------------
    if (MVP[-1] + MVI[-1] + MVD[-1] + MVFF[-1]) > MVMax:
        MVI[-1] = MVMax - MVP[-1] - MVD[-1] - MVFF[-1]
    elif (MVP[-1] + MVI[-1] + MVD[-1] + MVFF[-1]) < MVMin:
        MVI[-1] = MVMin - MVP[-1] - MVD[-1] - MVFF[-1]

    # Ajout sur MV
    MV.append(MVP[-1] + MVI[-1] + MVD[-1] + MVFF[-1])







#----------------------------------------------------------------------------------------------   



#-----------------------------------


#-----------------------------------        
# class Controller:  // pour plus tard
    
    # def __init__(self, parameters):
        
    #     self.parameters = parameters
    #     self.parameters['Kp'] = parameters['Kp'] if 'Kp' in parameters else 1.0
    #     self.parameters['theta'] = parameters['theta'] if 'theta' in parameters else 0.0
    #     self.parameters['Tlead1'] = parameters['Tlead1'] if 'Tlead1' in parameters else 0.0
    #     self.parameters['Tlead2'] = parameters['Tlead2'] if 'Tlead2' in parameters else 0.0
    #     self.parameters['Tlag1'] = parameters['Tlag1'] if 'Tlag1' in parameters else 0.0
    #     self.parameters['Tlag2'] = parameters['Tlag2'] if 'Tlag2' in parameters else 0.0
    #     self.parameters['nInt'] = parameters['nInt'] if 'nInt' in parameters else 0        

#-----------------------------------        
