import sys
import numpy as np
import math
import matplotlib.pyplot as plt

def latlong_psp(
    file,
    ):

    if type(file) is not dict:
        raise ValueError(
            f"Argument '{file}' should be a file, "
            f"instead got shape {file.shape}."
            )

    file_keys = []
    for key in file.keys():
        file_keys.append(key)
        
    time = file[file_keys[0]]
    psp_hgi_x = file[file_keys[1]]
    psp_hgi_y = file[file_keys[2]]
    psp_hgi_z = file[file_keys[3]]
    
    length = len(file[file_keys[1]])
    fact = 180/math.pi

    key_list = ['time','radius','theta','phi','lat','long']

    result = {}
    
    for i in key_list:
        result[i] = np.zeros(length)
        
    
    for j in range(length):
        result[key_list[0]][j] = time[j]
        result[key_list[1]][j] = np.sqrt((psp_hgi_x[j])**2+(psp_hgi_y[j])**2+(psp_hgi_z[j])**2)
        result[key_list[2]][j] = np.arctan2(np.sqrt((psp_hgi_x[j]**2)+(psp_hgi_y[j]**2)),psp_hgi_z[j])*fact #Theta
        result[key_list[3]][j] = np.arctan2(psp_hgi_y[j],psp_hgi_x[j])*fact #Phi

        result[key_list[4]][j] = result[key_list[2]][j] - 90   #Theta lat [-90,-90]
        result[key_list[5]][j] = result[key_list[3]][j] - 180  #Phi long [-180,180]

    for i in range(length):
        if  result[key_list[5]][i] < - 180:
            result[key_list[5]][i] = result[key_list[5]][i] + 360
        elif  result[key_list[5]][i] > 180:
            result[key_list[5]][i] = result[key_list[5]][i] - 360
        else:
            result[key_list[5]][i] = result[key_list[5]][i]

        if  result[key_list[4]][i] < - 90:
            result[key_list[4]][i] = result[key_list[4]][i] + 180
        elif  result[key_list[4]][i] > 90:
            result[key_list[4]][i] = result[key_list[4]][i] - 180
        else:
            result[key_list[4]][i] = result[key_list[4]][i]
            
    return result

def latlong_wind(
    file,
    ):

    if type(file) is not dict:
        raise ValueError(
            f"Argument '{file}' should be a file, "
            f"instead got shape {file.shape}."
            )

    file_keys = []
    for key in file.keys():
        file_keys.append(key)

    length = len(file[file_keys[0]])
    fact = 180/math.pi

    result = {}
 
    for i in file_keys:
        result[i] = np.zeros(length)
        for j in range(len(file[i])):
            result[i][j] = file[i][j]

    for i in range(length):
        result[file_keys[2]][i] = result[file_keys[2]][i] #- 180   #Long
        result[file_keys[1]][i] = result[file_keys[1]][i] #- 90 #Lat

    for i in range(length):
        if  result[file_keys[2]][i] < - 180:
            result[file_keys[2]][i] = result[file_keys[2]][i] + 360
        elif  result[file_keys[2]][i] > 180:
            result[file_keys[2]][i] = result[file_keys[2]][i] - 360
        else:
            result[file_keys[2]][i] = result[file_keys[2]][i]
        
        if  result[file_keys[1]][i] < - 90:
            result[file_keys[1]][i] = result[file_keys[1]][i] + 180
        elif  result[file_keys[1]][i] > 90:
            result[file_keys[1]][i] = result[file_keys[1]][i] - 180
        else:
            result[file_keys[1]][i] = result[file_keys[1]][i]
        
    return result

def latlong_graph(
    psp_orbit,
    wind_orbit,
):

    psp_keys = []
    for key in psp_orbit.keys():
        psp_keys.append(key)
    
    wind_keys = []
    for key in wind_orbit.keys():
        wind_keys.append(key)

    x_dim = 10
    y_dim = 10

    plt.figure(figsize=(x_dim, y_dim))
    plt.plot(psp_orbit[psp_keys[0]], psp_orbit[psp_keys[5]], label='Long PSP')
    #plt.plot(psp_orbit[psp_keys[0]], psp_orbit[psp_keys[3]], label='Phi PSP')
    plt.plot(wind_orbit[wind_keys[0]], wind_orbit[wind_keys[2]], label='Wind Long')
    plt.title('Graph of Longitudes', fontsize=24)
    plt.ylabel('Degrees',fontsize=20)
    plt.xlabel('Index',fontsize=20)
    plt.legend(loc='upper right',fontsize=14)
    plt.grid()
    plt.show()

    plt.figure(figsize=(x_dim, y_dim))
    plt.plot(psp_orbit[psp_keys[0]], psp_orbit[psp_keys[4]], label='Lat PSP')
    plt.plot(psp_orbit[psp_keys[0]], psp_orbit[psp_keys[2]], label='Theta PSP')
    plt.plot(wind_orbit[wind_keys[0]], wind_orbit[wind_keys[1]], label='Wind Lat')
    plt.title('Graph of Latitudes')
    plt.ylabel('Degrees')
    plt.xlabel('Index')
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()

    return
