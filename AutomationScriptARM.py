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
	from configARM import configARM
	logfile = create_file("" + configARM['LOG_FILE'] + "")
	logerr = create_file("" + configARM['LOG_FILERR'] + "")
	if(configARM['GLOBAL_FLAG'] == "1"):
		logfile.write("************** Test Summary Report **************** \n")
		metalog = "************** NPM CACHE CLEAR **************** \t" 
		retryLoad1("npm cache clear",logfile,metalog)		
		metalog = "************** NPM AZURE INSTALL **************** \t" 
		retryLoad1("npm install azure -g",logfile,metalog)		
		metalog = "************** Azure Help Command **************** \t"
		retryLoad1("azure",logfile,metalog)

		if(configARM['AD_Login'] == "1"):
		  metalog = "************** Azure Login **************** \t" 
		  retryLoad1("azure login -u " + configARM['LOGINUSER'] + " -p " + configARM['LOGINPASSWORD']+ " --quiet",logfile,metalog)
		  metalog = "************** Azure Config Mode ARM **************** \t" 
		  retryLoad1("azure config mode arm ",logfile,metalog)
		  
		else:
		 metalog = "************** Azure Login **************** \t" 
		 retryLoad1("azure login -u " + configARM['LOGINUSER'] + " -p " + configARM['LOGINPASSWORD']+ " --quiet",logfile,metalog)
		 metalog = "************** Azure Config Mode ARM **************** \t" 
		 retryLoad1("azure config mode arm ",logfile,metalog)
		 
		 # AZURE RESOURCE GROUP Create		
		 metalog = " ************** Azure Resource Group Create ******************* \t"
		 retryLoad1("azure group create " + configARM['GRPNAME'] + " " + configARM['LOCATION'], logfile, metalog)
		 
		 # NETWORK ROUTE-TABLE Create List Show Delete
		 metalog = "************** Azure Network Route-Table Create ******************* \t"
		 retryLoad1("azure network route-table create" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['LOCATION'], logfile, metalog)
		 metalog = "************** Azure Network Route-Table Show ******************* \t"
		 retryLoad1("azure network route-table show" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Route-Table List ******************* \t"
		 retryLoad1("azure network route-table list" + " " + configARM['GRPNAME'], logfile, metalog)
		 
		 # NETWORK ROUTE-TABLE ROUTE Create Set List Show Delete
		 metalog = "************** Azure Network Route-Table Route Create ******************* \t"
		 retryLoad1("azure network route-table route create" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME']+ " " + configARM['ROUTE_ADDRESS_PREFIX']+ " " + configARM['NEXT_HOP_TYPE'], logfile, metalog)
		 metalog = "************** Azure Network Route-Table Route Set ******************* \t"
		 retryLoad1("azure network route-table route set" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Route-Table Route Show ******************* \t"
		 retryLoad1("azure network route-table route show" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Route-Table Route List ******************* \t"
		 retryLoad1("azure network route-table route list" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Route-Table Route Delete ******************* \t"
		 retryLoad1("azure network route-table route delete" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME']+" -q ", logfile, metalog)
		 
		 
		 # # NETWORK VNET Create Set List Show
		 metalog = " ************** Azure Network Vnet Create ******************* \t"
		 retryLoad1("azure network vnet create " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['LOCATION'] + " -a " + configARM['ADDRESS_PREFIXES']  + " -t " + configARM['TAGS'], logfile, metalog)
		 metalog = " ************** Azure Network Vnet Set ******************* \t"
		 retryLoad1("azure network vnet set " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['LOCATION'] + " -t " + configARM['TAGS_SET'], logfile, metalog)
		 metalog = "************** Azure Network Vnet List ******************* \t"
		 retryLoad1("azure network vnet list " + " " + configARM['GRPNAME'], logfile, metalog)
		 metalog = "************** Azure Network Vnet Show ******************* \t"
		 retryLoad1("azure network vnet show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'], logfile, metalog)
		 
		 # # NETWORK NSG Create Set List Show
		 metalog = " ************** Azure Network Nsg Create ******************* \t"
		 retryLoad1("azure network nsg create " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['LOCATION'] + " -t " + configARM['TAGS'], logfile, metalog)
		 metalog = " ************** Azure Network Nsg Set ******************* \t"
		 retryLoad1("azure network nsg set " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " -t " + configARM['TAGS_SET'], logfile, metalog)
		 metalog = "************** Azure Network Nsg List ******************* \t"
		 retryLoad1("azure network nsg list " + " " + configARM['GRPNAME'], logfile, metalog)
		 metalog = "************** Azure Network Nsg Show ******************* \t"
		 retryLoad1("azure network nsg show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'], logfile, metalog)
		 
		 # NETWORK VNET SUBNET Create Set List Show
		 metalog = " ************** Azure Network Vnet Subnet Create ******************* \t"
		 retryLoad1("azure network vnet subnet create " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'] + " -a " + configARM['ADDRESS_PREFIXES'] + " -o " + configARM['NETWORK_NSG_NAME'] + " -r " + configARM['ROUTE_TABLE_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network Vnet Set ******************* \t"
		 retryLoad1("azure network vnet subnet set " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'] + " -a " + configARM['ADDRESS_PREFIXES_SET'] + " -o " + configARM['NETWORK_NSG_NAME'] + " -r " + configARM['ROUTE_TABLE_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Vnet List ******************* \t"
		 retryLoad1("azure network vnet subnet list " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Vnet Show ******************* \t"
		 retryLoad1("azure network vnet subnet show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'], logfile, metalog)
		 
		 
		 
		 # NETWORK NSG RULE Create Set List Show Delete
		 metalog = " ************** Azure Network Nsg Rule Create ******************* \t"
		 retryLoad1("azure network nsg rule create " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'] + " -d " + configARM['DESCRIPTION'] + " -p " + configARM['PROTOCOL'] + " -f " + configARM['SOURCE_ADDRESS_PREFIX'] + " -o " + configARM['SOURCE_PORT_RANGE'] + " -e " + configARM['DESTINATION_ADDRESS_PREFIX'] + " -u " + configARM['DESTINATION_PORT_RANGE'] + " -c " + configARM['ACCESS'] + " -y " + configARM['PRIORITY'] + " -r " + configARM['DIRECTION'], logfile, metalog)
		 metalog = " ************** Azure Network Nsg Rule Set ******************* \t"
		 retryLoad1("azure network nsg rule set " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'] + " -d " + configARM['DESCRIPTION_SET'] + " -p " + configARM['PROTOCOL_SET'] + " -f " + configARM['SOURCE_ADDRESS_PREFIX_SET'] + " -o " + configARM['SOURCE_PORT_RANGE_SET'] + " -e " + configARM['DESTINATION_ADDRESS_PREFIX_SET'] + " -u " + configARM['DESTINATION_PORT_RANGE_SET'] + " -c " + configARM['ACCESS_SET'] + " -y " + configARM['PRIORITY_SET'] + " -r " + configARM['DIRECTION_SET'], logfile, metalog)
		 metalog = "************** Azure Network Nsg Rule List ******************* \t"
		 retryLoad1("azure network nsg rule list " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Nsg Rule Show ******************* \t"
		 retryLoad1("azure network nsg rule show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'], logfile, metalog)
		 metalog = "************** Azure Network Nsg Rule Delete ******************* \t"
		 retryLoad1("azure network nsg rule delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'] + " --quiet ", logfile, metalog)
		 
		 # NETWORK Public-Ip Create Set List Show
		 metalog = " ************** Azure Network Public-Ip Create ******************* \t"
		 retryLoad1("azure network public-ip create " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'] + " " + configARM['LOCATION'] + " -d " + configARM['DOMAIN_NAME']+str(random_no)+ " -a " + configARM['ALLOCATION_METHOD'] + " -i " + configARM['IDLE_TIMEOUT'] + " -t " + configARM['TAGS'], logfile, metalog)
		 metalog = " ************** Azure Network Public-Ip Set ******************* \t"
		 retryLoad1("azure network public-ip set " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'] + " -d " + configARM['DOMAIN_NAME_SET']+str(random_no) + " -a " + configARM['ALLOCATION_METHOD_SET'] + " -i " + configARM['IDLE_TIMEOUT_SET'] + " -t " + configARM['TAGS_SET'], logfile, metalog)
		 metalog = "************** Azure Network Public-Ip List ******************* \t"
		 retryLoad1("azure network public-ip list " + " " + configARM['GRPNAME'], logfile, metalog)
		 metalog = "************** Azure Network Public-Ip Show ******************* \t"
		 retryLoad1("azure network public-ip show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'], logfile, metalog)
		 	 
		 # NETWORK NIC Create Set List Show
		 metalog = " ************** Azure Network Nic Create ******************* \t"
		 retryLoad1("azure network nic create " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " " + configARM['LOCATION'] + " -o " + configARM['NETWORK_NSG_NAME'] + " -a " + configARM['PRIVATEIP_ADDRESS'] + " -k " + configARM['NETWORK_SUBNET_NAME'] + " -m " + configARM['NETWORK_VNET_NAME'] + " -t " + configARM['TAGS'], logfile, metalog)
		 metalog = " ************** Azure Network Nic Set ******************* \t"
		 retryLoad1("azure network nic set " + configARM['GRPNAME'] + " "  + configARM['NETWORK_NIC_NAME'] + " " + configARM['LOCATION'] + " -o " + configARM['NETWORK_NSG_NAME'] + " -a " + configARM['PRIVATEIP_ADDRESS'] + " -k " + configARM['NETWORK_SUBNET_NAME'] + " -m " + configARM['NETWORK_VNET_NAME'] + " -t " + configARM['TAGS_SET'], logfile, metalog)
		 metalog = "************** Azure Network Nic List ******************* \t"
		 retryLoad1("azure network nic list " + " " + configARM['GRPNAME'], logfile, metalog)
		 metalog = "************** Azure Network Nic Show ******************* \t"
		 retryLoad1("azure network nic show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'], logfile, metalog)
		
		 # LOADBALANCER  Create List Show
		 metalog = " ************** Azure Network LoadBalancer Create ******************* \t"
		 retryLoad1("azure network lb create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LOCATION'] + " -t " + configARM['TAGS'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer List ******************* \t"
		 retryLoad1("azure network lb list " + configARM['GRPNAME'] , logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Show ******************* \t"
		 retryLoad1("azure network lb show " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] , logfile, metalog)
		 
		 # LOADBALANCER Frontend-ip Create Set List
		 metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip Create ******************* \t"
		 retryLoad1("azure network lb frontend-ip create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_FRONTENDIP_NAME'] + " -e " + configARM['NETWORK_SUBNET_NAME'] + " -m " + configARM['NETWORK_VNET_NAME'], logfile, metalog) 
		 metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip Set ******************* \t"
		 retryLoad1("azure network lb frontend-ip set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_FRONTENDIP_NAME'] + " -e " + configARM['NETWORK_SUBNET_NAME'] + " -m " + configARM['NETWORK_VNET_NAME'], logfile, metalog) 
		 metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip List ******************* \t"
		 retryLoad1("azure network lb frontend-ip list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, metalog)
		 
		 # LOADBALANCER PROBE Create Set List
		 metalog = " ************** Azure Network LoadBalancer Probe Create ******************* \t"
		 retryLoad1("azure network lb probe create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_PROBE_NAME'] + " -p " + configARM['LB_PROBE_PROTOCOL']  + " -o " + configARM['LB_PROBE_PORT']  + " -i " + configARM['LB_PROBE_INTERVAL']  + " -c " + configARM['LB_PROBE_COUNT'], logfile, metalog) 
		 metalog = " ************** Azure Network LoadBalancer Probe Set ******************* \t"
		 retryLoad1("azure network lb probe set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_PROBE_NAME'] + " -p " + configARM['LB_PROBE_PROTOCOL']  + " -o " + configARM['LB_PROBE_PORT']  + " -i " + configARM['LB_PROBE_INTERVAL']  + " -c " + configARM['LB_PROBE_COUNT'], logfile, metalog) 
		 metalog = " ************** Azure Network LoadBalancer Probe List ******************* \t"
		 retryLoad1("azure network lb probe list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, metalog)
		
		 # LOADBALANCER Inbound-Nat-Rule Create Set List Delete
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule Create ******************* \t"
		 retryLoad1("azure network lb inbound-nat-rule create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_INBOUNDNATRULE_NAME'], logfile, metalog) 
		 # Refer https://github.com/MSOpenTech/azure-xplat-cli/issues/465 
		 # metalog = " ************** Azure Network NIC Inbound-Nat-Rule ADD ******************* \t"
		 # retryLoad1("azure network nic inbound-nat-rule add " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -r " + configARM['LB_INBOUNDNATRULE_NAME'], logfile, metalog)
		 # metalog = " ************** Azure Network NIC Inbound-Nat-Rule Remove ******************* \t"
		 # retryLoad1("azure network nic inbound-nat-rule remove " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -r " + configARM['LB_INBOUNDNATRULE_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule Set ******************* \t"
		 retryLoad1("azure network lb inbound-nat-rule set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_INBOUNDNATRULE_NAME'] + " -i " + configARM['LB_FRONTENDIP_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule List ******************* \t"
		 retryLoad1("azure network lb inbound-nat-rule list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule Delete ******************* \t"
		 retryLoad1("azure network lb inbound-nat-rule delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_INBOUNDNATRULE_NAME'] + " -q ", logfile, metalog)
		
		 # LOADBALANCER Address-Pool Create Add Remove List
		 metalog = " ************** Azure Network LoadBalancer Address-Pool Create ******************* \t"
		 retryLoad1("azure network lb address-pool create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_ADDPOOL_NAME'], logfile, metalog) 
		 # Refer https://github.com/MSOpenTech/azure-xplat-cli/issues/464
		 # metalog = " ************** Azure Network NIC Address-Pool ADD ******************* \t"
		 # retryLoad1("azure network nic address-pool add " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -a " + configARM['LB_ADDPOOL_NAME'], logfile, metalog)
		 # metalog = " ************** Azure Network NIC Address-Pool Remove ******************* \t"
		 # retryLoad1("azure network nic address-pool remove " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -a " + configARM['LB_ADDPOOL_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Address-Pool List ******************* \t"
		 retryLoad1("azure network lb address-pool list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] , logfile, metalog)
		
		 # LOADBALANCER Rule Create Set List Delete
		 metalog = " ************** Azure Network LoadBalancer Rule Create ******************* \t"
		 retryLoad1("azure network lb rule create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_RULE_NAME'] + " -p " + configARM['LB_RULE_PROTOCOL']  + " -f " + configARM['LB_RULE_FRONTPORT']  + " -b " + configARM['LB_RULE_BACKPORT']  + " -e " + configARM['LB_RULE_ENABLEFIP']  + " -i " + configARM['LB_RULE_IDLETIMEOUT']  + " -a " + configARM['LB_PROBE_NAME']  + " -t " + configARM['LB_FRONTENDIP_NAME']  + " -o " + configARM['LB_ADDPOOL_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Rule Set ******************* \t"
		 retryLoad1("azure network lb rule set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_RULE_NAME'] + " -p " + configARM['LB_RULE_PROTOCOL']  + " -f " + configARM['LB_RULE_FRONTPORT']  + " -b " + configARM['LB_RULE_BACKPORT']  + " -e " + configARM['LB_RULE_ENABLEFIP']  + " -i " + configARM['LB_RULE_IDLETIMEOUT']  + " -a " + configARM['LB_PROBE_NAME']  + " -t " + configARM['LB_FRONTENDIP_NAME']  + " -o " + configARM['LB_ADDPOOL_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Rule List ******************* \t"
		 retryLoad1("azure network lb rule list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network LoadBalancer Rule Delete ******************* \t"
		 retryLoad1("azure network lb rule delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_RULE_NAME'] + " -q ", logfile, metalog)
		 
		 # DNS-ZONE  Create Set List Show
		 metalog = " ************** Azure Network DNS-ZONE  Create ******************* \t"
		 retryLoad1("azure network dns-zone create " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " -t " + configARM['DNS_TAG'], logfile, metalog)
		 metalog = " ************** Azure Network DNS-ZONE  Set ******************* \t"
		 retryLoad1("azure network dns-zone set " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " -t " + configARM['DNS_TAG'], logfile, metalog)
		 metalog = " ************** Azure Network DNS-ZONE  Show ******************* \t"
		 retryLoad1("azure network dns-zone show " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network DNS-ZONE  List ******************* \t"
		 retryLoad1("azure network dns-zone list " + configARM['GRPNAME'], logfile, metalog)
		 
		 # DNS-RECORD-SET  Create Set List Show
		 metalog = " ************** Azure Network DNS-RECORD-SET  Create ******************* \t"
		 retryLoad1("azure network dns-record-set create " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'], logfile, metalog)
		 metalog = " ************** Azure Network DNS-RECORD-SET List ******************* \t"
		 retryLoad1("azure network dns-record-set list " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " -y " + configARM['DNS_TYPE'], logfile, metalog)
		 metalog = " ************** Azure Network DNS-RECORD-SET Set ******************* \t"
		 retryLoad1("azure network dns-record-set set " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'] + " -l 255 ", logfile, metalog)
		 metalog = " ************** Azure Network DNS-RECORD-SET Show ******************* \t"
		 retryLoad1("azure network dns-record-set show " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'], logfile, metalog)
		 
		 # Traffic-Manager Profile Create Set List Show
		 metalog = " ************** Azure Network Traffic-Manager  Profile Create ******************* \t"
		 retryLoad1("azure network traffic-manager profile create " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " -u " + configARM['PROFILE_STATUS'] + " -m " + configARM['ROUTING_METHOD'] + " -r " + configARM['RELATIVE_DNS'] + " -l " + configARM['TIME_TO_LIVE'] + " -p " + configARM['MONITOR_PROTOCOL'] + " -o " + configARM['MONITOR_PORT'] + " -a " + configARM['MONITOR_PATH'], logfile, metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Set ******************* \t"
		 retryLoad1("azure network traffic-manager profile set " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " -u " + configARM['PROFILE_STATUS'] + " -m " + configARM['ROUTING_METHOD']+ " -l " + configARM['TIME_TO_LIVE'] + " -p " + configARM['MONITOR_PROTOCOL'] + " -o " + configARM['MONITOR_PORT'] + " -a " + configARM['MONITOR_PATH'], logfile, metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile List ******************* \t"
		 retryLoad1("azure network traffic-manager profile list " + configARM['GRPNAME'], logfile, metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Show ******************* \t"
		 retryLoad1("azure network traffic-manager profile show " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'], logfile, metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Is-DNS-Available ******************* \t"
		 retryLoad1("azure network traffic-manager profile is-dns-available " + configARM['GRPNAME'] + " " + configARM['RELATIVE_DNS'], logfile, metalog)
		 
		 # Traffic-Manager Profile Endpoint Create Set List Show
		 metalog = " ************** Azure Network Traffic-Manager  Profile Endpoint Create ******************* \t"
		 retryLoad1("azure network traffic-manager profile endpoint create " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " " + configARM['TRAFFIC_MP_ENDPOINT'] + " -l " + configARM['TRAFFIC_MP_ENDPOINT_LOCATION'] + " -y " + configARM['ENDPT_TYPE'] + " -e " + configARM['ENDPT_TARGET'] + " -u " + configARM['ENDPOINT_STATUS'] + " -w " + configARM['ENDPOINT_WEIGHT'] + " -p " + configARM['ENDPOINT_PRIORITY'], logfile, metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Endpoint Set ******************* \t"
		 retryLoad1("azure network traffic-manager profile endpoint set " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " " + configARM['TRAFFIC_MP_ENDPOINT'] + " -y " + configARM['ENDPT_TYPE'] + " -e " + configARM['ENDPT_TARGET'] + " -u " + configARM['ENDPOINT_STATUS'] + " -w " + configARM['ENDPOINT_WEIGHT'] + " -p " + configARM['ENDPOINT_PRIORITY'], logfile, metalog)
		 
		 #Traffic-Manager  Profile Endpoint Delete
		 metalog = " ************** Azure Network Traffic-Manager  Profile Endpoint Delete ******************* \t"
		 retryLoad1("azure network traffic-manager profile endpoint delete " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " " + configARM['TRAFFIC_MP_ENDPOINT'] + " --quiet ", logfile, metalog)
		 
		 # Traffic-Manager Profile Delete
		 metalog = " ************** Azure Network Traffic-Manager Profile Delete ******************* \t"
		 retryLoad1("azure network traffic-manager profile delete " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " --quiet ", logfile, metalog)
		 
		 # DNS-RECORD-SET  Delete
		 metalog = " ************** Azure Network DNS-RECORD-SET Delete ******************* \t"
		 retryLoad1("azure network dns-record-set delete " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'] + " --quiet ", logfile, metalog)
		 
		 # DNS-ZONE  Delete
		 metalog = " ************** Azure Network DNS ZONE  Show ******************* \t"
		 retryLoad1("azure network dns-zone delete " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " --quiet ", logfile, metalog)
		 
		 
		 # LOADBALANCER Address-Pool Delete
		 metalog = " ************** Azure Network LoadBalancer Address-Pool Delete ******************* \t"
		 retryLoad1("azure network lb address-pool delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_ADDPOOL_NAME'] + " -q ", logfile, metalog)
		 
		 # LOADBALANCER FrontEnd-Ip Delete
		 # metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip Delete ******************* \t"
		 # retryLoad1("azure network lb frontend-ip delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_FRONTENDIP_NAME'] + " -q ", logfile, metalog)
		 
		 # LOADBALANCER Probe Delete
		 metalog = " ************** Azure Network LoadBalancer Probe Delete ******************* \t"
		 retryLoad1("azure network lb probe delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_PROBE_NAME'] + " -q ", logfile, metalog)
		 
		 # LOADBALANCER Delete
		 metalog = " ************** Azure Network LoadBalancer Delete ******************* \t"
		 retryLoad1("azure network lb delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " -q ", logfile, metalog)
		
		 # NETWORK NIC Delete
		 metalog = "************** Azure Network Nic Delete ******************* \t"
		 retryLoad1("azure network nic delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " --quiet ", logfile, metalog)
		 
		 # # NETWORK VNET SUBNET Delete
		 metalog = "************** Azure Network Vnet Subnet Delete ******************* \t"
		 retryLoad1("azure network vnet subnet delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'] + " --quiet ", logfile, metalog)
		 
		 # # NETWORK ROUTE_TABLE DELETE
		 metalog = "************** Azure Network Route-Table Delete ******************* \t"
		 retryLoad1("azure network route-table delete" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME']+" -q ", logfile, metalog)
		 
		 # # NETWORK VNET Delete
		 metalog = "************** Azure Network Vnet Delete ******************* \t"
		 retryLoad1("azure network vnet delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " --quiet ", logfile, metalog)
		 
		 # # NETWORK NSG Delete
		 metalog = "************** Azure Network Nsg Delete ******************* \t"
		 retryLoad1("azure network nsg delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " --quiet ", logfile, metalog)
		 		 
		 # NETWORK VNET PUBLIC-IP Delete
		 metalog = "************** Azure Network Public-Ip Delete ******************* \t"
		 retryLoad1("azure network public-ip delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'] + " --quiet ", logfile, metalog)

		 # VM COAMMANDS
		 metalog = " ************** Azure VM Create ******************* \t"
		 retryLoad1("azure vm create " + configARM['GRPNAME'] + " " + configARM['VM_NAME'] + " -l " + configARM['LOCATION'] + " Windows " + " -q " + configARM['VM_IMAGE']+ " -f " + configARM['VM_NIC']+ " -u " + configARM['VM_USER']+ " -p " + configARM['VM_PASSWORD']+ " -i " + configARM['VM_PUBLICIP']+ " -w " + configARM['VM_PUBLICIPDOMAIN']+ " -F " + configARM['VM_VNET']+ " -P " + configARM['VM_VNET_ADDPREFIX']+ " -j " + configARM['VM_SUBNET']+ " -k " + configARM['VM_SUBNETADDPREFIX']+ " -o " + configARM['VM_STORAGE']+ " -R " + configARM['VM_STORAGECONT'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Quick-Create ******************* \t"
		 retryLoad1("azure vm quick-create " + configARM['GRPNAME'] + " " + configARM['VM_QuickNAME'] + " " + configARM['LOCATION'] + " Windows " + " -Q " + configARM['VM_IMAGE_URN']+ " -u " + configARM['VM_USER']+ " -p " + configARM['VM_PASSWORD'], logfile, metalog)
		  
		 metalog = " ************** Azure VM List ******************* \t"
		 retryLoad1("azure vm list " + configARM['GRPNAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Sizes For the Previous Created VM ******************* \t"
		 retryLoad1("azure vm sizes " + " -g " +  configARM['GRPNAME']+ " -n " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Extension Set ******************* \t"
		 retryLoad1("azure vm extension set " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " " + configARM['VM_EXT_NAME']+ " " + configARM['VM_PUBLISHER']+ " " + configARM['VM_VERSION'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Extension Get ******************* \t"
		 retryLoad1("azure vm extension get " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Show ******************* \t"
		 retryLoad1("azure vm show " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " --json ", logfile, metalog)
		 
		 metalog = " ************** Azure VM Stop ******************* \t"
		 retryLoad1("azure vm stop " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Start ******************* \t"
		 retryLoad1("azure vm start " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Restart ******************* \t"
		 retryLoad1("azure vm restart " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Reset-Access ******************* \t"
		 retryLoad1("azure vm reset-access " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " -u " + configARM['VM_NEWUSER']+ " -p " + configARM['VM_PASSWORD']+ " -e " + configARM['VM_EXT_VERSION']+ " -R " + configARM['VM_USER'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Disk-Attach-New ******************* \t"
		 retryLoad1("azure vm disk attach-new " + configARM['GRPNAME']+ " " + configARM['VM_QuickNAME']+ " 1 " + " " + configARM['VM_VHD_NAME']+str(random_no)+".vhd", logfile, metalog)
		 
		 metalog = " ************** Azure VM Disk Detach ******************* \t"
		 retryLoad1("azure vm disk detach " + configARM['GRPNAME']+ " " + configARM['VM_QuickNAME']+ " " + configARM['VM_LUN'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Deallocate ******************* \t"
		 retryLoad1("azure vm deallocate " + configARM['GRPNAME']+ " " + configARM['VM_QuickNAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Stop ******************* \t"
		 retryLoad1("azure vm stop " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Sizes For Given Location ******************* \t"
		 retryLoad1("azure vm sizes " + " -l " + configARM['LOCATION'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Generalize ******************* \t"
		 retryLoad1("azure vm generalize " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Capture ******************* \t"
		 retryLoad1("azure vm capture " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " " + configARM['VM_VHD_PREFIX'], logfile, metalog)
		 
		 metalog = " ************** Azure VM Get-Instance-View ******************* \t"
		 retryLoad1("azure vm get-instance-view " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, metalog)
		 
		 metalog = " ************** Azure AvailSet Create ******************* \t"
		 retryLoad1("azure availset create " + configARM['GRPNAME']+ " " + configARM['AVAILSET_NAME']+ " " + configARM['LOCATION'], logfile, metalog)
		 
		 metalog = " ************** Azure AvailSet List ******************* \t"
		 retryLoad1("azure availset list " + configARM['GRPNAME'], logfile, metalog)
		 
		 metalog = " ************** Azure AvailSet Show ******************* \t"
		 retryLoad1("azure availset show " + configARM['GRPNAME']+ " " + configARM['AVAILSET_NAME']+ " --json ", logfile, metalog)
		 
		 metalog = " ************** Azure AvailSet Delete ******************* \t"
		 retryLoad1("azure availset delete " + configARM['GRPNAME']+ " " + configARM['AVAILSET_NAME']+ " -q ", logfile, metalog)
		 
		 metalog = " ************** Azure VM Delete ******************* \t"
		 retryLoad1("azure vm delete " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " -q ", logfile, metalog)
		 
		 metalog = " ************** Azure Resource Group Delete ******************* \t"
		 retryLoad1("azure group delete " + configARM['GRPNAME'] + " -q ", logfile, metalog)
		
		
	if(configARM['GLOBAL_FLAG'] == "0"):
		# logfile.write("************** Test Summary Report **************** \n")
		# metalog = "************** NPM CACHE CLEAR **************** \t" 
		# execute_command_with_flag("npm cache clear",logfile,configARM['NPM_CLEAR_FLAG'],metalog)	
		# metalog = "************** NPM AZURE INSTALL **************** \t" 
		# execute_command_with_flag("npm install azure -g",logfile,configARM['NPM_INSTALL_FLAG'],metalog)		
		# metalog = "************** Azure Help Command **************** \t"
		# execute_command_with_flag("azure",logfile,configARM['AZURE_HELP_FLAG'],metalog)

		if(configARM['AD_Login'] == "1"):
		 metalog = "************** Azure Login **************** \t" 
		 execute_command_with_flag("azure login -u "+ configARM['LOGINUSER'] + " -p " + configARM['LOGINPASSWORD'] + " --quiet",logfile,configARM['AZURE_LOGIN_FLAG'],metalog)
		else:
		 # metalog = "************** Azure Login **************** \t" 
		 # execute_command_with_flag("azure login -u " + configARM['LOGINUSER'] + " -p " + configARM['LOGINPASSWORD'] + " --quiet",logfile,metalog)

		 # AZURE RESOURCE GROUP Create		
		 metalog = " ************** Azure Resource Group Create ******************* \t"
		 execute_command_with_flag("azure group create " + configARM['GRPNAME'] + " " + configARM['LOCATION'], logfile, configARM['RESOURCEGROUP_CREATE_FLAG'], metalog)
		 
		 
		 # NETWORK ROUTE-TABLE Create List Show Delete
		 metalog = "************** Azure Network Route-Table Create ******************* \t"
		 retryLoad1("azure network route-table create" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['LOCATION'], logfile, configARM['ROUTE_TABLE_CREATE_FLAG'], metalog)
		 metalog = "************** Azure Network Route-Table Show ******************* \t"
		 retryLoad1("azure network route-table show" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'], logfile, configARM['ROUTE_TABLE_SHOW_FLAG'], metalog)
		 metalog = "************** Azure Network Route-Table List ******************* \t"
		 retryLoad1("azure network route-table list" + " " + configARM['GRPNAME'], logfile, configARM['ROUTE_TABLE_LIST_FLAG'], metalog)
		 
		 # NETWORK ROUTE-TABLE ROUTE Create Set List Show Delete
		 metalog = "************** Azure Network Route-Table Route Create ******************* \t"
		 retryLoad1("azure network route-table route create" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME']+ " " + configARM['ROUTE_ADDRESS_PREFIX']+ " " + configARM['NEXT_HOP_TYPE'], logfile, configARM['ROUTE_TBL_ROUTE_CREATE_FLAG'], metalog)
		 metalog = "************** Azure Network Route-Table Route Set ******************* \t"
		 retryLoad1("azure network route-table route set" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME'], logfile, configARM['ROUTE_TBL_ROUTE_SET_FLAG'], metalog)
		 metalog = "************** Azure Network Route-Table Route Show ******************* \t"
		 retryLoad1("azure network route-table route show" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME'], logfile, configARM['ROUTE_TBL_ROUTE_SHOW_FLAG'], metalog)
		 metalog = "************** Azure Network Route-Table Route List ******************* \t"
		 retryLoad1("azure network route-table route list" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'], logfile, configARM['ROUTE_TBL_ROUTE_LIST_FLAG'], metalog)
		 metalog = "************** Azure Network Route-Table Route Delete ******************* \t"
		 retryLoad1("azure network route-table route delete" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME'] + " " + configARM['ROUTE_NAME']+" -q ", logfile, configARM['ROUTE_TBL_ROUTE_DELETE_FLAG'], metalog)
		 
		 # NETWORK VNET Create Set List Show
		 metalog = " ************** Azure Network Vnet Create ******************* \t"
		 execute_command_with_flag("azure network vnet create " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['LOCATION'] + " -a " + configARM['ADDRESS_PREFIXES']  + " -t " + configARM['TAGS'], logfile, configARM['NETWORKVNET_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Vnet Set ******************* \t"
		 execute_command_with_flag("azure network vnet set " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['LOCATION'] + " -t " + configARM['TAGS_SET'], logfile, configARM['NETWORKVNET_SET_FLAG'], metalog)
		 metalog = "************** Azure Network Vnet List ******************* \t"
		 execute_command_with_flag("azure network vnet list " + " " + configARM['GRPNAME'], logfile, configARM['NETWORKVNET_LIST_FLAG'], metalog)
		 metalog = "************** Azure Network Vnet Show ******************* \t"
		 execute_command_with_flag("azure network vnet show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'], logfile, configARM['NETWORKVNET_SHOW_FLAG'], metalog)
		 
		 # NETWORK NSG Create Set List Show
		 metalog = " ************** Azure Network Nsg Create ******************* \t"
		 execute_command_with_flag("azure network nsg create " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['LOCATION'] + " -t " + configARM['TAGS'], logfile, configARM['NETWORKNSG_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Nsg Set ******************* \t"
		 execute_command_with_flag("azure network nsg set " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " -t " + configARM['TAGS_SET'], logfile, configARM['NETWORKNSG_SET_FLAG'], metalog)
		 metalog = "************** Azure Network Nsg List ******************* \t"
		 execute_command_with_flag("azure network nsg list " + " " + configARM['GRPNAME'], logfile, configARM['NETWORKNSG_LIST_FLAG'], metalog)
		 metalog = "************** Azure Network Nsg Show ******************* \t"
		 execute_command_with_flag("azure network nsg show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'], logfile, configARM['NETWORKNSG_SHOW_FLAG'], metalog)
		 
		 # NETWORK VNET SUBNET Create Set List Show
		 metalog = " ************** Azure Network Vnet Subnet Create ******************* \t"
		 execute_command_with_flag("azure network vnet subnet create " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'] + " -a " + configARM['ADDRESS_PREFIXES'] + " -o " + configARM['NETWORK_NSG_NAME'], logfile, configARM['NETWORKVNETSUBNET_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Vnet Set ******************* \t"
		 execute_command_with_flag("azure network vnet subnet set " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'] + " -a " + configARM['ADDRESS_PREFIXES_SET'] + " -o " + configARM['NETWORK_NSG_NAME'], logfile, configARM['NETWORKVNETSUBNET_SET_FLAG'], metalog)
		 metalog = "************** Azure Network Vnet List ******************* \t"
		 execute_command_with_flag("azure network vnet subnet list " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'], logfile, configARM['NETWORKVNETSUBNET_LIST_FLAG'], metalog)
		 metalog = "************** Azure Network Vnet Show ******************* \t"
		 execute_command_with_flag("azure network vnet subnet show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'], logfile, configARM['NETWORKVNETSUBNET_SHOW_FLAG'], metalog)	
		 
		 # NETWORK NSG RULE Create Set List Show Delete
		 metalog = " ************** Azure Network Nsg Rule Create ******************* \t"
		 execute_command_with_flag("azure network nsg rule create " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'] + " -d " + configARM['DESCRIPTION'] + " -p " + configARM['PROTOCOL'] + " -f " + configARM['SOURCE_ADDRESS_PREFIX'] + " -o " + configARM['SOURCE_PORT_RANGE'] + " -e " + configARM['DESTINATION_ADDRESS_PREFIX'] + " -u " + configARM['DESTINATION_PORT_RANGE'] + " -c " + configARM['ACCESS'] + " -y " + configARM['PRIORITY'] + " -r " + configARM['DIRECTION'], logfile, configARM['NETWORKNSGRULE_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Nsg Rule Set ******************* \t"
		 execute_command_with_flag("azure network nsg rule set " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'] + " -d " + configARM['DESCRIPTION_SET'] + " -p " + configARM['PROTOCOL_SET'] + " -f " + configARM['SOURCE_ADDRESS_PREFIX_SET'] + " -o " + configARM['SOURCE_PORT_RANGE_SET'] + " -e " + configARM['DESTINATION_ADDRESS_PREFIX_SET'] + " -u " + configARM['DESTINATION_PORT_RANGE_SET'] + " -c " + configARM['ACCESS_SET'] + " -y " + configARM['PRIORITY_SET'] + " -r " + configARM['DIRECTION_SET'], logfile, configARM['NETWORKNSGRULE_SET_FLAG'], metalog)
		 metalog = "************** Azure Network Nsg Rule List ******************* \t"
		 execute_command_with_flag("azure network nsg rule list " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'], logfile, configARM['NETWORKNSGRULE_LIST_FLAG'], metalog)
		 metalog = "************** Azure Network Nsg Rule Show ******************* \t"
		 execute_command_with_flag("azure network nsg rule show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'], logfile, configARM['NETWORKNSGRULE_SHOW_FLAG'], metalog)
		 metalog = "************** Azure Network Nsg Rule Delete ******************* \t"
		 execute_command_with_flag("azure network nsg rule delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " " + configARM['NETWORK_NSG_RULE_NAME'] + " --quiet ", logfile, configARM['NETWORKNSGRULE_DELETE_FLAG'], metalog)
		 
		 # NETWORK Public-Ip Create Set List Show
		 metalog = " ************** Azure Network Public-Ip Create ******************* \t"
		 execute_command_with_flag("azure network public-ip create " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'] + " " + configARM['LOCATION'] + " -d " + configARM['DOMAIN_NAME'] + " -a " + configARM['ALLOCATION_METHOD'] + " -i " + configARM['IDLE_TIMEOUT'] + " -t " + configARM['TAGS'], logfile, configARM['NETWORKPUBLICIP_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Public-Ip Set ******************* \t"
		 execute_command_with_flag("azure network public-ip set " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'] + " -d " + configARM['DOMAIN_NAME_SET'] + " -a " + configARM['ALLOCATION_METHOD_SET'] + " -i " + configARM['IDLE_TIMEOUT_SET'] + " -t " + configARM['TAGS_SET'], logfile, configARM['NETWORKPUBLICIP_SET_FLAG'], metalog)
		 metalog = "************** Azure Network Public-Ip List ******************* \t"
		 execute_command_with_flag("azure network public-ip list " + " " + configARM['GRPNAME'], logfile, configARM['NETWORKPUBLICIP_LIST_FLAG'], metalog)
		 metalog = "************** Azure Network Public-Ip Show ******************* \t"
		 execute_command_with_flag("azure network public-ip show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'], logfile, configARM['NETWORKPUBLICIP_SHOW_FLAG'], metalog)
		 	 
		 # NETWORK NIC Create Set List Show
		 metalog = " ************** Azure Network Nic Create ******************* \t"
		 execute_command_with_flag("azure network nic create " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " " + configARM['LOCATION'] + " -o " + configARM['NETWORK_NSG_NAME'] + " -p " + configARM['NETWORK_PUBLICIP'] + " -a " + configARM['PRIVATEIP_ADDRESS'] + " -k " + configARM['NETWORK_SUBNET_NAME'] + " -m " + configARM['NETWORK_VNET_NAME'] + " -t " + configARM['TAGS'], logfile, configARM['NETWORKNIC_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Nic Set ******************* \t"
		 execute_command_with_flag("azure network nic set " + configARM['GRPNAME'] + " "  + configARM['NETWORK_NIC_NAME'] + " " + configARM['LOCATION'] + " -o " + configARM['NETWORK_NSG_NAME'] + " -p " + configARM['NETWORK_PUBLICIP'] + " -a " + configARM['PRIVATEIP_ADDRESS'] + " -k " + configARM['NETWORK_SUBNET_NAME'] + " -m " + configARM['NETWORK_VNET_NAME'] + " -t " + configARM['TAGS_SET'], logfile, configARM['NETWORKNIC_SET_FLAG'], metalog)
		 metalog = "************** Azure Network Nic List ******************* \t"
		 execute_command_with_flag("azure network nic list " + " " + configARM['GRPNAME'], logfile, configARM['NETWORKNIC_LIST_FLAG'], metalog)
		 metalog = "************** Azure Network Nic Show ******************* \t"
		 execute_command_with_flag("azure network nic show " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'], logfile, configARM['NETWORKNIC_SHOW_FLAG'], metalog)
		
		 # LOADBALANCER  Create List Show
		 metalog = " ************** Azure Network LoadBalancer Create ******************* \t"
		 execute_command_with_flag("azure network lb create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LOCATION'] + " -t " + configARM['TAGS'], logfile, configARM['NETWORKLB_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer List ******************* \t"
		 execute_command_with_flag("azure network lb list " + configARM['GRPNAME'] , logfile, configARM['NETWORKLB_LIST_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Show ******************* \t"
		 execute_command_with_flag("azure network lb show " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] , logfile, configARM['NETWORKLB_SHOW_FLAG'], metalog)
		 
		 # LOADBALANCER Frontend-ip Create Set List
		 metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip Create ******************* \t"
		 execute_command_with_flag("azure network lb frontend-ip create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_FRONTENDIP_NAME'] + " -i " + configARM['NETWORK_PUBLICIP'], logfile, configARM['NETWORKLB_FRONTENDIP_CREATE_FLAG'], metalog) 
		 metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip Set ******************* \t"
		 execute_command_with_flag("azure network lb frontend-ip set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_FRONTENDIP_NAME'] + " -e " + configARM['NETWORK_SUBNET_NAME'] + " -m " + configARM['NETWORK_VNET_NAME'], logfile, configARM['NETWORKLB_FRONTENDIP_SET_FLAG'], metalog) 
		 metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip List ******************* \t"
		 execute_command_with_flag("azure network lb frontend-ip list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, configARM['NETWORKLB_FRONTENDIP_LIST_FLAG'], metalog)
		 
		 # LOADBALANCER PROBE Create Set List
		 metalog = " ************** Azure Network LoadBalancer Probe Create ******************* \t"
		 execute_command_with_flag("azure network lb probe create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_PROBE_NAME'] + " -p " + configARM['LB_PROBE_PROTOCOL']  + " -o " + configARM['LB_PROBE_PORT']  + " -i " + configARM['LB_PROBE_INTERVAL']  + " -c " + configARM['LB_PROBE_COUNT'], logfile, configARM['NETWORKLB_PROBE_CREATE_FLAG'], metalog) 
		 metalog = " ************** Azure Network LoadBalancer Probe Set ******************* \t"
		 execute_command_with_flag("azure network lb probe set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_PROBE_NAME'] + " -p " + configARM['LB_PROBE_PROTOCOL']  + " -o " + configARM['LB_PROBE_PORT']  + " -i " + configARM['LB_PROBE_INTERVAL']  + " -c " + configARM['LB_PROBE_COUNT'], logfile, configARM['NETWORKLB_PROBE_SET_FLAG'], metalog) 
		 metalog = " ************** Azure Network LoadBalancer Probe List ******************* \t"
		 execute_command_with_flag("azure network lb probe list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, configARM['NETWORKLB_PROBE_LIST_FLAG'], metalog)
		
		 # LOADBALANCER Inbound-Nat-Rule Create Set List Delete
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule Create ******************* \t"
		 execute_command_with_flag("azure network lb inbound-nat-rule create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_INBOUNDNATRULE_NAME'], logfile, configARM['NETWORKLB_INBOUNDNATRULE_CREATE_FLAG'], metalog)
		 
		 # metalog = " ************** Azure Network NIC Inbound-Nat-Rule ADD ******************* \t"
		 # retryLoad1("azure network nic inbound-nat-rule add " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -r " + configARM['LB_INBOUNDNATRULE_NAME'], logfile, configARM['NIC_NAT_RULE_ADD_FLAG'], metalog)
		 # metalog = " ************** Azure Network NIC Inbound-Nat-Rule Remove ******************* \t"
		 # retryLoad1("azure network nic inbound-nat-rule remove " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -r " + configARM['LB_INBOUNDNATRULE_NAME'], logfile, configARM['NIC_NAT_RULE_REMOVE_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule Set ******************* \t"
		 execute_command_with_flag("azure network lb inbound-nat-rule set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_INBOUNDNATRULE_NAME'] + " -i " + configARM['LB_FRONTENDIP_NAME'], logfile, configARM['NETWORKLB_INBOUNDNATRULE_SET_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule List ******************* \t"
		 execute_command_with_flag("azure network lb inbound-nat-rule list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, configARM['NETWORKLB_INBOUNDNATRULE_LIST_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Inbound-Nat-Rule Delete ******************* \t"
		 execute_command_with_flag("azure network lb inbound-nat-rule delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_INBOUNDNATRULE_NAME'] + " -q ", logfile, configARM['NETWORKLB_INBOUNDNATRULE_DELETE_FLAG'], metalog)
		
		 # LOADBALANCER Address-Pool Create Add Remove List
		 metalog = " ************** Azure Network LoadBalancer Address-Pool Create ******************* \t"
		 execute_command_with_flag("azure network lb address-pool create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_ADDPOOL_NAME'], logfile, configARM['NETWORKLB_ADDRESSPOOL_CREATE_FLAG'], metalog) 
		 
		 # metalog = " ************** Azure Network NIC Address-Pool ADD ******************* \t"
		 # retryLoad1("azure network nic address-pool add " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -a " + configARM['LB_ADDPOOL_NAME'], logfile, configARM['NIC_ADDRESSPOLL_ADD_FLAG'], metalog)
		 # metalog = " ************** Azure Network NIC Address-Pool Remove ******************* \t"
		 # retryLoad1("azure network nic address-pool remove " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " -l " + configARM['NETWORK_LB_NAME'] + " -a " + configARM['LB_ADDPOOL_NAME'], logfile, configARM['NIC_ADDRESSPOLL_REMOVE_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Address-Pool List ******************* \t"
		 execute_command_with_flag("azure network lb address-pool list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] , logfile, configARM['NETWORKLB_ADDRESSPOOL_LIST_FLAG'], metalog)
		
		 # LOADBALANCER Rule Create Set List Delete
		 metalog = " ************** Azure Network LoadBalancer Rule Create ******************* \t"
		 execute_command_with_flag("azure network lb rule create " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_RULE_NAME'] + " -p " + configARM['LB_RULE_PROTOCOL']  + " -f " + configARM['LB_RULE_FRONTPORT']  + " -b " + configARM['LB_RULE_BACKPORT']  + " -e " + configARM['LB_RULE_ENABLEFIP']  + " -i " + configARM['LB_RULE_IDLETIMEOUT']  + " -a " + configARM['LB_PROBE_NAME']  + " -t " + configARM['LB_FRONTENDIP_NAME']  + " -o " + configARM['LB_ADDPOOL_NAME'], logfile, configARM['NETWORKLB_RULE_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Rule Set ******************* \t"
		 execute_command_with_flag("azure network lb rule set " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_RULE_NAME'] + " -p " + configARM['LB_RULE_PROTOCOL']  + " -f " + configARM['LB_RULE_FRONTPORT']  + " -b " + configARM['LB_RULE_BACKPORT']  + " -e " + configARM['LB_RULE_ENABLEFIP']  + " -i " + configARM['LB_RULE_IDLETIMEOUT']  + " -a " + configARM['LB_PROBE_NAME']  + " -t " + configARM['LB_FRONTENDIP_NAME']  + " -o " + configARM['LB_ADDPOOL_NAME'], logfile, configARM['NETWORKLB_RULE_SET_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Rule List ******************* \t"
		 execute_command_with_flag("azure network lb rule list " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'], logfile, configARM['NETWORKLB_RULE_LIST_FLAG'], metalog)
		 metalog = " ************** Azure Network LoadBalancer Rule Delete ******************* \t"
		 execute_command_with_flag("azure network lb rule delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_RULE_NAME'] + " -q ", logfile, configARM['NETWORKLB_RULE_DELETE_FLAG'], metalog)
		 
		 # DNS-ZONE  Create Set List Show
		 metalog = " ************** Azure Network DNS-ZONE  Create ******************* \t"
		 retryLoad1("azure network dns-zone create " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " -t " + configARM['DNS_TAG'], logfile, configARM['DNS_ZONE_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network DNS-ZONE  Set ******************* \t"
		 retryLoad1("azure network dns-zone set " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " -t " + configARM['DNS_TAG'], logfile, configARM['DNS_ZONE_SET_FLAG'], metalog)
		 metalog = " ************** Azure Network DNS-ZONE  Show ******************* \t"
		 retryLoad1("azure network dns-zone show " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'], logfile, configARM['DNS_ZONE_SHOW_FLAG'], metalog)
		 metalog = " ************** Azure Network DNS-ZONE  List ******************* \t"
		 retryLoad1("azure network dns-zone list " + configARM['GRPNAME'], logfile, configARM['DNS_ZONE_LIST_FLAG'], metalog)
		 
		 # DNS-RECORD-SET  Create Set List Show
		 metalog = " ************** Azure Network DNS-RECORD-SET  Create ******************* \t"
		 retryLoad1("azure network dns-record-set create " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'], logfile, configARM['DNS_RECORDSET_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network DNS-RECORD-SET List ******************* \t"
		 retryLoad1("azure network dns-record-set list " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " -y " + configARM['DNS_TYPE'], logfile, configARM['DNS_RECORDSET_LIST_FLAG'], metalog)
		 metalog = " ************** Azure Network DNS-RECORD-SET Set ******************* \t"
		 retryLoad1("azure network dns-record-set set " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'] + " -l 255 ", logfile, configARM['DNS_RECORDSET_SET_FLAG'], metalog)
		 metalog = " ************** Azure Network DNS-RECORD-SET Show ******************* \t"
		 retryLoad1("azure network dns-record-set show " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'], logfile, configARM['DNS_RECORDSET_SHOW_FLAG'], metalog)
		 
		 # Traffic-Manager Profile Create Set List Show
		 metalog = " ************** Azure Network Traffic-Manager  Profile Create ******************* \t"
		 retryLoad1("azure network traffic-manager profile create " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " -u " + configARM['PROFILE_STATUS'] + " -m " + configARM['ROUTING_METHOD'] + " -r " + configARM['RELATIVE_DNS'] + " -l " + configARM['TIME_TO_LIVE'] + " -p " + configARM['MONITOR_PROTOCOL'] + " -o " + configARM['MONITOR_PORT'] + " -a " + configARM['MONITOR_PATH'], logfile, configARM['TRAFFIC_MANAGER_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Set ******************* \t"
		 retryLoad1("azure network traffic-manager profile set " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " -u " + configARM['PROFILE_STATUS'] + " -m " + configARM['ROUTING_METHOD']+ " -l " + configARM['TIME_TO_LIVE'] + " -p " + configARM['MONITOR_PROTOCOL'] + " -o " + configARM['MONITOR_PORT'] + " -a " + configARM['MONITOR_PATH'], logfile, configARM['TRAFFIC_MANAGER_SET_FLAG'], metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile List ******************* \t"
		 retryLoad1("azure network traffic-manager profile list " + configARM['GRPNAME'], logfile, configARM['TRAFFIC_MANAGER_LIST_FLAG'], metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Show ******************* \t"
		 retryLoad1("azure network traffic-manager profile show " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'], logfile, configARM['TRAFFIC_MANAGER_SHOW_FLAG'], metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Is-DNS-Available ******************* \t"
		 retryLoad1("azure network traffic-manager profile is-dns-available " + configARM['GRPNAME'] + " " + configARM['RELATIVE_DNS'], logfile, configARM['TRAFFIC_MANAGER_IS_DNS_AVAILABLE_FLAG'], metalog)
		 
		 # Traffic-Manager Profile Endpoint Create Set 
		 metalog = " ************** Azure Network Traffic-Manager  Profile Endpoint Create ******************* \t"
		 retryLoad1("azure network traffic-manager profile endpoint create " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " " + configARM['TRAFFIC_MP_ENDPOINT'] + " -l " + configARM['TRAFFIC_MP_ENDPOINT_LOCATION'] + " -y " + configARM['ENDPT_TYPE'] + " -e " + configARM['ENDPT_TARGET'] + " -u " + configARM['ENDPOINT_STATUS'] + " -w " + configARM['ENDPOINT_WEIGHT'] + " -p " + configARM['ENDPOINT_PRIORITY'], logfile, configARM['TRAFFIC_MANAGER_ENDPOINT_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure Network Traffic-Manager  Profile Endpoint Set ******************* \t"
		 retryLoad1("azure network traffic-manager profile endpoint set " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " " + configARM['TRAFFIC_MP_ENDPOINT'] + " -y " + configARM['ENDPT_TYPE'] + " -e " + configARM['ENDPT_TARGET'] + " -u " + configARM['ENDPOINT_STATUS'] + " -w " + configARM['ENDPOINT_WEIGHT'] + " -p " + configARM['ENDPOINT_PRIORITY'], logfile, configARM['TRAFFIC_MANAGER_ENDPOINT_SET_FLAG'], metalog)
		 
		 #Traffic-Manager  Profile Endpoint Delete
		 metalog = " ************** Azure Network Traffic-Manager  Profile Endpoint Delete ******************* \t"
		 retryLoad1("azure network traffic-manager profile endpoint delete " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " " + configARM['TRAFFIC_MP_ENDPOINT'] + " --quiet ", logfile, configARM['TRAFFIC_MANAGER_ENDPOINT_DELETE_FLAG'], metalog)
		 
		 # Traffic-Manager Profile Delete
		 metalog = " ************** Azure Network Traffic-Manager Profile Delete ******************* \t"
		 retryLoad1("azure network traffic-manager profile delete " + configARM['GRPNAME'] + " " + configARM['TRAFFIC_MANAGER_PROFILE_NAME'] + " --quiet ", logfile, configARM['TRAFFIC_MANAGER_DELETE'], metalog)
		 
		 # DNS-RECORD-SET  Delete
		 metalog = " ************** Azure Network DNS-RECORD-SET Delete ******************* \t"
		 retryLoad1("azure network dns-record-set delete " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " " + configARM['DNS_ZONE_REC_NAME'] + " " + configARM['DNS_TYPE'] + " --quiet ", logfile, configARM['DNS_RECORDSET_DELETE_FLAG'], metalog)
		 
		 # DNS-ZONE  Delete
		 metalog = " ************** Azure Network DNS ZONE  Show ******************* \t"
		 retryLoad1("azure network dns-zone delete " + configARM['GRPNAME'] + " " + configARM['DNS_ZONE_NAME'] + " --quiet ", logfile, configARM['DNS_ZONE_DELETE_FLAG'], metalog)
		
		 # LOADBALANCER Address-Pool Delete
		 metalog = " ************** Azure Network LoadBalancer Address-Pool Delete ******************* \t"
		 execute_command_with_flag("azure network lb address-pool delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_ADDPOOL_NAME'] + " -q ", logfile, configARM['NETWORKLB_ADDRESSPOOL_DELETE_FLAG'], metalog)
		 
		 # LOADBALANCER FrontEnd-Ip Delete
		 # metalog = " ************** Azure Network LoadBalancer FrontEnd-Ip Delete ******************* \t"
		 # execute_command_with_flag("azure network lb frontend-ip delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_FRONTENDIP_NAME'] + " -q ", logfile, configARM['NETWORKLB_FRONTENDIP_DELETE_FLAG'], metalog)
		 
		 # LOADBALANCER Probe Delete
		 metalog = " ************** Azure Network LoadBalancer Probe Delete ******************* \t"
		 execute_command_with_flag("azure network lb probe delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " " + configARM['LB_PROBE_NAME'] + " -q ", logfile, configARM['NETWORKLB_PROBE_DELETE_FLAG'], metalog)
		 
		 # LOADBALANCER Delete
		 metalog = " ************** Azure Network LoadBalancer Delete ******************* \t"
		 execute_command_with_flag("azure network lb delete " + configARM['GRPNAME'] + " " + configARM['NETWORK_LB_NAME'] + " -q ", logfile, configARM['NETWORKLB_DELETE_FLAG'], metalog)
		
		 # NETWORK VNET SUBNET Delete
		 metalog = "************** Azure Network Vnet Subnet Delete ******************* \t"
		 execute_command_with_flag("azure network vnet subnet delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " " + configARM['NETWORK_SUBNET_NAME'] + " --quiet ", logfile, configARM['NETWORKVNETSUBNET_DELETE_FLAG'], metalog)
		 
		 # # NETWORK ROUTE_TABLE DELETE
		 metalog = "************** Azure Network Route-Table Delete ******************* \t"
		 retryLoad1("azure network route-table delete" + " " + configARM['GRPNAME'] + " " + configARM['ROUTE_TABLE_NAME']+" -q ", logfile, configARM['ROUTE_TABLE_DELETE_FLAG'], metalog)
		 
		 # NETWORK VNET Delete
		 metalog = "************** Azure Network Vnet Delete ******************* \t"
		 execute_command_with_flag("azure network vnet delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_VNET_NAME'] + " --quiet ", logfile, configARM['NETWORKVNET_DELETE_FLAG'], metalog)
		 
		 # NETWORK NSG Delete
		 metalog = "************** Azure Network Nsg Delete ******************* \t"
		 execute_command_with_flag("azure network nsg delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NSG_NAME'] + " --quiet ", logfile, configARM['NETWORKNSG_DELETE_FLAG'], metalog)
		 
		 # NETWORK NIC Delete
		 metalog = "************** Azure Network Nic Delete ******************* \t"
		 execute_command_with_flag("azure network nic delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_NIC_NAME'] + " --quiet ", logfile, configARM['NETWORKNIC_DELETE_FLAG'], metalog)
		 
		 # NETWORK VNET PUBLIC-IP Delete
		 metalog = "************** Azure Network Public-Ip Delete ******************* \t"
		 execute_command_with_flag("azure network public-ip delete " + " " + configARM['GRPNAME'] + " " + configARM['NETWORK_PUBLICIP'] + " --quiet ", logfile, configARM['NETWORKPUBLICIP_DELETE_FLAG'], metalog)

		 # VM COMMANDS
		 metalog = " ************** Azure VM Create ******************* \t"
		 execute_command_with_flag("azure vm create " + configARM['GRPNAME'] + " " + configARM['VM_NAME'] + " -l " + configARM['LOCATION'] + " Windows " + " -q " + configARM['VM_IMAGE']+ " -f " + configARM['VM_NIC']+ " -u " + configARM['VM_USER']+ " -p " + configARM['VM_PASSWORD']+ " -i " + configARM['VM_PUBLICIP']+ " -w " + configARM['VM_PUBLICIPDOMAIN']+ " -F " + configARM['VM_VNET']+ " -P " + configARM['VM_VNET_ADDPREFIX']+ " -j " + configARM['VM_SUBNET']+ " -k " + configARM['VM_SUBNETADDPREFIX']+ " -o " + configARM['VM_STORAGE']+ " -R " + configARM['VM_STORAGECONT'], logfile, configARM['VM_CREATE_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Quick-Create ******************* \t"
		 execute_command_with_flag("azure vm quick-create " + configARM['GRPNAME'] + " " + configARM['VM_QuickNAME'] + " " + configARM['LOCATION'] + " Windows " + " -Q " + configARM['VM_IMAGE_URN']+ " -u " + configARM['VM_USER']+ " -p " + configARM['VM_PASSWORD'], logfile, configARM['VM_QUICKCREATE_FLAG'], metalog)		  
		 metalog = " ************** Azure VM List ******************* \t"
		 execute_command_with_flag("azure vm list " + configARM['GRPNAME'], logfile, configARM['VM_LIST_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Sizes For the Previous Created VM ******************* \t"
		 execute_command_with_flag("azure vm sizes " + " -g " +  configARM['GRPNAME']+ " -n " + configARM['VM_NAME'], logfile, configARM['VM_SIZE_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Sizes For Given Location ******************* \t"
		 execute_command_with_flag("azure vm sizes " + " -l " + configARM['LOCATION'], logfile, configARM['VMLOCATION_SIZE_FLAG'], metalog)	 
		 metalog = " ************** Azure VM Extension Set ******************* \t"
		 execute_command_with_flag("azure vm extension set " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " " + configARM['VM_EXT_NAME']+ " " + configARM['VM_PUBLISHER']+ " " + configARM['VM_VERSION'], logfile, configARM['VM_EXTENSIONSET_FLAG'], metalog)
		 metalog = " ************** Azure VM Extension Get ******************* \t"
		 execute_command_with_flag("azure vm extension get " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, configARM['VM_EXTENSIONGET_FLAG'], metalog) 
		 metalog = " ************** Azure VM Show ******************* \t"
		 execute_command_with_flag("azure vm show " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " --json ", logfile, configARM['VM_SHOW_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Stop ******************* \t"
		 execute_command_with_flag("azure vm stop " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, configARM['VM_STOP_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Start ******************* \t"
		 execute_command_with_flag("azure vm start " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, configARM['VM_START_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Restart ******************* \t"
		 execute_command_with_flag("azure vm restart " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, configARM['VM_RESTART_FLAG'], metalog)	 
		 metalog = " ************** Azure VM Reset-Access ******************* \t"
		 execute_command_with_flag("azure vm reset-access " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " -u " + configARM['VM_NEWUSER']+ " -p " + configARM['VM_PASSWORD']+ " -e " + configARM['VM_EXT_VERSION']+ " -R " + configARM['VM_USER'], logfile, configARM['VM_RESETACCESS_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Disk-Attach-New ******************* \t"
		 execute_command_with_flag("azure vm disk attach-new " + configARM['GRPNAME']+ " " + configARM['VM_QuickNAME']+ " 1 " + " " + configARM['VM_VHD_NAME'], logfile, configARM['VM_DISKATTACHNEW_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Disk Detach ******************* \t"
		 execute_command_with_flag("azure vm disk detach " + configARM['GRPNAME']+ " " + configARM['VM_QuickNAME']+ " " + configARM['VM_LUN'], logfile, configARM['VM_DISKDETACH_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Stop ******************* \t"
		 execute_command_with_flag("azure vm stop " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, configARM['VM_STOPAGAIN_FLAG'], metalog)	 
		 metalog = " ************** Azure VM Generalize ******************* \t"
		 execute_command_with_flag("azure vm generalize " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, configARM['VM_GENERALIZE_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Capture ******************* \t"
		 execute_command_with_flag("azure vm capture " + configARM['GRPNAME']+ " " + configARM['VM_NAME']+ " " + configARM['VM_VHD_PREFIX'], logfile, configARM['VM_CAPTURE_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Get-Instance-View ******************* \t"
		 execute_command_with_flag("azure vm get-instance-view " + configARM['GRPNAME']+ " " + configARM['VM_NAME'], logfile, configARM['VM_GETINSTANCEVIEW_FLAG'], metalog)		 
		 metalog = " ************** Azure VM Deallocate ******************* \t"
		 execute_command_with_flag("azure vm deallocate " + configARM['GRPNAME']+ " " + configARM['VM_QuickNAME'], logfile, configARM['VM_DEALLOCATE_FLAG'], metalog) 
		 
		 metalog = " ************** Azure AvailSet Create ******************* \t"
		 execute_command_with_flag("azure availset create " + configARM['GRPNAME']+ " " + configARM['AVAILSET_NAME']+ " " + configARM['LOCATION'], logfile, configARM['VM_AVAILSET_CREATE_FLAG'], metalog)
		 metalog = " ************** Azure AvailSet List ******************* \t"
		 execute_command_with_flag("azure availset list " + configARM['GRPNAME'], logfile, configARM['VM_AVAILSET_LIST_FLAG'], metalog)
		 metalog = " ************** Azure AvailSet Show ******************* \t"
		 execute_command_with_flag("azure availset show " + configARM['GRPNAME']+ " " + configARM['AVAILSET_NAME']+ " --json ", logfile, configARM['VM_AVAILSET_SHOW_FLAG'], metalog)
		 metalog = " ************** Azure AvailSet Delete ******************* \t"
		 execute_command_with_flag("azure availset delete " + configARM['GRPNAME']+ " " + configARM['AVAILSET_NAME']+ " -q ", logfile, configARM['VM_AVAILSET_DELETE_FLAG'], metalog)
		 
		 # AZURE RESOURCE GROUP Delete
		 metalog = " ************** Azure Resource Group Create ******************* \t"
		 execute_command_with_flag("azure group create " + configARM['GRPNAME'] + " -q ", logfile, configARM['RESOURCEGROUP_DELETE_FLAG'], metalog)
			
							
printstatus()
