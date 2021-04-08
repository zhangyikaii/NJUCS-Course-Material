import requests
import sys, getopt
import argparse

parser = argparse.ArgumentParser(description='SICP Submission Script')
parser.add_argument('-s', '--stuid', help='provide your student ID')
parser.add_argument('-n', '--stuname', help='provide your name')
args = parser.parse_args()
aname = 'lab08'
files = {
    'expr.py': open('expr.py', 'rb')
}

submit_url = f'http://114.212.84.18:5000/assignment/{aname}/submit'
params = {'stuid': args.stuid, 'stuname': args.stuname}
try:
    response = requests.post(submit_url, data=params, files=files)
    print(response.text)
    if response.status_code >= 500:
        print("Please contact TAs to solve this problem.")
    elif response.status_code >= 400:
        print("Please make sure you haven't changed submit.py.")
except requests.exceptions.ConnectionError:
    print("Connection error. Please check your network.")
