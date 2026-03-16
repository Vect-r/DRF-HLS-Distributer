def generate_m3u8(queryset,playlist_name) -> str:
    lines = ["#EXTM3U", f"#PLAYLIST:{playlist_name}", ""]

    for video in queryset:
        lines.append(f"#EXTINF:-1, {video.title}")
        lines.append(video.url)
        lines.append("")

    return "\n".join(lines)

def switcher(elem,lists:list):
    #gets element index from list
    elemIndex = lists.index(elem)
    try:
        #check if elem is last or middle (Not first).
        if elem == lists[-1] or elem != lists[0]:
            return lists[elemIndex-1]
        #if First,
        else:
            return lists[elemIndex+1]
    except IndexError:
        return elem