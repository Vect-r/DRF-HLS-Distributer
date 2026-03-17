from apps.master.models import 

def generate_m3u8(queryset,playlist_name) -> str:
    lines = ["#EXTM3U", f"#PLAYLIST:{playlist_name}", ""]

    for quality in queryset:
        lines.append(f"#EXTINF:-1, {quality.video.title} | {quality.quality} | {quality.codec}")
        lines.append(quality.url)
        lines.append("")

    return "\n".join(lines)

def get_quality_filtered(self,quality,video):
        match = video.qualities.filter(quality=quality)
        if not match:
            quality = switcher(quality,self.qualities)
            return self.get_quality_filtered(quality,video)
        return match

def get_codec_filtered(self,codec,queryset):
    match = queryset.filter(codec=codec)
    if not match:
        codec = switcher(codec,self.codecs)
        return self.get_codec_filtered(codec,queryset)
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