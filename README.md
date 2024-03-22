# gve_devnet_meraki_switch_port_use_report

The script creates reports in CSV format, showcasing low switch port usage for MS devices in your Meraki Organization

## Contacts

* Rey Diaz

## Solution Components

* Meraki

#### Features

- Fetches a list of Meraki switches in an organization.
- Retrieves status and usage data for all ports on each switch.
- Displays switch and port information in a formatted table in the console.
- Filters out ports with total data usage below a specified threshold.
- Exports the filtered list of low usage ports to a CSV file.
- Exports the filtered list of low usage ports to a CSV file.

## Prerequisites

#### Meraki API Keys

In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:

1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.

> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization).

> Note: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).

## Installation/Configuration

1. **Clone this repository**

   use `git clone [repository name]`. To find the repository name, click the green `Code` button above the repository files. Then, the dropdown menu will show the https domain name. Click the copy button to the right of the domain name to get the value to replace [repository name] placeholder.

2. **Install Python Packages**

   Navigate to the App directory and install the required Python packages using the following command:

```sh {"id":"01HR572BBEWRF5M460ZBWDDZ3Z"}
pip install -r requirements.txt
```

3. **Configure Environment Variables**

Create a `.env` file in the App directory with the following variables:

```yaml {"id":"01HR57GN6P4VMH1HSD63Q3Y8DR"}
API_KEY=your_meraki_api_key
ORG_ID=your_organization_id
BASE_URL=https://api.meraki.com/api/v1
USAGE_THRESHOLD_KB=your-usage-threshold
EXCLUDED_VLAN=vlan-to-exclude
```

Replace `your_meraki_api_key` , `your_organization_id` , `your-usage-threshold` and `vlan-to-exclude` with your actual Meraki API key, organization ID, and usage threshold.

## Usage

1. **Set Environment Variables**

   Ensure your `.env` file is correctly configured as mentioned in the **Installation** section.

2. **Run the Script**

   Execute the script from the terminal or command prompt:

```sh {"id":"01HR57840776GTBKEHH0AP0QFR"}
$ python3 program-name.py
```

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:

Please note: This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
