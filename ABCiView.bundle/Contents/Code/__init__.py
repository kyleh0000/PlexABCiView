from iview_class import *

ART = 'art-default.jpg'
ICON = 'icon-default.jpg'


def Start():
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')


@handler('/video/aubciview', 'Australian ABC iView', art=ART, thumb=ICON)
def MainMenu():
    oc = ObjectContainer(view_group='List', title2='ABC iView')


    #oc.add(VideoClipObject(key = RTMPVideoURL(url = 'rtmp://203.18.195.10/ondemand' + '?auth=7B8F0402DD370FF9299E', clip = 'mp4:comedy/madashell_02_08', swf_url = 'http://www.abc.net.au/iview/images/iview.jpg'), rating_key = '123',title = 'TEST'))

    cats = iView_Config.List_Categories()

    for key in cats:
        oc.add(DirectoryObject(
            key=Callback(GetSeriesByCaegory, category=key),
            title=cats[key]
        ))

    oc.objects.sort(key=lambda obj: obj.title)

    return oc


@route('/video/aubciview/category/{category}')
def GetSeriesByCaegory(category):
    cat = iView_Category(category)

    oc = ObjectContainer(view_group='List', title2=cat.title)

    series = cat.series_list

    for item in series:
        oc.add(DirectoryObject(
            key=Callback(GetEpisodesBySeries, series=item[0]),
            title=item[1]
        ))
    oc.objects.sort(key=lambda obj: obj.title)

    return oc


@route('/video/aubciview/series/{series}')
def GetEpisodesBySeries(series):
    show = iView_Series(series)

    oc = ObjectContainer(view_group='InfoList', title2=show.title, no_cache=True)

    episodes = show.episodes

    rtmp_url = iView_Config.RTMP_URL()

    for item in episodes:
        oc.add(Play_iView(item[1], item[2], item[3], item[4], item[5], rtmp_url))

    oc.objects.sort(key=lambda obj: obj.title)

    return oc


@route('/video/aubciview/episode/play')
def Play_iView(iView_Title, iView_Summary, iView_Path, iView_Thumb, iView_Duration, video_url, include_container=False):
    HTTP.ClearCache()

    call_args = {
        "iView_Title": iView_Title,
        "iView_Summary": iView_Summary,
        "iView_Path": iView_Path,
        "iView_Thumb": iView_Thumb,
        "iView_Duration": int(iView_Duration),
        "video_url": video_url,
        "include_container": True,
    }

    vco = VideoClipObject(
        key=Callback(Play_iView, **call_args),
        rating_key=iView_Path,
        title=iView_Title,
        summary=iView_Summary,
        thumb=iView_Thumb,
        duration=int(iView_Duration),
        items=[
            MediaObject(
                parts=[
                    PartObject(
                        key=RTMPVideoURL(url=video_url, clip=iView_Config.CLIP_PATH() + iView_Path,
                                         swf_url=iView_Config.SWF_URL)
                    )
                ]
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects=[vco])
    else:
        return vco
