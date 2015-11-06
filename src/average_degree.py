from datetime import datetime,timedelta
from collections import deque
import sys
import json
import re



def main():
    tweet_file = open(sys.argv[1])

    #deque for the combination of the timestamp and array of hashtags of each tweet
    nodestimeq = deque()
    #deque for the nodes in the graph, duplicated nodes can exist
    nodes = deque()
    #deque for the edges in the graph, duplicated edges can exist
    graph = deque()
    #the maximum difference between the timestamps of tweets in the graph  is 60 seconds
    tdiff = timedelta(seconds=60)
    
    # regular expression pattern for non-ascii unicode that is not in the range \u0020-\u007F
    re_pattern = re.compile(u'[^\u0020-\u007F]', re.UNICODE)
    for line in tweet_file:
        l = json.loads(line)
        if 'text' in l and 'created_at' in l:
            s = l['text'] 

            #remove non-ascii unicode
            #containuni returns the number of non-ascii unicodes that are removed
            s = re_pattern.sub('', s)

            #replace escape characters
            s = s.replace('\\/', '/')
            s = s.replace('\\\\', '\\')
            s = s.replace('\\\'', '\'')
            s = s.replace('\\\"', '\"')    
            s = s.replace('\n', ' ')
            s = s.replace('\t', ' ')

            #replace multiple spaces with a single space
            s = re.sub('\s+', ' ', s)
    
    
            t = l['created_at']
            #transform string timestamp into python datetime format
            ts = datetime.strptime(t,'%a %b %d %H:%M:%S +0000 %Y')

            #when deque for tweets is not empty
            while (len(nodestimeq)>0):
                #if the old tweet is within 60 seconds from the current latest tweet, do nothing and break from the loop
                if  ts - nodestimeq[0][0] <= tdiff:
                    break
                #if the old tweet is more than 60 seconds older than the latest tweet, remove the old tweet
                else:
                    #remove old tweet
                    oldnodes = nodestimeq.popleft()[1]
                    for i in xrange(len(oldnodes)):
                        #remove hashtag nodes in the old tweet
                        nodes.popleft()
                        for j in xrange(i+1,len(oldnodes)):
                            #remove edge in the old tweet
                            graph.popleft()

            #split tags from the tweet text, only choose non-empty tags, make all tags lower-case, use set to remove duplicate tags
            tags = {tag.strip("#").lower() for tag in s.split() if tag.startswith("#") and len(tag)>1}
            #only tweets with more than one tag are added to teh graph
            if len(tags)>1:
                #add each tag in the tweet to the tag deque
                for tag in tags:
                    nodes.append(tag)
                #add the timestamp and tags of the tweet into the tweet deque
                nodestimeq.append([ts, tags])

                #add the edges formed by tags in the tweet into the edge deque
                taglist = list(tags)
                for i in xrange(len(taglist)):
                    for j in xrange(i+1,len(taglist)):
                        graph.append(frozenset([taglist[i], taglist[j]]))

            #when there is no hashtag in the graph
            if len(nodes) == 0:
                print 'Graph is empty.'
                continue

            #the average number of degree for a non-directed graph is 2E/V, use set to remove duplicate hashtags and edges in the deque
            avg = 2.0*len(set(graph))/len(set(nodes))


            print "%.2f" % avg


if __name__ == '__main__':
    main()