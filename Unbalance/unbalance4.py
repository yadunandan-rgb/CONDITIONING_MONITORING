import numpy as np
import matplotlib.pyplot as plt
def unbalance5(fft_listX,fft_listY,fft_listZ,sampling_frequency,rpm,angle):
	N = sampling_frequency
	T = 1/N
	rpm = rpm//60               #to frequency
	limit_start1=int(0.8*rpm)            #CHANGE WITH RESPECT TO WINDOW BASED ON LOAD.
	limit_end1=int(1.2*(rpm))
	
	averaged_fftX = fft_listX
	averaged_fftY = fft_listY
	averaged_fftZ = fft_listZ

	start_angle=int(90-30)
	end_angle=int(90+30)

	yf_X=abs(np.array(averaged_fftX)[0:N // 2])
	xf_X = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
	
	yf_Y=abs(np.array(averaged_fftY)[0:N // 2])
	xf_Y = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
	yf_Z=abs(np.array(averaged_fftZ)[0:N // 2])
	xf_Z = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

	rms_fft_amplitude_X = np.sqrt(np.mean(np.square(yf_X)))
	above_rms_ampl_X = [list(yf_X).index(i) for i in yf_X if i>rms_fft_amplitude_X]
	above_rms_ampl_X_values = [i for i in yf_X if i>rms_fft_amplitude_X]
	frequencycorrestoaboveamp_X = [list(xf_X)[j] for j in above_rms_ampl_X]
	# print('frequencycorrestoaboveamp_X',len(yf_X),len(frequencycorrestoaboveamp_X))

	rms_fft_amplitude_Y = np.sqrt(np.mean(np.square(yf_Y)))
	above_rms_ampl_Y = [list(yf_Y).index(i) for i in yf_Y if i>rms_fft_amplitude_Y]
	above_rms_ampl_Y_values = [i for i in yf_Y if i>rms_fft_amplitude_Y]
	frequencycorrestoaboveamp_Y = [list(xf_Y)[j] for j in above_rms_ampl_Y]
	# print('frequencycorrestoaboveamp_X',len(yf_Y),len(frequencycorrestoaboveamp_Y))


	rms_fft_amplitude_Z = np.sqrt(np.mean(np.square(yf_Z)))
	above_rms_ampl_Z = [list(yf_Z).index(i) for i in yf_Z if i>rms_fft_amplitude_Z]
	above_rms_ampl_Z_values = [i for i in yf_Z if i>rms_fft_amplitude_Z]
	frequencycorrestoaboveamp_Z = [list(xf_Z)[j] for j in above_rms_ampl_Z]
	# print('frequencycorrestoaboveamp_X',len(yf_Z),len(frequencycorrestoaboveamp_Z))


	onexrangevaluesFreq_X = [i for i in frequencycorrestoaboveamp_X if limit_start1<= i <=limit_end1]
	onexrangevaluesFreq_Y = [i for i in frequencycorrestoaboveamp_Y if limit_start1<= i <=limit_end1]
	onexrangevaluesFreq_Z = [i for i in frequencycorrestoaboveamp_Z if limit_start1<= i <=limit_end1]

	oneXrangeAmplitude_X_index = [frequencycorrestoaboveamp_X.index(i) for i in onexrangevaluesFreq_X]
	oneXrangeAmplitude_X1 = [above_rms_ampl_X_values[i] for i in oneXrangeAmplitude_X_index]
	oneXrangeAmplitude_Y_index = [frequencycorrestoaboveamp_Y.index(i) for i in onexrangevaluesFreq_Y]
	oneXrangeAmplitude_Y1 = [above_rms_ampl_Y_values[i] for i in oneXrangeAmplitude_Y_index]
	oneXrangeAmplitude_Z_index = [frequencycorrestoaboveamp_Z.index(i) for i in onexrangevaluesFreq_Z]
	oneXrangeAmplitude_Z1 = [above_rms_ampl_Z_values[i] for i in oneXrangeAmplitude_Z_index]

	compareXand_Z = list(set([i for i in oneXrangeAmplitude_X1 for j in oneXrangeAmplitude_Z1 if i>j]))
	compareYand_Z = list(set([i for i in oneXrangeAmplitude_Y1 for j in oneXrangeAmplitude_Z1 if i>j]))
	
	if onexrangevaluesFreq_X == [] and onexrangevaluesFreq_Y == [] and onexrangevaluesFreq_Z==[]:
		print('1check for other faultssss')
	else:
		onexrpmvalue_X = float(np.mean(onexrangevaluesFreq_X))
		onexrpmvalue_Y = float(np.mean(onexrangevaluesFreq_Y))
		onexrpmvalue_Z = float(np.mean(onexrangevaluesFreq_Z))

		multi1xvalues_X = [i for i in frequencycorrestoaboveamp_X if ((onexrpmvalue_X*2)-2)<= i <= ((onexrpmvalue_X*2)+2) or ((onexrpmvalue_X*3)-2)<= i <= ((onexrpmvalue_X*3)+2)]
		multi1xvalues_Y = [i for i in frequencycorrestoaboveamp_Y if ((onexrpmvalue_Y*2)-2)<= i <= ((onexrpmvalue_Y*2)+2) or ((onexrpmvalue_Y*3)-2)<= i <= ((onexrpmvalue_Y*3)+2)]
		multi1xvalues_Z = [i for i in frequencycorrestoaboveamp_Z if ((onexrpmvalue_Z*2)-2)<= i <= ((onexrpmvalue_Z*2)+2) or ((onexrpmvalue_Z*3)-2)<= i <= ((onexrpmvalue_Z*3)+2)]
			
		multi1xvalueFrequeAmplitudes_for_ratioX =[frequencycorrestoaboveamp_X.index(i) for i in frequencycorrestoaboveamp_X if ((onexrpmvalue_X*2)-2)<= i <= ((onexrpmvalue_X*2)+2) or ((onexrpmvalue_X*3)-2)<= i <= ((onexrpmvalue_X*3)+2)]
		amplLessthanfiftypercent1xampl_X = [above_rms_ampl_X_values[i] for i in multi1xvalueFrequeAmplitudes_for_ratioX if i< (np.mean(oneXrangeAmplitude_X1)*0.5)]
		multi1xvalueFrequeAmplitudes_for_ratioY =[frequencycorrestoaboveamp_Y.index(i) for i in frequencycorrestoaboveamp_Y if ((onexrpmvalue_Y*2)-2)<= i <= ((onexrpmvalue_Y*2)+2) or ((onexrpmvalue_Y*3)-2)<= i <= ((onexrpmvalue_Y*3)+2)]
		amplLessthanfiftypercent1xampl_Y = [above_rms_ampl_Y_values[i] for i in multi1xvalueFrequeAmplitudes_for_ratioY if i< (np.mean(oneXrangeAmplitude_Y1)*0.5)]
		multi1xvalueFrequeAmplitudes_for_ratioZ =[frequencycorrestoaboveamp_Z.index(i) for i in frequencycorrestoaboveamp_Z if ((onexrpmvalue_Z*2)-2)<= i <= ((onexrpmvalue_Z*2)+2) or ((onexrpmvalue_Z*3)-2)<= i <= ((onexrpmvalue_Z*3)+2)]
		amplLessthanfiftypercent1xampl_Z = [above_rms_ampl_Z_values[i] for i in multi1xvalueFrequeAmplitudes_for_ratioZ if i< (np.mean(oneXrangeAmplitude_Z1)*0.5)]

		if amplLessthanfiftypercent1xampl_X!=[] or amplLessthanfiftypercent1xampl_Y!=[] or amplLessthanfiftypercent1xampl_Z!=[]:
			print('Unbalance will be there')

		if multi1xvalues_X == [] and multi1xvalues_Y==[]:
			if compareXand_Z!=[] and compareYand_Z!=[]:

				if  start_angle<= angle <=end_angle:
					print('Unbalance')
				else:
					print('2Check for Misalignment or other faults ')
			else:
				print('3Check for misalignment')
		else:	
			print('4Check for Misalignment')
	