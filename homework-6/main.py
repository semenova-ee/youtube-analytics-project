from src.video import Video

if __name__ == '__main__':
    broken_video = Video('broken_video_id')
    assert broken_video.title is None
    assert broken_video.like_count is None

print(broken_video.view_count)
print(broken_video._video_id)
print(broken_video.title)
print(broken_video.like_count)
print(broken_video.url)

ulay = Video('BgfuSBV5H1M')
print(ulay.view_count)
print(ulay._video_id)
print(ulay.title)
print(ulay.like_count)
print(ulay.url)