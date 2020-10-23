from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import datetime, TruncDate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import POST, LIKE, CustomUser
from .serializers import POSTSerializer, LIKESerializer
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password


class Post(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = POST.objects.all()
        serializer = POSTSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        instance = POSTSerializer(data=request.data)
        if instance.is_valid():
            instance.save(author=self.request.user)
            return Response(instance.data, status=status.HTTP_201_CREATED)
        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)


class Like(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        instance = LIKESerializer(data=request.data)
        if LIKE.objects.get(post=POST.objects.get(id=post_id)):
            return Response({"Post does not exist": {"post_id": post_id}},
                            status=status.HTTP_400_BAD_REQUEST)
        elif instance.is_valid():
            try:
                like = instance.save(author=self.request.user, post=POST.objects.get(id=post_id))
                return Response({"Liked": {"post_id": like.post.id, "created_date": like.created_date}},
                                status=status.HTTP_201_CREATED)
            except:
                return Response({"Already liked": {"post_id": post_id}},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            like = LIKE.objects.get(post=POST.objects.get(id=post_id), author=self.request.user)
            like.delete()
            return Response({"Unliked": {"post_id": post_id}},
                            status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"Like does not exist": {"post_id": post_id}},
                            status=status.HTTP_204_NO_CONTENT)


class Analytics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from_date = datetime.datetime.strptime(self.request.GET.get('from_date'), "%Y-%m-%d").date()
        to_date = datetime.datetime.strptime(self.request.GET.get('to_date'), "%Y-%m-%d").date()
        if from_date and to_date:
            data = LIKE.objects.filter(created_date__lte=to_date, created_date__gte=from_date) \
                .annotate(date=TruncDate('created_date')).values('created_date').annotate(likes=Count('id'))
            return Response(data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Activity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'last_login': self.request.user.last_login, 'last_request': self.request.user.last_request})


class ObtainToken(APIView):
    def post(self, request):
        user = CustomUser.objects.get(username=request.data['username'])
        pass_valid = check_password(request.data['password'], user.password)
        if user is not None and pass_valid:
            login(self.request, user)
            return Response(data=get_tokens_for_user(user), status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh.access_token.lifetime = timedelta(days=10)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
