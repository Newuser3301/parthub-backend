from rest_framework.permissions import BasePermission

class IsThreadParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        uid = getattr(request.user, "id", None)
        return obj.seller_id == uid or obj.buyer_id == uid
