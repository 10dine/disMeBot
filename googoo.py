from argparse import FileType
from google_images_search import GoogleImagesSearch

class GID:
    def __init__(self, GDK, GCS, GIS, srch_in) -> None:
        self.GDK = GDK
        self.GCS = GCS
        self.srch_in = srch_in
        self.GIS = GoogleImagesSearch(GDK, GCS)
        pass
    def Idown(self):
        s_params = {
            'q' : self.srch_in,
            'num' : 1,
            'fileType': 'jpg'
        }
        self.GIS.search(search_params=s_params, path_to_dir = '/', custom_image_name='temp')
        pass