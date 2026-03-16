def generate_m3u8(queryset,playlist_name) -> str:
    lines = ["#EXTM3U", f"#PLAYLIST:{playlist_name}", ""]

    for quality in queryset:
        lines.append(f"#EXTINF:-1, {quality.video.title} | {quality.quality} | {quality.codec}")
        lines.append(quality.url)
        lines.append("")

    return "\n".join(lines)

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