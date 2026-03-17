from apps.master.models import Quality

qualities = list(value for value,label in Quality.QUALITY_CHOICES)
codecs = list(value for value,label in Quality.CODECS.choices)

print(qualities,codecs)

def generate_m3u8(queryset,playlist_name,codec,quality) -> str:
    lines = ["#EXTM3U", f"#PLAYLIST:{playlist_name}", ""]


    quality_objs = [get_codec_filtered(codec,get_quality_filtered(quality,video)) for video in queryset]

    for v_quality in quality_objs:
        lines.append(f"#EXTINF:-1, {v_quality.video.title} | {v_quality.quality} | {v_quality.codec}")
        lines.append(v_quality.url)
        lines.append("")

    return "\n".join(lines)

def get_quality_filtered(quality,video):
        match = video.qualities.filter(quality=quality)
        if not match:
            quality = switcher(quality,qualities)
            return get_quality_filtered(quality,video)
        return match

def get_codec_filtered(codec,queryset):
    match = queryset.filter(codec=codec)
    if not match:
        codec = switcher(codec,codecs)
        return get_codec_filtered(codec,queryset)
    return match[0]

def switcher(elem,lists:list):
    #gets element index from list
    elemIndex = lists.index(elem)
    #check if elem is last or middle (Not first).
    if (elem == lists[-1]) or (elem != lists[0]):
        #if there is only one element in list the list will return the last element that is First Element in the list
        return lists[elemIndex-1]
    #if First,
    else:
        return lists[elemIndex+1]