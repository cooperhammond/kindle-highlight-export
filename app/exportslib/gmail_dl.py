import os
import sys
import traceback
import imaplib

from imbox import Imbox


def test_gmail_login(username, password):
    try:
        inbox = Imbox(
            'imap.gmail.com',
            username=username,
            password=password,
            ssl=True,
            ssl_context=None,
            starttls=False
        )
        inbox.logout()
        return True
    except imaplib.IMAP4.error:
        return False


def retrieve_kindle_highlight_files(username, password, dl_directory):

    file_locations = []

    inbox = Imbox(
                'imap.gmail.com',
                username=username,
                password=password,
                ssl=True,
                ssl_context=None,
                starttls=False
            )

    kindle_messages = inbox.messages(subject='Kindle Export for')

    for uid, message in kindle_messages:
        inbox.mark_seen(uid)

        for index, attachment in enumerate(message.attachments):
            try:
                filename = attachment.get('filename')

                if not os.path.exists(dl_directory):
                    os.makedirs(dl_directory)

                dl_path = f"{dl_directory}/{filename}"
                file_locations.append(os.path.abspath(dl_path))
                
                with open(dl_path, 'wb') as fp:
                    fp.write(attachment.get('content').read())
            except:
                pass
                traceback.print_exc()

    inbox.logout()

    return file_locations