
PLAYER_URL = "http://www.abc.net.au/iview/#/view/32405"

def GetCategories():
    url = 'http://www.abc.net.au/iview/xml/categories.xml'
    xml = XML.ElementFromURL(url)
    categories = []
    for category in xml.xpath('/categories/category'):
        id = category.get('id')
        name = category.find('name').text
        item = []
        item.append(id)
        item.append(name)
        categories.append(item)
    return categories
####################################################################################################

def GetSeriesByCategory(category):
	url = 'http://tviview.abc.net.au/iview/api2/?seriesIndex'
	data = JSON.ObjectFromURL(url)

	SeriesInfo = []
	
	for item in data:
		id = item['a']
		name = item['b']
		search = item['e']
		if category in search:
			found = []
			video = []
			found.append(id)
			found.append(name)
			for item1 in item['f']:
				ep = []
				ep.append(item1['a'])
				ep.append(item1['g'])
				video.append(ep)
			found.append(video)
				
			SeriesInfo.append(found)
			
	return SeriesInfo

####################################################################################################
def Start():

	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')




####################################################################################################
@handler('/video/iview', 'Hello World')
def MainMenu():
    
	#array_categories = GetCategories()
	
	#oc = ObjectContainer(view_group='List')
	#oc.add(DirectoryObject(key=Callback(SeriesList(), name=key), title='just_added'))
	
	#for item in array_categories:
	
	#	name = item[1]
		
	#	oc.add(DirectoryObject(
	#		key = Callback(SeriesList, category=item[0]),
	#		title = name
	#	))

	
	#return oc

    	oc = ObjectContainer(view_group='List')

    	#oc.add(VideoClipObject(key = RTMPVideoItem(url = 'rtmp://cp53909.edgefcs.net/ondemand?auth=daEdvcLcJbtaLbKbCc_d6bpalalcFaYd7a_-brAh7H-8-kms_wFAnM&aifp=v001', clip = 'mp4:flash/playback/_definst_/kids/bobbuilder_13_12', controls = True, live = True, swf_url = 'http://www.abc.net.au/iview/iview_383.swf', swfvfy = True), rating_key = "123" , title = "123"))
        
        oc.add(VideoClipObject(key = RTMPVideoURL(url = 'rtmp://cp53909.edgefcs.net/ondemand?auth=daEcmcHbgdQakcJbmaxc4b0brbpaed0b2cV-brAifV-8-lmo_xHtnF&aifp=v001', clip = 'mp4:flash/playback/_definst_/kids/bobbuilder_13_12', swf_url = 'http://www.abc.net.au/iview/images/iview.jpg'), rating_key = '123',title = 'TEST'))

        #oc.add(VideoClipObject(url = 'rtmp://cp53909.edgefcs.net/ondemand?auth=daEcrdpc8acdcbrdAa8avdpa5bGd3c8dQbB-brz_kl-8-qnq_rEtqH&aifp=v001', clip = 'mp4:flash/playback/_definst_/kids/bobbuilder_13_12', swfurl='http://www.abc.net.au/iview/images/iview.jpg', swfvfy='true'), title = 'TEST1')
    
        #oc.add(VideoClipObject(
        #                       key = RTMPVideoURL(url = 'rtmp://cp53909.edgefcs.net/ondemand?auth=daEcrdpc8acdcbrdAa8avdpa5bGd3c8dQbB-brz_kl-8-qnq_rEtqH&aifp=v001', clip = 'mp4:flash/playback/_definst_/kids/bobbuilder_13_12', swf_url = 'http://www.abc.net.au/iview/images/iview.jpg', swfvfy = True),
        #                      title = 'test'
        #                      ))
        
	#oc.add(WebVideoURL('http://www.abc.net.au/iview/#/view/32405'))
	
	
	return oc


def EpisodeList(series):

	oc = ObjectContainer(view_group='List', title2=series[0])
	
	#for item in series[2]:
		
		#oc.add(DirectoryObject(
		#	key = Callback(SeriesList, category='123'),
		#	title = item[0]
		#))

	#oc.add(VideoClipObject(key'rtmp://cp53909.edgefcs.net/ondemand?auth=daEbOdCbbdydWdxdbaYacc9cCcedtbKbEat-brzxyE-8-jnt_sHvqN', clip = 'mp4:flash/playback/_definst_/madashell_02_08.mp4', live = True), title = item[0]))
	
	return oc



###################################################################################
@route('/video/iview/sl/{category}')
def SeriesList(category):

	oc = ObjectContainer(view_group='List', title2=category)
	
	list = GetSeriesByCategory(category)
	
	for item in list:
	
		name = item[1]
		
		oc.add(DirectoryObject(
			key = Callback(EpisodeList, series=item),
			title = name
		))

	
	return oc


@route('/video/iview/cat')
def Categories():
	
	global array_categories
		
	return array_categories

