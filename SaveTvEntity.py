from mechanize import Browser
import re
import socket
import urllib

class SaveTvEntity:
	SAVETV_URL = "http://www.save.tv"

	def __init__(self, username, password):
		self.username = username
		self.password = password

		socket.setdefaulttimeout(60)		
		self.browser = Browser()
	
	def fetchDownloadableTelecaseIds(self):
		telecaseIds = []

		for recordingLink in self.browser.links(url_regex=".*usShowVideoArchiveDetail.cfm.*"):
			telecastId = self.extractTelecastId(recordingLink)
			print "Found Download. Telecast-ID: ", telecastId
			telecaseIds.append(telecastId)
		# return list of unique Ids.
		return list(set(telecaseIds))
	
	def extractTelecastId(self, pRecordingLink):
		absurl = pRecordingLink.absolute_url
		telecastId = absurl.split("TelecastID=")[1].split("&&sk")[0]
		return telecastId

	def getDownloadableRecordingLinks(self, pDownloadableRecordings):
		downloadLinks = {}
		for telecastID in pDownloadableRecordings:	
			print "Getting link for Telecast-ID ", telecastID
			dlInfoLink = self.browser.open("/STV/M/obj/cRecordOrder/croGetDownloadUrl.cfm?null.GetDownloadUrl&=&ajax=true&c0-id=9999_9999999999999&c0-methodName=GetDownloadUrl&c0-param0=number%3A"+telecastID+"&c0-param1=number%3A0&c0-param2=boolean%3Afalse&c0-scriptName=null&callCount=1&clientAuthenticationKey=&xml=true")

			tmpDlDetails = self.getDownloadLink(dlInfoLink.get_data())
			if tmpDlDetails <> "":
				downloadLinks[telecastID] = tmpDlDetails
		return downloadLinks

	def getDownloadLink(self, pDlInfoLink):
		p = re.compile("'(http://[^']*?m=dl[^']*)'")
		result = p.search(pDlInfoLink)
		url = ""
		if result:
			url = result.group(1)
			print "Found download URL: ", url
		else:
			print "No download URL found (probably recording still in progress)."
		return url

	def deleteFile(self, telecastID):
		post_data = urllib.urlencode({'lTelecastID' : telecastID})
		response = self.browser.open("/STV/M/obj/user/usShowVideoArchive.cfm", post_data)
		if response.code == 200:
			print "File for telecast-ID %s deleted." %(telecastID)
		
	def initialiseLogin(self):
		self.browser.open(self.SAVETV_URL)
		self.browser.follow_link(self.browser.links(url_regex=".*index\.cfm.*").next())
		#import pdb; pdb.set_trace()		
		self.browser.select_form(nr=0)
		self.browser["sUsername"] = self.username
		self.browser["sPassword"] = self.password

		self.browser.submit()	

		response = self.browser.follow_link(self.browser.links(url_regex=".*miscShowHeadFrame.cfm.*").next())
		p = re.compile("href=\"([^\"]*usShowVideoArchive[^\"]*)\"")
		url = p.search(response.get_data()).group(1)		

		response = self.browser.open(url);
