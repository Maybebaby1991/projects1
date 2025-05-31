def read_current_from_file(path):
	import numpy as np

	file = np.loadtxt(path , unpack=True)
	file = np.transpose(file)
	W_eV = file[0, :]
	Re_Jw_x =  file[1, :]
	Re_Jw_y =  file[2, :]
	Re_Jw_z =  file[3, :]
	Im_Jw_x =  file[4, :]
	Im_Jw_y =  file[5, :]
	Im_Jw_z =  file[6, :]

	Re_Ew_x =  file[7, :]
	Re_Ew_y =  file[8, :]
	Re_Ew_z =  file[9, :]
	Im_Ew_x =  file[10, :]
	Im_Ew_y =  file[11, :]
	Im_Ew_z =  file[12, :]

	Jw_x = np.array(Re_Jw_x + 1j * Im_Jw_x)
	Jw_y = np.array(Re_Jw_y + 1j * Im_Jw_y)
	Jw_z = np.array(Re_Jw_z + 1j * Im_Jw_z)

	Ew_x = np.array(Re_Ew_x + 1j * Im_Ew_x)
	Ew_y = np.array(Re_Ew_y + 1j * Im_Ew_y)
	Ew_z = np.array(Re_Ew_z + 1j * Im_Ew_z)

	return W_eV, Jw_x, Jw_y, Jw_z, Ew_x, Ew_y, Ew_z


import numpy as np
import matplotlib.pyplot as plt
import os

path = "D:/working harder making better/27_03_hBN_Coulomb"
os.chdir(path)

Folders_XUV = [
    "pictures_NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.0/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-15EPS-1.0/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-30EPS-1.0/",
    "pictures_NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.0/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.2/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.5/",
    "pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-2.0/"
]

Files_XUV = [
    "Current_w_pictures_NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.0_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-15EPS-1.0_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-30EPS-1.0_6.00.txt",
    "Current_w_pictures_NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.0_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.2_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.5_6.00.txt",
    "Current_w_pictures_ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-2.0_6.00.txt"
]

space_au_A       =   0.52917721092
d_susc_in_A = 10
d_susc_in_au = d_susc_in_A / space_au_A
theta_grad = 80
theta_rad = np.pi * theta_grad / 180
Absorption_XUV = []
freqs_XUV = []

assert len(Folders_XUV) == len(Files_XUV)
num_datasets = len(Folders_XUV)

for ii in range(num_datasets):
	w, Jw_x, Jw_y, Jw_z, Ew_x, Ew_y, Ew_z  = read_current_from_file(Folders_XUV[ii] + Files_XUV[ii])
	r = -1j*(np.conjugate(Ew_x)*Jw_x + np.conjugate(Ew_y)*Jw_y + np.conjugate(Ew_z)*Jw_z)
	E_squared_sum = np.abs(Ew_x)*np.abs(Ew_x) + np.abs(Ew_y)*np.abs(Ew_y) + np.abs(Ew_z)*np.abs(Ew_z)
	sw  = 4*np.pi* (100/137) * np.imag(r)/(E_squared_sum + 1e-18)
	Absorption_XUV.append(sw)
	freqs_XUV.append(w)

namefig = "Dependence on R0 term"
Labels = [
    "NoColumb",
    "5r0 Hartree",
    "10r0 Hartree",
    "15r0 Hartree after Pump",
    "30r0 Hartree after Pump",
    "NoColumb",
    "10r0eps1.0 Hartree",
    "10r0eps1.2 Hartree",
    "10r0eps1.5 Hartree",
    "10r0eps2.0 Hartree"
]
scale_fig = 1.
fig = plt.figure(namefig,figsize=(10*scale_fig,5*scale_fig));

plt.subplot2grid((1, 1), (0, 0), colspan=1)
for ii in range(10):
    plt.plot(freqs_XUV[ii], Absorption_XUV[ii],  label = Labels[ii] )
    plt.legend()
    plt.xlabel("Frequency, eV", fontsize=15)
    plt.ylabel("Absorption, %", fontsize=15)
    plt.grid()

'''plt.subplot2grid((2, 1), (1, 0), colspan=1)
for ii in range(5, num_datasets):
    plt.plot(freqs_XUV[ii], Absorption_XUV[ii],  label = Labels[ii] )
    plt.legend()
    plt.xlabel("Frequency, eV", fontsize=15)
    plt.ylabel("Absorption, %", fontsize=15)
    plt.grid()
'''
plt.tight_layout()
plt.savefig("./KRASIVO.pdf",bbox_inches='tight')
plt.show()