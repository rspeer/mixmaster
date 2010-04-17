import urllib, os, sys, gzip
import cPickle as pickle

def open_or_download(filename, URL):
    if not os.access(filename, os.F_OK):
        if not prompt_for_download(filename, URL):
            raise SystemExit
    return pickle.load(open(filename))

def prompt_for_download(filename, URL):
    print """
You don't have a file here called 'anagram_data.pickle'. It should be available
from the following URL:
"""
    print '\t'+URL
    print
    print "This will be a large download -- around 250 megabytes."
    response = raw_input("Download it to the current directory? [Y/n] ")
    if response == '' or response.lower().startswith('y'):
        return download(URL, filename)
    else:
        print "Not downloading. The program will have to exit now."
        return False

def _mkdir(newdir):
    """
    http://code.activestate.com/recipes/82465/
    
    works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("A file with the same name as the desired " \
                      "directory, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        if tail:
            os.mkdir(newdir)


def download(rem_filename, dest_filename):
    dir = os.path.dirname(dest_filename)
    member = os.path.basename(dest_filename)
    _mkdir(dir)
    def dlProgress(count, blockSize, totalSize):
        percent = int(count*blockSize*100/totalSize)
        sys.stdout.write("\r" + rem_filename + "... %2d%%" % percent)
        sys.stdout.flush()
    urllib.urlretrieve(rem_filename, dest_filename, reporthook=dlProgress)
    print
    print "Extracting."
    os.system('gunzip %s' % dest_filename)
    return True


