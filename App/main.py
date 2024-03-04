"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from dotenv import load_dotenv
import os
import requests
from rich.console import Console
from rich.table import Table
import csv

# Explicitly specify the path to your .env file
dotenv_path = './.env'
load_dotenv(dotenv_path=dotenv_path)

# API configuration and usage threshold
API_KEY = os.getenv('API_KEY')
ORG_ID = os.getenv('ORG_ID')
BASE_URL = os.getenv('BASE_URL')
USAGE_THRESHOLD_KB = int(os.getenv('USAGE_THRESHOLD_KB', 300000))  # Default to 300000 KB if not specified

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

console = Console()

def get_switches(org_id):
    url = f'{BASE_URL}/organizations/{org_id}/devices'
    response = requests.get(url, headers=headers)
    return [device for device in response.json() if device['model'].startswith('MS')]

def get_port_statuses(serial):
    timespan = 2592000  # 30 days in seconds
    url = f'{BASE_URL}/devices/{serial}/switch/ports/statuses'
    params = {'timespan': timespan}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        console.print(f"Failed to fetch port statuses for device {serial} with timespan of 30 days.", style="bold red")
        return []

def display_switches_with_ports(switches):
    for switch in switches:
        ports = get_port_statuses(switch['serial'])
        table = Table(title=f"Switch: {switch['name']} (Serial: {switch['serial']})", show_header=True, header_style="bold magenta")
        table.add_column("Network ID", style="dim")
        table.add_column("Switch Name")
        table.add_column("Port ID")
        table.add_column("Status")
        table.add_column("Total Usage (KB)", justify="right")
        table.add_column("Sent (KB)", justify="right")
        table.add_column("Received (KB)", justify="right")
        
        for port in ports:
            usage = port.get('usageInKb', {'total': 'N/A', 'sent': 'N/A', 'recv': 'N/A'})
            total_usage = str(usage.get('total', 'N/A'))
            sent_usage = str(usage.get('sent', 'N/A'))
            received_usage = str(usage.get('recv', 'N/A'))
            status = port.get('status', 'N/A')
            status_style = "green" if status == "Connected" else "red"
            
            table.add_row(
                switch.get('networkId', 'N/A'), 
                switch.get('name', 'N/A'),
                port.get('portId', 'N/A'), 
                f"[{status_style}]{status}[/]",
                total_usage,
                sent_usage,
                received_usage
            )
        console.print(table)

def filter_and_export_low_usage_ports_to_csv(switches, usage_threshold_kb, output_csv_file):
    with open(output_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Network ID", "Switch Name", "Port ID", "Status", "Total Usage (KB)", "Sent (KB)", "Received (KB)"])
        
        for switch in switches:
            ports = get_port_statuses(switch['serial'])
            for port in ports:
                usage = port.get('usageInKb', {'total': 0, 'sent': 0, 'recv': 0})
                total_usage = usage.get('total', 0)
                
                if total_usage < usage_threshold_kb:
                    writer.writerow([
                        switch.get('networkId', 'N/A'), 
                        switch.get('name', 'N/A'),
                        port.get('portId', 'N/A'), 
                        port.get('status', 'N/A'),
                        str(total_usage),
                        str(usage.get('sent', 'N/A')),
                        str(usage.get('recv', 'N/A'))
                    ])

def main():
    switches = get_switches(ORG_ID)
    if switches:
        display_switches_with_ports(switches)
        filter_and_export_low_usage_ports_to_csv(switches, USAGE_THRESHOLD_KB, "low_usage_ports.csv")
        console.print(f"Low usage ports have been exported to 'low_usage_ports.csv'.", style="bold green")
    else:
        console.print("No switches found or failed to retrieve switches.", style="bold red")

if __name__ == "__main__":
    main()
