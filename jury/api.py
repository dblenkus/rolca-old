from rest_framework import viewsets, serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('judge',)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_queryset(self):
        queryset = super(RatingViewSet, self).get_queryset()
        judge = self.request.user.id
        photo = self.request.QUERY_PARAMS.get('photo')
        if photo:
            return queryset.filter(judge__id=judge, photo__id=photo)
        else:
            return queryset.filter(judge__id=judge)

    def perform_create(self, serializer):
        serializer.save(judge=self.request.user)
