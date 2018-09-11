"""Views module definfing REST APIs and Business Logic."""
import re

from django.core.cache import cache
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, SmsSerializer
from .models import UserModel, SmsModel, PhoneNumberModel
from . import constants


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class SmsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = SmsModel.objects.all()
    serializer_class = SmsSerializer

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class InBoundViewSet(SmsViewSet):
    """View set class for Inbound sms API, it inherits the class SMSViewSet."""
    def create(self, request, *args, **kwargs):
        """Create method for InBoundViewSet API."""
        try:
            data = {k: v for k, v in self.request.data.items()
                    if k not in ['csrftoken']}
            _from = self.request.data.get('_from')
            to = self.request.data.get('to')
            text = self.request.data.get('text')
            # check if attributes are present
            if not _from:
                return Response({"message": "",
                                 "error": "from attribute is missing"})
            if not to:
                return Response({"message": "",
                                 "error": "to attribute is missing"})
            if not text:
                return Response({"message": "",
                                 "error": "text attribute is missing"})
            # check if attributes are valid
            if not isinstance(_from, str):
                return Response({"message": "",
                                 "error": "from attribute is invalid"})
            if not isinstance(_from, to):
                return Response({"message": "",
                                 "error": "to attribute is invalid"})
            if not isinstance(_from, text):
                return Response({"message": "",
                                 "error": "text attribute is invalid"})

            # check if to attribute present in phone_number table for current
            # user
            if to:
                phone_no = list(PhoneNumberModel.objects.filter(
                    phone_no=to, account_id=self.request.user.id))
                if not phone_no:
                    return Response({"message": "",
                                     "error": "to parameter not found"})

            if text:
                pattern = re.compile(constants.REG_EX)
                if pattern.match(text):
                    cache.set((_from, to), True, timeout=14400)
            res = SmsModel.objects.create(**data)
            res.save()
            return Response({"message": "inbound sms ok",
                             "error": ""},
                            status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "",
                             "error": "unknown failure"})


class OutBoundViewSet(SmsViewSet):
    """View set class for Inbound sms API, it inherits the class SMSViewSet."""
    def create(self, request, *args, **kwargs):
        """Create method for InBoundViewSet API."""
        try:
            data = {k: v for k, v in self.request.data.items()
                    if k not in ['csrftoken']}
            _from = self.request.data.get('_from')
            to = self.request.data.get('to')
            text = self.request.data.get('text')
            # check if attributes are present
            if not _from:
                return Response({"message": "",
                                 "error": "from attribute is missing"})
            if not to:
                return Response({"message": "",
                                 "error": "to attribute is missing"})
            if not text:
                return Response({"message": "",
                                 "error": "text attribute is missing"})
            # check if attributes are valid
            if not isinstance(_from, str):
                return Response({"message": "",
                                 "error": "from attribute is invalid"})
            if not isinstance(_from, to):
                return Response({"message": "",
                                 "error": "to attribute is invalid"})
            if not isinstance(_from, text):
                return Response({"message": "",
                                 "error": "text attribute is invalid"})

            # check if to attribute present in phone_number table for current
            # user
            if _from:
                phone_no = list(PhoneNumberModel.objects.filter(
                    phone_no=_from, account_id=self.request.user.id))
                if not phone_no:
                    return Response({"message": "",
                                     "error": "from parameter not found"})

            if to and cache.get((_from, to)):
                return Response({"message": "",
                                 "error": "sms from {} to {} "
                                          "blocked by STOP request"
                                          .format(_from, to)})

            res = SmsModel.objects.create(**data)
            res.save()
            return Response({"message": "inbound sms ok",
                             "error": ""},
                            status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "",
                             "error": "unknown failure"})
