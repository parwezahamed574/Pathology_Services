import logging
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.timezone import now
from django.forms.models import model_to_dict

from restapi.models import ReceiveSample
from restapi.serializers.receive_serializer import ReceiveSampleSerializer
from restapi.models.shipment_received import ShipmentReceived


logger = logging.getLogger(__name__)


def get_receive_sample_or_404(sample_id):
    return get_object_or_404(ReceiveSample, id=sample_id)


# =====================================================
# CREATE SAMPLE API
# =====================================================

class ReceiveSampleCreateAPIView(APIView):

    def post(self, request):
        try:
            serializer = ReceiveSampleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            sample = serializer.save(status="Shipped")

            return Response(
                {
                    "message": "Sample created successfully",
                    "data": ReceiveSampleSerializer(sample).data
                },
                status=status.HTTP_201_CREATED
            )

        except ValidationError as ve:
            return Response(
                {"error": ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# LIST + SEARCH API
# =====================================================

class ReceiveSampleListAPIView(APIView):

    def get(self, request):
        try:
            search = request.GET.get("search", "")
            status_value = request.GET.get("status")

            queryset = ReceiveSample.objects.filter(is_deleted=False)

            if status_value:
                queryset = queryset.filter(status=status_value)

            if search:
                queryset = queryset.filter(
                    Q(patient_name__icontains=search) |
                    Q(specimen_no__icontains=search) |
                    Q(shipment_no__icontains=search) |
                    Q(test_name__icontains=search)
                )

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# RECEIVE SAMPLE API
# =====================================================

class ReceiveSampleAPIView(APIView):

    def post(self, request, sample_id):
        try:
            sample = get_receive_sample_or_404(sample_id)

            sample.receive_date = request.data.get("receive_date")
            sample.receive_time = request.data.get("receive_time")
            sample.accepted_by = request.data.get("accepted_by")
            sample.remark = request.data.get("remark")
            sample.sub_optimal = request.data.get("sub_optimal", False)

            sample.shipment_received_id = request.data.get("shipment_received")

            sample.status = "Received"

            sample.save()

            serializer = ReceiveSampleSerializer(sample)

            return Response(
                {
                    "message": "Sample received successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Sample not found or Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# REJECT SAMPLE API
# =====================================================

class RejectSampleAPIView(APIView):

    def post(self, request, sample_id):
        try:
            sample = get_receive_sample_or_404(sample_id)

            sample.receive_date = request.data.get("receive_date")
            sample.receive_time = request.data.get("receive_time")

            sample.accepted_by = None
            sample.rejected_by = request.data.get("rejected_by")

            sample.remark = request.data.get("remark")
            sample.resend_new_sample = request.data.get("resend_new_sample", False)
            sample.sub_optimal = False
            sample.status = "Rejected"

            sample.save()

            serializer = ReceiveSampleSerializer(sample)

            return Response(
                {
                    "message": "Sample rejected successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Sample not found or Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# ACTIVITY LOGS API
# =====================================================

class ReceiveActivityLogsAPIView(APIView):

    def get(self, request):
        try:
            queryset = ReceiveSample.objects.filter(
                status__in=["Received", "Rejected"]
            ).order_by("-id")

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(
                {
                    "message": "Activity logs fetched successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# SOFT DELETE SAMPLE API
# =====================================================

class DeleteSampleAPIView(APIView):

    def delete(self, request, sample_id):
        try:
            sample = get_receive_sample_or_404(sample_id)

            sample.is_deleted = True
            sample.deleted_at = now()

            sample.save()

            return Response(
                {
                    "message": "Sample deleted successfully"
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Sample not found or Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# ACTIVE SAMPLES API
# =====================================================

class ActiveSamplesAPIView(APIView):

    def get(self, request):
        try:
            queryset = ReceiveSample.objects.filter(
                is_deleted=False
            ).order_by("-id")

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(
                {
                    "message": "Active samples fetched successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# DELETED SAMPLES API
# =====================================================

class DeletedSamplesAPIView(APIView):

    def get(self, request):
        try:
            queryset = ReceiveSample.objects.filter(
                is_deleted=True
            ).order_by("-id")

            serializer = ReceiveSampleSerializer(queryset, many=True)

            return Response(
                {
                    "message": "Deleted samples fetched successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================================
# CREATE SHIPMENT RECEIVED API
# =====================================================

class ShipmentReceivedCreateAPIView(APIView):

    def post(self, request):
        try:

            shipment = ShipmentReceived.objects.create(
                receive_date=request.data.get("receive_date"),
                received_no=request.data.get("received_no"),
                status=request.data.get("status"),
                result=request.data.get("result")
            )

            return Response(
                {
                    "message": "Shipment received created successfully",
                    "data": model_to_dict(shipment)
                },
                status=status.HTTP_201_CREATED
            )

        except Exception:
            logger.error(traceback.format_exc())

            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )