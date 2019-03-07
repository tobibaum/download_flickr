import os
import tqdm
import time
import urllib
import StringIO
import numpy as np
import pandas as pd
from PIL import Image
from multiprocessing import Pool
from matplotlib import pyplot as plt

n_workers = 224

def transform_url(url):
    return '.'.join(url.split('://')[1].replace('/','_').split('.')[:-1])+'.jpg'

def download_img(url, basedir='/disk4/tobi/data/tobis_photos/images'):
    try:
        outname = transform_url(url)
        outfile = os.path.join(basedir, outname)
        if not os.path.exists(outfile):
            try:
                img_cont = urllib.urlopen(url).read()
                img_pil = Image.open(StringIO.StringIO(img_cont))
                if img_pil.mode != 'RGB':
                    img_pil = img_pil.convert('RGB')
                img_pil.save(outfile, quality=95)
                print outfile
            except IOError:
                pass
            except urllib.ssl.CertificateError:
                pass
            except EOFError:
                pass
    except Exception as e:
        print url
        print 'new exception', e

def main():
    print 'load tsv...',
    t = time.time()
    img_file = 'all_original_urls.txt'
    with open(img_file) as fh:
        urls = [l.strip() for l in fh.readlines()]
    t = time.time() - t
    print '\ttook %.4fs'%t

    p = Pool(n_workers)
    p.map(download_img, urls)

if __name__ == '__main__':
    main()
