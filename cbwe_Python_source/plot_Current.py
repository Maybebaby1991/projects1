import os
def plot_Current_time_dep(save_dest, tE_full, EF_t, J_t, wi,
  W_eV, s_w):
# plotting x,y in a save_dest folder
  import matplotlib
  import matplotlib.pyplot as plt
  from scipy.fft import fft, rfft, fftfreq, fftshift
  import numpy as np
  from cbwe_Python_source.fft_creation import prepareDataFFT
  plt.close('all')
  t_max = tE_full[len(tE_full) - 1]
  t1 = 0

  n_tE  = len(tE_full)
  for j in range(0, len(tE_full)):
    if tE_full[j] > t_max:
      n_tE = j
      break


  tE = tE_full[0: n_tE]


  s_w_t = 0
  s_w_0_t = 0
  w_t = 0
  N_multipl = 50 #create array of data to get better resolution (we consider that t->+- inf we don't have anything)
  # array of step:
  stepDE = np.zeros(len(tE))

  for i in np.arange(1, len(tE), 1):
    stepDE[i] = (tE[i] - tE[i-1])
    

  stepDE[0] = stepDE[1]
  fs_to_ev = 4.1357 #/ (2 * np.pi)
  # fs_to_ev = 1

  # create a grid with fixed step for fft:
  tau = np.arange(-N_multipl*tE[len(tE)-1], N_multipl*tE[len(tE)-1], stepDE[0]/2)
  Wf = fftfreq(len(tau), (tau[1] - tau[0])/fs_to_ev)
  # Wf = fftshift(Wf)


  # decay factor of oscillations after pulse
  decay = np.zeros(len(tau)) + 1
  # decay = np.sin(np.pi* tau/ t_max)
  # decay0 = np.sin(np.pi* tau0/ t_max)

  for tt in range(len(tau)):
    if tau[tt] > t1:
      decay[tt] = np.exp((t1 - tau[tt])*0.09) # hBN
      # decay[tt] = np.exp((t1 - tau[tt])*0.09) # MoS2
      # decay[tt] = np.exp((t1 - tau[tt])*0.02) # aRuCl3



  E_tau = np.array([np.zeros(len(tau)), np.zeros(len(tau)), np.zeros(len(tau))])
  E_tau_non_scale = np.array([np.zeros(len(tau)), np.zeros(len(tau)), np.zeros(len(tau))])

  E_tau_non_scale[2] = prepareDataFFT(EF_t[1], tau, tE, N_multipl) # E_y
  E_tau_non_scale[1] = prepareDataFFT(EF_t[0], tau, tE, N_multipl) # E_x
  E_tau_non_scale[0] = prepareDataFFT(EF_t[2], tau, tE, N_multipl) # E_z


  E_tau[2] = decay * E_tau_non_scale[2] # E_y
  E_tau[1] = decay * E_tau_non_scale[1] # E_x
  E_tau[0] = decay * E_tau_non_scale[0] # E_z
  
  Jx_medium = np.sum(J_t[1] * stepDE) # medium value of current to see, if we have const component 
  Jy_medium = np.sum(J_t[2] * stepDE) 
  Ex_medium = np.sum(EF_t[1]) / len(EF_t[1])
  Ey_medium = np.sum(EF_t[2]) / len(EF_t[2])



  # current
  J_tau = np.array([np.zeros(len(tau)), np.zeros(len(tau)), np.zeros(len(tau))])

  J_tau_non_scale = np.array([np.zeros(len(tau)), np.zeros(len(tau)), np.zeros(len(tau))])
  J_tau_non_scale[2] = prepareDataFFT(J_t[1], tau, tE, N_multipl) # E_y
  J_tau_non_scale[1] = prepareDataFFT(J_t[0], tau, tE, N_multipl) # E_x
  J_tau_non_scale[0] = prepareDataFFT(J_t[2], tau, tE, N_multipl) # E_z


  J_tau[2] = decay * J_tau_non_scale[2] # E_y
  J_tau[1] = decay * J_tau_non_scale[1] # E_x
  J_tau[0] = decay * J_tau_non_scale[0] # E_z

  # tau_scale_ind = [(N_multipl * len(tau) // (N_multipl+1)): len(tau)]
  tau_scale_ind_end = len(tau)//2 + len(tau)//(2* N_multipl)# (N_multipl * len(tau) // (N_multipl+1))
  tau_scale_ind_begin = len(tau)//2
  # Ew = np.sqrt(Ey_tau*Ey_tau + Ex_tau*Ex_tau)
  
  # N_tau = prepareDataFFT(N, tau, tE)
  # N_tau0 = prepareDataFFT(N_cond0, tau0, tE_0)



  # plt.figure(figsize=(15, 10.5))
  plt.figure(figsize=(10, 7.5))
  # plt.title("frequency = " + str(wi) + " eV")

  plt.subplot2grid((3, 3), (0, 0), colspan=2)
  # plt.title("frequency = " + str(wi) + " eV")
  textstr = "$\omega_{pulse} = $" + str(wi) + " eV"
  props = dict( facecolor='white', alpha=0.5)
  y_text = np.amax( E_tau_non_scale[1][tau_scale_ind_begin:tau_scale_ind_end])
  plt.text(10, y_text, textstr,  fontsize=14, verticalalignment='top',  bbox=props)
  pl_Ex, = plt.plot(tau[tau_scale_ind_begin:tau_scale_ind_end], E_tau_non_scale[1][tau_scale_ind_begin:tau_scale_ind_end], label = '$E_x(t)$') # signal
  pl_Ey, = plt.plot(tau[tau_scale_ind_begin:tau_scale_ind_end], E_tau_non_scale[2][tau_scale_ind_begin:tau_scale_ind_end], label = '$E_y(t)$', alpha = 0.9, linestyle = '--') # signal
  
  pl_Ez, = plt.plot(tau[tau_scale_ind_begin:tau_scale_ind_end], E_tau_non_scale[0][tau_scale_ind_begin:tau_scale_ind_end], label = 'Ez', alpha = 0.9, linestyle = '-.') # signal
  # plt.xlim([10,15])
  plt.xlabel("time, fs")
  plt.ylabel("Electric field, a.u.")
  plt.legend(handles=[pl_Ex, pl_Ey, pl_Ez], loc = "upper right")
  plt.grid(True)
  plt.ticklabel_format(style="sci", scilimits=(0,0), axis="y")
  plt.xlim(right=25)
  plt.xlim(left=0)

  # plot current with coulomb 
  plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)
  # plt.title("Current, Coulomb interaction")

  textstr = "Current"
  y_text = np.amax( J_tau_non_scale[1][tau_scale_ind_begin:tau_scale_ind_end])
  plt.text(10, y_text, textstr,  fontsize=14, verticalalignment='top',  bbox=props)
  pl_Jx, = plt.plot(tau[tau_scale_ind_begin:tau_scale_ind_end], J_tau[1][tau_scale_ind_begin:tau_scale_ind_end], label = '$J_x(t)$') # signal
  pl_Jy, = plt.plot(tau[tau_scale_ind_begin:tau_scale_ind_end], J_tau[2][tau_scale_ind_begin:tau_scale_ind_end], label = '$J_y(t)$', alpha = 0.9, linestyle = '--') # signal
  label_med = '$<Jx>=$' + str(Jx_medium) 
  # plt.axhline(y=Jx_medium, label = label_med) 
  label_med = '$<Jy>=$' + str(Jy_medium)
  # plt.axhline(y=Jy_medium, label = label_med) 
  pl_Jz, = plt.plot(tau[tau_scale_ind_begin:tau_scale_ind_end], J_tau[0][tau_scale_ind_begin:tau_scale_ind_end], label = 'Jz') # signal
  # pl_N0, = plt.plot(time0, N_cond0, label = 'Coulomb Nk = 700', alpha=0.7)
  plt.legend()
  # plt.xlim([10,15])
  plt.xlabel("time, fs")
  plt.ylabel("Current, a.u.")
  plt.grid(True)
  plt.ticklabel_format(style="sci", scilimits=(0,0), axis="y")
  # plt.xlim(right=100)
  # plt.xlim(left=0)
  # topMax = 0
  # for i in np.arange(0, len(t), 1):
  # 	# if t[i] < 10:
  # 		if N[i] > topMax:
  # 			topMax = N[i]







  # # Fourier transforms:
  
  E_w = np.array([np.zeros(len(tau)) + 0j, np.zeros(len(tau)) + 0j, np.zeros(len(tau)) + 0j])

  J_w = np.array([np.zeros(len(tau)) + 0j, np.zeros(len(tau)) + 0j, np.zeros(len(tau)) + 0j])


  for i in range(0,3):
    E_w[i] = (fft(E_tau[i]))

    # E_w[i] = fftshift(E_w[i])
    J_w[i] = (fft(J_tau[i]))

    # J_w[i] = fftshift(J_w[i])




  #E(w) transform
  plt.subplot2grid((3, 3), (0, 2), colspan=1) # signal
  pl_Ex_fft, = plt.plot(Wf, np.abs(E_w[1]), label = '$E_x(\omega)$' ) # signal
  pl_Ey_fft, = plt.plot(Wf, np.abs(E_w[2]), label = '$E_y(\omega)$', alpha = 0.9, linestyle = '--') # signal
  pl_Ez_fft, = plt.plot(Wf, np.abs(E_w[0]), label = 'Ez', alpha = 0.9, linestyle = '-.') # signal

  plt.xlabel("$\omega$, ev")
  plt.ylabel("Electric field")
  plt.xlim(right=5)
  plt.xlim(left=0)
  plt.ylim(bottom=0)
  plt.legend(handles=[pl_Ex_fft, pl_Ey_fft])
  plt.grid(True)
  plt.ticklabel_format(style="sci", scilimits=(0,0), axis="y")
  # plt.ticklabel_format(style="sci", scilimits=(0,0), axis="y")

  #J(w) transform
  plt.subplot2grid((3, 3), (1, 2), colspan=1, rowspan=2) # signal
  pl_Jx_fft, = plt.plot(Wf, np.abs(J_w[1]), label = '$J_x(\omega)$') # signal
  pl_Jy_fft, = plt.plot(Wf, np.abs(J_w[2]), label = '$J_y(\omega)$', alpha = 0.9, linestyle = '--') # signal
  pl_Jz_fft, = plt.plot(Wf, np.abs(J_w[0]), label = 'Jz') # signal

  plt.xlabel("$\omega$, ev")
  plt.ylabel("Current")
  plt.xlim(right=9)
  plt.xlim(left=3)
  plt.ylim(bottom=0)
  plt.legend(handles=[pl_Jx_fft, pl_Jy_fft])
  plt.grid(True)
  plt.ticklabel_format(style="sci", scilimits=(0,0), axis="y")
  # plt.ticklabel_format(style="sci", scilimits=(0,0), axis="y")

  

  plt.subplots_adjust(wspace=0.245, hspace=0.302)
  dec = 2
  s = "%s_%." + str(dec) + "f"
  i = np.round(wi, decimals=2)
  namefolder = save_dest + "/Current"+ save_dest 
  folder = s % (namefolder, i)
  # plt.show()
  plt.savefig(folder + ".png")

  # data_abs = np.array([tau[tau_scale_ind_begin:tau_scale_ind_end], 
  # 	J_tau_non_scale[0][tau_scale_ind_begin:tau_scale_ind_end],
  # 	J_tau_non_scale[1][tau_scale_ind_begin:tau_scale_ind_end],
  # 	J_tau_non_scale[2][tau_scale_ind_begin:tau_scale_ind_end]])
  # namefolder = save_dest + "/Current(t)"+ save_dest 
  # folder = s % (namefolder, i)
  # namefile = folder + ".txt"
  # np.savetxt(namefile, data_abs)




  plt.clf()
  plt.close('all')

  # absorption on a maximum of a peak
  index_max = np.argmax(np.abs(E_w[0]) + np.abs(E_w[1]) + np.abs(E_w[2]) )

  delta_w = Wf[index_max] -  Wf[index_max-1]

  print("delta_w = ", delta_w)


  
  # print(absorption)
  # print(Wmax)
  # N_cond_final = N_free[0] # return population right after the pulse
  # N_cond_0_final = N_cond0[len(N_cond0) - 10] # return population right after the pulse
  # plt.show()
  # print(index_max)
  # Wmax = (Wf[index_max])
  # print(Wmax)
  W_eV_save = []
  Re_Jw0_save = []
  Re_Jw1_save = []
  Re_Jw2_save = []
  Re_Ew0_save = []
  Re_Ew1_save = []
  Re_Ew2_save = []
  Im_Jw0_save = []
  Im_Jw1_save = []
  Im_Jw2_save = []
  Im_Ew0_save = []
  Im_Ew1_save = []
  Im_Ew2_save = []
  for ii in  range(-4901,4301,1):# hBN strong field
  # for ii in  range(-6901,15301,1):# aRuCl3
  # for ii in  range(-39001,30301,3):# MoS2
  # for ii in  range(-10901,131001,3):# MoS2 ATAS

    index = index_max + ii
    # w_ii = wi + ii*delta_w
    # w0_ii = wi + ii*delta_w0

    Emax=[E_w[0][index], E_w[1][index], E_w[2][index]]
    Jwmax = [J_w[0][index], J_w[1][index], J_w[2][index]]
    Wmax = np.abs(Wf[index])
    # absorption
    r = -1j*(np.conjugate(Emax[0])*Jwmax[0] + np.conjugate(Emax[1])*Jwmax[1] + np.conjugate(Emax[2])*Jwmax[2])
    absorption  = np.imag(r)/(np.abs(Emax[0])*np.abs(Emax[0]) + np.abs(Emax[1])*np.abs(Emax[1]) + np.abs(Emax[2])*np.abs(Emax[2]))
    W_eV.append(Wmax) #  eV 
    s_w.append(4*np.pi* (100/137) * absorption)
    W_eV_save.append(Wf[index])
    Re_Jw0_save.append(np.real(Jwmax[0]))
    Re_Jw1_save.append(np.real(Jwmax[1]))
    Re_Jw2_save.append(np.real(Jwmax[2]))
    Im_Jw0_save.append(np.imag(Jwmax[0]))
    Im_Jw1_save.append(np.imag(Jwmax[1]))
    Im_Jw2_save.append(np.imag(Jwmax[2]))
    Re_Ew0_save.append(np.real(Emax[0]))
    Re_Ew1_save.append(np.real(Emax[1]))
    Re_Ew2_save.append(np.real(Emax[2]))
    Im_Ew0_save.append(np.imag(Emax[0]))
    Im_Ew1_save.append(np.imag(Emax[1]))
    Im_Ew2_save.append(np.imag(Emax[2]))
    # print(Wmax)

  del tau,  E_w, J_w, E_tau, J_tau, 

  data_abs = np.array([W_eV_save,
    Re_Jw0_save,
    Re_Jw1_save,
    Re_Jw2_save,
    Im_Jw0_save,
    Im_Jw1_save,
    Im_Jw2_save,
    Re_Ew0_save,
    Re_Ew1_save,
    Re_Ew2_save,
    Im_Ew0_save,
    Im_Ew1_save,
    Im_Ew2_save,
    ])
  namefolder = save_dest + "/Current_w_"+ save_dest 
  folder = s % (namefolder, i)
  namefile = folder + ".txt"
  np.savetxt(namefile, data_abs)
  return s_w, W_eV



  



def plot_w_dep_absorption(save_dest, s_w, W_eV):
  import matplotlib
  import matplotlib.pyplot as plt
  import numpy as np

  # for s in s_w:
  # 	if s_w[s] < 0:
  # 		s_w[s] = 0

  # for s in s_w0:
  # 	if s_w0[s] < 0:
  # 		s_w0[s] = 0

  print(len(s_w))
  # print(W_eV)
  # print(W0_eV)
  plt.figure(figsize=(10, 7.5))
  plt.subplots_adjust(hspace=0.302)
  plt.subplot(111)
  plt.title("Absorption")
  pl_c, = plt.plot(W_eV, (s_w), 'g^', markersize=1, label = ' ')

  # pl_c, = plt.plot(W_eV, (s_w), 'g^', markersize=1, label = 'ydir')
  # pl_nc, = plt.plot(W0_eV, (s_w0), 'bs', markersize=1, label = 'zdir', alpha = 0.5)
  plt.legend(handles=[pl_c])
  plt.grid(True)
  plt.xlabel("$\omega$, eV")
  plt.ylabel("Absorption, %")
  plt.xlim(right=9)
  plt.xlim(left=3)
  plt.ylim(bottom=0)



  # plt.subplot(312)
  # plt.plot(W_eV, 'g^')
  # plt.plot(W0_eV, 'bs', alpha = 0.5)
  # plt.grid(True)

  # plt.subplot(313)
  # plt.plot(s_w, 'g^')
  # plt.plot(s_w0, 'bs', alpha = 0.5)
  # plt.grid(True)
  # pl_nc, = plt.plot(W0_eV, (s_w0), 'bs', label = 'No Coulomb')
  # plt.legend(handles=[ pl_nc])
  # plt.grid(True)
  # plt.xlabel("$\omega$, eV")
  # plt.ylabel("Absorption")

  # plt.show()
  plt.savefig(save_dest + "/BROAD_SPECTRUM" + save_dest + "freq_depend.png")
  data_abs = np.array([W_eV, s_w])
  namefile = save_dest + "/absorption_w_depend.txt"
  np.savetxt(namefile, data_abs)
  # plt.close()
  plt.show()


# def plot_exciton_time_dep(save_dest, tE, tE_0,  
# 	EF_t, EF_t_0, Exciton, wi):
# 	import matplotlib
# 	import matplotlib.pyplot as plt
# 	import numpy as np

# 	plt.figure(figsize=(15, 7.5))
  
# 	plt.subplot(311)
# 	plt.title("frequency = " + str(wi) + " eV")
# 	plt.xlabel("time, fs")
# 	plt.ylabel("Electric field")
# 	pl_Ex, = plt.plot(tE, EF_t[1], label = 'Ex', alpha = 0.5) # signal
# 	pl_Ey, = plt.plot(tE, EF_t[2], label = 'Ey', alpha = 0.5) # signal
# 	pl_Ez, = plt.plot(tE, EF_t[0], label = 'Ez') # signal
# 	plt.legend(handles=[pl_Ex,pl_Ey, pl_Ez])


# 	plt.subplot(312)
# 	plt.xlabel("time, fs")
# 	plt.ylabel("Exciton strenght")
# 	pl_Exc_x, = plt.plot(tE, Exciton[1], label = 'Exciton core- valence', alpha = 0.5) # signal
# 	pl_Exc_z, = plt.plot(tE, Exciton[0], label = 'Exciton core- conduction', alpha = 0.5) # signal
# 	plt.legend(handles=[pl_Exc_x,pl_Exc_z])

# 	plt.subplot(313)
# 	plt.xlabel("time, fs")
# 	plt.ylabel("Exciton strenght")
# 	pl_Exc_y, = plt.plot(tE, Exciton[2], label = 'Exciton valence- conduction') # signal
# 	plt.legend(handles=[pl_Exc_y])

# 	# plt.savefig(save_dest + "/" + save_dest +str(wi)+ "EXCITON.png")

# 	plt.clf()
# 	plt.close('all')

