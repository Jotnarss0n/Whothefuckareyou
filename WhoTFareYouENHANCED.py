import subprocess
import re
import sys
import os
import time
from urllib.parse import urlparse

def validate_input(input_value):
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    url_pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    if re.match(ip_pattern, input_value):
        return "ip"
    elif re.match(domain_pattern, input_value):
        return "domain"
    elif re.match(url_pattern, input_value):
        return "url"
    else:
        return None

def run_command(command, tool_name, num_dots):
    sys.stdout.write("Running {}.".format(tool_name))
    sys.stdout.flush()
    
    for _ in range(num_dots):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.25)
    
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        sys.stdout.write(" completed.\n")
        sys.stdout.flush()
        return result
    except subprocess.CalledProcessError as e:
        sys.stdout.write(" Error: {}.\n".format(e.output))
        sys.stdout.flush()
        return None

def main():
    input_value = input("Enter a domain name, IP address, URL, or subdomain: ")
    
    input_type = validate_input(input_value)
    if not input_type:
        print("Invalid input. Please provide a valid domain name, IP address, URL, or subdomain.")
        return
    
    if input_type == "url":
        domain = urlparse(input_value).netloc
    else:
        domain = input_value

    # Create directory to save the results
    directory = domain
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    tools = [
        ("whois", "Whois", 15),
        ("nslookup", "Nslookup", 12),
        ("dig", "Dig", 17),
        ("dnsrecon -d", "Dnsrecon", 12)
    ]
    
    for tool, tool_name, num_dots in tools:
        command = "{} {}".format(tool, domain)
        tool_output = run_command(command, tool_name, num_dots)
        if tool_output:
            filename = "{}/{}-{}.md".format(directory, tool_name.lower(), domain)
            with open(filename, "w") as file:
                file.write("### {}\n\n```\n{}\n```\n".format(tool_name, tool_output))

    if input_type == "url":
        wget_command = "wget -r -P {} {}".format(directory, input_value)
        run_command(wget_command, "wget", 16)

    print("Script executed successfully. Check the .md files in the {} folder.".format(directory))

if __name__ == "__main__":
    main()
