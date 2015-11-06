
import sys
import json
import re


def main():
    tweet_file = open(sys.argv[1])
    uninum = 0
    re_pattern = re.compile(u'[^\u0020-\u007F]', re.UNICODE)
    for line in tweet_file:
        l = json.loads(line)
        if 'text' in l and 'created_at' in l:
            s = l['text'] 
            s,containuni= re_pattern.subn('', s)
            s = s.replace('\\/', '/')
            s = s.replace('\\\\', '\\')
            s = s.replace('\\\'', '\'') 
            s = s.replace('\\\"', '\"')
            s = s.replace('\n', ' ')
            s = s.replace('\t', ' ')
            s = re.sub('\s+', ' ', s)
            if containuni>0:
                uninum += 1
            print s+' ('+l['created_at']+')'
    print '\n'
    print uninum, 'tweets contained unicode.'

if __name__ == '__main__':
    main()