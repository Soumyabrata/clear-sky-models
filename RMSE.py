import numpy as np
import cv2

def RMSE(array1,array2):


	n = array1.size

	RMSE = np.sqrt((((array1-array2)**2).sum())/n)
	#print ('RMSE=',RMSE)

	return(RMSE)