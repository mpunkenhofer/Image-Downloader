# Author: Mathias Punkenhofer
# Mail: newsgroups.mpunkenhofer@gmail.com
# Date: 08 March 2017

import sys
import os
import re
import urllib.request
import urllib.error
import datetime
import collections
import uuid


def download_images(img_urls, dest_dir=''):
    """Downloads the images from the given urls"""
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for i, url in enumerate(img_urls):
        print('Status: Downloading %d of %d: ' % (i + 1, len(img_urls)) + img_urls[i].split(r'/')[-1] + ' ...')
        # use uuids for filenames for now (in future calculate hash from downloaded file an
        # check if we need a local copy or if we have one already
        filename = str(uuid.uuid4())
        urllib.request.urlretrieve(url, os.path.join(dest_dir, filename))

    return


def process_website(site, url=''):
    """Tries to find all image links on a given website (html)"""
    urls = []

    if site:
        print('Status: Processing website: ', url, ' ...')

        url_matches = re.findall(r'\"(\/\/\S+((\.png)|(\.gif)|(\.jpg)))', str(site))

        urls = set(['http:' + match[0] for match in url_matches])

    return urls


def get_website(url, dest_dir=''):
    """Tries to download a given website (html)"""
    website = ''
    try:
        print('Status: Downloading website: ', url, ' ...')

        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        request = urllib.request.Request(url, None, headers)  # The assembled request

        urlfile = urllib.request.urlopen(request)
        website = urlfile.read()
        urlfile.close()
    except ValueError:
        print('Error: Unknown url format: ', url)
    except IOError:
        print('Error: Couldn\'t read the url: ', url)

    if website:
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        timestamp = str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
        website_filename = timestamp + '_'

        website_filename_match = re.search(r'https?:\/\/(www.)?([^\/\s]*)', url)

        if website_filename_match:
            website_filename += website_filename_match.group(2)

        try:
            website_filename += '.html'
            website_file = open(os.path.join(dest_dir, website_filename), mode='wb')
            website_file.write(website)
        except IOError:
            print('Error: failed writing website file!')

    return process_website(website, url)


def main():
    # TODO remove debug output
    print('Debug version')

    args = collections.deque(sys.argv[1:])

    if not args:
        print('usage: ./img_downloader url [url ...] [--todir dir] [--filter regex]')

    todir_s = filter_s = ''
    urls = []

    while args:
        arg = args.popleft()

        if arg == '--todir':
            if args:
                todir_s = args.popleft()
            else:
                print('Error: --todir missing a target directory!')
                print('usage: ./img_downloader [--todir dir] [--filter regex] url [url ...]')
                sys.exit(1)
        elif arg == '--filter':
            if args:
                filter_s = args.popleft()
            else:
                print('Error: --filter missing a regex string!')
                print('usage: ./img_downloader [--todir dir] [--filter regex] url [url ...]')
                sys.exit(1)
        else:
            urls.append(arg)

    if not urls:
        print('Error: missing one or more website urls!')
        print('usage: ./img_downloader [--todir dir] [--filter regex] url [url ...]')
        sys.exit(1)

    # TODO remove debug output
    print('Passed Arguments:')
    print('--todir: ', todir_s)
    print('--filter: ', filter_s)
    print('urls: ', urls)

    image_urls = []
    for url in urls:
        image_urls += get_website(url, todir_s)

    download_images(image_urls, todir_s)


if __name__ == '__main__':
    main()
