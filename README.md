# IP-Lookup
This Program Will work as web service. Just run install_dependencies.sh file to install every python libraries. Then run IP-Lookup.py .

# Functionality
The program will download the latest IP/AS database from a free repository: https://raw.githubusercontent.com/sapics/ip-location-db/main/asn. Then generates a Interval tree to run fast lookup function. Lookup time is about 1 ms for 385k IPprefix.

# Calling webservice
You can Call IPlookup webservice via http://<Host-name>:8080/IPlookup/ip=x.x.x.x that x.x.x.x is requested ip. Http method is Get.

# Output
the output is a json tuple and send back IP, AS Number, and AS Name.

# run as service
You can run the program as a service.
