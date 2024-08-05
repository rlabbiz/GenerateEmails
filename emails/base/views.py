from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import threading

# Create your views here.

def openEmails(email):
    subprocess.run(['python3', '/home/rlabbiz/Desktop/generateEmails/emails/base/script.py', email])

@csrf_exempt
def emails(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)
            current_emails = data.get('emails', [])

            # Print emails to the console
            # print('Emails received:', current_emails[0])
            for email in current_emails:
                threading.Thread(target=openEmails, args=(email,)).start()

            # Return a success response
            return HttpResponse('ok', status=200)

        except json.JSONDecodeError:
            return HttpResponse('error', status=400)

    return HttpResponse('erorr', status=405)

def send(request):
    email_list = {}
    seen_lines = set()  # Set to track seen lines

    # Open the file for reading
    with open('/home/rlabbiz/Desktop/generateEmails/emails/base/emails.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            # Check if line has already been seen
            if line in seen_lines:
                continue  # Skip duplicate lines
            seen_lines.add(line)  # Add line to seen set

            # Split email and password
            try:
                email, password = line.split(':')
            except ValueError:
                print(f"Skipping malformed line: {line}")
                continue

            # Extract domain from email
            try:
                domain = email.split('@')[1]
            except IndexError:
                print(f"Skipping line with invalid email format: {line}")
                continue

            # Initialize the list for the domain if it doesn't exist
            if domain not in email_list:
                email_list[domain] = []

            # Add the email:password string to the appropriate domain array
            email_list[domain].append(f"{email}:{password}")

    return JsonResponse(email_list)
