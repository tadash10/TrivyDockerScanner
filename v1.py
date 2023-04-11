import subprocess
import json
import argparse
import os
import sys


def check_trivy():
    """
    Checks if Trivy is installed and available in the PATH.
    """
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(['trivy', '--version'], stdout=devnull, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print('Trivy not found. Please make sure Trivy is installed and available in the PATH.', file=sys.stderr)
        sys.exit(1)


def disclaimer():
    """
    Displays a disclaimer message before running the script.
    """
    print('*** DISCLAIMER ***')
    print('This script uses Trivy to scan Docker images for vulnerabilities. '
          'Please make sure Trivy is up-to-date and review its documentation for information on its limitations.')
    print('*** END DISCLAIMER ***\n')


def scan_image(image_name):
    """
    Scans the specified Docker image for vulnerabilities using Trivy.
    """
    command = f"trivy --quiet --format json {image_name}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        raise ValueError(f"Error scanning {image_name}: {error}")
    return json.loads(output)


def generate_report(image_name, vulnerabilities):
    """
    Generates a report on the specified Docker image's vulnerabilities.
    """
    if not vulnerabilities:
        print(f"No vulnerabilities found in {image_name}")
        return
    print(f"Vulnerabilities found in {image_name}:")
    for vulnerability in vulnerabilities:
        print(f"- {vulnerability['VulnerabilityID']} ({vulnerability['PkgName']}): {vulnerability['Severity']}")


def scan_images(images):
    """
    Scans the specified Docker images for vulnerabilities using Trivy.
    """
    check_trivy()
    for image_name in images:
        vulnerabilities = scan_image(image_name)
        generate_report(image_name, vulnerabilities)


def main():
    parser = argparse.ArgumentParser(description="Scan Docker images for vulnerabilities using Trivy")
    parser.add_argument("images", metavar="IMAGE", type=str, nargs="+",
                        help="Docker images to scan for vulnerabilities")
    args = parser.parse_args()
    scan_images(args.images)


if __name__ == "__main__":
    disclaimer()

    # Menu
    print("What would you like to do?")
    print("1. Scan Docker images for vulnerabilities")
    print("2. Exit")
    choice = input("Enter your choice (1/2): ")
    
    while choice not in ["1", "2"]:
        print("Invalid choice.")
        choice = input("Enter your choice (1/2): ")
    
    if choice == "1":
        main()
    else:
        print("Exiting...")

    # Your name
    print("BY T1")
