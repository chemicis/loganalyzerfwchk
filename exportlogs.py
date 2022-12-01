#Export logs with filter
import os
import sys


def read_path_file(pathlogs,filename):
	
	file_logs=[]
	try:
		for file in os.listdir(pathlogs): 
			if (file.startswith(filename) and file.endswith(".log")):
				print("file found: "+os.path.join(pathlogs,file)) 
				file_logs.append(os.path.join(pathlogs,file))
		print(file_logs)
			
	except Exception as e:
		print(e)
		finish()

	return file_logs

def export(list_path, device, filter):
	cont=1
	try:
		for file in list_path:
			print("Analyzing file: "+file )
			os.system('fw log -n -p -h '+device+' '+file+' | awk "'+filter+'" > /var/log/RevsionRegla/File-'+str(cont)+'.txt')
			cont+=1
			print("Done")
	except Exception as e:
		print(e)
		finish()
		 

def analyze():
	src_g=""
	dst_g=""
	svc_g=""
	snat_g=""
	date_g=""
	
	data_file = open("data.txt","a")
	ruta_dir="/var/log/RevsionRegla/"
	print("Generating output considering columns source, destination, service, SNAT\n")
	for ruta in os.listdir(ruta_dir):
		full_path_file=os.path.join(ruta_dir, ruta)
		if os.path.isfile(full_path_file):
			print(full_path_file)
			with open(full_path_file, 'r') as logrule:
				print("Analysis of File: "+full_path_file)
				for line in logrule:
					line_good = line.split()
					for source in line_good:
						if "src:" == source:
							position=line_good.index(source)
							src_g=line_good[position+1]

					for destino in line_good:
						if "dst:" == destino:
							position=line_good.index(destino)
							dst_g=line_good[position+1]
					for servicio in line_good:
						if "svc:" == servicio:
							position=line_good.index(servicio)
							svc_g=line_good[position+1]
					
					data_file.write(src_g+dst_g+svc_g+"\n")
					dst_g = "X"
					src_g = "X"
					svc_g = "X"
					snat_g = "X"
					date_g = "X"
	data_file.close()

def format():
	file2=open("data_format.txt","w")
	arrTemp=[]
	with open("data.txt", "r") as logfile:
		for line in logfile:
			arrTemp.append(line.replace(";",","))
		for line in arrTemp:
			file2.write(line[:-2]+"\n")
	file2.close()

def main():

	try:
		option_default="y"
		option=input("Do you want analyze files created on /var/log/RevsionRgla/?: [y]/abc.: ")
		if option==option_default.lower():
			analyze()
			format()
		else:
			pathlogs=input('Path of logs to export to txt: ')
			file_name=input('File name of file to analyze: ')
			list_path=read_path_file(pathlogs,file_name)
			device=input('Enter the IP of origin FW to filter the log: ')
			filtro=input('Enter the some filter, for example /src: 10.2.4.3/ && /dst: 20.3.4.3/, please have in mind structure of log to add fields: ')
			print(pathlogs)
			list_path=read_path_file(pathlogs,file_name)
			export(list_path, device, filtro)
			analyze()
			format()
			print("File generated: data_format.txt")
	
	except KeyboardInterrupt:
		print("Program terminated manually!")
		raise SystemExit

	except Exception as e:
		print(e+"\nFinish.")
		finish()

def finish():
	sys.exit()


if __name__ == '__main__':
  main()


##Version 2.0