from rest_framework import permissions


class CategoryPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return request.user.groups.filter(name='Manager').exists()
        return request.user.is_superuser

class MenuItemPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return request.user.groups.filter(name='Manager').exists()


class OrderPermission(permissions.BasePermission):
    pass

class OrderItemPermission(permissions.BasePermission):
    pass

class CartPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not(request.user.is_superuser) and  \
            not(request.user.groups.filter(name='Manager').exists()) \
                and not(request.user.groups.filter(name='Delivery').exists() )
         


class ManagerPermission(permissions.BasePermission):
     def has_permission(self, request, view):
        if request.user.groups.filter(name='Manager').exists():
            return True
        return False
  

class DeliveryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Delivery').exists():
            return True
        return False