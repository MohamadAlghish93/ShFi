# system libs
import argparse
import random
import string
import os, time, shutil

# Web interface UI
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server, config

_root_folder = './data'


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return result_str


def share_files():
    random_string = get_random_string(5)
    upload_folder = f'{_root_folder}/{random_string}/'

    files_source = file_upload("Select files to share:", accept="*", required=True, multiple=True)

    for file_source in files_source:

        if not os.path.isdir(upload_folder):
            os.mkdir(upload_folder)

        filename, file_extension = os.path.splitext(file_source['filename'])
        file_path = f'{upload_folder}{filename}{file_extension}'
        with open(file_path, "wb") as file:
            file.write(file_source['content'])

    files = os.listdir(upload_folder)
    files = [f"{upload_folder}{f}" for f in files if os.path.isfile(f"{upload_folder}{f}")]  # Filtering only the files.

    list_files_table = [['Type', 'Content']]
    for file in files:
        t_filename, t_file_extension = os.path.splitext(file)
        in_file = open(file, "rb")  # opening for [r]eading as [b]inary
        data_file = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
        in_file.close()
        list_files_table.append([t_filename, put_file(f'{t_filename}{t_file_extension}', data_file)])

        # Table Output
    put_table([
        [put_markdown('**Your Reference No**'), put_markdown(f'`{random_string}`')]
    ])
    put_table(list_files_table)


def open_share():
    # Password input
    search_folder = input("Your Reference No.")
    download_folder = f'{_root_folder}/{search_folder}/'

    files = os.listdir(download_folder)
    files = [f"{download_folder}{f}" for f in files if
             os.path.isfile(f"{download_folder}{f}")]  # Filtering only the files.

    list_files_table = [['Type', 'Content']]
    for file in files:
        t_filename, t_file_extension = os.path.splitext(file)
        in_file = open(file, "rb")  # opening for [r]eading as [b]inary
        data_file = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
        in_file.close()
        list_files_table.append([t_filename, put_file(f'{t_filename}{t_file_extension}', data_file)])

    # Table Output
    put_table(list_files_table)


# @config(theme='dark')
def main():
    try:
        run_js("""
            $('head').append('<style>.container {max-width: 1080px;}</style>')
            """)
        # Drop-down selection
        action_type = select('Select Service?', ['New Share Files', 'Open Share Files'])

        if not os.path.isdir(_root_folder):
            os.mkdir(_root_folder)

        Thirty_days_ago = time.time() - (30 * 86400)

        ##
        for i in os.listdir(_root_folder):
            path = os.path.join(_root_folder, i)

            if os.stat(path).st_mtime < Thirty_days_ago:

                if os.path.isfile(path):
                    try:
                        os.remove(path)
                    except:
                        print("Could not remove file:", i)

                else:
                    try:
                        shutil.rmtree(path)

                    except:
                        print("Could not remove directory:", i)
        ###

        if action_type == 'New Share Files':
            share_files()
        else:
            open_share()

    except Exception as e:
        put_text(f'Error : {e}').style('color: red;')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, debug=False, port=args.port, cdn=False)
    # start_server(main, debug=True, port=8080, cdn=False)
