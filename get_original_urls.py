import sys
import tqdm
from flickr import FlickrAPI

auth_file = 'AUTH.key'
auth = dict([map(lambda x: x.strip(), l.split('=')) \
        for l in open(auth_file).readlines()])


if not 'KEY' in auth:
    print 'please create an api key in the flickr app-garden and add to AUTH.key'
    raise

if not 'TOKEN' in auth:
    f = FlickrAPI(api_key=auth['KEY'],
              api_secret=auth['SECRET'],
              callback_url='http://www.example.com/callback/')
    visit = f.get_authentication_tokens()['auth_url']
    print 'please visit %s  and add TOKEN and VERIFIER to AUTH.key'%visit 
    raise

f = FlickrAPI(api_key=auth['KEY'],
          api_secret=auth['SECRET'],
          oauth_token=auth['TOKEN'],
          oauth_token_secret=auth['VERIFIER'])

page = 1
photos_per_page = 500
all_photos = []

stop_next = False
while True:
    print '\r%d'%len(all_photos),
    sys.stdout.flush()

    params = {'page': page, 'per_page' : photos_per_page, 'user_id' : 'me',
              'extras': 'original_format'}
    try:
        result = f.get("flickr.people.getPhotos", params=params)
    except:
        continue
    ps = result['photos']['photo']
    all_photos.extend(ps)
    page+=1
    if stop_next:
        break
    if len(ps) != photos_per_page:
        stop_next = True

urls = []
for a in tqdm.tqdm(all_photos):
    vals = a['farm'], a['server'], a['id'],a['originalsecret'],a['originalformat']
    url = 'https://farm%s.staticflickr.com/%s/%s_%s_o.%s'% vals
    urls.append(url)

outfile = 'all_original_urls.txt'
with open(outfile, 'w') as fh:
    fh.writelines([l+'\n' for l in urls)
print 'done! all urls in %s'%outfile
