from tqdm import tqdm
import numpy as np
import cv2
import copy
import os
num_points = sum(1 for line in open('SIST_000_oct0_05.xyz'))
fp = open('SIST_000_oct0_05.xyz')
keys = ['x','y','z','r','g','b']
points = []
interval = 0.001 # sampling resolution

def simu_carema(points,img_z,img_y,out_para_set,resolution,f,id):
	scale = int(10 ** resolution)
	img = np.zeros((img_z*scale+1, img_y*scale+1,3))  # set a img to save the RPG of the project points

	line1=[float(out_para_set[0].split(',')[0]),float(out_para_set[0].split(',')[1]),float(out_para_set[0].split(',')[2]),float(out_para_set[0].split(',')[3])]
	line2=[float(out_para_set[1].split(',')[0]),float(out_para_set[1].split(',')[1]),float(out_para_set[1].split(',')[2]),float(out_para_set[1].split(',')[3])]
	line3=[float(out_para_set[2].split(',')[0]),float(out_para_set[2].split(',')[1]),float(out_para_set[2].split(',')[2]),float(out_para_set[2].split(',')[3])]
	line4=[float(out_para_set[3].split(',')[0]),float(out_para_set[3].split(',')[1]),float(out_para_set[3].split(',')[2]),float(out_para_set[3].split(',')[3])]
	mat_list=[]
	mat_list.append(line1)
	mat_list.append(line2)
	mat_list.append(line3)
	mat_list.append(line4)
	R_total = np.mat(mat_list)
	print(R_total,"\n")
	points2 =copy.deepcopy(points)
	print("----------- outpara Processing ----------")
	for point in points2:
		point_mat=np.mat([point['x'],point['y'],point['z'],1.0]).T
		point_trans= R_total * point_mat # translate to carema axis
		#print(point_trans)
		# print(point_trans)
		point['x']= point_trans[0,0]
		point['y'] =point_trans[1,0]
		point['z'] =point_trans[2,0]
	print("------------- inpara Processing --------------")
	points2.sort(key=lambda s:s['x'],reverse=True)
	while points2[-1]['x']<=0:
		points2.pop()
	for point in points2:
		in_mat=np.mat([[f,0,0,0],[0,f,0,0],[0,0,1,0]])
		point_mat = np.mat([point['y'], point['z'], point['x'],1]).T
		point_XYZ= in_mat * point_mat
		point['y'] = round(point_XYZ[0, 0]/point_XYZ[2, 0]+img_y/2.0, resolution)
		point['z'] = round(point_XYZ[1, 0]/point_XYZ[2, 0]+img_z/2.0, resolution)
		if (point['y']>=0.0 and point['y']<= float(img_y) and point['z']>=0.0 and point['z']<=float(img_z)):
			img[int(((img_z-point['z'])*scale)),int(((img_y-point['y'])*scale))]=[np.uint8(point['b']),np.uint8(point['g']),np.uint8(point['r'])]

	cv2.imwrite(os.getcwd()+"\\..\\..\\video\\frames\\"+str(id)+".jpg",img)

###############################################
for line in tqdm(fp,total=num_points,desc='loading pointcloud'):
	if not line:
		continue
	row_list = line.split()
	elements = list(map(float,row_list[2:5])) + list(map(int,row_list[5:]))
	#if elements[3]==255 and elements[4]==255 and elements[5]==255:
	#	continue
	points.append(dict(zip(keys,elements)))
file = open(os.getcwd() + "\\..\\..\\camera_video.txt", 'r')
Lines = file.readlines()
print(Lines)
Lines_size = len(Lines)
for i in range(0, Lines_size-1, 3):
	id = Lines[i].strip('\n')
	in_para_set = Lines[i + 1].strip(';\n').split(';')
	f = in_para_set[0].split(',')[0]
	out_para_set = Lines[i + 2].strip(';\n').split(';')
	print(out_para_set)
	print(id)
	simu_carema(points, 9, 16,out_para_set, 2, 5, id)
	print("saved")


#simu_carema(points,30,40,(2,0,0),0,0,0,2,4)

#output=simu_carema(points,30,40,(25,25,2),0,0,0,1,5)
#kernel = np.array([[-1,-1,0],[-1,0,1],[0,1,1]])
#output = cv2.filter2D(output,-1,kernel)