#!/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import os
import subprocess

path = os.getcwd()




def read_file(fich):
    npot=int(0)
    CSFs={}
    time=[]
    with open(fich,"r") as f:
        for line in f:
            kk=line.split()
            if len(kk)!=0:
                CSF=[]
                npot=len(kk)
                key=kk[0]
                time.append(key)
                for i in range(1,npot):
                    CSF.append(float(kk[i]))
                    CSFs[key]=CSF
    return CSFs,time


def read_folders(namefolder,folderlist):
    ATA  = {}
    EF   = {}
    Pop  = {}
    time = []
    npop = 0
    l=0
    for i in folderlist:
        Abs = {}
        EFi = {}
        Popi = {}
    
        Abs,time  = read_file(namefolder + i + "/Output/TransientAbs.txt")
        EFi,time  = read_file(namefolder  + i + "/Output/EF.txt")
        ##Popi,time = read_file(namefolder + i + "/Output/Losses.txt")
        Polx    = get_polarization(namefolder + i + "/input.txt")
        ATA[l] = Abs
        EF[l]   = EFi
        Pop[l]  = Popi
        ##for item in Popi:
        ##    npop = len(Popi[item])
        l=l+1
    ##return ATA,EF,Pop,time,Polx,npop
    return ATA,EF,time,Polx

def folders(delays):
    folderlist = []
    testfolder=delays
    testfolder = testfolder[::-1]
    for i in range(len(testfolder)):
        folderlist.append("delay_" + "{:.1f}".format(testfolder[i]))
    
    del testfolder
    folderlist=np.array(folderlist)
    folderlist=folderlist.astype(str)

    # replace_func1 = np.vectorize(lambda x: str(x.replace('.','_')))
    # replace_func2 = np.vectorize(lambda x: str(x.replace('-','_')))
    # replace_func3 = np.vectorize(lambda x: str(x.replace('_0_00','0_00')))

    # folderlist=replace_func1(folderlist)
    # folderlist=replace_func2(folderlist)
    # folderlist=replace_func3(folderlist)
    print(folderlist)

    return folderlist

def get_polarization(fich):
    reading = False
    Polx=[]
    with open(fich,"r") as f:
        for line in f:
            kk=line.split()
            if len(kk)!=0:
                if "laserprobe" in line:
                    reading = True
                if "polarization" in line and reading:
                    #print(float(kk[1]),float(kk[2]),float(kk[3]))
                    Polx.append(float(kk[1]))
                    Polx.append(float(kk[2]))
                    Polx.append(float(kk[3]))
                    reading = False
                else:
                    pass
    norm = (Polx[0]**2+Polx[1]**2+Polx[2]**2)**0.5
    Polx[0]*= 1./norm;
    Polx[1]*= 1./norm;
    Polx[2]*= 1./norm;
    return Polx


# t1 - dipole
# ex - field
# time 
def fft_abs(t1_raw, ex_raw, time_raw, xlim):
    import numpy as np
    from numpy import sin, cos, exp, pi, e, sqrt
    from scipy import signal
    from cbwe_Python_source.fft_creation import prepareDataFFT_ATA

    time_au_fs   = 0.02418884326505
    energy_au_eV = 27.211396;
    dt_au      = (time_raw[1] - time_raw[0])/time_au_fs # Spacing [au]
    sfreq_au   = 1.00 / dt_au # Sampling Frequency [au]

    time =  np.arange(time_raw[0], time_raw[len(time_raw) - 1], time_raw[1] - time_raw[0])
    
    ex = prepareDataFFT_ATA(ex_raw, time, time_raw)
    t1 = prepareDataFFT_ATA(t1_raw, time, time_raw)
    # ex_reverse = np.flip(ex)
    # t1_reverse = np.flip(t1)

    zeros_for_append = np.zeros(10* len(t1))
    ex = np.append(zeros_for_append, ex)
    # ex = np.append(ex, ex_reverse)
    ex = np.append(ex, zeros_for_append)

    t1 = np.append(zeros_for_append, t1)
    # t1 = np.append(t1, t1_reverse)
    t1 = np.append(t1, zeros_for_append)

    ex_av = np.sum(ex) / len(ex)
    t1_av = np.sum(t1) / len(t1)

    # ex -= ex_av

    t1_fft = np.fft.ifft(t1)
    ex_fft = np.fft.ifft(ex)
    freq = np.fft.fftfreq(len(t1),d=dt_au)
    freq_ev  = (2 * pi) * freq * energy_au_eV
    
    Abs = 2.*(t1_fft*(np.conjugate(ex_fft))).imag
    Abs/= (ex_fft.real)**2+(ex_fft.imag)**2
    Abs*= 4.*pi*137. #freq*4.*pi*137 freq << w_x (photon of the x rays)
    
    order_freq = np.fft.ifftshift(freq_ev)
    condition  = (order_freq > xlim[0]) & (order_freq < xlim[1])
    winAbs   = np.extract(condition,np.fft.ifftshift(Abs))
    winfreq  = np.extract(condition,order_freq)

    return winAbs,winfreq, ex, t1, time


def plot_ATA(ATA1,ATA2,time_1, time_2,Polx,xlim,delays,output_ATA,label_plot, path_2_save):
    from numpy import sin, cos, exp, pi, e, sqrt
    from scipy import interpolate
    import matplotlib.colors as colors

    #delays = np.asarray([float(i) for i in ATA1])
    nx = int(0)
    ny = len(delays)
    z = np.arange(nx)
    initial = True
    Abs_no_pump = []
    w_no_pump = []
    Abs_at_zero = []
    w_at_zero = []

    # for ii in ATA1: #loop for each delay
    ii = 0
    print(ii)
    print(Polx)

    # if ii in ATA2:
    ex = []
    ex0 = []
    t1 = []
    t2 = []
    for i in ATA1[ii]:
        ex.append(sqrt(ATA1[ii][i][0]**2+ATA1[ii][i][1]**2+ATA1[ii][i][2]**2))
        t1.append( (Polx[0]*ATA1[ii][i][3]+Polx[1]*ATA1[ii][i][5]+Polx[2]*ATA1[ii][i][7]) + 1.j * (Polx[0]*ATA1[ii][i][4]+Polx[1]*ATA1[ii][i][6]+Polx[2]*ATA1[ii][i][8]) )
    for i in ATA2[0]:
        ex0.append(sqrt(ATA2[0][i][0]**2+ATA2[0][i][1]**2+ATA2[0][i][2]**2))
        t2.append( (Polx[0]*ATA2[0][i][3]+Polx[1]*ATA2[0][i][5]+Polx[2]*ATA2[0][i][7]) + 1j * (Polx[0]*ATA2[0][i][4]+Polx[1]*ATA2[0][i][6]+Polx[2]*ATA2[0][i][8]) )
        
    winAbs1,winfreq, ex_prep1, t1_prep1, time_prep1 = fft_abs(t1,ex,time_1,xlim)
    
    winAbs2,winfreq2 , ex_prep2, t1_prep2, time_prep2 = fft_abs(t2,ex0,time_2,xlim)

    if ii == 0: #save absorption at delay == 0
        Abs_at_zero.append(winAbs1)
        w_at_zero.append(winfreq)
    
    if initial:
        
        nx = len(winfreq)
        #z  = np.arange(nx*ny).reshape(ny,nx) using an arange it is not working due to the data type of the array
        z = np.ones((ny,nx))
        Abs_no_pump.append(winAbs2)
        w_no_pump.append(winfreq2)
        initial = False
    
    
    # z[list(ATA1).index(ii)] = winAbs1 #- winAbs2  ##(delay,energy)
    
    # f = interpolate.interp2d(delays,winfreq,np.transpose(z), kind='cubic') # x = winfreq, y = delays, we have transposed the z matrix
 
    #xnew = np.arange(-5.01, 5.01, 1e-2)
    #ynew = np.arange(-5.01, 5.01, 1e-2)
    #znew = f(xnew, ynew)
    #plt.plot(winfreq, z[0, :], 'ro-', xnew, znew[0, :], 'b-')
    #plt.plot(winfreq, z[24, :], winfreq, z[34, :])
    #plt.savefig("test_abs.png")
    #plt.figure()
    
    # nbinsx = 8*len(winfreq)
    # nbinsy = 8*len(delays)
    # x = winfreq
    # y = delays
    # #xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
    # plt.figure(figsize=(13,5))
    # xi = np.mgrid[x.min():x.max():nbinsx*1j]
    # yi = np.mgrid[y.min():y.max():nbinsy*1j]
    # zi = f(yi,xi) #we have transposed the function
    # set_norm = colors.TwoSlopeNorm(vmin=zi.min(), vcenter=0, vmax=zi.max())
    # im=plt.pcolormesh(yi, xi, zi, cmap=plt.get_cmap('bwr'), shading='auto',  norm = set_norm)

    # #im=plt.contourf(yi, xi, zi, cmap=plt.get_cmap('bwr'), shading='auto')
    # # plt.plot([], [], ' ', label=label_plot)
    # # plt.clim(-0.9*zi.max(),0.9*zi.max())
    # plt.colorbar(im)
    # #plt.colorbar(zi)
    # plt.xlabel("Time delay (fs)",fontsize=14)
    # plt.ylabel("Energy (eV)",fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)
               
    # plt.legend(loc=3,fontsize="x-large",fancybox=True)
    # #plt.ylim()
    
    # plt.savefig(output_ATA+".pdf",bbox_inches='tight')
    
    # # pathp=[[-1.,.1],[1.,.1],[1., 9.9],[-1., 9.9]]
    # # currentAxis = plt.gca()
    # # currentAxis.add_patch(patches.Polygon(pathp,alpha=1.,fill=None,edgecolor="black",linestyle="--",linewidth=3))
    
    # plt.savefig(output_ATA+".png",bbox_inches='tight')

    tag = "2p_"
    # namefile = tag + "Abs_with_delays" + ".txt"
    # np.savetxt(namefile, zi)
    # namefile = tag +  "Freqs" + ".txt"
    # np.savetxt(namefile, xi)
    # namefile = tag +  "Delays" + ".txt"
    # np.savetxt(namefile, yi)
    namefile = path_2_save + tag +  "Abs_no_pump" + ".txt"
    np.savetxt(namefile, Abs_no_pump)
    namefile = path_2_save + tag +  "w_no_pump" + ".txt"
    np.savetxt(namefile, w_no_pump)
    namefile = path_2_save + tag +  "Abs_at_zero" + ".txt"
    np.savetxt(namefile, Abs_at_zero)
    namefile = path_2_save + tag +  "w_at_zero" + ".txt"
    np.savetxt(namefile, w_at_zero)

    # namefile = path_2_save + tag +  "Re_t1_prep1" + ".txt"
    # np.savetxt(namefile, np.real(t1_prep1))
    # namefile = path_2_save + tag +  "Im_t1_prep1" + ".txt"
    # np.savetxt(namefile, np.imag(t1_prep1))

    # namefile = path_2_save + tag +  "Re_ex_prep1" + ".txt"
    # np.savetxt(namefile, np.real(ex_prep1))
    # namefile = path_2_save + tag +  "Im_ex_prep1" + ".txt"
    # np.savetxt(namefile, np.imag(ex_prep1))

    # namefile = path_2_save + tag +  "Re_t1_1" + ".txt"
    # np.savetxt(namefile, np.real(t1))
    # namefile = path_2_save + tag +  "Im_t1_1" + ".txt"
    # np.savetxt(namefile, np.imag(t1))

    # namefile = path_2_save + tag +  "Re_ex_1" + ".txt"
    # np.savetxt(namefile, np.real(ex))
    # namefile = path_2_save + tag +  "Im_ex_1" + ".txt"
    # np.savetxt(namefile, np.imag(ex))

    # namefile = path_2_save + tag +  "time_1" + ".txt"
    # np.savetxt(namefile, time_1)



    # namefile = path_2_save + tag +  "time_prep1" + ".txt"
    # np.savetxt(namefile, time_prep1)
    





    # namefile = path_2_save + tag +  "Re_t1_prep2" + ".txt"
    # np.savetxt(namefile, np.real(t1_prep2))
    # namefile = path_2_save + tag +  "Im_t1_prep2" + ".txt"
    # np.savetxt(namefile, np.imag(t1_prep2))

    # namefile = path_2_save + tag +  "Re_ex_prep2" + ".txt"
    # np.savetxt(namefile, np.real(ex_prep2))
    # namefile = path_2_save + tag +  "Im_ex_prep2" + ".txt"
    # np.savetxt(namefile, np.imag(ex_prep2))


    # namefile = path_2_save + tag +  "time_prep2" + ".txt"
    # np.savetxt(namefile, time_prep2)

    # namefile =  "Abs_at_zero" + ".txt"   ex_prep2, t1_prep2, time_prep2
    # no_pump = np.array([w_at_zero, Abs_at_zero])
    # np.savetxt(namefile, no_pump)

    
    plt.show()
    return 0




'''if (len(sys.argv)!=6):
 print("1st arg: namefolder1")##0_28386  0_85159
 print("2nd arg: namefolder2")
 print("3rd arg: Min")
 print("4th arg: Max")
 print("5th arg: step")
 quit()
 '''
 
namefolder1 = 'aba'
namefolder2 = 0
minT = 0
maxT = 0
dT   = 1

month="february"

print(minT)
print(maxT)
print(dT)

# path1 = "/home/mikhail/Documents/Rabota/temp_cbwe/18_05_2022_ATAS_BN/ATA_NOCOULOMB_Nk_300intens_1000000.0_t1_-2.3_dt_0.05/"
# path2 = "/home/mikhail/Documents/Rabota/temp_cbwe/18_05_2022_ATAS_BN/ATA_NO_Pump_NOCOULOMB_Nk_300intens_0.0_t1_-2.3_dt_0.05/"
path1_folder = "NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1"
path1 = "D:/working harder making better/27_03_hBN_Coulomb" + "/" + path1_folder + "/"

# path2_folder = "NoPump_UncellArea_19.33_Nk_400epsStepAbs0.02intens0.0_t1_-2.3_Ncut20_qTF_0.01_dt_0.05_delayXUV_-15w_Pump_"
path2_folder = "NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1"
path2 = "D:/working harder making better/27_03_hBN_Coulomb" + "/" + path2_folder + "/"


files1 = path1
files2 = path2
# files1 = path + "/" + month + "/" + "11_5/" + namefolder1 + "/"
# files2 = path + "/" + month + "/" + "12_5/" + namefolder2 + "/"


print("Delays -> [min,max,dT]=["+str(minT)+","+str(maxT)+","+str(dT)+"] fs")

print(files1)
print(files2)

delays = np.arange(minT,maxT+dT,dT)

folderlist=[] #folders(delays)
folderlist.append(path1_folder + "_6.00")

folderlist_0=[]
folderlist_0.append(path2_folder + "_6.00")




#READ PUMP AND PROBE DATA
ATA1,EF1,time_1,Polx = read_folders(files1,folderlist)
ATA2,EF2,time_2,Polx = read_folders(files2,folderlist_0)

xlim  = [-35.0, 10.0]
x_1 = [float(numeric_string) for numeric_string in time_1]
x_2 = [float(numeric_string) for numeric_string in time_2]


#PLOT ATA SPECTRUM
print("Producing ATA spectrum... ")

delays=-delays
delays.sort()

label_plot= namefolder1
'''replace_func = np.vectorize(lambda x: str(x.replace('_','.')))
label_plot=replace_func(label_plot)'''


plot_ATA(ATA1, ATA2,x_1, x_2,Polx,xlim,delays,"ATA"+"_"+namefolder1,label_plot, path1)
#print("done")

###python3 test.py 0_85159 0_85159 -6.8 34.0 1.7