import os
import ConfigParser

from SaveTvEntity import SaveTvEntity
from SaveTvDownloadWorker import SaveTvDownloadWorker

class SaveTvDownloader:
	def readConfiguration(self):
		config = ConfigParser.RawConfigParser({'Timeout': '120', 'DeleteAfterDownload' : 'no'})
		config.read(os.path.dirname(os.path.realpath(__file__)) + '/savetv.cfg')
		
		self.SAVETV_USERNAME = config.get('SaveTV', 'Benutzername')
		self.SAVETV_PASSWORD = config.get('SaveTV', 'Passwort')
		self.DOWNLOAD_DIRECTORY = os.path.normpath(config.get('System', 'Zielverzeichnis')) + os.sep
		self.DELETE_AFTER_DOWNLOAD = config.getboolean('Optionen', 'DeleteAfterDownload')
		self.TIMEOUT = config.get('Optionen', 'Timeout')
		
	def doDownload(self):
		svte = SaveTvEntity(self.SAVETV_USERNAME, self.SAVETV_PASSWORD, self.TIMEOUT)
		svte.initialiseLogin()
		availableRecordingIds = svte.fetchDownloadableTelecaseIds()
		dlLinks = svte.getDownloadableRecordingLinks(availableRecordingIds)
		for telecastID, link in dlLinks.iteritems():
			downloader = SaveTvDownloadWorker(link, self.DOWNLOAD_DIRECTORY, self.SAVETV_USERNAME, self.TIMEOUT)
			file_complete = downloader.download()
			if self.DELETE_AFTER_DOWNLOAD and file_complete:
				svte.deleteFile(telecastID)

if __name__ == "__main__":
	downloader = SaveTvDownloader()
	downloader.readConfiguration()
	downloader.doDownload()

