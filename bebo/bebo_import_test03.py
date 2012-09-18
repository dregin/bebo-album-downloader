# Created on 10 Apr 2010
# @author: dregin

import re
import os
import sys
import zipfile
import smtplib
# from email.MIMEText import MIMEText
import urllib

# sys.path.append("/usr/share/pyshared/mechanize")
from BeautifulSoup import BeautifulSoup
from mechanize import Browser

album_page = 0
image_page = 0

home_dir = "bebo_pix"
albums_dir = "albums"
album_link_list = []
image_link_list = []
album_names = []

username = sys.argv[1]
email = sys.argv[2]
get_original = sys.argv[3]
proxy = {'http':'http://proxy.dcu.ie:3128', 'https':'http://proxy.dcu.ie:3128'}

user_dir = home_dir + '/' + username
user_dir
site = "http://www.bebo.com"
url = ''.join([site, '/', username])

def get_mechanize_instance():
	browser = Browser()
	if proxy != "":
		br.set_proxies(proxy)
	return browser

def get_num_pagination_albums(soup):	
	h2_html = soup.findAll('h2')					# Find content of all h2 tags
	m = re.search('[^(]+\((\d+)', str(h2_html[0]))	# Find numbers after '('
	num_albums = int(m.group(1))					# Return first number of above search results
	
	num_pages = num_albums // 21
	if num_albums % 21 > 0:
		num_pages = num_pages + 1
	return num_pages

def get_num_pagination_images(soup):
	h2_html = soup.findAll('h2')					# Find content of all h2 tags
	m = re.search('[^(]+\((\d+)', str(h2_html[0]))	# Find numbers after '('
	num_images = int(m.group(1))					# Return first number of above search results
	
	num_pages = num_images // 24
	if num_images % 24 > 0:
		num_pages = num_pages + 1
	return num_pages

def get_album_links(num_album_pages, albums_page, br):
	for x in range (1, num_album_pages+1):									# For each album page
		album_page_link = ''.join([albums_page,'&amp;&PageNbr=',str(x)])
		print album_page_link
		album_response = br.open(album_page_link)
		print album_response.geturl()
		soup = BeautifulSoup(album_response.read())
		album_links = soup.body.findAll('a', attrs = {'title':re.compile(".+")})	# All <a> tags that actually have titles.
		for i in album_links:
			album_url = ''.join([site, i['href']])		# Take the href value of the <a> tags found above.
			album_name = i['title']
			album_link_list.append(album_url)
			album_names.append(album_name)
	return album_link_list

def get_image_links(album_link, album_name):
	br = Browser()
	# Go to album link
	page_html = br.open(album_link)
	soup = BeautifulSoup(page_html.read())
	# Get Album title
	# Create Album Directory if it doesn't already exist
	album_directory = album_name.replace('/', ' ')
	album_path = './' + user_dir + '/' + album_directory + '/'
	if not os.path.isdir(album_path):
		sys.stdout.write("Creating " + album_directory + " directory...... ")
		try:
			os.mkdir(album_path)
		except OSError, e:
			print e
		print "Done!"
	# Get pagination for pages of album
	num_image_pages = get_num_pagination_images(soup)
	# Get all image links
	if num_image_pages > 1:
		for x in range(1, num_image_pages + 1):
			response1 = br.follow_link(text_regex=str(x))
			image_page_link = ''.join([albums_page,'&amp;&PageNbr=',str(x)])
	# All the images are linked on the first page but some of them are missing.
	# The first part of the name is constant.
	# Return image links
	return 0

def download_images():
	return 0

def zip_images():
	return 0

def mail_link():
	return 0

def makeArchive(fileList, archive):
	try:
		a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)
		for f in fileList:
			print "archiving file %s" % (f)
			a.write(f)
		a.close()
		return True
	except:
		return False

def dirEntries(dir_name, subdir, *args):
	fileList = []
	for file in os.listdir(dir_name):
		dirfile = os.path.join(dir_name, file)
		if os.path.isfile(dirfile):
			if not args:
				fileList.append(dirfile)
			else:
				if os.path.splitext(dirfile)[1][1:] in args:
					fileList.append(dirfile)
		elif os.path.isdir(dirfile) and subdir:
			print "Accessing directory:", dirfile
			fileList.extend(dirEntries(dirfile, subdir, *args))
	return fileList

def download(url, directory):
	opener = urllib.FancyURLopener(proxy)
	webFile = opener.open(url)
	localFile = open(directory + url.split('/')[-1], 'w')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()
	
if __name__ == '__main__':
	# Create directory to hold user directories
	if not os.path.isdir('./' + home_dir + '/'):
		sys.stdout.write("Creating home directory...... ") 
		os.mkdir('./' + home_dir + '/')
		print "Done!"
	# Creat user's directory to hold albums
	if not os.path.isdir('./' + user_dir + '/'):
		sys.stdout.write("Creating user directory... ")
		os.mkdir('./' + user_dir + '/')
		print "Done!"
	# Setup browser
	br = Browser()
	if proxy != "":
		br.set_proxies(proxy)
	br.open(url)
	# Use browser
	response1 = br.follow_link(text_regex=r"Photos", nr=0)
	assert br.viewing_html()
	# Find list of albums 
	soup = BeautifulSoup(response1.read())

	num_album_pages = get_num_pagination_albums(soup)
	albums_page = response1.geturl()

	album_links = get_album_links(num_album_pages, albums_page, br) # Build a list of album links from every page of albums

	
	for link, name in map(None, album_links, album_names):
		# DEBUG PRINT
		get_image_links(link, name)
		print link + " : " + name
	print len(album_links)
	response1.close()    

