from rest_framework.permissions import BasePermission

class SVIPPremission(BasePermission):
    message = "必须是SVIP才能访问"
    def has_permission(self,request,view):
        if request.user.user_type != 3: # SVIP
            return False
        return True


class MyPremission(BasePermission):
    def has_permission(self,request,view):
        if request.user.user_type == 3:
            return False
        return True