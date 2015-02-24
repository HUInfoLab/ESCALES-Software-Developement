# -*- coding: utf-8 -*-
'''
Created on Feb 23, 2015

@author: Mario
'''

from bs4 import BeautifulSoup
from collections import defaultdict as dd
import re
import urllib2
    
'''Use this code to get the html directly from the site'''
pageUrl = "http://www.jamiiforums.com/kenyan-news/188407-kenyas-pm-in-trouble.html"
 
hdr = {'User-Agent': 'Chrome/23.0.1271.64'}
      
req = urllib2.Request(pageUrl, headers=hdr)
 
jamiipage = urllib2.urlopen(req)
   
jamiihtml = jamiipage.read()

'''Use a downloaded page instead by uncommenting this and giving the appropriate file path'''
# jamiihtml = open("D:\\Documents\\Research\\Data\\JamiiForums\\JamiiExamplePage.html")

jamiiSoup = BeautifulSoup(jamiihtml)

'''Find thread ID in thread info section or pagination links'''
threadId = jamiiSoup.find("input",attrs={"name":"t"})['value']

'''Find thread title in header at top of page'''
threadTitle = jamiiSoup.find("h1").find("a").text
print "Thread_ID:",threadId,"Thread title:",threadTitle

'''Find subforums in navbits'''
forumGroup = jamiiSoup.find_all("li",attrs={"class":"navbit"})[1].text
subforum = jamiiSoup.find_all("li",attrs={"class":"navbit"})[2].text
print "Forums:",forumGroup + ":",subforum,"\n\n"

'''Find and create list of containers for posts'''
rawPostData = jamiiSoup.find_all("li",attrs={"class":"postbit"})

# print rawPostData[4].prettify()

'''Default dict to store data structure for all post data,
this lets us prevent duplication if we are scraping multiple pages at once.
The first post of a thread is displayed at the top of every page,
so it will be duplicated unless we check to make sure we don't already have that post.'''
postData = dd(list)

for post in rawPostData:
  '''post id is in top level tag for post container, strip it to just the number'''
  postId = re.search("\d+$",post['id'],re.UNICODE).group()
  
  '''user id is final element of many links in a post, easiest to identify is the user avatar'''
  userId = re.search("\d+$",post.find('a',attrs={"class":"postuseravatarlink"})['href'],re.UNICODE).group()
  
  '''user name is always in the first <strong> tags, since it's displayed at top of post'''
  userName = post.find('strong').text
  
  '''post date and time. Need separate handling for recent posts,
  would need to convert "today" and "yesterday" to appropriate dates'''
  postDateTime = post.find("span",attrs={"class":"date"}).text
  
  likedBy = []
  
  '''likes are a list of links in the vbseo_liked tag, just pull off the user ids at end of links'''
  for likingUser in post.find("div",attrs={"class":"vbseo_liked"}).find_all('a'):
    likedBy.append(int(re.search("\d+$",likingUser["href"],re.UNICODE).group()))
  
  postData[postId].extend([postId,threadId,userId,userName])
  
  '''post title is within h2 header'''
  postTitle = post.find("h2").text.strip()
  
  '''post body includes quoted posts'''
  rawPostBody = post.find('blockquote',attrs={"class":"postcontent restore"})
  
  '''quotations are inside the post body, easier to extract them first'''
  quotedPosts = []
  quotedText = []
  for quotation in rawPostBody.find_all('div',attrs={"class":"quote_container"}):
    quotedPosts.append(int(re.search("\d+$",quotation.find('div',attrs={"class":"bbcode_postedby"}).find('a')["href"],re.UNICODE).group()))
    quotedText.append(quotation.find('div',attrs={"class":"message"}).text)
  
  '''because we then have to remove interior blockquotes from the post body, leaving only the user's own writing'''
  while True:
    try:
      rawPostBody.div.decompose()
    except:
      break
  postBody = rawPostBody.text.strip()
  
  '''Finally, we have all the data per post'''
  print "Post_ID:",postId,"| User_ID:",userId,"| User_Name:",userName,"| Posted at:",postDateTime
  print "Post Title:",postTitle
  print "Quoted Posts:",quotedPosts
  print "Quoted Text:",quotedText
  print "Post Body:",postBody
  print "Liked by:",likedBy,"\n\n"