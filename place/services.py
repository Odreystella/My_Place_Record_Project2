from place.models import Place

class PlaceService():
    @staticmethod
    def get_all_posts():
        return Place.objects.all()