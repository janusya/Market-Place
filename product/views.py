import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import ProfileProductSerializer, CategorySerializer
from .models import Product, Category
from .serializers import ProductGetSerializer
from permissions import IsSellerOfProduct, IsSellerAndHasStore


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductListView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductGetSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['category']
    # pagination_class = StandardResultsSetPagination

    permission_classes = (
        AllowAny,
    )

    def get(self, request, product_id=None):
        if product_id is not None:
            product = get_object_or_404(Product.objects.all(), pk=product_id)
            srz_data = self.serializer_class(instance=product)
            return Response(data=srz_data.data, status=status.HTTP_200_OK)

        products = Product.objects.all()
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(products, request)
        srz_data = self.serializer_class(instance=result_page, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def find_products(request):
    products = Product.objects.filter(
        name=request.data['name'])  # , category=request.data['category'], price=request.data['price'])
    serializer = ProductGetSerializer(products, many=True)

    return Response(serializer.data)


class CreateProductView(APIView):
    """
        check if user have store, create new product
    """

    serializer_class = ProfileProductSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        self.check_object_permissions(request, request.user)

        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save(
                seller=request.user.store,
            )
            return Response({'message': 'The product has successfully created.'}, status=status.HTTP_201_CREATED)


class UpdateProductView(APIView):
    """
        check user is seller of product and update it
    """

    serializer_class = ProfileProductSerializer

    permission_classes = (
        IsSellerOfProduct,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request, product_id=None):
        product = get_object_or_404(Product, pk=product_id)
        self.check_object_permissions(request, product)
        srz_data = self.serializer_class(data=request.data, instance=product, partial=True)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            product.save()
            return Response(data=srz_data.data, status=status.HTTP_204_NO_CONTENT)


class DeleteProductView(APIView):
    """
        check user is seller of product and delete it
    """
    permission_classes = (
        IsSellerOfProduct,
    )

    def delete(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        self.check_object_permissions(request, product)
        product.delete()
        return Response({'message': 'The product has successfully deleted.'}, status=status.HTTP_200_OK)


class ProfileProductListView(GenericAPIView):
    """
        list of products for seller user
    """

    serializer_class = ProfileProductSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    def get(self, request):
        products = request.user.store.products.all()
        srz_data = self.serializer_class(instance=products, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CategoryListView(GenericAPIView):
    """
        get list of categories for show to all users
    """

    serializer_class = CategorySerializer
    permission_classes = (
        AllowAny,
    )

    def get(self, request):
        categories = Category.objects.all()
        srz_data = self.serializer_class(instance=categories, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class FilterProducByCategoryView(GenericAPIView):
    """
        get list of products for show to users with special category
    """

    serializer_class = ProductGetSerializer
    permission_classes = (
        AllowAny,
    )

    def get(self, request, category_slug):
        products = Product.objects.filter(category__slug=category_slug)
        srz_data = self.serializer_class(instance=products, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
