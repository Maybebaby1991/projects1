
import numpy as np

import sys
import os
import subprocess
import datetime


from cbwe_Python_source.plot_Current import plot_Current_time_dep
from cbwe_Python_source.plot_Current import plot_w_dep_absorption
# from cbwe_Python_source.plot_Current_GeS import plot_exciton_time_dep
from sys import getsizeof


# The program runs in terminal, by commands:
# python3 Plot_absorption.py "folder_with_data" argv[2] argv[3] argv[4]
# args defined below

#if len(sys.argv) != 5:
	#print("1st arg: namefolder")
	#print("2nd arg: Min")
	#print("3rd arg: Max")
	#print("4th arg: step")
	#quit()


# reading input 
#namefolder = sys.argv[1]  # constant part of foldernames
minT = 6.0 
maxT = 7.0
dT = 10

# path of folder with all data 
path = "D:/working harder making better/27_03_hBN_Coulomb"
# path = "/home/mikhail/Documents/Data_Sauron/14_12_2023_aRuCl3"
# path = "/home/mikhail/Documents/Data_Sauron/05_12_2023_MoS2_Camarasa_NoSOC"
os.chdir(path)

# # folder with data without Coulomb
# # namefolder0= ""
# namefolder0 = "./" + namefolder0 + "/" + namefolder0
namefolder = "NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1"
# namefolder = "2s_circular010001_G_num502657_probe0_UncellArea_1.0_Nk_400epsStepAbs0.02intens500000000.0_t1_-2.3_Ncut20_laser120_qTF_0.01_dt_0.03_delayXUV_46.0w_Pump_"

folder_of_set =  "pictures_" + namefolder
if (not os.path.isdir(folder_of_set)):
	os.mkdir(folder_of_set)
#dec = (int(len(str(dT))) - 2) # lenth of decimal part to display
dec  = 2# (int(len(str(dT)))-2) number of symbols after point

s_w = [] # absorption of a particular frequency with Coulomb
# s_w0 = [] ## absorption of a particular frequency without Coulomb

W_eV = [] 
# W0_eV = [] 


N_c =0

c_eV = 1240.0

# we put range in eV
for ii in np.arange(minT, maxT + 0.1 * dT, dT):
	i = np.round(ii, decimals=2)
	s = "%s_%." + str(dec) + "f"
	folder = s % (namefolder, i)
	print(folder)

	# if data with this name exist, we:
	if (os.path.isdir("./" + namefolder + "/" + folder + "/Output")):
		#  READ DATA:
		file = np.loadtxt("./" + namefolder + "/"
								 + folder + "/Output/EF.txt", unpack=True)
		EF_t = np.array([file[1],file[2],file[3]])
		tE = np.array(file[0])
		file1 = np.loadtxt("./" + namefolder + "/" + 
									folder + "/Output/J1.txt", unpack=True)
		file2 = np.loadtxt("./" + namefolder + "/" + 
									folder + "/Output/J2.txt", unpack=True)
		J1_1 = np.array(file1[1])
		J1_3 = np.array(file1[3])
		J1_5 = np.array(file1[5])
		J2_1 = np.array(file2[1])
		J2_2 = np.array(file2[2])
		J2_3 = np.array(file2[3])
		len_files = [len(tE), len(J1_1), len(J2_1)] # slicing array so they match length
		min_len_files = np.min(len_files)

		tE = tE[:min_len_files]
		J1_1 = J1_1[:min_len_files] - J1_1[0]
		J1_3 = J1_3[:min_len_files] - J1_3[0]
		J1_5 = J1_5[:min_len_files] - J1_5[0]
		J2_1 = J2_1[:min_len_files] - J2_1[0]
		J2_2 = J2_2[:min_len_files] - J2_2[0]
		J2_3 = J2_3[:min_len_files] - J2_3[0]

		# J_t = np.array([file1[1]+file2[1], file1[3]+file2[2], (file1[5]+file2[3])]) 
		J_t = [J1_1 + J2_1, J1_3 + J2_2, J1_5 + J2_3]


		# zeros_tE = np.zeros(len(tE))
		# for it, ttt in enumerate(tE):
		# 	if ttt < 8:
		# 		zeros_tE[it] = 1.
		# J_t[0] -= zeros_tE;
		# J_t[1] -= zeros_tE;
		# J_t[2] -= zeros_tE;

		print("file1 size:", getsizeof(file1))
		print("s_w size:", getsizeof(s_w))


		s_w, W_eV,  = plot_Current_time_dep(folder_of_set, 
			tE, EF_t, J_t, i, W_eV, s_w)

		# if (os.path.isfile("./" + namefolder + "/" + folder + "/Output/Exciton.txt")):
		# 	file = np.loadtxt("./" + namefolder + "/"
		# 							 + folder + "/Output/Exciton.txt", unpack=True)
		# 	Exciton = np.array([file[0],file[1],file[2]])

			# plot_exciton_time_dep_GeS(folder_of_set, tE, tE_0,  
			# 	EF_t, EF_t_0, Exciton, i)

		
	
plot_w_dep_absorption(folder_of_set, s_w, W_eV)





