import subprocess
import json
import argparse
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    report = ''
    if not vulnerabilities:
        report += f"No vulnerabilities found in {image_name}\n"
    else:
        report += f"Vulnerabilities found in {image_name}:\n"
        for vulnerability in vulnerabilities:
            report += f"- {vulnerability['VulnerabilityID']} ({vulnerability['PkgName']}): {vulnerability['Severity']}\n"
    return report


def scan_images(images):
    """
    Scans the specified Docker images for vulnerabilities using Trivy.
    """
    check_trivy()
    report = ''
    for image_name in images:
        vulnerabilities = scan_image(image_name)
        report += generate_report(image_name, vulnerabilities)
    return report


def send_email(to_address, subject, body):
    """
    Sends an email with the specified subject and body to the specified email address.
    """
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'your_email_address@gmail.com'  # replace with your email address
    smtp_password = 'your_email_password'  # replace with your email password

    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_address
    message['Subject'] = subject
    message.attach(MIMEText(body))

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(smtp_username, to_address, message.as_string())


def main():
    parser = argparse.ArgumentParser(description="Scan Docker images for vulnerabilities using Trivy")
    parser.add_argument("images", metavar="IMAGE", type=str, nargs="+",
                        help="Docker images to scan for vulnerabilities")
    parser.add_argument("--email", type=str, required=True,
                        help="Email address to send the scan report to")
   
