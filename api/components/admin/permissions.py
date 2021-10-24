from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from api import models
from rest_framework import status,exceptions

import logging
logger = logging.getLogger(__name__)


class IsOwner(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        try:
            point = models.Point.objects.get(pk=request.user.point_id)
        except Exception as ex:
            logger.error(ex)
            raise exceptions.PermissionDenied("Você não está vinculado a um ponto")

        # ? verifica se o usuário é dono do ponto atual
        if point.owner.id != request.user.id:
            raise exceptions.PermissionDenied("Você não é dono do ponto")
        return True