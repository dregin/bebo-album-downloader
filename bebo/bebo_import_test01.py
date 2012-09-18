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

home_dir = "bebo pix"
albums_dir = "albums"
album_link_list = []
image_link_list = []

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

def get_pagination_albums(h2_html):	# The contents of the h2 tag that tells us how many albums are on the page
	num_albums = re.search('[0-9]+', h2_html)
	num_pages = num_albums // 21
	if num_albums % 21 > 0:
		num_pages = num_pages + 1
	return num_pages
	
def get_pagination_images(browser, page):



def get_album_links():

def get_image_links():

def download_images():

def zip_images():

def mail_link():

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
	album_links = soup.body.findAll('a', attrs = {'title':re.compile(".+")})
	for i in album_links:
		album_url = ''.join([site, i['href']])
		album_link_list.append(album_url)

	response1.close()    
	# Open each link
	i = 0
	for album in album_link_list:        
		# Create Album Directory
		album_directory = album_links[i]['title'].replace('/', ' ')
		album_path = './' + user_dir + '/' + album_directory + '/'
		# strip slashes from directory name
		if not os.path.isdir(album_path):
			sys.stdout.write("Creating " + album_directory + " directory...... ")
			try:
				os.mkdir(album_path)
			except OSError, e:
				print e
			print "Done!"
		i = i + 1
		response2 = br.open(album)
		soup = BeautifulSoup(response2.read())
		response1.close()
		image_links = soup.body.findAll('a', attrs = {'href':re.compile("^/c/photos/view+")})

		# List of Image Links
		for image_link in image_links:
			image_page_url = ''.join([site, image_link['href']])
			image_link_list.append(image_page_url)
        
			response3 = br.open(image_page_url)
			soup_image = BeautifulSoup(response3.read())
			response3.close()        
			# If the user WANTS to download originals
			if get_original == "on":
				# Find the link with '...o.jpg' at the end.
				image_url = soup_image.body.findAll('a', {'href':re.compile(".+o.jpg$")})
				print [ each.get('href') for each in soup.findAll('a', attr = {'http':re.compile("o.jpg")})]
				# If there IS an "original" version of the picture
				if image_url:
					try:
						print "1"
						print image_url
						download(image_url[0]['href'], album_path)
						print "2"
					except IndexError, e:
						print e
				# If there ISN'T an "original" version of the picture
				else:
					image_url = soup_image.body.findAll('img', attrs = {'src':re.compile("/large/.+jpg$")})
					try:
						print "3"
						download(image_url[0]['src'], album_path)
						print "4"
					except IndexError, e:
						print e
			# If the user DOESN'T want to download originals
			else:
				image_url = soup_image.body.findAll('img', attrs = {'src':re.compile("/large/.+jpg$")})
				try:
					print "5"
					download(image_url[0]['src'], album_path)
					print "6"
				except IndexError, e:
					print e
	# Create zip file of images
	zip_file = username + ".zip"
	zip_folder = r"./bebo pix/" + username + '/'
	dir_list = dirEntries(zip_folder, True)
	if not os.path.isdir("./albums/"):
		try:
			os.mkdir("./albums/")
		except OSError, e:
			print e
	makeArchive(dir_list, "./albums/" + zip_file)
	os.system("chmod 755 ./albums/" + username + ".zip")
	# Mail the user the link
	os.system("echo http://www.redbrick.dcu.ie/~dregin/bebo/albums/" + (username) + ".zip | mail -s \"Link To Your Bebo Albums\" " + (email))
