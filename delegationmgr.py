import argparse
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/gmail.settings.sharing', 'https://www.googleapis.com/auth/gmail.settings.basic']

parser = argparse.ArgumentParser(
    prog='delegationmgr',
    description='Manages Delegations in Gmail',
    usage='%(prog)s -h | -l EMAIL | -c EMAIL -o EMAIL | -d EMAIL -o EMAIL')

mutexParserGroup = parser.add_mutually_exclusive_group()
mutexParserGroup.add_argument('-c', '--create', help='create delegation access for specified EMAIL address', metavar='EMAIL')
mutexParserGroup.add_argument('-d', '--delete', help='deletes delegation access for specified EMAIL address', metavar='EMAIL')
mutexParserGroup.add_argument('-l', '--list', help='lists delegation access on specified EMAIL address', metavar='EMAIL' )

parser.add_argument('-o', '--on', help='specify target EMAIL address to grant/revoke delegation access to/from', metavar='EMAIL')

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

if (args.create or args.delete) and not args.on:
    parser.error("-o/--on is required when using -c/--create and -d/--delete")

# main body of code, a beaut int he.

# Construct credentials to be used

SERVICE_ACCOUNT_FILE = 'service_account_key.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# different options for what we can be doing
if args.create:
    # Create delegation
    # Requires
    # - args.create (the email address which will be given access)
    # - args.on (the email address which will have access granted to

    # first setup delegated creds
    delegated_credentials = credentials.with_subject(args.on)

    # have a bash and see what happens
    try:
        service = build('gmail', 'v1', credentials=delegated_credentials)

        # Email address of how is getting permission to manage the inbox 

        body = {
            'delegateEmail': args.create,
            'verificationStatus': 'accepted'
            }
        request = service.users().settings().delegates().create(userId='me', body=body).execute()
        print(request)
        

    except HttpError as error:
        print(f'An error occurred: {error}')

elif args.delete:
    # deletes delegations
    # Requires
    # - args.delete (the email address whose access will be revoked)
    # - args.on (the email address which will no longer be able to be accessed)

    delegated_credentials = credentials.with_subject(args.on)

    try:
        service = build('gmail', 'v1', credentials=delegated_credentials)

        # Email address of how is getting permission to manage the inbox 
        request = service.users().settings().delegates().delete(userId='me', delegateEmail=args.delete).execute()
        print(request)
        

    except HttpError as error:
        print(f'An error occurred: {error}')

elif args.list:
    delegated_credentials = credentials.with_subject(args.list)

    try:
        service = build('gmail', 'v1', credentials=delegated_credentials)

        # Email address of how is getting permission to manage the inbox 
        request = service.users().settings().delegates().list(userId='me').execute()
        print(request)
        

    except HttpError as error:
        print(f'An error occurred: {error}')