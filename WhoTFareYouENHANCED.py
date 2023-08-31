import os
import sys
import subprocess
import re
import time

def validate_input(input_value):
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", input_value):
        return "ip"
    elif re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", input_value):
        return "domain"
    elif re.match(r"^[a-zA-Z0-9.-]+$", input_value):
        return "subdomain"
    elif re.match(r"^https?://", input_value):
        return "url"
    else:
        return "invalid"

def run_command(tool, command, directory, input_value):
    try:
        print(f"Running {tool}", end="")
        sys.stdout.flush()
        sleep_dots = '..............'
        for dot in sleep_dots:
            sys.stdout.write(dot)
            sys.stdout.flush()
            time.sleep(0.25)
        result = subprocess.run(command.split() + [input_value], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        result_stdout = result.stdout
        sanitized_input_value = re.sub(r"https?://", "", input_value).replace("/", "_")
        with open(f"{directory}/{tool}-{sanitized_input_value}.md", "w") as f:
            f.write(f"### {tool}\n\n```\n{result_stdout}\n```\n")
        print(" completed.")
    except Exception as e:
        print(f"Error running {tool}")
        with open(f"{directory}/{tool}-{sanitized_input_value}.md", "w") as f:
            f.write(f"### {tool}\n\nError:\n```\nError running {tool}\n```\n")

def main():
    input_value = input("Enter a domain name, IP address, URL, or subdomain: ")
    input_type = validate_input(input_value)
    if input_type == "invalid":
        print("Invalid input. Please provide a valid domain name, IP address, URL, or subdomain.")
        return
    
    directory = re.sub(r"https?://", "", input_value)
    directory = re.sub(r"/.*", "", directory)
    os.makedirs(directory, exist_ok=True)
    
    tools = {
        "Whois": "whois",
        "Nslookup": "nslookup",
        "Dig": "dig",
        "Dnsrecon": "dnsrecon -d",
    }
    
    for tool, command in tools.items():
        run_command(tool, command, directory, input_value)
    
    # Run wget -r
    if input_type == "url":
        print("Running wget", end="")
        sys.stdout.flush()
        sleep_dots = '..............'
        for dot in sleep_dots:
            sys.stdout.write(dot)
            sys.stdout.flush()
            time.sleep(0.25)
        subprocess.run(["wget", "-r", "-P", directory, input_value], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        print(" completed.")
    
    print(f"Script executed successfully. Check the .md files in the {directory} folder.")

if __name__ == "__main__":
    main()
