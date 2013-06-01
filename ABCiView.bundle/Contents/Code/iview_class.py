class iView_Config():

	BASE_URL = 'http://www.abc.net.au/iview/'
		
	CFG_URL = BASE_URL + 'xml/config.xml'
	CFG_XML = XML.ElementFromURL(CFG_URL)
		
	AUTH_URL = CFG_XML.xpath('/config/param[@name="auth"]')[0].get("value")
	API_URL = CFG_XML.xpath('/config/param[@name="api"]')[0].get("value")
		
	CAT_URL = BASE_URL + CFG_XML.xpath('/config/param[@name="categories"]')[0].get("value")
	
	RTMP_Server = CFG_XML.xpath('/config/param[@name="server_streaming"]')[0].get("value") + '?auth='
	SWF_URL = 'http://www.abc.net.au/iview/images/iview.jpg'
		
	CAT_XML = XML.ElementFromURL(CAT_URL)
	SERIES_URL = API_URL + 'seriesIndex'
	SERIES_JSON = JSON.ObjectFromURL(SERIES_URL)
	category_list = {}
	
	@classmethod
	def RTMP_URL(self):
	
		xml = XML.ElementFromURL(url=self.AUTH_URL)
		token = xml.xpath('//a:token/text()', namespaces={'a': 'http://www.abc.net.au/iView/Services/iViewHandshaker'})[0]
		return xml.xpath('//a:server/text()', namespaces={'a': 'http://www.abc.net.au/iView/Services/iViewHandshaker'})[0] + '?auth=' + token
	
	@classmethod
	def CLIP_PATH(self):
		xml = XML.ElementFromURL(self.AUTH_URL)
		path = xml.xpath('//a:path/text()', namespaces={'a': 'http://www.abc.net.au/iView/Services/iViewHandshaker'})
		if not path:
			return 'mp4:'
		
		return 'mp4:' + path[0]
		
	@classmethod
	def List_Categories(self):
		 cats = {}
		 for cat in self.CAT_XML.xpath('/categories/category'):
		 	 id = cat.get('id')
		 	 name = cat.find('name').text
		 	 if id in ['test', 'index']:
		 	 	continue
		 	 cats[id] = name
		 
		 return cats
	
	
	
class iView_Series(object):
	
	def __init__(self, key):
		
		self.id = key
		json = JSON.ObjectFromURL(iView_Config.API_URL + 'series=' + key)
		
		self.title = json[0]['b']
		self.description = json[0]['c']
		self.category = json[0]['e']
		self.img = json[0]['d']
		self.episode_count = len(json[0]['f'])
		self.episodes = self.Episodes(json[0]['f'])
		
	def Episodes(self, json):
		eps = []
		for ep in json:
			id = ep['a']
			title = ep['b']
			description = ep['d']
			url = ep['n'][:-4]
			thumb = ep['s']
			duration = int(ep['j'])
			tmp = []
			tmp.append(id)
			tmp.append(title)
			tmp.append(description)
			tmp.append(url)
			tmp.append(thumb)
			tmp.append(duration)
			eps.append(tmp)
			
		return eps

	
class iView_Category(object):
	
	def __init__(self, key):
	
		self.id = key
		cats = iView_Config.List_Categories()
		self.title = cats[key]
		self.series_list = self.Series(key)
	
	def Series(self, search):
		series = []
		for show in iView_Config.SERIES_JSON:
			id = show['a']
			title = show['b']
			category = show['e']
			count = len(show['f'])
			tmp = []
			tmp.append(id)
			tmp.append(title)
			tmp.append(category)
			tmp.append(count)
			
			if category.find(search) >= 0:
				series.append(tmp)
			
		return series
	
	
	
	