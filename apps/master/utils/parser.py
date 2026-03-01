def generate_m3u8(queryset,playlist_name) -> str:
    lines = ["#EXTM3U", f"#PLAYLIST:{playlist_name}", ""]

    for video in sorted(queryset, key=lambda v: v.position):
        lines.append(f"#EXTINF:-1,{video.title}")
        lines.append(video.url)
        lines.append("")

    return "\n".join(lines)