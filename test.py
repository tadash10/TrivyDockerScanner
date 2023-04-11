import subprocess
import json
import argparse

def scan_image(image_name):
    """
    Scans the specified Docker image for vulnerabilities using Trivy
    """
    command = f"trivy --quiet --format json {image_name}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        raise ValueError(f"Error scanning {image_name}: {error}")
    return json.loads(output)

def generate_report(image_name, vulnerabilities):
    """
    Generates a report on the specified Docker image's vulnerabilities
    """
    if not vulnerabilities:
        print(f"No vulnerabilities found in {image_name}")
        return
    print(f"Vulnerabilities found in {image_name}:")
    for vulnerability in vulnerabilities:
        print(f"- {vulnerability['VulnerabilityID']} ({vulnerability['PkgName']}): {vulnerability['Severity']}")
        
def main():
    parser = argparse.ArgumentParser(description="Scan Docker images for vulnerabilities using Trivy")
    parser.add_argument("images", metavar="IMAGE", type=str, nargs="+",
                        help="Docker images to scan for vulnerabilities")
    args = parser.parse_args()
    
    for image_name in args.images:
        vulnerabilities = scan_image(image_name)
        generate_report(image_name, vulnerabilities)

if __name__ == "__main__":
    main()
