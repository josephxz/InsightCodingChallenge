from datetime import datetime,timedelta
from collections import deque
import sys
import json
import re



def main():
    tweet_file = open(sys.argv[1])
    nodestimeq = deque()
    nodes = deque()
    graph = deque()
    tdiff = timedelta(seconds=60)
    
    
    re_pattern = re.compile(u'[^\u0020-\u007F]', re.UNICODE)
    for line in tweet_file:
        l = json.loads(line)
        if 'text' in l and 'created_at' in l:
            s = l['text'] 
            s = re_pattern.sub('', s)
            s = s.replace('\\/', '/')
            s = s.replace('\\\\', '\\')
            s = s.replace('\\\'', '\'')
            s = s.replace('\\\"', '\"')    
            s = s.replace('\n', ' ')
            s = s.replace('\t', ' ')
            s = re.sub('\s+', ' ', s)
            #print s+' ('+l['created_at']+')'
    
    
    
            
            #lasttime = datetime.min
            #for line in tweet_file:
                #print line
            t = l['created_at']
            ts = datetime.strptime(t,'%a %b %d %H:%M:%S +0000 %Y')
            #print ts

            while (len(nodestimeq)>0):
                if  ts - nodestimeq[0][0] <= tdiff:
                    break
                else:
                    oldnodes = nodestimeq.popleft()[1]
                    for i in xrange(len(oldnodes)):
                        nodes.popleft()
                        for j in xrange(i+1,len(oldnodes)):
                            graph.popleft()


            tags = {tag.strip("#").lower() for tag in s.split() if tag.startswith("#") and len(tag)>1}
            if len(tags)>1:
                for tag in tags:
                    nodes.append(tag)
                nodestimeq.append([ts, tags])
                taglist = list(tags)
                for i in xrange(len(taglist)):
                    for j in xrange(i+1,len(taglist)):
                        graph.append(frozenset([taglist[i], taglist[j]]))

            if len(nodes) == 0:
                print 'Graph is empty.'
                continue
            avg = 2.0*len(set(graph))/len(set(nodes))

            #print tags
            #print set(nodes)
            #print set(graph)
            print len(set(graph))
            print "%.2f" % avg


if __name__ == '__main__':
    main()