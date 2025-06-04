# fix points where current is suddenly wrong without any reason
def data_clean(data):
	import numpy as np
	N_fix = 0
	fixation = True

	while fixation and N_fix<15:
		fixation = False # run this loop until we have data to fix
		N_fix +=1

		av_data = np.sum(np.abs(data))/ len(data)

		for j in range(1,len(data)-1):
			criteria = 0
			if np.abs(data[j] + data[j-1]) > 1e-10:
				criteria = 2* np.abs(data[j]- data[j-1]) /  np.abs(data[j] + data[j-1])

			# if av_data > 0:
			# 	criteria /= av_data

			if criteria >  0.1:
				# data[j+1] =  data[j]
				data[j] = (data[j+1] + data[j-1])/2 # fix points where current is suddenly wrong without any reason
				fixation = True

	print("N_fix = ", N_fix)
	
	return data





def prepareDataFFT(data, tau, t, N_multipl):
	import numpy as np
	from cbwe_Python_source.fft_creation import data_clean


	data_tau = np.zeros(len(tau))
	j=0 # left part of the prepared data - zeros because signal starts at t=0
	
	data = data_clean(data)
	

	for i in range(len(tau)//2, len(tau)//2 + len(tau)//(2* N_multipl)):
		
		while tau[i] > t[j]:
			j += 1

		if (j> (len(t) - 2)) or (j > (len(data) - 2)):
			break

		
	
		data_tau[i] = (tau[i] - t[j]) * data[j+1] + (t[j+1] - tau[i]) * data[j]
		if  np.abs((t[j+1] -  t[j])) > 0:
			data_tau[i] /= (t[j+1] -  t[j])
		else:
			data_tau[i] = data_tau[i-1]

	return data_tau




def prepareDataFFT_ATA(data, tau, t):
	import numpy as np

	data_tau = 1j * np.zeros(len(tau))
	
	j=0 # left part of the prepared data - zeros because signal starts at t=0
	for i in range(len(tau)):

		while tau[i] > t[j]:
			j += 1

		if (j> (len(t) - 2)) or (j > (len(data) - 2)):
			break

		data_tau[i] = (tau[i] - t[j]) * data[j+1] + (t[j+1] - tau[i]) * data[j]

		if  np.abs((t[j+1] -  t[j])) > 0:
			data_tau[i] /= (t[j+1] -  t[j])
		else:
			data_tau[i] = data_tau[i-1]

		# if tau[i] > 24:
		# 	data_tau[i] = 0



	return data_tau