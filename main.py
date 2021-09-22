import asyncio
import lyricsgenius
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

GENIUS_ACCES_TOKEN = ''

async def get_media_info():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()

        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

async def get_multiple_media_info():
    sessions = await MediaManager.request_async()

    session_info = []

    current_sessions = sessions.get_sessions()
    for current_session in current_sessions:
        if current_session:
            info = await current_session.try_get_media_properties_async()

            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
            info_dict['genres'] = list(info_dict['genres'])

        session_info.append(info_dict)

    return(session_info)


if __name__ == '__main__':
    genius = lyricsgenius.Genius(GENIUS_ACCES_TOKEN)
  
    if len(sys.argv) > 1:

        if sys.argv[1] == '-s' or sys.argv[1] == 'select':
            media_info_list = asyncio.run(get_multiple_media_info())
            print(f"Select media:\n{', '.join([str(media_info_list.index(info)) + ': ' +info['title'] for info in media_info_list])}")
            media_index = int(input('>'))
            media_info = media_info_list[media_index]
            song = genius.search_song(media_info['title'], media_info['album_artist'])

            if song != None:
                print(song.lyrics)
                print(f"\n{media_info['title']} by {media_info['artist']}\nGenres: {[', '.join(media_info['genres'])]}")

            else:
                print(f"Didn't find any lyrics for {media_info['title']}")

        elif sys.argv[1] == '-c' or sys.argv[1] == 'current':
            media_info = asyncio.run(get_media_info())
            song = genius.search_song(media_info['title'], media_info['artist'])

            if song != None:
                print(song.lyrics)
                print(f"\n{media_info['title']} by {media_info['artist']}\nGenres: {', '.join(media_info['genres'])}")

            else:
                print(f"Didn't find any lyrics for {media_info['title']}")

    else:
        print('Usage: main.py < select | current >',
            '\n               < -s     | -c      >')
