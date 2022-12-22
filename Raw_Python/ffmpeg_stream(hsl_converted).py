from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import ffmpeg_streaming


video = ffmpeg_streaming.input('rtmp://127.0.0.1:1935/live/test',capture=True)
_360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
hls = video.hls(Formats.h264())
hls.representations(_360p)
hls.output('media/hls.m3u8')