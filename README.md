* Install [Python2.7][0] and make sure python is added in env variabales
* config.py is the config file
* change the following in config.py
	* PUBLISHSETTINGS_FILE <\<path of publish setting file>>	`Hint: Downloaded path of publishsetting file`
	* LOG_FILE <\<path for the log file>>			`Hint: C:\log files\log.json`
	* FILE_PATH <\<path for the Json log file>>		`Hint: C:\json files\export.json`
	* CERT_FILE <\<path for the .pem file>>
	* SUBSCRIPTION_ID <\<Subscription id of azure account>>	`Hint: Subscription id mentioned in .publishsettings `
	* IMAGE_NAME <\<Valid linux Image name>>	`Hint: Image name obtained from vm image list and OS is LINUX `
	* WIN_IMAGE_NAME <\<Valid windows Image name>>	`Hint: Image name obtained from vm image list and OS is WINDOWS `
	* VM_COMM_IMAGE_NAME <\<Valid community Image name>>	`Hint: VMDepo image url obtained from vmdepo in virtual mach->images from portal`
	* VM_DISK_SOURCE_PATH <\<source disk path for vm>> `Hint: media link obtained from vm disk show diskname`
	* IMAGE_BLOB_URL <\<destination image path for images creation>> `Hint: conatinerUrl/vm-images/image.vhd`
	* DISK_IMAGE_BLOB_URL <\<destination disk path for disk creation>> `Hint: conatinerUrl/disks/disk.vhd`
	* VM_DISK_ATTACH_BLOB_URL <\<destination disk path for disk attach>> `Hint: conatinerUrl/disks/disk.vhd`
	
* open cmd prompt and cd to proj folder(where AutomationScript.py and config.py are present)
* run the script using following command "python AutomationScript.py"

# Note 
* if GLOBAL_FLAG=0 then only those command which has its flag value as 1 will execute
* if GLOBAL_FLAG=1 the all the commands will execute
* if GLOBAL_FLAG=0 mode change flag variables(present below #**FLAG VALUES**) to run or skip commands
* To run the python script against a downloaded repo, replace azure with node bin/azure in all the commands,
  for eg : the downloaded xplat code is in D:\azure-xplat , place the scripts inside the D:\azure-xplat , then replace the commands "azure" with "node bin/azure" in AutomationScript.py file.

[0]: http://www.python.org/download/releases/2.7.3/
