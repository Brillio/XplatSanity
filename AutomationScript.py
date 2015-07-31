	#!/usr/bin/python

import sys,os,subprocess
import time
import sys
import random

count_err = 0
count_ok = 0
cmd_ok = 0
random_no = random.randrange(10, 10000, 2)

def create_file(path):
	if os.path.exists(path):
		os.remove(path)
	logfile = open(path,'a')
	return logfile

def execute_command_with_flag(cmd,logfile,flag,metalog):
	if(flag == "1"):
		p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		lines = p1.stdout.read()
		p1.wait()
		out,err =  p1.communicate()
		str1 = metalog.replace("*","")
		if(err):
		 logerr.write(metalog)
		 for linerr in err:
		  logerr.write(linerr)
		 global count_err
		 count_err+=1
		 print str1 + '--FAIL' + '\n'
		else:
		 logfile.write(metalog)
		 for line in lines:
		  logfile.write(line)
		 global count_ok
		 count_ok+=1
		 print "\n" + str1 + "--PASS" + '\n'
		 
		 
def printstatus():
 print 'Total No of Pass:',count_ok
 print 'Total No of Fail:', count_err

def retryLoad1(retryCommand,logfile,metalog):
    for y in range(5):
     try:
      execute_command(retryCommand,logfile,metalog) 
     except Exception as e:
      print e
      #continue
     else:
	  if cmd_ok == 0:
       #raise Exception('failed')
	   continue
	  else:
	   break
	   
    
	  
def execute_command(cmd,logfile,metalog):
   	p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	lines = p1.stdout.read()
	p1.wait()
	cmd_ok=0
	out,err =  p1.communicate()
	str1 = metalog.replace("*","")
	if(err):
	 logerr.write(metalog)
	 for linerr in err:
	  logerr.write(linerr)
	 global count_err
	 count_err+=1
	 print str1 + '--FAIL' + '\n'
	else:
	 logfile.write(metalog)
	 for line in lines:
	  logfile.write(line)
	 global count_ok
	 count_ok+=1
	 global cmd_ok
	 cmd_ok=1
	 print str1 + "--PASS" +"\n"


if __name__ == "__main__":
	from config import config
	logfile = create_file("" + config['LOG_FILE'] + "")
	logerr = create_file("" + config['LOG_FILERR'] + "")
	if(config['GLOBAL_FLAG'] == "1"):
		logfile.write("************** Test Summary Report **************** \n")
		metalog = "************** NPM CACHE CLEAR **************** \t" 
		retryLoad1("npm cache clear",logfile,metalog)		
		metalog = "************** NPM AZURE INSTALL **************** \t" 
		retryLoad1("npm install azure -g",logfile,metalog)		
		metalog = "************** Azure Help Command **************** \t"
		retryLoad1("azure",logfile,metalog)

		if(config['AD_Login'] == "0"):
		 metalog = "************** Azure Login **************** \t" 
		 retryLoad1("azure login -u "+ config['LOGINUSER'] + " -p " + config['LOGINPASSWORD'] + " --quiet",logfile,metalog)
		else:
		 metalog = " ************** Azure Account Download ******************* \t"
		 retryLoad1("azure account download ",logfile,metalog)		
		 metalog = " ************** Azure Account Import ******************* \t"
		 retryLoad1("azure account import "+ config['PUBLISHSETTINGS_FILE'],logfile,metalog)		
		metalog = " ************** Azure Account List ******************* \t"
		retryLoad1("azure account list ",logfile,metalog)
		metalog = " ************** Azure Account Set ******************* \t"
		retryLoad1("azure account set "+ config['SUBSCRIPTION_ID'],logfile,metalog)

		metalog = " ************** Azure Service List ******************* \t"
		retryLoad1("azure service list",logfile,metalog)
		
		metalog = "************** Azure Network List ******************* \t"
		retryLoad1("azure network vnet list",logfile,metalog)
		metalog = "************** Azure Network Create ******************* \t"
		retryLoad1("azure network vnet create "+config['NETWORK_NAME'] + " -l "+config['LOCATION'],logfile,metalog)
		metalog = "************** Azure Network Show ******************* \t"
		retryLoad1("azure network vnet show "+config['NETWORK_NAME'],logfile,metalog)
		
		metalog = " ************** Azure network reserved-ip list ******************* \t"
		retryLoad1("azure network reserved-ip list",logfile,metalog)
		metalog = " ************** Azure network reserved-ip create ******************* \t"
		retryLoad1("azure network reserved-ip create " + config['RIPNAME'] + " " + config['LOCATION'], logfile,metalog)
		metalog = " ************** Azure  network reserved-ip show ******************* \t"
		retryLoad1("azure network reserved-ip show " + config['RIPNAME'],logfile,metalog)

		metalog = "************** Azure Account Affinity Group List ******************* \t"
		retryLoad1("azure account affinity-group list ",logfile,metalog)
		metalog = "************** Azure Account Affinity Group Create ******************* \t"		
		retryLoad1("azure account affinity-group create -l "+config['LOCATION']+ " -e "+config['AFFINITY_GRP_LABEL']+ " -d "+config['AFFINITY_GRP_DESC']+ " " +config['AFFINITY_GRP_NAME'] ,logfile,metalog)		
		metalog = "************** Azure Account Affinity Group Show ******************* \t"		
		retryLoad1("azure account affinity-group show " +config['AFFINITY_GRP_NAME'] ,logfile,metalog)			

		metalog = "************** Azure Account Storage List ******************* \t"
		retryLoad1("azure storage account list ",logfile,metalog)		
		metalog = "************** Azure Location List ******************* \t"
		retryLoad1("azure vm location list",logfile,metalog)
		metalog = "************** Azure Config List ******************* \t"
		retryLoad1("azure config list ",logfile,metalog)		
		metalog = "************** Azure Config Set ******************* \t"
		retryLoad1("azure config set "+ config['CONFIG_KEY'] + " " + config['CONFIG_VALUE'],logfile,metalog)

		metalog = "************** Azure VM Disk List ******************* \t"
		retryLoad1("azure vm disk list",logfile,metalog)		
		metalog = "************** Azure VM Disk Create ******************* \t"
		retryLoad1("azure vm disk create -a " + config['AFFINITY_GRP_NAME'] + " -u "+config['DISK_IMAGE_BLOB_URL']+" -l " +config['LOCATION']+" -o "+'''"LINUX"''' + " -p 2 -m -f -e " + config['VM_DISK_LABEL'] + " -d "+ config['VM_DISK_DESC'] + " " + config['VM_DISK_IMAGE_NAME']+ " "+config['VM_DISK_SOURCE_PATH'],logfile,metalog)
		metalog = "************** Azure VM Disk Show ******************* \t"
		retryLoad1("azure vm disk show "+config['VM_DISK_IMAGE_NAME'],logfile,metalog)

		metalog = "************** Azure VM Image List ******************* \t"
		retryLoad1("azure vm image list",logfile,metalog)		
		metalog = "************** Azure VM Image Create ******************* \t"
		retryLoad1("azure vm image create -a " + config['AFFINITY_GRP_NAME'] + " -u "+config['IMAGE_BLOB_URL']+" -l " +config['LOCATION']+" -o "+'''"LINUX"'''+ " -p 2 -m -f -e " + config['VM_IMAGE_LABEL'] + " -d "+ config['VM_IMAGE_DESC'] + " " + config['VM_IMAGE_NAME']+ " " +config['DISK_IMAGE_BLOB_URL'],logfile,metalog)
		metalog = "************** Azure VM Image Show ******************* \t"
		retryLoad1("azure vm image show "+config['VM_IMAGE_NAME'],logfile,metalog)

		metalog = "************** Azure VM List ******************* \t"
		retryLoad1("azure vm list",logfile,metalog)		
		metalog = "************** Azure VM Create ******************* \t"
		retryLoad1("azure vm create "+config['VM_NAME']+" "+config['IMAGE_NAME']+" "+config['USER_NAME']+" "+config['PASSWORD']+" -l " +config['LOCATION']+" -e ",logfile,metalog)

		metalog = "************** Azure Vm Extension list ************\t"
		retryLoad1("azure vm extension list",logfile,metalog)		
		metalog = "************** Azure Vm Extension Get ************\t"
		retryLoad1("azure vm extension get "+config['VM_NAME'],logfile,metalog)
		metalog = "************** Azure Vm Extension Set ************\t"
		retryLoad1("azure vm extension set "+config['VM_NAME'] +" "+config['EXTN_NAME']+" "+config['EXTN_PUB_NAME']+" "+config['EXTN_VERSION']+" -c "+config['EXTN_FILE'],logfile,metalog)
		
		metalog = "************** Azure Disk List with VMName ************\t"
		retryLoad1("azure vm disk list "+config['VM_NAME'],logfile,metalog)

		metalog = "************** Azure Windows VM Create ******************* \t"
		retryLoad1("azure vm create "+config['VM_WIN_NAME']+" "+config['WIN_IMAGE_NAME']+" testuser "+config['PASSWORD']+" -l " +config['LOCATION'],logfile,metalog)

		metalog = "************** PIP Commands ****************************** \t"
		metalog = "************** VM Create with PIP ****************************** \t"
		retryLoad1("azure vm create "+ "-i  " + config['PUBLICIPNAME']+ " " +config['VM_WIN_PIP'] +" "+config['WIN_IMAGE_NAME']+ " " + "testuser "+ " " +config['PASSWORD']+" -l " +config['LOCATION'],logfile,metalog)

		metalog = "************** PIP List ****************************** \t"
		retryLoad1("azure vm public-ip list "+config['VM_WIN_PIP'],logfile,metalog)
		
		metalog = "************** PIP REMOVE ****************************** \t"
		retryLoad1("azure vm public-ip delete "+config['VM_WIN_PIP']+ "  " + config['PUBLICIPNAME'] + " -q ",logfile,metalog)
		
		metalog = "************** PIP SET ****************************** \t"
		retryLoad1("azure vm public-ip set "+config['VM_WIN_PIP'] +" " + config['PUBLICIPSET'],logfile,metalog)
		 
		metalog = "************** PIP VM DELETE ****************************** \t" 
		retryLoad1("azure vm delete "+ config['VM_WIN_PIP'] + " -b -q",logfile,metalog)
		
		metalog = "************** Azure Windows VM Create ******************* \t"
		retryLoad1("azure vm create "+config['VM_WIN_ACL']+" "+config['WIN_IMAGE_NAME']+" testuser "+config['PASSWORD']+" -l " +config['LOCATION'],logfile,metalog)
		
		metalog = "************** Azure VM End Point For Acl Create ******************* \t"
		retryLoad1("azure vm endpoint create "+config['VM_WIN_ACL']+" 21 23 ",logfile,metalog)
		
		metalog = "************** ACL Create RULE ****************************** \t"
		retryLoad1("azure vm endpoint acl-rule create " + config['VM_WIN_ACL'] + " " + config['ENDPOINT'] + " " + config['ORDER'] + " " + config['ACL_ACTION'] + " " + config['REMOTESUBNET'],logfile,metalog)
		
		metalog = "************** ACL List****************************** \t" 
		retryLoad1("azure vm endpoint acl-rule list "+ config['VM_WIN_ACL'] + " " + config['ENDPOINT'],logfile,metalog)
		
		metalog = "************** ACL Rule Delete****************************** \t" 
		retryLoad1("azure vm endpoint acl-rule delete "+ config['VM_WIN_ACL'] + " " + config['ENDPOINT']+ " " + config['ORDER']+" -q ",logfile,metalog)
		
		metalog = "************** ACL VM DELETE ****************************** \t" 
		retryLoad1("azure vm delete "+ config['VM_WIN_ACL'] + " -b -q",logfile,metalog)
		
		metalog = "************** Azure VM Show ******************* \t"
		retryLoad1("azure vm show "+config['VM_NAME'],logfile,metalog)
		metalog = "************** Azure VM Start ******************* \t"
		retryLoad1("azure vm start "+config['VM_NAME'],logfile,metalog)

		metalog = "************** Azure VM Export ******************* \t"
		retryLoad1("azure vm export "+config['VM_NAME']+ " " + config['FILE_PATH'],logfile,metalog)

		metalog = "************** Azure VM End Point Create ******************* \t"
		retryLoad1("azure vm endpoint create "+config['VM_NAME']+" 21 23 ",logfile,metalog)
		
		metalog = "************** Azure VM End Point Create-Multiple ******************* \t"
		retryLoad1("azure vm endpoint create-multiple "+config['VM_NAME']+" "+config['ONLYPP_PUBLICPORT'] + "::::::::::::,"+config['PPANDLP_PUBLICPORT'] +":"+config['PPANDLP_LOCALPORT']+":::::::::::,",logfile,metalog)
		metalog = "************** Azure VM End Point show ******************* \t"
		retryLoad1("azure vm endpoint show "+config['VM_NAME']+ " tcp-21-23 ",logfile,metalog)
		metalog = "************** Azure VM Endpoint List ******************* \t"
		retryLoad1("azure vm endpoint list "+config['VM_NAME'],logfile,metalog)
		metalog = "************** Azure VM Endpoint Set ******************* \t"
		retryLoad1("azure vm endpoint set "+config['VM_NAME']+ " tcp-21-23 -n testpoint ",logfile,metalog)
		metalog = "************** Azure VM Endpoint Delete ******************* \t"
		retryLoad1("azure vm endpoint delete "+config['VM_NAME']+ " testpoint ",logfile,metalog)

		metalog = "************** Azure VM Disk Attach ******************* \t"
		retryLoad1("azure vm disk attach "+config['VM_NAME']+" "+config['VM_DISK_IMAGE_NAME'],logfile,metalog)
		metalog = "************** Azure VM Disk Attach New ******************* \t"
		retryLoad1("azure vm disk attach-new "+config['VM_NAME']+" 177 "+config['VM_DISK_ATTACH_BLOB_URL']+str(random_no)+".vhd",logfile,metalog)
		metalog = "************** Azure VM Disk Detach ******************* \t"
		retryLoad1("azure vm disk detach "+config['VM_NAME']+" 1",logfile,metalog)
		retryLoad1("azure vm disk detach "+config['VM_NAME']+" 0",logfile,metalog)

		metalog = "************** Azure VM Restart ******************* \t"
		retryLoad1("azure vm restart "+config['VM_NAME'],logfile,metalog)
		metalog = "************** Azure VM ShutDown ******************* \t"
		retryLoad1("azure vm shutdown "+config['VM_NAME'],logfile,metalog)
		metalog = "************** Azure VM Capture ******************* \t"
		retryLoad1("azure vm capture "+config['VM_NAME']+" "+config['TARGET_IMG_NAME']+ " -t ",logfile,metalog)
		
		metalog = "************** Azure static-ip VM Create******************* \t"
		retryLoad1("azure vm create "+config['STATICIP_VM_NAME']+" "+config['IMAGE_NAME']+" communityUser PassW0rd$ "+" --virtual-network-name "+config['NETWORK_NAME'] + " " + "--affinity-group" +  " " + config['AFFINITY_GRP_NAME'] + " " + " --static-ip "+ " " + config['STATIC_IP_TO_CREATE'],logfile,metalog)
		metalog = "************** Azure static-ip Set ******************* \t"
		retryLoad1("azure vm static-ip set "+ config['STATICIP_VM_NAME'] +" "+ config['STATIC_IP_TO_SET'],logfile,metalog)
		metalog = "************** Azure static-ip Check ******************* \t"
		retryLoad1("azure network vnet static-ip check "+config['NETWORK_NAME'] + " " + config['STATIC_IP_TO_SET'],logfile,metalog)
		metalog = "************** Azure static-ip Remove ******************* \t"
		retryLoad1("azure vm static-ip remove "+config['STATICIP_VM_NAME'],logfile,metalog)
		metalog = "************** Azure static-ip VM Restart ******************* \t"
		retryLoad1("azure vm restart "+config['STATICIP_VM_NAME'],logfile,metalog)
		metalog = "************** Azure static-ip VM Delete ******************* \t"
 		retryLoad1("azure vm delete "+config['STATICIP_VM_NAME'] + " -b --quiet ",logfile,metalog)
		metalog = "************** Azure static-ip Docker VM Delete ******************* \t"
		retryLoad1("azure vm delete "+config['DOCKER_STATIC_VM_NAME'] + " -b --quiet ",logfile,metalog)
		
		
		metalog = "************** Azure Service Delete ******************* \t"
		retryLoad1("azure service delete "+config['VM_NAME'] + " --quiet ",logfile,metalog)
		metalog = "************** Azure VM Create-from ******************* \t"
		retryLoad1("azure vm create-from "+config['VM_NAME']+" "+config['FILE_PATH'] + " -l " +config['LOCATION'],logfile,metalog)
		metalog = "************** Azure VM Community Image Create ******************* \t"
		retryLoad1("azure vm create " + config['VM_COMM_NAME'] + " -o "+config['VM_COMM_IMAGE_NAME']+" -l "+config['LOCATION']+" communityUser PassW0rd$",logfile,metalog)
		metalog = "************** Azure VM SSHCert Create ******************* \t"
		retryLoad1("azure vm create " + config['VM_SSH_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser --ssh-cert "+config['CERT_FILE'] + " -e --no-ssh-password -r -l "+config['LOCATION'],logfile,metalog)
		metalog = "************** Azure VM Comm Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_COMM_NAME'] + " -b --quiet ",logfile,metalog)
		metalog = "************** Azure VM SSHCert Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_SSH_NAME'] + " -b --quiet",logfile,metalog)

		metalog = "************** Azure VM reserved-ip Create ******************* \t"
		retryLoad1("azure vm create " + config['VM_RIP_NAME'] + " "+config['IMAGE_NAME']+" "+config['USER_NAME']+" "+config['PASSWORD']+" -l " +config['LOCATION']+" -R " + config['RIPNAME'] + " --ssh",logfile,metalog)
		metalog = "************** Azure VM reserved-ip Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_RIP_NAME'] + " -b --quiet ",logfile,metalog)	
		
		metalog = "************** Azure VM Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_NAME'] + " -b --quiet ",logfile,metalog)
		metalog = "************** Azure Windows VM Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_WIN_NAME'] + " -b --quiet ",logfile,metalog)
		metalog = " ************** Azure network reserved-ip delete ******************* \t"
		retryLoad1("azure network reserved-ip delete " + config['RIPNAME'] +" -q",logfile,metalog)
		
		# metalog = "************* Azure VM Disk Upload ******************* \t"
		# retryLoad1("azure vm disk upload "+config['DISK_UPLOAD_SOURCE_PATH']+" "+config['DISK_UPLOAD_BLOB_URL']+" "+config['STORAGE_ACCOUNT_KEY'],logfile,metalog)		

		metalog = "************* Azure VM Image Delete ******************* \t"
		retryLoad1("azure vm image delete "+config['VM_IMAGE_NAME'],logfile,metalog)
		metalog = "************** Azure VM Captured Image Delete ******************* \t"
		retryLoad1("azure vm image delete "+config['TARGET_IMG_NAME'],logfile,metalog)
		metalog = "************** Azure VM Disk Delete ******************* \t"
		retryLoad1("azure vm disk delete "+config['VM_DISK_IMAGE_NAME'],logfile,metalog)
		
		
 		metalog = "********************** Azure VM Docker Create********************************* \t"	
 		retryLoad1("azure vm docker create "+ config['VM_DOCKER_NAME'] + " "+ config['VM_DOCKER_IMG_NAME'] +" "+ config['USER_NAME'] +" "+ config['PASSWORD'] +" -l " +config['LOCATION']+" " + config['CERT_FILE'] + " " + config['VM_DOCKER_PORT'] ,logfile,metalog)
 		metalog = "************** Azure VM Docker Delete ******************* \t"
 		retryLoad1("azure vm delete "+config['VM_DOCKER_NAME'] + " -b --quiet ",logfile,metalog)

		
		metalog = "************** Azure VM Create_VNet ******************* \t"
		retryLoad1("azure vm create " + config['VM_VNET_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser PassW0rd$ --virtual-network-name " + config['NETWORK_NAME'] + " -n vnet_img_vm",logfile,metalog)
		metalog = "************** Azure VM Create_Size ******************* \t"
		retryLoad1("azure vm create " + config['VM_SIZE_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser PassW0rd$ -z Small -c -l "+config['LOCATION'],logfile,metalog)
		metalog = "************** Azure create VM_CUSTOM_DATA ******************* \t"
		retryLoad1("azure vm create -d " + config['CUSTOM_DATA_FILE'] + " " + config['VM_CUSTOMDATA_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser PassW0rd$ -l "+config['LOCATION'],logfile,metalog)
		
		metalog = "************** Azure VM_VNet Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_VNET_NAME'] + " -b --quiet ",logfile,metalog)
		metalog = "************** Azure vnet_img_vm Delete ******************* \t"
		retryLoad1("azure vm delete vnet_img_vm -b --quiet ",logfile,metalog)
		metalog = "************** Azure VM_SIZE Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_SIZE_NAME'] + " -b --quiet ",logfile,metalog)
		metalog = "************** Azure VM_CUSTOM_DATA Delete ******************* \t"
		retryLoad1("azure vm delete "+config['VM_CUSTOMDATA_NAME'] + " -b --quiet ",logfile,metalog)

		
		metalog = " ************** LoadBalancer Vm should create with vnet ******************* \t"
		retryLoad1("azure vm create " + config['VM_NAME'] + " " + " --virtual-network-name "+ config['NETWORK_NAME'] + " -l " + config['LOCATION'] + " " + config['IMAGE_NAME'] + " " + config['USER_NAME'] + " " + config['PASSWORD'] ,logfile,metalog)		
		metalog = " ************** LoadBalancer Add ******************* \t"
		retryLoad1("azure service internal-load-balancer add " + config['VM_NAME'] + " -t " + config['SUBNET'] + " -n " + config['INTERNAL_LB_NAME'] ,logfile,metalog)		
		metalog = " ************** LoadBalancer List ******************* \t"
		retryLoad1("azure service internal-load-balancer list " + config['VM_NAME'] ,logfile,metalog)	
		metalog = " ************** LoadBalancer Set ******************* \t"
		retryLoad1("azure service internal-load-balancer set " + config['VM_NAME'] + " " + config['INTERNAL_LB_NAME_UPDATE'] + " -t " + config['SUBNET'] + " -a " + config['SUBNETIP'] ,logfile,metalog)		
		metalog = " ************** LoadBalancer Delete ******************* \t"
		retryLoad1("azure service internal-load-balancer delete " + config['VM_NAME'] + " -n " + config['INTERNAL_LB_NAME'] + " --quiet " ,logfile,metalog)
		metalog = "************** Azure LoadBalancer VM Delete ******************* \t"
		retryLoad1("azure vm delete " + config['VM_NAME'] + " -b --quiet " ,logfile,metalog)
		
		
		# ASM NETWORK NEW COMMANDS Starts
		# NETWORK NSG Create List Show
		metalog = " ************** Network Nsg Create ******************* \t"
		retryLoad1("azure network nsg create " + config['NETWORK_NSG_NAME'] +  " -l " + config['LOCATION'] + " -b " + config['NSG_LABEL'], logfile, metalog)
		metalog = " ************** Network Nsg List ******************* \t"
		retryLoad1("azure network nsg list " ,logfile,metalog)	
		metalog = " ************** Network Nsg Show ******************* \t"
		retryLoad1("azure network nsg show " + config['NETWORK_NSG_NAME'], logfile, metalog)
		
		# NETWORK NSG RULE Create Set List Show Delete
		metalog = " ************** Network Nsg Rule Create ******************* \t"
		retryLoad1("azure network nsg rule create " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'] + " -p " + config['PROTOCOL'] + " -f " + config['SOURCE_ADDRESS_PREFIX'] + " -o " + config['SOURCE_PORT_RANGE'] + " -e " + config['DESTINATION_ADDRESS_PREFIX'] + " -u " + config['DESTINATION_PORT_RANGE'] + " -c " + config['ACTION'] + " -y " + config['PRIORITY'] + " -r " + config['TYPE'], logfile, metalog)
		metalog = " ************** Network Nsg Rule Set ******************* \t"
		retryLoad1("azure network nsg rule set " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'] + " -p " + config['PROTOCOL_SET'] + " -f " + config['SOURCE_ADDRESS_PREFIX_SET'] + " -o " + config['SOURCE_PORT_RANGE_SET'] + " -e " + config['DESTINATION_ADDRESS_PREFIX_SET'] + " -u " + config['DESTINATION_PORT_RANGE_SET'] + " -c " + config['ACTION_SET'] + " -y " + config['PRIORITY_SET'] + " -r " + config['TYPE_SET'], logfile, metalog)
		metalog = " ************** Network Nsg Rule List ******************* \t"
		retryLoad1("azure network nsg rule list " + config['NETWORK_NSG_NAME'], logfile, metalog)	
		metalog = " ************** Network Nsg Rule Show ******************* \t"
		retryLoad1("azure network nsg rule show " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'], logfile, metalog)
		metalog = " ************** Network Nsg Rule Delete ******************* \t"
		retryLoad1("azure network nsg rule delete " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'] +  " -q ", logfile, metalog)
		
		# NETWORK VNET SUBNET Create Set List Show
		metalog = " ************** Azure Network Vnet Subnet Create ******************* \t"
		retryLoad1("azure network vnet subnet create " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -a " + config['ADDRESS_PREFIXES'], logfile, metalog)
		metalog = " ************** Azure Network Vnet Subnet Set ******************* \t"
		retryLoad1("azure network vnet subnet set " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -a " + config['ADDRESS_PREFIXES_SET'], logfile, metalog)
		metalog = "************** Azure Network Vnet Subnet List ******************* \t"
		retryLoad1("azure network vnet subnet list " + config['NETWORK_NAME'], logfile, metalog)
		metalog = "************** Azure Network Vnet Subnet Show ******************* \t"
		retryLoad1("azure network vnet subnet show " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'], logfile, metalog)
		
		# NETWORK NSG SUBNET Add Remove
		metalog = "************** Azure Network Nsg Subnet Add ******************* \t"
		retryLoad1("azure network nsg subnet add " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'], logfile, metalog)
		metalog = "************** Azure Network Nsg Subnet Remove ******************* \t"
		retryLoad1("azure network nsg subnet remove " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -q ", logfile, metalog)
		
		# NETWORK ROUTE-TABLE Create Set List Show
		metalog = " ************** Azure Network Route-Table Create ******************* \t"
		retryLoad1("azure network route-table create " + config['NETWORK_ROUTE_TABLE'] + " " + config['LOCATION'] + " -b " + config['ROUTE_LABEL'], logfile, metalog)
		metalog = "************** Azure Network Route-Table List ******************* \t"
		retryLoad1("azure network route-table list ", logfile, metalog)
		metalog = "************** Azure Network Route-Table Show ******************* \t"
		retryLoad1("azure network route-table show " + config['NETWORK_ROUTE_TABLE'], logfile, metalog)
		
		# NETWORK ROUTE-TABLE ROUTE Set Delete
		metalog = "************** Azure Network Route-Table Route Set ******************* \t"
		retryLoad1("azure network route-table route set " + config['NETWORK_ROUTE_TABLE'] + " " + config['NETWORK_ROUTE'] + " " + config['ROUTE_ADDRESS_PREFIXES'] + " " + config['NEXT_HOP_TYPE'], logfile, metalog)
		metalog = "************** Azure Network Route-Table Route Delete ******************* \t"
		retryLoad1("azure network route-table route delete " + config['NETWORK_ROUTE_TABLE'] + " " + config['NETWORK_ROUTE'] + " -q ", logfile, metalog)
		
		# NETWORK SUBNET ROUTE-TABLE Add Show Delete
		metalog = " ************** Azure Network Subnet Route-Table Add ******************* \t"
		retryLoad1("azure network vnet subnet route-table add " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -r " + config['NETWORK_ROUTE_TABLE'], logfile, metalog)
		metalog = " ************** Azure Network Subnet Route-Table Show ******************* \t"
		retryLoad1("azure network vnet subnet route-table show " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -d " + config['NETWORK_ROUTE_TABLE'], logfile, metalog)
		metalog = "************** Azure Network Subnet Route-Table Delete ******************* \t"
		retryLoad1("azure network vnet subnet route-table delete " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " " + config['NETWORK_ROUTE_TABLE'] + " -q ", logfile, metalog)
		
		# NETWORK Traffic-Manager Profile Create Set List Show Enable Disable Delete
		metalog = " ************** Azure Network Traffic-Manager Profile Create ******************* \t"
		retryLoad1("azure network traffic-manager profile create " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'] + " -d " + config['DOMAIN_NAME'] + " -m " + config['lOADBALANCING_METHOD'] + " -o " + config['MONITOR_PORT'] + " -p " + config['MONITOR_PROTOCOL'] + " -r " + config['MONITOR_RELATIVE_PATH'] + " -t " + config['TTL'], logfile, metalog)		
		metalog = " ************** Azure Network Traffic-Manager Profile Set ******************* \t"
		retryLoad1("azure network traffic-manager profile set " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'] + " -m " + config['lOADBALANCING_METHOD_SET'] + " -o " + config['MONITOR_PORT_SET'] + " -p " + config['MONITOR_PROTOCOL_SET'] + " -r " + config['MONITOR_RELATIVE_PATH_SET'] + " -t " + config['TTL_SET'], logfile, metalog)		
		metalog = " ************** Azure Network Traffic-Manager Profile List ******************* \t"
		retryLoad1("azure network traffic-manager profile list ",logfile,metalog)	
		metalog = " ************** Azure Network Traffic-Manager Profile Show ******************* \t"
		retryLoad1("azure network traffic-manager profile show " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'], logfile, metalog)
		metalog = " ************** Azure Network Traffic-Manager Profile Enable ******************* \t"
		retryLoad1("azure network traffic-manager profile enable " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'], logfile, metalog)
		metalog = " ************** Azure Network Traffic-Manager Profile Disable ******************* \t"
		retryLoad1("azure network traffic-manager profile disable " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'], logfile, metalog)
		metalog = " ************** Azure Network Traffic-Manager Profile Delete ******************* \t"
		retryLoad1("azure network traffic-manager profile delete " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'] + " -q " ,logfile,metalog)
		
		# NETWORK Application-Gateway Create Set List Show Start Stop Delete
		metalog = " ************** Azure Network Application-Gateway Create ******************* \t"
		retryLoad1("azure network application-gateway create " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -e " + config['NETWORK_NAME'] + " -t " + config['NETWORK_SUBNET_NAME'] + " -c " + config['INSTANCE_COUNT'] + " -z " + config['GATEWAY_SIZE'] + " -d " + config['APPGATEWAY_DESCRIPTION'], logfile, metalog)		
		metalog = " ************** Azure Network Application-Gateway Set ******************* \t"
		retryLoad1("azure network application-gateway set " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -e " + config['NETWORK_NAME'] + " -t " + config['NETWORK_SUBNET_NAME'] + " -c " + config['INSTANCE_COUNT_SET'] + " -z " + config['GATEWAY_SIZE_SET'] + " -d " + config['APPGATEWAY_DESCRIPTION_SET'], logfile, metalog)		
		metalog = " ************** Azure Network Application-Gateway List ******************* \t"
		retryLoad1("azure network application-gateway list ",logfile,metalog)	
		metalog = " ************** Azure Network Application-Gateway Show ******************* \t"
		retryLoad1("azure network application-gateway show " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no), logfile, metalog)
		# Commented because Start has an Issue 
		# metalog = " ************** Azure Network Application-Gateway Start ******************* \t"
		# retryLoad1("azure network application-gateway start " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no), logfile, metalog)
		metalog = " ************** Azure Network Application-Gateway Stop ******************* \t"
		retryLoad1("azure network application-gateway stop " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no), logfile, metalog)
		
		# NETWORK Application-Gateway config Import, Show
		metalog = "************** Azure Network Application-Gateway Config Import ******************* \t"
		retryLoad1("azure network application-gateway config import " + " -n " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -t " + config['APPGATE_EXPORT_FILE'], logfile, metalog)
		metalog = "************** Azure Network Application-Gateway Config Show ******************* \t"
		retryLoad1("azure network application-gateway config show " + " -n " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no), logfile, metalog)
		
		# NETWORK Application-Gateway address-pool Add 
		metalog = "************** Azure Network Application-Gateway Address-Pool Add ******************* \t"
		retryLoad1("azure network application-gateway address-pool add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -r " + config['ADDRESSPOOL_IP'], logfile, metalog)
		
		# NETWORK Application-Gateway http-settings Add 
		metalog = "************** Azure Network Application-Gateway Http-Settings Add ******************* \t"
		retryLoad1("azure network application-gateway http-settings add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPSETTINGS_NAME']+str(random_no) + " -p " + config['HTTPSETTINGS_PROTOCOL'] + " -o " + config['HTTPSETTINGS_PORT'] + " -c " + config['HTTPSETTINGS_CBAFFINITY'], logfile, metalog)
		
		
		# NETWORK Application-Gateway frontend-ip Add & Remove
		# metalog = "************** Azure Network Application-Gateway Frontend-IP Add ******************* \t"
		# retryLoad1("azure network application-gateway frontend-ip add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDIP_NAME'] + " -t " + config['FRONTENDIP_TYPE'] + " -i " + config['FRONTENDIP_STATICIP'], logfile, metalog)
		
		# NETWORK Application-Gateway frontend-port Add & Remove
		metalog = "************** Azure Network Application-Gateway Frontend-Port Add ******************* \t"
		retryLoad1("azure network application-gateway frontend-port add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDPORT_NAME']+str(random_no) + " -o " + config['FRNTENDPORT_PORT'], logfile, metalog)
		
		# NETWORK Application-Gateway http-listener Add & Remove
		metalog = "************** Azure Network Application-Gateway Http-Listener Add ******************* \t"
		retryLoad1("azure network application-gateway http-listener add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPLISTENER_NAME']+str(random_no) + " -i " + config['APPGATE_FRONTENDIP_NAME'] + " -p " + config['APPGATE_FRONTENDPORT_NAME']+str(random_no) + " -t " + config['HTTPLISTENER_PROTOCOL'], logfile, metalog)
		
		# NETWORK Application-Gateway lb-rule Add 
		metalog = "************** Azure Network Application-Gateway LB-Rule Add ******************* \t"
		retryLoad1("azure network application-gateway lb-rule add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_LBRULE_NAME']+str(random_no) + " -i " + config['APPGATE_HTTPSETTINGS_NAME']+str(random_no) + " -l " + config['APPGATE_HTTPLISTENER_NAME']+str(random_no) + " -p " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -t " + config['LBRULE_TYPE'], logfile, metalog)
		
		# NETWORK Application-Gateway config Export
		metalog = "************** Azure Network Application-Gateway Config Export ******************* \t"
		retryLoad1("azure network application-gateway config export " + " -n " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -t " + config['APPGATE_EXPORT_FILE'], logfile, metalog)
		
		# NETWORK Application-Gateway lb-rule Remove
		metalog = "************** Azure Network Application-Gateway LB-Rule Remove ******************* \t"
		retryLoad1("azure network application-gateway lb-rule remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_LBRULE_NAME']+str(random_no) + " -q ", logfile, metalog)
		
		# NETWORK Application-Gateway address-pool Remove
		metalog = "************** Azure Network Application-Gateway Address-Pool Remove ******************* \t"
		retryLoad1("azure network application-gateway address-pool remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -q ", logfile, metalog)
		
		# NETWORK Application-Gateway http-listener Remove
		metalog = "************** Azure Network Application-Gateway Http-Listener Remove ******************* \t"
		retryLoad1("azure network application-gateway http-listener remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPLISTENER_NAME']+str(random_no) + " -q ", logfile, metalog)
		
		# NETWORK Application-Gateway http-settings Remove
		metalog = "************** Azure Network Application-Gateway Http-Settings Remove ******************* \t"
		retryLoad1("azure network application-gateway http-settings remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPSETTINGS_NAME']+str(random_no) + " -q ", logfile, metalog)
		
		# # # # Functionality not yet implemented, Issue No. MSOpenTech#293
		# # # NETWORK Application-Gateway frontend-ip Remove
		# # metalog = "************** Azure Network Application-Gateway Frontend-IP Remove ******************* \t"
		# # retryLoad1("azure network application-gateway frontend-ip remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDIP_NAME'] + " -q ", logfile, metalog)
		
		# NETWORK Application-Gateway frontend-port Remove
		metalog = "************** Azure Network Application-Gateway Frontend-Port Remove ******************* \t"
		retryLoad1("azure network application-gateway frontend-port remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDPORT_NAME']+str(random_no) + " -q ", logfile, metalog)
		
		
		# NETWORK Application-Gateway ssl-cert Add Remove
		metalog = "************** Azure Network Application-Gateway SSL_Cert Add ******************* \t"
		retryLoad1("azure network application-gateway address-pool add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -r " + config['ADDRESSPOOL_IP'], logfile, metalog)
		metalog = "************** Azure Network Application-Gateway SSL_Cert Remove ******************* \t"
		retryLoad1("azure network application-gateway address-pool remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -q ", logfile, metalog)
		
		
		# NETWORK Application-Gateway Delete
		metalog = " ************** Azure Network Application-Gateway Delete ******************* \t"
		retryLoad1("azure network application-gateway delete " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -q " ,logfile,metalog)
		
		# NETWORK NSG Delete
		metalog = " ************** Network NSG Delete ******************* \t"
		retryLoad1("azure network nsg delete " + config['NETWORK_NSG_NAME'] +  " -q ", logfile, metalog)
		
		# NETWORK ROUTE-TABLE Delete
		metalog = " ************** Network Route-Table Delete ******************* \t"
		retryLoad1("azure network route-table delete " + config['NETWORK_ROUTE_TABLE'] +  " -q ", logfile, metalog)
		
		# NETWORK VNET SUBNET Delete
		metalog = "************** Azure Network Vnet Subnet Delete ******************* \t"
		retryLoad1("azure network vnet subnet delete " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " --quiet ", logfile, metalog)
		 
		#Gateway Command - Start Here
		
		# NETWORK Vnet & Subnet Create for Gateway Create
		metalog = " ************** Azure Network Vnet for Gateway create ******************* \t"
		retryLoad1("azure network vnet create "+config['NETWORK_VPN_VNET_NAME'] + " -e " +config['VPN_VNET_ADDRESS'] + " -i " +config['VPN_VNETCIDR'] + " -p " +config['VPN_VNET_SUBNET_START_IP'] + " -r " +config['VPN_VNET_SUBNET_CIDR'] + " -l " +config['VPN_LOCATION'],logfile,metalog)
		metalog = " ************** Azure Network Vnet Subnet for Gateway create ******************* \t"
		retryLoad1("azure network vnet subnet create " + " -t "+config['NETWORK_VPN_VNET_NAME'] + " -n " +config['NETWORK_VPN_SUBNET_NAME'] + " -a " +config['VPN_SUBNET_ADDRESS'],logfile,metalog)
		
		# NETWORK LOCAL-NETWORK Create List Show Add
		metalog = " ************** Azure Network Local-Network Create ******************* \t"
		retryLoad1("azure network local-network create " + config['NETWORK_LOCALNETWORK_NAME'] + " -a " + config['LOCAL_NETWORK_ADDRESS'] + " -w " + config['VPN_GATEWAY_ADDRESS'], logfile, metalog)				
		metalog = " ************** Azure Network Local-Network List ******************* \t"
		retryLoad1("azure network local-network list ",logfile,metalog)	
		metalog = " ************** Azure Network Local-Network Show ******************* \t"
		retryLoad1("azure network local-network show " + " -n " + config['NETWORK_LOCALNETWORK_NAME'], logfile, metalog)
		metalog = "************** Azure Network Vnet Local-Network Add ******************* \t"
		retryLoad1("azure network vnet local-network add " + config['NETWORK_VPN_VNET_NAME'] + " " + config['NETWORK_LOCALNETWORK_NAME'], logfile, metalog)
		
		# NETWORK Vpn Gateway Create Show Shared-Key Set Reset Connection List Vpn-Device List Diagnostics Start Stop & Get Delete
		metalog = "************** Azure Network Vpn-Gateway Create ******************* \t"
		retryLoad1("azure network vpn-gateway create " + " -n " +config['NETWORK_VPN_VNET_NAME'] + " -t " +config['VPN_GAETWAY_TYPE'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway Show ******************* \t"
		retryLoad1("azure network vpn-gateway show " + " -n " +config['NETWORK_VPN_VNET_NAME'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway shared-key set ******************* \t"
		retryLoad1("azure network vpn-gateway shared-key set " + " -n " +config['NETWORK_VPN_VNET_NAME']+ " -t " +config['NETWORK_LOCALNETWORK_NAME']+ " -k " +config['VPN_KEYVALUE'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway shared-key reset ******************* \t"
		retryLoad1("azure network vpn-gateway shared-key reset " + " -n " +config['NETWORK_VPN_VNET_NAME']+ " -t " +config['NETWORK_LOCALNETWORK_NAME']+ " -l " +config['VPN_KEYLENGHT'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway Connection List ******************* \t"
		retryLoad1("azure network vpn-gateway connection list " + " -n " +config['NETWORK_VPN_VNET_NAME'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Device List ******************* \t"
		retryLoad1("azure network vpn-gateway device list ", logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway Diagnostics Start ******************* \t"
		retryLoad1("azure network vpn-gateway diagnostics start " +config['NETWORK_VPN_VNET_NAME']+ " -d " +config['VPN_DURATION']+ " -a " +config['VPN_STORAGE']+ " -k " +config['VPN_STORAGE_KEY']+ " -c " +config['VPN_CONTAINER'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway Diagnostics Stop ******************* \t"
		retryLoad1("azure network vpn-gateway diagnostics stop " +config['NETWORK_VPN_VNET_NAME'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway Diagnostics Get ******************* \t"
		retryLoad1("azure network vpn-gateway diagnostics get " +config['NETWORK_VPN_VNET_NAME'], logfile, metalog)
		metalog = "************** Azure Network Vpn-Gateway Delete ******************* \t"
		retryLoad1("azure network vpn-gateway delete " + " -n " +config['NETWORK_VPN_VNET_NAME'] + " -q " , logfile, metalog)
		
		# NETWORK LOCAL-NETWORK Remove 
		metalog = "************** Azure Network Vnet Local-Network Remove ******************* \t"
		retryLoad1("azure network vnet local-network remove " + config['NETWORK_VPN_VNET_NAME'] + " " + config['NETWORK_LOCALNETWORK_NAME'], logfile, metalog)
		# NETWORK Vnet for Gateway delete
		metalog = " ************** Azure Network Vnet for Gateway delete ******************* \t"
		retryLoad1("azure network vnet delete "+config['NETWORK_VPN_VNET_NAME'] + " --quiet ",logfile,metalog)
		# NETWORK LOCAL-NETWORK Set Delete
		metalog = " ************** Azure Network Local-Network Set ******************* \t"
		retryLoad1("azure network local-network set " + config['NETWORK_LOCALNETWORK_NAME'] + " -a " + config['LOCAL_NETWORK_ADDRESS_SET'] + " -w " + config['VPN_GATEWAY_ADDRESS_SET'], logfile, metalog)
		metalog = " ************** Azure Network Local-Network Delete ******************* \t"
		retryLoad1("azure network local-network delete " + config['NETWORK_LOCALNETWORK_NAME'] + " -q " ,logfile,metalog)
		
		#Gateway Command - End Here
		# ASM NETWORK NEW COMMANDS ENDS
						
		metalog = "************** Azure Network Delete ******************* \t"
		retryLoad1("azure network vnet delete "+config['NETWORK_NAME'] + " --quiet ",logfile,metalog)
		metalog = "************** Azure Affinity Group Delete ******************* \t"
		retryLoad1("azure account affinity-group delete "+config['AFFINITY_GRP_NAME'] + " --quiet",logfile,metalog)
		
		metalog = "************** Azure Account Clear ******************* \t"
		retryLoad1("azure account clear --quiet",logfile,metalog)
		
		
	if(config['GLOBAL_FLAG'] == "0"):
		logfile.write("************** Test Summary Report **************** \n")
		metalog = "************** NPM CACHE CLEAR **************** \t" 
		execute_command_with_flag("npm cache clear",logfile,config['NPM_CLEAR_FLAG'],metalog)	
		metalog = "************** NPM AZURE INSTALL **************** \t" 
		execute_command_with_flag("npm install azure -g",logfile,config['NPM_INSTALL_FLAG'],metalog)		
		metalog = "************** Azure Help Command **************** \t"
		execute_command_with_flag("azure",logfile,config['AZURE_HELP_FLAG'],metalog)

		if(config['AD_Login'] == "0"):
		 metalog = "************** Azure Login **************** \t" 
		 execute_command_with_flag("azure login -u "+ config['LOGINUSER'] + " -p " + config['LOGINPASSWORD'] + " --quiet",logfile,config['AZURE_LOGIN_FLAG'],metalog)
		else:
		 metalog = "************** Azure Account Download ******************* \t"
		 execute_command_with_flag("azure account download ",logfile,config['ACCOUNT_DWNLD_FLAG'],metalog)		
		 metalog = "************* Azure Account Import ******************* \t"
		 execute_command_with_flag("azure account import "+ config['PUBLISHSETTINGS_FILE'],logfile,config['ACCOUNT_IMPRT_FLAG'],metalog)	
		metalog = "************** Azure Account List ******************* \t"
		execute_command_with_flag("azure account list ",logfile,config['ACCOUNT_LIST_FLAG'],metalog)		
		metalog = "************** Azure Account Set ******************* \t"
		execute_command_with_flag("azure account set "+ config['SUBSCRIPTION_ID'],logfile,config['ACCOUNT_SET_FLAG'],metalog)
		
		

		metalog = "************** Azure Service List ******************* \t"
		execute_command_with_flag("azure service list",logfile,config['AZURE_SERV_LIST_FLAG'],metalog)

		metalog = " ************** Azure network reserved-ip list ******************* \t"
		execute_command_with_flag("azure network reserved-ip list",logfile,config['RESERVED_IP_LIST_FLAG'],metalog)
		metalog = " ************** Azure network reserved-ip create ******************* \t"
		execute_command_with_flag("azure network reserved-ip create " + config['RIPNAME'] + " " + config['LOCATION'], logfile,config['RESERVED_IP_CREATE_FLAG'],metalog)
		metalog = " ************** Azure  network reserved-ip show ******************* \t"
		execute_command_with_flag("azure network reserved-ip show " + config['RIPNAME'],logfile,config['RESERVED_IP_SHOW_FLAG'],metalog)

		metalog = "************** Azure Account Affinity Group List ******************* \t"
		execute_command_with_flag("azure account affinity-group list",logfile,config['ACCOUNT_AFF_GRP_FLAG'],metalog)		
		metalog = "************** Azure Account Affinity Group Create ******************* \t"		
		execute_command_with_flag("azure account affinity-group create -l "+config['LOCATION']+ " -e "+config['AFFINITY_GRP_LABEL']+ " -d "+config['AFFINITY_GRP_DESC']+ " " +config['AFFINITY_GRP_NAME'] ,logfile,config['ACCOUNT_AFF_GRP_CREATE_FLAG'],metalog)		
		metalog = "************** Azure Account Affinity Group Show ******************* \t"		
		execute_command_with_flag("azure account affinity-group show " +config['AFFINITY_GRP_NAME'] ,logfile,config['ACCOUNT_AFF_GRP_SHOW_FLAG'],metalog)		

		metalog = "************** Azure Account Storage List ******************* \t"
		execute_command_with_flag("azure storage account list",logfile,config['ACCOUNT_STORAGE_LIST_FLAG'],metalog)		
		metalog = "************** Azure Location List ******************* \t"
		execute_command_with_flag("azure vm location list",logfile,config['AZURE_LOC_LIST_FLAG'],metalog)
		metalog = "************** Azure Config List ******************* \t"
		execute_command_with_flag("azure config list",logfile,config['ACCOUNT_CONFIG_LIST_FLAG'],metalog)		
		metalog = "************** Azure Config Set ******************* \t"
		execute_command_with_flag("azure config set "+ config['CONFIG_KEY'] + " " + config['CONFIG_VALUE'],logfile,config['ACCOUNT_CONFIG_SET_FLAG'],metalog)

		metalog = "************** Azure VM Disk List ******************* \t"
		execute_command_with_flag("azure vm disk list",logfile,config['DISK_LIST_FLAG'],metalog)		
		metalog = "************** Azure VM Disk Create ******************* \t"
		execute_command_with_flag("azure vm disk create -a " + config['AFFINITY_GRP_NAME'] + " -u "+config['DISK_IMAGE_BLOB_URL']+" -l " +config['LOCATION']+" -o "+'''"LINUX"''' + " -p 2 -m -f -e " + config['VM_DISK_LABEL'] + " -d "+ config['VM_DISK_DESC'] + " " + config['VM_DISK_IMAGE_NAME']+ " "+config['VM_DISK_SOURCE_PATH'],logfile,config['DISK_CREATE_FLAG'],metalog)
		
		metalog = "************** Azure VM Disk Show ******************* \t"
		execute_command_with_flag("azure vm disk show "+config['VM_DISK_IMAGE_NAME'],logfile,config['DISK_SHOW_FLAG'],metalog)

		metalog = "************** Azure VM Image List ******************* \t"
		execute_command_with_flag("azure vm image list",logfile,config['IMAGE_LIST_FLAG'],metalog)		
		metalog = "************** Azure VM Image Create ******************* \t"
		execute_command_with_flag("azure vm image create -a " + config['AFFINITY_GRP_NAME'] + " -u "+config['IMAGE_BLOB_URL']+" -l " +config['LOCATION']+" -o "+'''"LINUX"'''+ " -p 2 -m -f -e " + config['VM_IMAGE_LABEL'] + " -d "+ config['VM_IMAGE_DESC'] + " " + config['VM_IMAGE_NAME']+ " " +config['DISK_IMAGE_BLOB_URL'],logfile,config['IMAGE_CREATE_FLAG'],metalog)
		metalog = "************** Azure VM Image Show ******************* \t"
		execute_command_with_flag("azure vm image show "+config['VM_IMAGE_NAME'],logfile,config['IMAGE_SHOW_FLAG'],metalog)

		metalog = "************** Azure VM List ******************* \t"
		execute_command_with_flag("azure vm list",logfile,config['VM_LIST_FLAG'],metalog)		
		metalog = "************** Azure VM Create ******************* \t"
		execute_command_with_flag("azure vm create "+config['VM_NAME']+" "+config['IMAGE_NAME']+" "+config['USER_NAME']+" "+config['PASSWORD']+" -l " +config['LOCATION']+" -e ",logfile,config['VM_CREATE_FLAG'],metalog)
		
		metalog = "************** Azure Vm Extension list ************\t"
		execute_command_with_flag("azure vm extension list",logfile,config['VM_EXTENSION_LIST_FLAG'],metalog)		
		metalog = "************** Azure Vm Extension Get ************\t"
		execute_command_with_flag("azure vm extension get "+config['VM_NAME'],logfile,config['VM_EXTENSION_GET_FLAG'],metalog)
		metalog = "************** Azure Vm Extension Set ************\t"
		execute_command_with_flag("azure vm extension set "+config['VM_NAME'] +" "+config['EXTN_NAME']+" "+config['EXTN_PUB_NAME']+" "+config['EXTN_VERSION'] +" "+" -C "+config['EXTN_FILE'],logfile,config['VM_EXTENSION_SET_FLAG'],metalog)
		
		metalog = "************** Azure Disk List with VMName ************\t"
		execute_command_with_flag("azure vm disk list "+config['VM_NAME'],logfile,config['DISK_LIST_VM_NAME_FLAG'],metalog)
        
		metalog = "************** PIP Commands ****************************** \t"
		metalog = "************** VM Create with PIP ****************************** \t"
		execute_command_with_flag("azure vm create "+ " -i " + config['PUBLICIPNAME'] + config['VM_WIN_PIP'] + config['WIN_IMAGE_NAME'] + " testuser " + config['PASSWORD'] + " -l " +config['LOCATION'],logfile,config['PIP_VM_CREATE_FLAG'],metalog)

		metalog = "************** PIP List ****************************** \t"
		execute_command_with_flag("azure vm public-ip list " + config['VM_WIN_PIP'],logfile,config['PIP_VM_LIST_FLAG'],metalog)
		
		metalog = "************** PIP REMOVE ****************************** \t"
		execute_command_with_flag("azure vm public-ip delete "+config['VM_WIN_PIP'] + config['PUBLICIPNAME'] + " -b --quiet ",logfile,config['PIP_VM_REMOVE_FLAG'],metalog)
		
		metalog = "************** PIP SET ****************************** \t"
		execute_command_with_flag("azure vm public-ip set "+config['VM_WIN_PIP'] +" " +config['PUBLICIPSET'],logfile,config['PIP_VM_SET_FLAG'],metalog)
		 
		metalog = "************** PIP VM DELETE ****************************** \t" 
		execute_command_with_flag("azure vm delete "+ config['VM_WIN_PIP'] + " -b -q",logfile,config['PIP_VM_DELETE_FLAG'],metalog)
		
		metalog = "************** Azure Windows VM Create ******************* \t"
		execute_command_with_flag("azure vm create "+config['VM_WIN_ACL']+" "+config['WIN_IMAGE_NAME']+" testuser "+config['PASSWORD']+" -l " +config['LOCATION'],logfile,config['ACL_VM_CREATE_FLAG'],metalog)

		metalog = "************** ACL Create RULE ****************************** \t"
		execute_command_with_flag("azure vm endpoint acl-rule create "+ config['VM_WIN_ACL'] + " " + config['ENDPOINT'] + " " + config['ORDER'] + " " + config['ACTION'] + " " + config['REMOTESUBNET'],logfile,config['ACL_RULE_CREATE_FLAG'],metalog)
		
		metalog = "************** ACL List****************************** \t" 
		execute_command_with_flag("azure vm endpoint acl-rule list "+ config['VM_WIN_ACL'] + " " + config['ENDPOINT'],logfile,config['ACL_RULE_LIST_FLAG'],metalog)
		
		metalog = "************** ACL Rule Delete****************************** \t" 
		execute_command_with_flag("azure vm endpoint acl-rule delete "+ config['VM_WIN_ACL'] + " " + config['ENDPOINT']+ " " + config['ORDER'],logfile,config['ACL_RULE_DELETE_FLAG'],metalog)
		
		metalog = "************** ACL VM DELETE ****************************** \t" 
		execute_command_with_flag("azure vm delete "+ config['VM_WIN_ACL'] + " -b -q",logfile,config['PIP_VM_DELETE_FLAG'],metalog)
		
		metalog = "************** Azure Windows VM Create ******************* \t"
		execute_command_with_flag("azure vm create "+config['VM_WIN_NAME']+" "+config['WIN_IMAGE_NAME']+" testuser "+config['PASSWORD']+" -l " +config['LOCATION'],logfile,config['VM_CREATE_FLAG'],metalog)
		metalog = "************** Azure VM Show ******************* \t"
		execute_command_with_flag("azure vm show "+config['VM_NAME'],logfile,config['VM__SHOW_FLAG'],metalog)
		metalog = "************** Azure VM Start ******************* \t"
		execute_command_with_flag("azure vm start "+config['VM_NAME'],logfile,config['VM_START_FLAG'],metalog)

		metalog = "************** Azure VM Export ******************* \t"
		execute_command_with_flag("azure vm export "+config['VM_NAME']+ " " + config['FILE_PATH'],logfile,config['VM_EXPORT_FLAG'],metalog)

		metalog = "************** Azure VM End Point Create ******************* \t"
		execute_command_with_flag("azure vm endpoint create "+config['VM_NAME']+" 21 23 ",logfile,config['VM_ENDPNT_CREATE_FLAG'],metalog)
		metalog = "************** Azure VM End Point Create-Multiple ******************* \t"
		execute_command_with_flag("azure vm endpoint create-multiple "+config['VM_NAME']+" "+config['ONLYPP_PUBLICPORT'] + ","+config['PPANDLP_PUBLICPORT'] +":"+config['PPANDLP_LOCALPORT']+","+config['PP_LPANDLBSET_PUBLICPORT'] +":"+config['PP_LPANDLBSET_LOCALPORT']+":"+config['PP_LPANDLBSET_PROTOCOL']+":"+config['PP_LPANDLBSET_ENABLEDIRECTSERVERRETURN']+":"+config['PP_LPANDLBSET_LOADBALANCERSETNAME']+","+config['PP_LP_LBSETANDPROB_PUBLICPORT'] +":"+config['PP_LP_LBSETANDPROB_LOCALPORT']+":"+config['PP_LP_LBSETANDPROB_PROTOCOL']+":"+config['PP_LP_LBSETANDPROB_ENABLEDIRECTSERVERRETURN']+":"+config['PP_LP_LBSETANDPROB_LOADBALANCERSETNAME']+":"+config['PP_LP_LBSETANDPROB_PROBPROTOCOL']+":"+config['PP_LP_LBSETANDPROB_PROBPORT'],logfile,config['VM_ENDPNT_CREATE_MUL_FLAG'],metalog)
		metalog = "************** Azure VM End Point show ******************* \t"
		execute_command_with_flag("azure vm endpoint show "+config['VM_NAME'],logfile,config['VM_ENDPNT_SHOW_FLAG'],metalog)
		metalog = "************** Azure VM Endpoint List ******************* \t"
		execute_command_with_flag("azure vm endpoint list "+config['VM_NAME'],logfile,config['VM_ENDPNT_LIST_FLAG'],metalog)
		metalog = "************** Azure VM Endpoint Update ******************* \t"
		execute_command_with_flag("azure vm endpoint update "+config['VM_NAME']+ " -n tcp-5555-5565 +" "+ -l 4440 +" "+ -t 4441 +" " +",logfile,config['VM_ENDPNT_UPD_FLAG'],metalog)
		metalog = "************** Azure VM Endpoint Delete ******************* \t"
		execute_command_with_flag("azure vm endpoint delete "+config['VM_NAME']+ " testpoint ",logfile,config['VM_ENDPNT_DEL_FLAG'],metalog)

		metalog = "************** Azure VM Disk Attach ******************* \t"
		execute_command_with_flag("azure vm disk attach "+config['VM_NAME']+" "+config['VM_DISK_IMAGE_NAME'],logfile,config['DISK_ATTCH_FLAG'],metalog)
		metalog = "************** Azure VM Disk Attach New ******************* \t"
		execute_command_with_flag("azure vm disk attach-new "+config['VM_NAME']+" 177 "+config['VM_DISK_ATTACH_BLOB_URL'],logfile,config['DISK_ATTCH_NEW_FLAG'],metalog)
		metalog = "************** Azure VM Disk Detach ******************* \t"
		execute_command_with_flag("azure vm disk detach "+config['VM_NAME']+" 1",logfile,config['DISK_DETACH_FLAG'],metalog)
		execute_command_with_flag("azure vm disk detach "+config['VM_NAME']+" 0",logfile,config['DISK_DETACH_FLAG'],metalog)

		metalog = "************** Azure VM Restart ******************* \t"
		execute_command_with_flag("azure vm restart "+config['VM_NAME'],logfile,config['VM_RESTART_FLAG'],metalog)
		metalog = "************** Azure VM ShutDown ******************* \t"
		execute_command_with_flag("azure vm shutdown "+config['VM_NAME'],logfile,config['VM_SHUTDWN_FLAG'],metalog)
		metalog = "************** Azure VM Capture ******************* \t"
		execute_command_with_flag("azure vm capture "+config['VM_NAME']+" "+config['TARGET_IMG_NAME']+ " -t ",logfile,config['VM_CAPTURE_FLAG'],metalog)

		metalog = "************** Azure Network List ******************* \t"
		execute_command_with_flag("azure network vnet list",logfile,config['NETWORK_CREATE_FLAG'],metalog)
		metalog = "************** Azure Network Create ******************* \t"
		execute_command_with_flag("azure network vnet create "+config['NETWORK_NAME'] + " -a "+config['AFFINITY_GRP_NAME'],logfile,config['NETWORK_CREATE_FLAG'],metalog)
		metalog = "************** Azure Network Show ******************* \t"
		execute_command_with_flag("azure network vnet show "+config['NETWORK_NAME'],logfile,config['NETWORK_CREATE_FLAG'],metalog)
		metalog = "************** Azure VM Create_VNet ******************* \t"
		execute_command_with_flag("azure vm create " + config['VM_VNET_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser PassW0rd$ --virtual-network-name " + config['NETWORK_NAME'] + " -n " + config['VM_VNET_LABEL'] + " --affinity-group "+config['AFFINITY_GRP_NAME'],logfile,config['VM_VNET_CREATE_FLAG'],metalog)
		metalog = "************** Azure VM Create_Size ******************* \t"
		execute_command_with_flag("azure vm create " + config['VM_SIZE_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser PassW0rd$ -z Medium -c -l "+config['LOCATION'],logfile,config['VM_SIZE_CREATE_FLAG'],metalog)
		metalog = "************** Azure create VM_CUSTOM_DATA ******************* \t"
		execute_command_with_flag("azure vm create -d " + config['CUSTOM_DATA_FILE'] + " " + config['VM_CUSTOMDATA_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser PassW0rd$ -l "+config['LOCATION'],logfile,config['VM_CUSTOMDATA_CREATE_FLAG'],metalog)
		
		metalog = "************** Azure static-ip VM Create******************* \t"
		execute_command_with_flag("azure vm create "+config['STATICIP_VM_NAME']+" "+config['IMAGE_NAME']+" communityUser PassW0rd$ "+" --virtual-network-name "+config['NETWORK_NAME'] + " " + "--affinity-group" +  " " + config['AFFINITY_GRP_NAME'] + " " + " --static-ip "+ " " + config['STATIC_IP_TO_CREATE'],logfile,config['VM_STATICIP_CREATE_FLAG'],metalog)
		metalog = "************** Azure static-ip Set ******************* \t"
		execute_command_with_flag("azure vm static-ip set "+ config['STATICIP_VM_NAME'] +" "+ config['STATIC_IP_TO_SET'],logfile,config['VM_STATICIP_CREATE_FLAG'],metalog)
		metalog = "************** Azure static-ip Check ******************* \t"
		execute_command_with_flag("azure network vnet static-ip check "+config['NETWORK_NAME'] + " " + config['STATIC_IP_TO_SET'],logfile,config['VM_STATICIP_CREATE_FLAG'],metalog)
		metalog = "************** Azure static-ip Remove ******************* \t"
		execute_command_with_flag("azure vm static-ip remove "+config['STATICIP_VM_NAME'],logfile,config['VM_STATICIP_CREATE_FLAG'],metalog)
		metalog = "************** Azure static-ip VM Restart ******************* \t"
		execute_command_with_flag("azure vm restart "+config['STATICIP_VM_NAME'],logfile,config['VM_STATICIP_CREATE_FLAG'],metalog)
		metalog = "************** Azure static-ip VM Delete ******************* \t"
 		execute_command_with_flag("azure vm delete "+config['STATICIP_VM_NAME'] + " -b --quiet ",logfile,config["VM_STATICIP_CREATE_FLAG"],metalog)
		metalog = "************** Azure static-ip Docker VM Create******************* \t"
		execute_command_with_flag("azure vm docker create "+config['DOCKER_STATIC_VM_NAME']+" "+config['VM_DOCKER_IMG_NAME']+" communityUser PassW0rd$ "+" --virtual-network-name "+config['NETWORK_NAME'] + " " + "--affinity-group" +  " " + config['AFFINITY_GRP_NAME'] + " " + " --static-ip "+ " " + config['STATIC_IP_TO_CREATE'] + " " + config['CERT_FILE'] + " " + config['VM_DOCKER_PORT'],logfile,config['VM_STATICIP_CREATE_FLAG'],metalog)
		metalog = "************** Azure static-ip Docker VM Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['DOCKER_STATIC_VM_NAME'] + " -b --quiet ",logfile,config['VM_STATICIP_CREATE_FLAG'],metalog)
		
		metalog = "************** Azure VM_VNet Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_VNET_LABEL'] + " -b --quiet ",logfile,config['VM_VNET_DEL_FLAG'],metalog)
		metalog = "************** Azure VM_SIZE Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_SIZE_NAME'] + " -b --quiet ",logfile,config['VM_SIZE_DEL_FLAG'],metalog)
		metalog = " ************** Azure VM_CUSTOM_DATA Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_CUSTOMDATA_NAME'] + " -b --quiet ",logfile,config['VM_CUSTOMDATA_DEL_FLAG'],metalog)

		metalog = "************** Azure Service Delete ******************* \t"
		execute_command_with_flag("azure service delete "+config['VM_NAME'] + " --quiet ",logfile,config['AZURE_SERVICE_DEL_FLAG'],metalog)
		metalog = "************** Azure VM Create-from ******************* \t"
		execute_command_with_flag("azure vm create-from "+config['VM_NAME']+" "+config['FILE_PATH'] + " -l " +config['LOCATION'],logfile,config['VM_CREATE_FROM_FLAG'],metalog)
		metalog = "************** Azure VM Community Image Create ******************* \t"
		execute_command_with_flag("azure vm create " + config['VM_COMM_NAME'] + " -o "+config['VM_COMM_IMAGE_NAME']+" -l "+config['LOCATION']+" communityUser PassW0rd$",logfile,config['VM_COMM_IMG_CREATE_FLAG'],metalog)
		metalog = "************** Azure VM SSHCert Create ******************* \t"
		execute_command_with_flag("azure vm create " + config['VM_SSH_NAME'] + " " + config['VM_VNET_IMAGE_NAME'] + " communityUser --ssh-cert "+config['CERT_FILE'] + " -e --no-ssh-password -r -l "+config['LOCATION'],logfile,config['VM_SSH_FLAG'],metalog)
		metalog = "************** Azure VM Comm Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_COMM_NAME'] + " -b --quiet",logfile,config['VM_COMM_DEL_FLAG'],metalog)
		metalog = "************** Azure VM SSHCert Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_SSH_NAME'] + " -b --quiet ",logfile,config['VM_SSH_DEL_FLAG'],metalog)

		metalog = "************** Azure VM reserved-ip Create ******************* \t"
		execute_command_with_flag("azure vm create " + config['VM_RIP_NAME'] + " "+config['IMAGE_NAME']+" "+config['USER_NAME']+" "+config['PASSWORD']+" -l " +config['LOCATION']+" -R " + config['RIPNAME'] + " --ssh",logfile,config['VM_RIP_CREATE_FLAG'],metalog)
		metalog = "************** Azure VM reserved-ip Create ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_RIP_NAME'] + " -b --quiet ",logfile,config['VM_RIP_DEL_FLAG'],metalog)
		
		# NETWORK NSG Create Set List Show
		metalog = " ************** Azure Network Nsg Create ******************* \t"
		execute_command_with_flag("azure network nsg create " + config['NETWORK_NSG_NAME'] + " -l " + config['LOCATION'] + " -b " + config['NSG_LABEL'], logfile, config['NETWORKNSG_CREATE_FLAG'], metalog)
		metalog = "************** Azure Network Nsg List ******************* \t"
		execute_command_with_flag("azure network nsg list ", logfile, config['NETWORKNSG_LIST_FLAG'], metalog)
		metalog = "************** Azure Network Nsg Show ******************* \t"
		execute_command_with_flag("azure network nsg show " + config['NETWORK_NSG_NAME'], logfile, config['NETWORKNSG_SHOW_FLAG'], metalog)
		
		# NETWORK NSG RULE Create Set List Show Delete
		metalog = " ************** Azure Network Nsg Rule Create ******************* \t"
		execute_command_with_flag("azure network nsg rule create " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'] + " -p " + config['PROTOCOL'] + " -f " + config['SOURCE_ADDRESS_PREFIX'] + " -o " + config['SOURCE_PORT_RANGE'] + " -e " + config['DESTINATION_ADDRESS_PREFIX'] + " -u " + config['DESTINATION_PORT_RANGE'] + " -c " + config['ACTION'] + " -y " + config['PRIORITY'] + " -r " + config['TYPE'], logfile, config['NETWORKNSGRULE_CREATE_FLAG'], metalog)
		metalog = " ************** Azure Network Nsg Rule Set ******************* \t"
		execute_command_with_flag("azure network nsg rule set " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'] + " -p " + config['PROTOCOL_SET'] + " -f " + config['SOURCE_ADDRESS_PREFIX_SET'] + " -o " + config['SOURCE_PORT_RANGE_SET'] + " -e " + config['DESTINATION_ADDRESS_PREFIX_SET'] + " -u " + config['DESTINATION_PORT_RANGE_SET'] + " -c " + config['ACTION_SET'] + " -y " + config['PRIORITY_SET'] + " -r " + config['TYPE_SET'], logfile, config['NETWORKNSGRULE_SET_FLAG'], metalog)
		metalog = "************** Azure Network Nsg Rule List ******************* \t"
		execute_command_with_flag("azure network nsg rule list " + config['NETWORK_NSG_NAME'], logfile, config['NETWORKNSGRULE_LIST_FLAG'], metalog)
		metalog = "************** Azure Network Nsg Rule Show ******************* \t"
		execute_command_with_flag("azure network nsg rule show " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'], logfile, config['NETWORKNSGRULE_SHOW_FLAG'], metalog)
		metalog = "************** Azure Network Nsg Rule Delete ******************* \t"
		execute_command_with_flag("azure network nsg rule delete " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NSG_RULE_NAME'] + " --quiet ", logfile, config['NETWORKNSGRULE_DELETE_FLAG'], metalog)
		 
		 # NETWORK VNET SUBNET Create Set List Show
		metalog = " ************** Azure Network Vnet Subnet Create ******************* \t"
		execute_command_with_flag("azure network vnet subnet create " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -a " + config['ADDRESS_PREFIXES'] + " -o " + config['NETWORK_NSG_NAME'], logfile, config['NETWORKVNETSUBNET_CREATE_FLAG'], metalog)
		metalog = " ************** Azure Network Vnet Subnet Set ******************* \t"
		execute_command_with_flag("azure network vnet subnet set " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -a " + config['ADDRESS_PREFIXES_SET'], logfile, config['NETWORKVNETSUBNET_SET_FLAG'], metalog)
		metalog = "************** Azure Network Vnet Subnet List ******************* \t"
		execute_command_with_flag("azure network vnet subnet list " + config['NETWORK_NAME'], logfile, config['NETWORKVNETSUBNET_LIST_FLAG'], metalog)
		metalog = "************** Azure Network Vnet Subnet Show ******************* \t"
		execute_command_with_flag("azure network vnet subnet show " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'], logfile, config['NETWORKVNETSUBNET_SHOW_FLAG'], metalog)
		
		# NETWORK NSG SUBNET Add Remove
		metalog = "************** Azure Network Nsg Subnet Add ******************* \t"
		execute_command_with_flag("azure network nsg subnet add " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'], logfile, config['NETWORKNSGSUBNET_ADD_FLAG'], metalog)
		metalog = "************** Azure Network Nsg Subnet Remove ******************* \t"
		execute_command_with_flag("azure network nsg subnet remove " + config['NETWORK_NSG_NAME'] + " " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -q ", logfile, config['NETWORKNSGSUBNET_REMOVE_FLAG'], metalog)
		
		# NETWORK ROUTE-TABLE Create List Show
		metalog = " ************** Azure Network Route-Table Create ******************* \t"
		execute_command_with_flag("azure network route-table create " + config['NETWORK_ROUTE_TABLE'] + " " + config['LOCATION'] + " -b " + config['ROUTE_LABEL'], logfile, config['NETWORKROUTETABLE_CREATE_FLAG'], metalog)
		metalog = "************** Azure Network Route-Table List ******************* \t"
		execute_command_with_flag("azure network route-table list ", logfile, config['NETWORKROUTETABLE_LIST_FLAG'], metalog)
		metalog = "************** Azure Network Route-Table Show ******************* \t"
		execute_command_with_flag("azure network route-table show " + config['NETWORK_ROUTE_TABLE'], logfile, config['NETWORKROUTETABLE_SHOW_FLAG'], metalog)
		
		# NETWORK ROUTE-TABLE ROUTE Set Delete
		metalog = "************** Azure Network Route-Table Route Set ******************* \t"
		execute_command_with_flag("azure network route-table route set " + config['NETWORK_ROUTE_TABLE'] + " " + config['NETWORK_ROUTE'] + " " + config['ROUTE_ADDRESS_PREFIXES'] + " " + config['NEXT_HOP_TYPE'], logfile, config['NETWORKROUTETABLE_ROUTE_SET_FLAG'], metalog)
		metalog = "************** Azure Network Route-Table Route Delete ******************* \t"
		execute_command_with_flag("azure network route-table route delete " + config['NETWORK_ROUTE_TABLE'] + " " + config['NETWORK_ROUTE'] + " -q ", logfile, config['NETWORKROUTETABLE_ROUTE_DELETE_FLAG'], metalog)
		
		# NETWORK SUBNET ROUTE-TABLE Add Show Delete
		metalog = " ************** Azure Network Subnet Route-Table Add ******************* \t"
		execute_command_with_flag("azure network vnet subnet route-table add " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -r " + config['NETWORK_ROUTE_TABLE'], logfile, config['NETWORKSUBNET_ROUTETABLE_ADD_FLAG'], metalog)
		metalog = " ************** Azure Network Subnet Route-Table Show ******************* \t"
		execute_command_with_flag("azure network vnet subnet route-table show " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -d " + config['NETWORK_ROUTE_TABLE'], logfile, config['NETWORKSUBNET_ROUTETABLE_SHOW_FLAG'], metalog)
		metalog = "************** Azure Network Subnet Route-Table Delete ******************* \t"
		execute_command_with_flag("azure network vnet subnet route-table delete " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " -r " + config['NETWORK_ROUTE_TABLE'] + " -q ", logfile, config['NETWORKSUBNET_ROUTETABLE_DELETE_FLAG'], metalog)
		
		# NETWORK Traffic-Manager Profile Create Set List Show Enable Disable Delete
		metalog = " ************** Azure Network Traffic-Manager Profile Create ******************* \t"
		execute_command_with_flag("azure network traffic-manager profile create " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'] + " -d " + config['DOMAIN_NAME'] + " -m " + config['lOADBALANCING_METHOD'] + " -o " + config['MONITOR_PORT'] + " -p " + config['MONITOR_PROTOCOL'] + " -r " + config['MONITOR_RELATIVE_PATH'] + " -t " + config['TTL'], logfile, config['TRAFFICMANAGER_PROFILE_CREATE_FLAG'], metalog)		
		metalog = " ************** Azure Network Traffic-Manager Profile Set ******************* \t"
		execute_command_with_flag("azure network traffic-manager profile set " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'] + " -m " + config['lOADBALANCING_METHOD_SET'] + " -o " + config['MONITOR_PORT_SET'] + " -p " + config['MONITOR_PROTOCOL_SET'] + " -r " + config['MONITOR_RELATIVE_PATH_SET'] + " -t " + config['TTL_SET'], logfile, config['TRAFFICMANAGER_PROFILE_SET_FLAG'], metalog)		
		metalog = " ************** Azure Network Traffic-Manager Profile List ******************* \t"
		execute_command_with_flag("azure network traffic-manager profile list ",logfile, config['TRAFFICMANAGER_PROFILE_LIST_FLAG'], metalog)	
		metalog = " ************** Azure Network Traffic-Manager Profile Show ******************* \t"
		execute_command_with_flag("azure network traffic-manager profile show " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'], logfile, config['TRAFFICMANAGER_PROFILE_SHOW_FLAG'], metalog)
		metalog = " ************** Azure Network Traffic-Manager Profile Enable ******************* \t"
		execute_command_with_flag("azure network traffic-manager profile enable " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'], logfile, config['TRAFFICMANAGER_PROFILE_ENABLE_FLAG'], metalog)
		metalog = " ************** Azure Network Traffic-Manager Profile Disable ******************* \t"
		execute_command_with_flag("azure network traffic-manager profile disable " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'], logfile, config['TRAFFICMANAGER_PROFILE_DISABLE_FLAG'], metalog)
		metalog = " ************** Azure Network Traffic-Manager Profile Delete ******************* \t"
		execute_command_with_flag("azure network traffic-manager profile delete " + config['NETWORK_TRAFFICMANAGER_PROFILE_NAME'] + " -q " ,logfile, config['TRAFFICMANAGER_PROFILE_DELETE_FLAG'], metalog)
		
		# NETWORK Application-Gateway Create Set List Show Start Stop
		metalog = " ************** Azure Network Application-Gateway Create ******************* \t"
		execute_command_with_flag("azure network application-gateway create " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -e " + config['NETWORK_NAME'] + " -t " + config['NETWORK_SUBNET_NAME'] + " -c " + config['INSTANCE_COUNT'] + " -z " + config['GATEWAY_SIZE'] + " -d " + config['APPGATEWAY_DESCRIPTION'], logfile, config['APPLICATIONGATEWAY_CREATE_FLAG'], metalog)		
		metalog = " ************** Azure Network Application-Gateway Set ******************* \t"
		execute_command_with_flag("azure network application-gateway set " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -e " + config['NETWORK_NAME'] + " -t " + config['NETWORK_SUBNET_NAME'] + " -c " + config['INSTANCE_COUNT_SET'] + " -z " + config['GATEWAY_SIZE_SET'] + " -d " + config['APPGATEWAY_DESCRIPTION_SET'], logfile, config['APPLICATIONGATEWAY_SET_FLAG'], metalog)		
		metalog = " ************** Azure Network Application-Gateway List ******************* \t"
		execute_command_with_flag("azure network application-gateway list ", logfile, config['APPLICATIONGATEWAY_LIST_FLAG'], metalog)	
		metalog = " ************** Azure Network Application-Gateway Show ******************* \t"
		execute_command_with_flag("azure network application-gateway show " + config['NETWORK_APPLICATION_GATEWAY_NAME'], logfile, config['APPLICATIONGATEWAY_SHOW_FLAG'], metalog)
		metalog = " ************** Azure Network Application-Gateway Start ******************* \t"
		execute_command_with_flag("azure network application-gateway start " + config['NETWORK_APPLICATION_GATEWAY_NAME'], logfile, config['APPLICATIONGATEWAY_START_FLAG'], metalog)
		metalog = " ************** Azure Network Application-Gateway Stop ******************* \t"
		execute_command_with_flag("azure network application-gateway stop " + config['NETWORK_APPLICATION_GATEWAY_NAME'], logfile, config['APPLICATIONGATEWAY_STOP_FLAG'], metalog)
		
		# NETWORK Application-Gateway config Import, Show
		metalog = "************** Azure Network Application-Gateway Config Import ******************* \t"
		execute_command_with_flag("azure network application-gateway config import " + " -n " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -t " + config['APPGATE_EXPORT_FILE'], logfile, config['APPGATE_CONFIG_IMPORT_FLAG'], metalog)
		metalog = "************** Azure Network Application-Gateway Config Show ******************* \t"
		execute_command_with_flag("azure network application-gateway config show " + " -n " + config['NETWORK_APPLICATION_GATEWAY_NAME'], logfile, config['APPGATE_CONFIG_SHOW_FLAG'], metalog)
		
		# NETWORK Application-Gateway address-pool Add
		metalog = "************** Azure Network Application-Gateway Address-Pool Add ******************* \t"
		execute_command_with_flag("azure network application-gateway address-pool add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -r " + config['ADDRESSPOOL_IP'], logfile, config['APPGATE_ADDPOOL_ADD_FLAG'], metalog)
		
		# NETWORK Application-Gateway http-settings Add
		metalog = "************** Azure Network Application-Gateway Http-Settings Add ******************* \t"
		execute_command_with_flag("azure network application-gateway http-settings add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPSETTINGS_NAME']+str(random_no) + " -p " + config['HTTPSETTINGS_PROTOCOL'] + " -o " + config['HTTPSETTINGS_PORT'] + " -c " + config['HTTPSETTINGS_CBAFFINITY'], logfile, config['APPGATE_HTTPSETTINGS_ADD_FLAG'], metalog)
		
		# NETWORK Application-Gateway frontend-ip Add 
		metalog = "************** Azure Network Application-Gateway Frontend-IP Add ******************* \t"
		execute_command_with_flag("azure network application-gateway frontend-ip add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDIP_NAME'] + " -t " + config['FRONTENDIP_TYPE'] + " -i " + config['FRONTENDIP_STATICIP'], logfile, config['APPGATE_FRONTENDIP_ADD_FLAG'], metalog)
		
		# NETWORK Application-Gateway frontend-port Add
		metalog = "************** Azure Network Application-Gateway Frontend-Port Add ******************* \t"
		execute_command_with_flag("azure network application-gateway frontend-port add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDPORT_NAME']+str(random_no) + " -o " + config['FRNTENDPORT_PORT'], logfile, config['APPGATE_FRONTENDPORT_ADD_FLAG'], metalog)
		
		# NETWORK Application-Gateway http-listener Add 
		metalog = "************** Azure Network Application-Gateway Http-Listener Add ******************* \t"
		execute_command_with_flag("azure network application-gateway http-listener add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPLISTENER_NAME']+str(random_no) + " -i " + config['APPGATE_FRONTENDIP_NAME'] + " -p " + config['APPGATE_FRONTENDPORT_NAME']+str(random_no) + " -t " + config['HTTPLISTENER_PROTOCOL'], logfile, config['APPGATE_HTTPLISTENER_ADD_FLAG'], metalog)
		
		# NETWORK Application-Gateway lb-rule Add
		metalog = "************** Azure Network Application-Gateway LB-Rule Add ******************* \t"
		execute_command_with_flag("azure network application-gateway lb-rule add " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_LBRULE_NAME']+str(random_no) + " -i " + config['APPGATE_HTTPSETTINGS_NAME']+str(random_no) + " -l " + config['APPGATE_HTTPLISTENER_NAME']+str(random_no) + " -p " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -t " + config['LBRULE_TYPE'], logfile, config['APPGATE_LBRULE_ADD_FLAG'], metalog)
		
		# NETWORK Application-Gateway lb-rule Remove
		metalog = "************** Azure Network Application-Gateway LB-Rule Remove ******************* \t"
		execute_command_with_flag("azure network application-gateway lb-rule remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_LBRULE_NAME']+str(random_no) + " -q ", logfile, config['APPGATE_LBRULE_REMOVE_FLAG'], metalog)
		
		# NETWORK Application-Gateway address-pool Remove
		metalog = "************** Azure Network Application-Gateway Address-Pool Remove ******************* \t"
		execute_command_with_flag("azure network application-gateway address-pool remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_ADDRESSPOOL_NAME']+str(random_no) + " -q ", logfile, config['APPGATE_ADDPOOL_REMOVE_FLAG'], metalog)
		
		# NETWORK Application-Gateway http-listener Remove
		metalog = "************** Azure Network Application-Gateway Http-Listener Remove ******************* \t"
		execute_command_with_flag("azure network application-gateway http-listener remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPLISTENER_NAME']+str(random_no) + " -q ", logfile, config['APPGATE_HTTPLISTENER_REMOVE_FLAG'], metalog)
		
		# NETWORK Application-Gateway http-settings Remove
		metalog = "************** Azure Network Application-Gateway Http-Settings Remove ******************* \t"
		execute_command_with_flag("azure network application-gateway http-settings remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_HTTPSETTINGS_NAME']+str(random_no) + " -q ", logfile, config['APPGATE_HTTPSETTINGS_REMOVE_FLAG'], metalog)
		
		# # # Functionality not yet implemented, Issue No. MSOpenTech#293
		# # NETWORK Application-Gateway frontend-ip Remove
		# metalog = "************** Azure Network Application-Gateway Frontend-IP Remove ******************* \t"
		# execute_command_with_flag("azure network application-gateway frontend-ip remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDIP_NAME'] + " -q ", logfile, config['APPGATE_FRONTEND_REMOVE_FLAG'], metalog)
		
		# NETWORK Application-Gateway frontend-port Remove
		metalog = "************** Azure Network Application-Gateway Frontend-Port Remove ******************* \t"
		execute_command_with_flag("azure network application-gateway frontend-port remove " + " -w " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -n " + config['APPGATE_FRONTENDPORT_NAME']+str(random_no) + " -q ", logfile, config['APPGATE_FRONTENDPORT_REMOVE_FLAG'], metalog)
		
		# NETWORK Application-Gateway config Export
		metalog = "************** Azure Network Application-Gateway Config Export ******************* \t"
		execute_command_with_flag("azure network application-gateway config export " + " -n " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -t " + config['APPGATE_EXPORT_FILE'], logfile, config['APPGATE_CONFIG_EXPORT_FLAG'], metalog)
		
		# NETWORK Application-Gateway Delete
		metalog = " ************** Azure Network Application-Gateway Delete ******************* \t"
		execute_command_with_flag("azure network application-gateway delete " + config['NETWORK_APPLICATION_GATEWAY_NAME']+str(random_no) + " -q " ,logfile, config['APPLICATIONGATEWAY_DELETE_FLAG'], metalog)
		
		#Gateway Command - Start Here
		
		# NETWORK Vnet & Subnet Create for Gateway Create
		metalog = " ************** Azure Network Vnet for Gateway create ******************* \t"
		execute_command_with_flag("azure network vnet create "+config['NETWORK_VPN_VNET_NAME'] + " -e " +config['VPN_VNET_ADDRESS'] + " -i " +config['VPN_VNETCIDR'] + " -p " +config['VPN_VNET_SUBNET_START_IP'] + " -r " +config['VPN_VNET_SUBNET_CIDR'] + " -l " +config['VPN_LOCATION'],logfile,config['VNET_FORGATEWAY_CREATE_FLAG'],metalog)
		metalog = " ************** Azure Network Vnet Subnet for Gateway create ******************* \t"
		execute_command_with_flag("azure network vnet subnet create " + " -t "+config['NETWORK_VPN_VNET_NAME'] + " -n " +config['NETWORK_VPN_SUBNET_NAME'] + " -a " +config['VPN_SUBNET_ADDRESS'],logfile,config['SUBNET_FORGATEWAY_CREATE_FLAG'],metalog)
		
		# NETWORK LOCAL-NETWORK Create List Show Add
		metalog = " ************** Azure Network Local-Network Create ******************* \t"
		execute_command_with_flag("azure network local-network create " + config['NETWORK_LOCALNETWORK_NAME'] + " -a " + config['LOCAL_NETWORK_ADDRESS'] + " -w " + config['VPN_GATEWAY_ADDRESS'], logfile, config['LOCAL_NETWORK_CREATE_FLAG'],metalog)				
		metalog = " ************** Azure Network Local-Network List ******************* \t"
		execute_command_with_flag("azure network local-network list ",logfile,config['LOCAL_NETWORK_LIST_FLAG'],metalog)	
		metalog = " ************** Azure Network Local-Network Show ******************* \t"
		execute_command_with_flag("azure network local-network show " + " -n " + config['NETWORK_LOCALNETWORK_NAME'], logfile, config['LOCAL_NETWORK_SHOW_FLAG'],metalog)
		metalog = "************** Azure Network Vnet Local-Network Add ******************* \t"
		execute_command_with_flag("azure network vnet local-network add " + config['NETWORK_VPN_VNET_NAME'] + " " + config['NETWORK_LOCALNETWORK_NAME'], logfile,config['VNET_LOCAL_NETWORK_ADD_FLAG'], metalog)
		
		# NETWORK Vpn Gateway Create Show Shared-Key Set Reset Connection List Vpn-Device List Diagnostics Start Stop & Get Delete
		metalog = "************** Azure Network Vpn-Gateway Create ******************* \t"
		execute_command_with_flag("azure network vpn-gateway create " + " -n " +config['NETWORK_VPN_VNET_NAME'] + " -t " +config['VPN_GAETWAY_TYPE'], logfile,config['VPN_GATEWAY_CREATE_FLAG'], metalog)
		metalog = "************** Azure Network Vpn-Gateway Show ******************* \t"
		execute_command_with_flag("azure network vpn-gateway show " + " -n " +config['NETWORK_VPN_VNET_NAME'], logfile,config['VPN_GATEWAY_SHOW_FLAG'], metalog)
		metalog = "************** Azure Network Vpn-Gateway shared-key set ******************* \t"
		execute_command_with_flag("azure network vpn-gateway shared-key set " + " -n " +config['NETWORK_VPN_VNET_NAME']+ " -t " +config['NETWORK_LOCALNETWORK_NAME']+ " -k " +config['VPN_KEYVALUE'], logfile, config['VPN_GATEWAY_SHAREDKEY_SET_FLAG'],metalog)
		metalog = "************** Azure Network Vpn-Gateway shared-key reset ******************* \t"
		execute_command_with_flag("azure network vpn-gateway shared-key reset " + " -n " +config['NETWORK_VPN_VNET_NAME']+ " -t " +config['NETWORK_LOCALNETWORK_NAME']+ " -l " +config['VPN_KEYLENGHT'], logfile, config['VPN_GATEWAY_SHAREDKEY_RESET_FLAG'],metalog)
		metalog = "************** Azure Network Vpn-Gateway Connection List ******************* \t"
		execute_command_with_flag("azure network vpn-gateway connection list " + " -n " +config['NETWORK_VPN_VNET_NAME'], logfile,config['VPN_GATEWAY_CONNECTION_LIST_FLAG'], metalog)
		metalog = "************** Azure Network Vpn-Device List ******************* \t"
		execute_command_with_flag("azure network vpn-gateway device list ", logfile, config['VPN_GATEWAY_DEVICE_LIST_FLAG'],metalog)
		metalog = "************** Azure Network Vpn-Gateway Diagnostics Start ******************* \t"
		execute_command_with_flag("azure network vpn-gateway diagnostics start " +config['NETWORK_VPN_VNET_NAME']+ " -d " +config['VPN_DURATION']+ " -a " +config['VPN_STORAGE']+ " -k " +config['VPN_STORAGE_KEY']+ " -c " +config['VPN_CONTAINER'], logfile, config['VPN_GATEWAY_DIAGNOSTIC_START_FLAG'],metalog)
		metalog = "************** Azure Network Vpn-Gateway Diagnostics Stop ******************* \t"
		execute_command_with_flag("azure network vpn-gateway diagnostics stop " +config['NETWORK_VPN_VNET_NAME'], logfile, config['VPN_GATEWAY_DIAGNOSTIC_STOP_FLAG'],metalog)
		metalog = "************** Azure Network Vpn-Gateway Diagnostics Get ******************* \t"
		execute_command_with_flag("azure network vpn-gateway diagnostics get " +config['NETWORK_VPN_VNET_NAME'], logfile, config['VPN_GATEWAY_DIAGNOSTIC_GET_FLAG'],metalog)
		metalog = "************** Azure Network Vpn-Gateway Delete ******************* \t"
		execute_command_with_flag("azure network vpn-gateway delete " + " -n " +config['NETWORK_VPN_VNET_NAME'] + " -q " , logfile, config['VPN_GATEWAY_DELETE_FLAG'],metalog)
		
		# NETWORK LOCAL-NETWORK Remove 
		metalog = "************** Azure Network Vnet Local-Network Remove ******************* \t"
		execute_command_with_flag("azure network vnet local-network remove " + config['NETWORK_VPN_VNET_NAME'] + " " + config['NETWORK_LOCALNETWORK_NAME'], logfile,config['LOCAL_NETWORK_REMOVE_FLAG'], metalog)
		# NETWORK Vnet for Gateway delete
		metalog = " ************** Azure Network Vnet for Gateway delete ******************* \t"
		execute_command_with_flag("azure network vnet delete "+config['NETWORK_VPN_VNET_NAME'] + " --quiet ",logfile,config['VNET_FORGATEWAY_DELETE_FLAG'],metalog)
		# NETWORK LOCAL-NETWORK Set Delete
		metalog = " ************** Azure Network Local-Network Set ******************* \t"
		execute_command_with_flag("azure network local-network set " + config['NETWORK_LOCALNETWORK_NAME'] + " -a " + config['LOCAL_NETWORK_ADDRESS_SET'] + " -w " + config['VPN_GATEWAY_ADDRESS_SET'], logfile, config['LOCAL_NETWORK_SET_FLAG'],metalog)
		metalog = " ************** Azure Network Local-Network Delete ******************* \t"
		execute_command_with_flag("azure network local-network delete " + config['NETWORK_LOCALNETWORK_NAME'] + " -q " ,logfile,config['LOCAL_NETWORK_DELETE_FLAG'],metalog)
		
		#Gateway Command - End Here
		
		# NETWORK NSG Delete
		metalog = "************** Azure Network Nsg Delete ******************* \t"
		execute_command_with_flag("azure network nsg delete " + config['NETWORK_NSG_NAME'] + " --quiet ", logfile, config['NETWORKNSG_DELETE_FLAG'], metalog)
		
		# NETWORK ROUTE-TABLE Delete
		metalog = " ************** Azure Network Route-Table Delete ******************* \t"
		execute_command_with_flag("azure network route-table delete " + " " + config['NETWORK_ROUTE_TABLE'] + " -q ", logfile, config['NETWORKROUTETABLE_DELETE_FLAG'], metalog)
		
		# NETWORK VNET SUBNET Delete
		metalog = "************** Azure Network Vnet Subnet Delete ******************* \t"
		execute_command_with_flag("azure network vnet subnet delete " + config['NETWORK_NAME'] + " " + config['NETWORK_SUBNET_NAME'] + " --quiet ", logfile, config['NETWORKVNETSUBNET_DELETE_FLAG'], metalog)
		
		metalog = "************** Azure Network Delete ******************* \t"
		execute_command_with_flag("azure network vnet delete "+config['NETWORK_NAME'] + " --quiet ",logfile,config['NETWORK_DELETE_FLAG'],metalog)				
		metalog = "************** Azure VM Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_NAME'] + " -b --quiet ",logfile,config['VM_DEL_FLAG'],metalog)
		metalog = "************** Azure Windows VM Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_WIN_NAME'] + " -b --quiet ",logfile,config['VM_DEL_FLAG'],metalog)
		metalog = " ************** Azure  network reserved-ip delete ******************* \t"
		execute_command_with_flag("azure network reserved-ip delete " + config['RIPNAME'] +" -q",logfile,config['RESERVED_IP_DELETE_FLAG'],metalog)

		metalog = "************** Azure VM Disk Upload ******************* \t"
		execute_command_with_flag("azure vm disk upload "+config['DISK_UPLOAD_SOURCE_PATH']+" "+config['DISK_UPLOAD_BLOB_URL']+" "+config['STORAGE_ACCOUNT_KEY'],logfile,config['DISK_UPLOAD_FLAG'],metalog)		

		metalog = "************** Azure VM Image Delete ******************* \t"
		execute_command_with_flag("azure vm image delete "+config['VM_IMAGE_NAME'],logfile,config['IMAGE_DEL_FLAG'],metalog)
		metalog = "************** Azure VM Captured Image Delete ******************* \t"
		execute_command_with_flag("azure vm image delete "+config['TARGET_IMG_NAME'],logfile,config['VM_CAPTURE_FLAG'],metalog)
		metalog = "************** Azure VM Disk Delete ******************* \t"
		execute_command_with_flag("azure vm disk delete "+config['VM_DISK_IMAGE_NAME'],logfile,config['DISK_DEL_FLAG'],metalog)
		metalog = "************** Azure Affinity Group Delete ******************* \t"
		execute_command_with_flag("azure account affinity-group delete "+config['AFFINITY_GRP_NAME'] + " --quiet ",logfile,config['VM_AFFINITY_DEL_FLAG'],metalog)

		metalog = "**********************Azure VM Docker Create[Docker Port]********************************* \t"	
 		execute_command_with_flag("azure vm docker create "+ config['VM_DOCKER_NAME'] + " "+ config['VM_DOCKER_IMG_NAME'] +" "+ config['USER_NAME'] +" "+ config['PASSWORD'] +" -l " +config['LOCATION']+ " " + config['CERT_FILE'] + " " + config['VM_DOCKER_PORT'] ,logfile,config['VM_DOCKER_CREATE_FLAG'],metalog)
 		metalog = "************** Azure VM Docker Delete ******************* \t"
 		execute_command_with_flag("azure vm delete "+config['VM_DOCKER_NAME'] + " -b --quiet ",logfile,config["VM_DOCKER_DELETE_FLAG"],metalog)
  		metalog = "************** Azure Account Clear ******************* \t"
		execute_command_with_flag("azure account clear --quiet",logfile,config['ACCOUNT_CLEAR_FLAG'],metalog)
		
		metalog = " ************** Loadbalancer Vm should create with vnet ******************* \t"
		execute_command_with_flag("azure vm create " + config['VM_NAME'] + " " + " --virtual-network-name "+ config['NETWORK_NAME'] + " -l " + config['LOCATION'] + " " + config['IMAGE_NAME'] + " " + config['USER_NAME'] + " " + config['PASSWORD'] ,logfile,config['LOADBALANCER_CREATE_FLAG'],metalog)		
		metalog = " ************** Loadbalancer Add ******************* \t"
		execute_command_with_flag("azure service internal-load-balancer add " + config['VM_NAME'] + " -t " + config['SUBNET'] + " -n " + config['INTERNAL_LB_NAME'] ,logfile,config['LOADBALANCER_ADD_FLAG'],metalog)		
		metalog = " ************** Loadbalancer List ******************* \t"
		execute_command_with_flag("azure service internal-load-balancer list " + config['VM_NAME'],logfile,config['LOADBALANCER_LIST_FLAG'],metalog)	
		metalog = " ************** Loadbalancer Set ******************* \t"
		execute_command_with_flag("azure service internal-load-balancer set " + config['VM_NAME'] + config['INTERNAL_LB_NAME_UPDATE'] + " -t " + config['SUBNET'] + " -a " + config['SUBNETIP']  ,logfile,config['LOADBALANCER_SET_FLAG'],metalog)		
		metalog = " ************** Loadbalancer Delete ******************* \t"
		execute_command_with_flag("azure service internal-load-balancer delete " + config['VM_NAME'] + " -n " + config['INTERNAL_LB_NAME'] + " --quiet " ,logfile,config['LOADBALANCER_DELETE_FLAG'],metalog)
		metalog = "************** Azure LoadBalancer VM Delete ******************* \t"
		execute_command_with_flag("azure vm delete "+config['VM_NAME'] + " -b --quiet ",logfile,config['VM_LOADBALANCER_DEL_FLAG'],metalog)		
							
printstatus()
