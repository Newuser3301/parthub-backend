from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from b2b.models import B2BPost, B2BProfile, PostStatus
from b2b.serializers import B2BPostSerializer, B2BProfileSerializer
from b2b.permissions import IsAuthorOrReadOnly

from billing.services import can_create_b2b_post, inc_b2b_post


class MyB2BProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = B2BProfileSerializer

    def get_object(self):
        profile, _ = B2BProfile.objects.get_or_create(user=self.request.user)
        return profile


class B2BPostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = B2BPostSerializer

    # filtering/search
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description", "category"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        qs = B2BPost.objects.select_related("author").filter(status=PostStatus.ACTIVE)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs

    def perform_create(self, serializer):
        # B2B enabled check
        profile = getattr(self.request.user, "b2b_profile", None)
        if not profile or not profile.is_enabled:
            raise PermissionDenied("B2B yoqilmagan (admin panelda yoqiladi)")

        ok, msg = can_create_b2b_post(self.request.user)
        if not ok:
            raise PermissionDenied(msg)

        post = serializer.save(author=self.request.user)
        inc_b2b_post(self.request.user)
        return post


class B2BPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    serializer_class = B2BPostSerializer
    queryset = B2BPost.objects.select_related("author").all()

    def perform_destroy(self, instance):
        # delete allowed only for author due to permission class
        instance.delete()
