from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer


class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response({'profile': user_profile.data},
                            status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Error in GetUserProfileView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            data = self.request.data

            address_line_1 = data['address_line_1']
            address_line_2 = data['address_line_2']
            city = data['city']
            state_province_region = data['state_province_region']
            postal_zip_code = data['postal_zip_code']
            telephone_number = data['telephone_number']
            country_region = data['country_region']

            user_profile = UserProfile.objects.filter(user=user).update(
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state_province_region=state_province_region,
                postal_zip_code=postal_zip_code,
                telephone_number=telephone_number,
                country_region=country_region
            )

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response(
                {'profile': user_profile.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Error in UpdateUserProfileView'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
