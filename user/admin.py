from django.contrib import admin

from user.models import User

# admin.site.register(User)
@admin.register(User)          # admin 페이지에 등록
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'created_at', 'last_login_at', 'is_superuser', 'is_active')
    list_display_links = ('id', 'email')
    exclude = ('password',)                           # 사용자 상세 정보에서 비밀번호 필드를 노출하지 않음

    def created_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    created_at.admin_order_field = '-date_joined'      # 가장 최근에 가입한 사람부터 리스팅
    created_at.short_description = '가입일'
    last_login_at.admin_order_field = 'last_login_at'
    last_login_at.short_description = '최근로그인'