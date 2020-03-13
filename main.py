from polito_sync import PolitoWebClass

import json

if __name__ == "__main__":

    settings = None

    try:
        with open("settings.json") as s:
            settings = json.load(s)
    except:
        print("Error: rename settings file as settings.json")
    
    session = PolitoWebClass()
    session.setVideoLessons(settings['VideoLessons'])
    session.setDownloadFolder(settings['download_folder'])
    session.setUserAgent('Mozilla/5.0')
    if settings['credentials']['enabled']:
        session.login(settings['credentials']['username'], settings['credentials']['password'])
    else:
        session.login()
    session.menu()
