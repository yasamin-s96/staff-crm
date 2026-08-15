from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import LogoutSerializer


class LogoutView(APIView):
    def post(self, *args, **kwargs):
        logout_serializer = LogoutSerializer(data=self.request.data)
        logout_serializer.is_valid(raise_exception=True)
        input_token = logout_serializer.validated_data["refresh"]
        try:
            refresh_token = RefreshToken(input_token)

            if int(refresh_token["user_id"]) == self.request.user.id:
                refresh_token.blacklist()

        except TokenError:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
