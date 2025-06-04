#!/bin/env python3

# import numpy as np
import sys
import os
import subprocess
import shutil

program = "sbatch"
path    = os.getcwd()

def print_input(folder,delay,dec, Nk, qTF, dt, eps, cycles, intens, 
	Ncut, t_fin, t1, delay_XUV, labelInput,
	start_print_time, end_print_time, step_print,r0):
	# s="%."+str(dec)+"f"
	# delayd = s % (i)
	s="""NEWINPUT

tdse{
tightbinding Haldane_CoreBN_Nedge gap=  7.25 t1=  """ + str(t1)+ """ t2= 0 phi0= 0.0                  
dt  """ + str(dt)+ """ au               
t_fin """ + str(t_fin)+ """ au
Adams_Bashforth
}




nkPT{
1 """ + str(int(Nk))+ """ """ + str(int(Nk))+ """
}


decoherence{
corehole 0.00396892 au
}

Coulomb{
qTF 0.01
Ncut 20
epsilon_static """ + str((eps))+ """
r0 """ + str((r0))+ """
G_distance 50
Rytova_Keldysh
}


laserpump sin2  {
cycles """ + str((cycles))+ """    
wavelength """ + str((delay))+ """ nm
intensity """ + str(intens)+ """ wcm2
polarization circular 0 1 0 0 0 1
}




observables{  
it_resolution 1                                
TAbs
Current
}
"""
	outfile = open(str(folder)+"/input.txt",'w')
	outfile.write(s)
	outfile.close()














# main text of program
if (len(sys.argv)!=5):
	print("1st arg: namefolder")
	print("2nd arg: Min")
	print("3rd arg: Max")
	print("4th arg: step")
	quit()

namefolder_init = sys.argv[1]
minT = float(sys.argv[2])
maxT = float(sys.argv[3])
dT   = float(sys.argv[4])

time_au_fs =   0.02418884326505;


Nk = 200
qTF =  0.01
dt = 0.1 # time step


eps = 2.0 # area and epsilon, we divide our results on it. This is in Vacuum Galvani 2019


t_laser = 3; # in fs

t1 = -2.3 # Galvani TB hopping
space_au_A       =   0.52917721092
r0 = 10
gleb = r0 # similar to MoS2 Slobodeniuk parameter in Angsrom
r0 /= space_au_A # convert to a.u.
# t1 = -2.8 # TB hopping crys DFT
# cycles  = 46 
intens = 1.e+9 # 
# intens = 0 #calibrate ATA

labelInput = "G_num502657_Ncut20_"

t_fin = 110 /time_au_fs #1.5 * t_laser /time_au_fs; # in a.u.

start_print_time = 1110.0 /time_au_fs
end_print_time = 2.0/ time_au_fs
step_print = 0.02/ time_au_fs
# t_fin_0 = 0.7*cycles*9.6 / time_au_fs # fs -> au t final - 4 wave pockets, different for different pump pulse
Ncut = 20


delay_XUV = 0#-14.5 #fs
delay_XUV_max = 1.1
delay_XUV_step = 10.1
while delay_XUV < delay_XUV_max:
	# str_param = str(eps) + "_Nk_" + str(Nk) + "intens"+str(intens/1e+11) + "_Ncut" +str(Ncut) + "_qTF_" + str(qTF) + "_dt_" + str(dt) + "_cycles_" + str(cycles)
	str_param = "UncellArea_" + "_Nk_" + str(Nk)  + "intens_" + '{:.2e}'.format(intens)+ "_t1_" +str(t1) + "_Ncut" +str(Ncut) + "_qTF_" + str(qTF) + "_dt_" + str(dt)+"_delayXUV_" + str(delay_XUV) + "w_Pump_" + "R0-" + str(gleb)+ "EPS-" + str(eps)
	# str_param = "NOCOULOMB_Nk_" + str(Nk) + "intens_" + '{:.2e}'.format(intens) + "_t1_" +str(t1) + "_dt_" + str(dt) +"_delayXUV_" + str(delay_XUV) + "w_Pump_" # + "_cycles_" + str(cycles)


	pathCalc    = os.getcwd()
	src_path = pathCalc + "/Coulomb_G_num502657_Ncut20_"
	print(pathCalc)

	namefolder = namefolder_init + str_param
	if (not os.path.isdir(namefolder)):
		os.mkdir(namefolder)
	os.chdir("./" + namefolder)
	pathCalc    = os.getcwd()

	dec  = 2# (int(len(str(dT)))-2) number of symbols after point
	# print("Delays -> [min,max,dT]=["+str(minT)+","+str(maxT)+","+str(dT)+"] fs")

	c_eV = 1240.0



	# we put range in eV 
	i = minT
	while i < maxT: # in range(minT,maxscancel T + 0.1*dT,dT):
		# t_fin = t_fin_0 / i
		W_nm = c_eV/i # from nm to eV 
		s="%s_%."+str(dec)+"f"

		cycles = int(t_laser * i / 4) 

		namefolder_pr = namefolder # + "_cycles_" + str(cycles)
		folder = s % (namefolder_pr,i)
		if (not os.path.isdir(folder)):
			os.mkdir( folder)
			# if (not os.path.isdir(folder + "/Output")):
				# os.mkdir( folder + "/Output")
				# os.mkdir( folder + "/Output/Coulomb")


			# path_copy = src_path + "/V_Hartree_" + labelInput +".txt"
			# path_paste = pathCalc + "/" + folder + "/Output/Coulomb/V_Hartree_" + labelInput +".txt"

			# shutil.copy(path_copy, path_paste)
			# path_copy = src_path + "/A_coeff" + labelInput +".txt"
			# path_paste = pathCalc + "/" + folder + "/Output/Coulomb/A_coeff" + labelInput +".txt"
			# shutil.copy(path_copy, path_paste)

			# shutil.copy(src_path + "/B_coeff" + labelInput +".txt", pathCalc + "/" + folder + "/Output/Coulomb/B_coeff" + labelInput +".txt")
			# shutil.copy(src_path + "/C_coeff" + labelInput +".txt", pathCalc + "/" + folder + "/Output/Coulomb/C_coeff" + labelInput +".txt")
			# shutil.copy(src_path + "/D_coeff" + labelInput +".txt", pathCalc + "/" + folder + "/Output/Coulomb/D_coeff" + labelInput +".txt")
			# shutil.copy(src_path + "/Screen_const_" + labelInput +".txt", pathCalc + "/" + folder + "/Output/Coulomb/Screen_const_" + labelInput +".txt")
			print_input(folder,W_nm, dec, Nk, qTF, dt, eps, 
				cycles, intens, Ncut, t_fin, t1, delay_XUV, labelInput,
				start_print_time, end_print_time, step_print, r0 )
			os.chdir(pathCalc + "/" + folder)
			print(os.getcwd())
			#proc = subprocess.Popen([program,"input.txt"])
			proc = subprocess.Popen([program,"../../EDUS_submission.do"])
			os.chdir(pathCalc)
			proc.wait()

		i+= dT

	os.chdir(path)
	delay_XUV += delay_XUV_step
	delay_XUV = round(delay_XUV, 1)

	#
	#s2=print_E_molcas.do(fich,outfile,"DO Y= " + geom)
	#g2.append(geom)

	# Coulomb_band_reconstruction


	# Coulomb_diag_basis



# Coulomb{
# qTF """ + str(qTF)+ """
# Ncut """ + str(Ncut)+ """
# epsilon_static """ + str(eps)+ """
# G_distance 400
# Read_Coulomb_from_files
# labelInput """ + labelInput + """

# Rytova_Keldysh
# }


# decoherence{
# corehole 0.00396892 au
# }

# observables{   
# PrintPopulation                                            
# TAbs
# Current
# }

# laserpump sin2  {
# cycles 5    
# wavelength 210.16949152542372 nm
# intensity 100000.0 wcm2
# polarization circular 0 1 0 0 0 1                 
# }
