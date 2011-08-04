import os
import ConfigParser

from SaveTvEntity import SaveTvEntity
from SaveTvDownloadWorker import SaveTvDownloadWorker

class SaveTvDownloader:
	def readConfiguration(self):
		config = ConfigParser.RawConfigParser()
		config.read(os.path.dirname(os.path.realpath(__file__)) + '/savetv.cfg')
		
 		self.SAVETV_USERNAME = config.get('SaveTV', 'Benutzername')
		self.SAVETV_PASSWORD = config.get('SaveTV', 'Passwort')
		self.DOWNLOAD_DIRECTORY = os.path.normpath(config.get('System', 'Zielverzeichnis')) + os.sep

	def doDownload(self):
		svte = SaveTvEntity(self.SAVETV_USERNAME, self.SAVETV_PASSWORD)
		svte.initialiseLogin()
		availableRecordingIds = svte.fetchDownloadableTelecaseIds()
		dlLinks = svte.getDownloadableRecordingLinks(availableRecordingIds)
		for telecastID, link in dlLinks.iteritems():
			downloader = SaveTvDownloadWorker(link, self.DOWNLOAD_DIRECTORY, self.SAVETV_USERNAME)
			downloader.download()
		
if __name__ == "__main__":
	downloader = SaveTvDownloader()
	downloader.readConfiguration()
	downloader.doDownload()		
		
