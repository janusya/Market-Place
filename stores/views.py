from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import StoreFeedbacks, Store
from .serializers import StoreSerializer, FeedbacksSerializer
from permissions import IsSeller, IsSellerAndHasStore


class CreateStoreView(APIView):

    serializer_class = StoreSerializer

    permission_classes = (
        IsSeller,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        self.check_object_permissions(request, request.user)
        try:
            store = request.user.store
            return Response({'message': 'You already create a store'})
        except:

            srz_data = self.serializer_class(data=request.data)
            if srz_data.is_valid(raise_exception=True):
                srz_data.save(
                    founder=request.user,
                )

                return Response({'message': 'The store has successfully created'})


class UpdateStoreView(APIView):

    serializer_class = StoreSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request):
        self.check_object_permissions(request, request.user)
        srz_data = self.serializer_class(data=request.data, instance=request.user.store, partial=True)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            return Response({'message': 'The store has successfully updated'})


class RetrieveStoreView(GenericAPIView):

    serializer_class = StoreSerializer
    permission_classes = (
        AllowAny,
    )

    def get(self, request, store_id=None):
        if store_id is not None:
            store = get_object_or_404(Store, pk=store_id)
            srz_data = self.serializer_class(instance=store)
            return Response(data=srz_data.data, status=status.HTTP_200_OK)

        stores = Store.objects.all()
        srz_data = self.serializer_class(instance=stores, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class FeedBacksViewSet(ModelViewSet):
    queryset = StoreFeedbacks.objects.all()
    serializer_class = FeedbacksSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


