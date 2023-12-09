# Interleave treeIP-Lookup
This Program Will work as a web service. Firstly, run sh install_dependencies.sh file to install all needed libraries. Then run IP-Lookup.py -p <webservice_port>.

# Functionality
The program will download the latest IP/AS database from a free repository: https://raw.githubusercontent.com/sapics/ip-location-db/main/asn. Then generates a Interval tree to run fast lookup function. Lookup time is about 1 ms for 385k IPprefix.

# Calling the Webservice
You can Call IPlookup webservice via http://<Host-name>:8080/IPlookup/ip=x.x.x.x that x.x.x.x is requested ip. Http method is Get.

# Output
the output is a json tuple and send back IP, AS Number, and AS Name.

# run as service
You can run the program as a service, or by directly running python3 IP-lookup -p <webservice_port, default is 8080>

# Libraries
intervaltree==3.1.0
Flask==2.0.1
requests==2.26.0
