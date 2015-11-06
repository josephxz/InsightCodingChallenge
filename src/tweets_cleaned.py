import sys
import json
import re


def main():
    tweet_file = open(sys.argv[1])

    #number tweets that contain non-ascii unicode
    uninum = 0

    #pattern that matches unicode no in the range \u0020-\u007F
    re_pattern = re.compile(u'[^\u0020-\u007F]', re.UNICODE)
    for line in tweet_file:
        l = json.loads(line)
        if 'text' in l and 'created_at' in l:
            s = l['text'] 

            #remove non-ascii unicode; 
            #containuni returns the number of non-ascii unicodes that are removed
            s,containuni= re_pattern.subn('', s)

            #replace escape characters
            s = s.replace('\\/', '/')
            s = s.replace('\\\\', '\\')
            s = s.replace('\\\'', '\'') 
            s = s.replace('\\\"', '\"')
            s = s.replace('\n', ' ')
            s = s.replace('\t', ' ')

            #replace multiple spaces with a single space
            s = re.sub('\s+', ' ', s)

            #calculate the total number of tweets that contain non-ascii unicode
            if containuni>0:
                uninum += 1
            print s+' ('+l['created_at']+')'
    print '\n'
    print uninum, 'tweets contained unicode.'

if __name__ == '__main__':
    main()