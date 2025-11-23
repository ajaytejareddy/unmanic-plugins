import logging
from unmanic.libs.unplugins.settings import PluginSettings

logger = logging.getLogger("Unmanic.Plugin.simple_hevc_transcoder")

class Settings(PluginSettings):
    settings = {}

def on_library_management_file_test(data):
    file_probe = data.get('probe')
    if not file_probe:
        logger.warning("Probe data not found in file test for simple_hevc_transcoder.")
        return data
    try:
        video_streams = file_probe.get_video_streams()
        if not video_streams:
            return data
        if video_streams[0].get('codec_name') == 'hevc':
            return data
        data['add_file_to_pending_tasks'] = True
    except Exception as e:
        logger.error(f"Error in simple_hevc_transcoder during file test: {e}")
    return data

def on_worker_process(data):
    file_in = data.get('file_in')
    file_out = data.get('file_out')
    ffmpeg_command = [
        "ffmpeg", "-y",
        "-hwaccel", "vaapi",
        "-hwaccel_device", "/dev/dri/renderD128",
        "-i", file_in,
        "-c:v", "hevc_vaapi",
        "-qp", "23",
        "-c:a", "copy",
        "-c:s", "copy",
        file_out
    ]
    data['exec_command'] = ffmpeg_command
    data['command_progress_parser'] = None
    data['repeat'] = False
    logger.info(f"Generated ffmpeg command by simple_hevc_transcoder: {' '.join(ffmpeg_command)}")
    return data
