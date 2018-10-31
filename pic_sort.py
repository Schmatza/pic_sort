##### This Code reads the date of photos and creates folder and names and tags those #####
### 1) Read Birthdate and create weekly folder, afterwards move the file in the folder
### 2) 

import os, time, errno
from ctypes import *
import datetime
import pathlib
import json
import osx_tags

### Get absolute path of file Function
def generate_absolute_path(photo_name): #Picture needs to be in Folder or Subfolder -> testfolder/testfile.jpg
	absolute_path = os.path.abspath(photo_name)
	return absolute_path

### Get Birthdate year and week of file to create weekly folder
def get_birth_year_week(file_name):
	stat = os.stat(file_name)
	try:
		tmp_date = datetime.date.fromtimestamp(stat.st_birthtime)
		return tmp_date
	except AttributeError:
		#return datetime.date.fromtimestamp(time.ctime(stat.st_mtime))
		tmp_date1 = datetime.date.fromtimestamp(stat.st_mtime) #ctime (under Windows creation time / under Linux last modification time)
		return tmp_date1.year, tmp_date1.isocalendar()[1]
		# We're probably on Linux. No easy way to get creation dates here,
		# so we'll settle for when its content was last modified.

### Silent Remove

def silent_remove(file_name):
	try:
		os.remove(file_name)
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

### Check if the raw file has a jpg with the same name and move it only when it is tagged
#def move_tagged_raf(file_name,source_folder,target_folder):



### Input Variables
source_folder = input('Please Specify the input folder')
#input('Please specify the source folder where the photos are in')
target_folder = input('Please specify the target folder')
#input('Please sepcify the target folder where the photos are safed')
#photo_name = input('Please insert the path of the file (eg. test/DSCF7322.JPG)')

#photo_path = generate_absolute_path(photo_name)
#generated_photo_name = source_folder+os.path.basename(photo_path)
#birthtime = get_birth_year_week(generated_photo_name) 
#weekly_folder = str(birthtime[0])+'_KW'+str(birthtime[1])

### Loop through the list until all photos are sorted in weekly folder
tmp_source_photo_list = list()
tmp_jpg_photo_list = list()
tmp_raf_photo_list = list()
tmp_mov_video_list = list()

tmp_jpg_wo_ext_list = list()

extensions = ['.jpg','.JPG','.raf','.RAF','.MOV','.mov'] #Insert Extensions of files that should be listed and therwith moved to the folder
extensions_jpg = ['.jpg','.JPG']
extensions_raf = ['.raf','.RAF']
extensions_mov = ['.mov','.MOV']

for file in os.listdir(source_folder):
	if file.endswith(tuple(extensions_jpg)):
		tmp_source_photo_list.append(file)
		tmp_jpg_photo_list.append(file)
	elif file.endswith(tuple(extensions_raf)):
		tmp_source_photo_list.append(file)
		tmp_raf_photo_list.append(file)
	elif file.endswith(tuple(extensions_mov)):
		tmp_source_photo_list.append(file)
		tmp_mov_video_list.append(file)

## Get List without .jpg extensions

for item in tmp_jpg_photo_list:
	tmp_jpg_wo_ext_list.append(os.path.splitext(item)[0])

## Create Dict that safes the Tags of all JPGs

tmp_jpg_tags = {}
for item in tmp_jpg_photo_list:
	tmp_jpg_tags[os.path.splitext(item)[0]] = osx_tags.Tags(generate_absolute_path(source_folder+item)).read()

#print(tmp_jpg_tags) $$

crf = 0
hang_owl = 0
ncrfc = 0

change_log = {}

if tmp_source_photo_list == []:
	print('The source_folder is empty. Please insert Photos before you run the software')
else:
	for tmp_photo in tmp_source_photo_list:
		birthtime = get_birth_year_week(source_folder+tmp_photo)
		year_calender_week = str(birthtime[0])+'_KW_'+str(birthtime[1])
		year = str(birthtime[0])
		calender_week = str(birthtime[1])
		filename = os.path.splitext(tmp_photo)[0]
		file_extension_dot = os.path.splitext(tmp_photo)[1].upper()
		file_extension = os.path.splitext(tmp_photo)[1][1:].upper()
		#year_list = next(os.walk(target_folder))[1]

		#if file_extension == 'RAF' and filename in prf_source_list:
			#check if there is a jpg duplicate
			#filename
		
		if file_extension_dot == '.RAF':
			#tagprf = osx_tags.Tags(generate_absolute_path(source_folder+filename+'.JPG')).read()
			#print(tagprf)
			if 'Green\n2' in tmp_jpg_tags[filename] and filename in tmp_jpg_wo_ext_list:
				osx_tags.Tags(generate_absolute_path(source_folder+tmp_photo)).add('Green')
				if 'Blue\n4' in tmp_jpg_tags[filename] and filename in tmp_jpg_wo_ext_list:
					osx_tags.Tags(generate_absolute_path(source_folder+tmp_photo)).add('Blue')
				pathlib.Path(generate_absolute_path(target_folder+year+'/'+year+'_KW_'+calender_week+'/'+file_extension.upper())).mkdir(parents=True, exist_ok=True)
				os.rename(generate_absolute_path(source_folder+tmp_photo),generate_absolute_path(target_folder+year+'/'+year+'_KW_'+calender_week+'/'+file_extension.upper()+'/'+year_calender_week+'_'+filename+file_extension_dot))
				change_log[tmp_photo] = datetime.datetime.now()
			elif 'Blue\n4' in tmp_jpg_tags[filename] and filename in tmp_jpg_wo_ext_list:
				osx_tags.Tags(generate_absolute_path(source_folder+tmp_photo)).add('Blue')
				pathlib.Path(generate_absolute_path(target_folder+year+'/'+year+'_KW_'+calender_week+'/'+file_extension.upper())).mkdir(parents=True, exist_ok=True)
				os.rename(generate_absolute_path(source_folder+tmp_photo),generate_absolute_path(target_folder+year+'/'+year+'_KW_'+calender_week+'/'+file_extension.upper()+'/'+year_calender_week+'_'+filename+file_extension_dot))
				change_log[tmp_photo] = datetime.datetime.now()
			else:
				ncrfc += 1 ## Not Copied Raw File Counter
			change_log['Not Copied Raw File Counter:'] = ncrfc
		else:
			pathlib.Path(generate_absolute_path(target_folder+year+'/'+year+'_KW_'+calender_week+'/'+file_extension.upper())).mkdir(parents=True, exist_ok=True)
			os.rename(generate_absolute_path(source_folder+tmp_photo),generate_absolute_path(target_folder+year+'/'+year+'_KW_'+calender_week+'/'+file_extension.upper()+'/'+year_calender_week+'_'+filename+file_extension_dot))
			change_log[tmp_photo] = datetime.datetime.now()
			#silent_remove(generate_absolute_path(source_folder+tmp_photo))
		
## Check if there are equally named pictures with an jpg and raf extention: move only raf whith tag



	with open ('change_log_file.txt', 'a') as change_log_file:
		change_log_file.write(json.dumps(change_log, indent=4, sort_keys=True, default=str))
		print('change log has been extended')
		print('The pictures where copied and are completely sorted')


"""
change_log_file = open('change_log_file','w')
for item in change_log:
	change_log_file.write('%s\n' % change_log[item])
change_log_file .close()
"""


