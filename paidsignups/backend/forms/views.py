from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Form
from .serializers import FormSerializer, FormCreateSerializer, FormPublicSerializer


class FormViewSet(viewsets.ModelViewSet):
    """Form CRUD operations"""
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active', 'is_published']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'views', 'submissions']

    def get_queryset(self):
        return Form.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return FormCreateSerializer
        return FormSerializer

    def perform_create(self, serializer):
        form = serializer.save()
        # Update user's form count
        self.request.user.forms_created += 1
        self.request.user.save()

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def public(self, request, pk=None):
        """Get public form data for embedding"""
        form = get_object_or_404(Form, id=pk, is_active=True, is_published=True)
        # Increment view count
        form.views += 1
        form.save(update_fields=['views'])
        serializer = FormPublicSerializer(form)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a form"""
        form = self.get_object()
        form.pk = None
        form.id = None
        form.slug = f"{form.slug}-copy"
        form.name = f"{form.name} (Copy)"
        form.is_published = False
        form.views = 0
        form.submissions = 0
        form.save()

        # Update user's form count
        request.user.forms_created += 1
        request.user.save()

        serializer = self.get_serializer(form)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def toggle_publish(self, request, pk=None):
        """Toggle form published status"""
        form = self.get_object()
        form.is_published = not form.is_published
        form.save(update_fields=['is_published'])
        return Response({'is_published': form.is_published})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get form statistics"""
        forms = self.get_queryset()
        return Response({
            'total_forms': forms.count(),
            'published_forms': forms.filter(is_published=True).count(),
            'total_views': sum(f.views for f in forms),
            'total_submissions': sum(f.submissions for f in forms),
        })
