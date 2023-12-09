import ipaddress
from intervaltree import IntervalTree
import time
import requests
from flask import Flask, request, jsonify
import argparse

def parse_line(line):
    parts = line.split(',')
    if len(parts) == 4:
        start_ip, end_ip, as_number, isp = parts[0].strip(), parts[1].strip(), int(parts[2]), parts[3].strip()
        return start_ip, end_ip, as_number, isp
    else:
        return None


def ip_to_int(ip):
    return int(ipaddress.IPv4Address(ip))


def populate_interval_tree(file_path):
    interval_tree = IntervalTree()
    i=0
    start=time.time()
    with open(file_path, 'r') as file:
        for line in file:
            parsed_line = parse_line(line)
            if parsed_line:
                start_ip, end_ip, as_number, isp = parsed_line
                start_ip_int, end_ip_int = ip_to_int(start_ip), ip_to_int(end_ip)

                if start_ip_int == end_ip_int:
                    # Handle single IP case
                    interval_tree[start_ip_int:start_ip_int + 1] = (as_number, isp)
                else:
                    # Handle range case
                    interval_tree[start_ip_int:end_ip_int] = (as_number, isp)
            i+=1
    end=time.time()
    gentime=end-start
    print(f'Number of added IP prefix is: {i}, and time to generate is: {gentime} s')

    return interval_tree


def find_isp(ip, interval_tree):
    ip_obj = ipaddress.ip_address(ip)
    ip_int = ip_to_int(ip_obj)
    overlapping_intervals = interval_tree[ip_int]

    for interval in overlapping_intervals:
        return interval.data

    return "Not found"

def download_file():
    url = 'https://raw.githubusercontent.com/sapics/ip-location-db/main/asn/asn-ipv4.csv'
    local_filename = 'asn-ipv4.csv'
    response = requests.get(url, stream=True)
    with open(local_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)




# Example usage
download_file()
print(f'File downloaded!')
interval_tree = populate_interval_tree(r'asn-ipv4.csv')

app = Flask(__name__)
@app.route('/IPlookup', methods=['GET'])
def IPlookup():
    try:
        # Get the IP address from the query parameters
        ip_address = request.args.get('ip')

        # Check if the IP address is provided
        if not ip_address:
            raise ValueError("IP address is required")
        result_as_number, result_isp = find_isp(ip_address, interval_tree)
        result= {
            'ip': ip_address,
            'as_number': result_as_number,
            'as_name': result_isp
        }

        # Return the result in JSON format
        return jsonify(result)

    except Exception as e:
        # Return an error response if an exception occurs
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    # Run the Flask application on port 8080
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080, help='Port number for the Flask app')
    args = parser.parse_args()
    app.run(debug=True, port=args.port)





