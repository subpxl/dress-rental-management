from django.contrib.auth.decorators import  permission_required,user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.http import  JsonResponse

from config.config import Config

def is_shop_admin(user):
    return user.groups.filter(name=Config.ShopAdmin).exists()

def is_manager(user):
    return user.groups.filter(name=Config.Manager).exists()

def is_staff(user):
    return user.groups.filter(name=Config.Staff).exists()



class ShopAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return   self.request.user.groups.filter(name=Config.ShopAdmin).exists()

    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'no permission allowed'}
        )

class ManagerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return   self.request.user.groups.filter(name=Config.Manager).exists()

    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'no permission allowed to manager '}
        )


class StaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return   self.request.user.groups.filter(name=Config.Staff).exists()

    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'no permission allowed to staff'}
        )
