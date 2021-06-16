from utils import build_error_msg, build_success_msg

from place.models import Place, Category, Photo
from place.dto import CreateDto

class PlaceService():
    @staticmethod
    def get_all_posts():
        return Place.objects.all()

    @staticmethod
    def find_by_post(category_pk):
        return Place.objects.filter(category__pk=category_pk)

    @staticmethod
    def find_by_category(category_pk):
        return Category.objects.filter(pk=category_pk).first()

    @staticmethod
    def create(dto:CreateDto):
        if not dto.name or not dto.location or not dto.memo or not dto.best_menu or not dto.additional_info or not dto.stars:
            return build_error_msg('MISSING_INPUT')
        # tag = Tag.objects.filter(name=dto.tags).first()
        # if tag:
        #     tag = Place.tags.add(tag) 
        # category = Category.objects.filter(pk=dto.pk)
        place = Place.objects.create(
            category=dto.category,
            author=dto.author,
            name=dto.name,
            location=dto.location,
            memo=dto.memo,
            best_menu=dto.best_menu,
            additional_info=dto.additional_info,
            stars=dto.stars,
            # image=dto.image
        )
        for image in dto.image:
            Photo.objects.create(
                place=place,
                image=image
            )

        # place.tags.add(dto.tag)
        return build_success_msg('')
