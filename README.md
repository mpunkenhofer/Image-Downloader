# Image-Downloader
A python script which downloads all images of a given website(s)

usage: ./img_downloader [--todir dir] [--filter regex] url [url ...]

## Script flags
##### *--todir* dir
_dir_ is the directory of the script output - the downloaded images will be there.
If this flag is omitted the images will be downloaded to the directory where the script was run from. 
##### *--filter* regex
_regex_ can be a regular expression (for syntax see [here](https://docs.python.org/2/library/re.html#regular-expression-syntax)) 
Any image link the script finds on the website(s) that matches in any way the regex pattern will be filtered out - the image will not be downloaded.
If the regular expression is not valid, it will be ignored and no images will be filtered out. 

## Details
### Python version
python 3.4
### File output
For now the original file names are being discarded - a uuid for each file is generated which serves as the file name - this was done in order to avoid name collisions.