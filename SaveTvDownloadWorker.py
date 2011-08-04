import socket, urllib, os, sys, commands
from threading import Timer


class SaveTvDownloadWorker:
	"""
	Inspired by: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/83208
	"""
	
	def __init__(self, pUrl, pDdirectory, pUsername):
		self.dnldUrl = pUrl
		self.download_directory = pDdirectory
		self.username = pUsername

	def download(self):
		existSize = 0

		myUrlclass = urllib.FancyURLopener()
		socket.setdefaulttimeout(60)		
		webPage = myUrlclass.open(self.dnldUrl)
		fileLength = long(webPage.headers['Content-Length'])
		try:
			contentDisposition = webPage.headers['Content-Disposition']
			filename = contentDisposition.split("filename=")[1]
		except:
			filename = self.dnldUrl.split("/")
			filename = filename[len(filename)-1]
		webPage.close()		
		#import pdb; pdb.set_trace()

		self.originalFilename = filename

		# save.tv seems to offer files for other users. Check and only accept files containing our username.
		if (self.username not in filename):
			print "File %s is not for me." %(filename)
			return

		if (os.path.isfile(self.download_directory + filename)):
			print "File %s already downloaded." %(filename)
			return

		filename = filename + ".part"

		alreadyDownloadedBytes = long(self.getAlreadyDownloadedBytes(filename))	
		if alreadyDownloadedBytes == fileLength:
			print "%s already downloaded, size: %s" %(filename, alreadyDownloadedBytes)
			self.markFileAsFinished(filename, self.originalFilename)
			return
		
		if alreadyDownloadedBytes >= fileLength:
			print "%s already present, but size is too big (file: %s, web: %s)" %(filename, alreadyDownloadedBytes, fileLength)
			return

		print "Downloading %s with size %s (already downloaded: %s)" %(filename, fileLength, alreadyDownloadedBytes)

		sys.stdout.flush()

		wgetResult = commands.getstatusoutput("wget -c -nv -O \"%s\" %s" %(self.download_directory + filename, self.dnldUrl))
		print wgetResult

		sys.stdout.flush()

		# Wenn Datei komplett, ".part" entfernen
		if (self.getAlreadyDownloadedBytes(filename) == fileLength):
			self.removePartEndingFromFileName(filename, self.originalFilename)
			return True
		return False
		
	def getAlreadyDownloadedBytes(self, filename):
		if os.path.exists(self.download_directory+filename):
			existSize = os.path.getsize(self.download_directory+filename)
			return existSize
		return 0

	def removePartEndingFromFileName(self, filename, originalFilename):
		os.rename(self.download_directory+filename, self.download_directory+originalFilename)

if __name__ == "__main__":
	std = SaveTvDownloadWorker("http://80.190.216.181/25966898_CB5E3E716DE63A1ED50B48A0A6F415CB/?m=dl", "/tmp/")
	std.download()
