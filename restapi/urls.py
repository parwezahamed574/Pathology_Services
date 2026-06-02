from django.urls import path

from restapi.views import (
    ReceiveSampleCreateAPIView,
    ReceiveSampleListAPIView,
    ReceiveSampleAPIView,
    RejectSampleAPIView,
    ReceiveActivityLogsAPIView,
    DeleteSampleAPIView,
    ActiveSamplesAPIView,
    DeletedSamplesAPIView,
    ShipmentReceivedCreateAPIView,
)

urlpatterns = [

    # CREATE SAMPLE API
    path(
        "create-sample/",
        ReceiveSampleCreateAPIView.as_view(),
        name="create-sample"
    ),

    # SAMPLE LIST API
    path(
        "samples/",
        ReceiveSampleListAPIView.as_view(),
        name="sample-list"
    ),

    # RECEIVE SAMPLE API
    path(
        "receive-sample/<int:sample_id>/",
        ReceiveSampleAPIView.as_view(),
        name="receive-sample"
    ),

    # REJECT SAMPLE API
    path(
        "reject-sample/<int:sample_id>/",
        RejectSampleAPIView.as_view(),
        name="reject-sample"
    ),

    # ACTIVITY LOGS API
    path(
        "activity-logs/",
        ReceiveActivityLogsAPIView.as_view(),
        name="activity-logs"
    ),

    # DELETE SAMPLE API
    path(
        "delete-sample/<int:sample_id>/",
        DeleteSampleAPIView.as_view(),
        name="delete-sample"
    ),

    # ACTIVE SAMPLES API
    path(
        "active-samples/",
        ActiveSamplesAPIView.as_view(),
        name="active-samples"
    ),

    # DELETED SAMPLES API
    path(
        "deleted-samples/",
        DeletedSamplesAPIView.as_view(),
        name="deleted-samples"
    ),

    # CREATE SHIPMENT RECEIVED API
    path(
        "create-shipment-received/",
        ShipmentReceivedCreateAPIView.as_view(),
        name="create-shipment-received"
    ),

]