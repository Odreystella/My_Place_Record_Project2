from place.models import Place

class PlaceService():
    @staticmethod
    def get_all_posts():
        return Place.objects.all()

    @staticmethod
    def find_by_post(category_pk):
        return Place.objects.filter(category__pk=category_pk)