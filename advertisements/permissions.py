from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        # Добавляем проверку на метод 'GET' и статус 'OPEN'
        if request.method == 'GET' and request.query_params.get('status') == 'OPEN':
            return True
        return request.user and request.user.is_authenticated



    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.method in SAFE_METHODS:
             return True
        return request.user == obj.creator
