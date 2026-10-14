import logging
from decouple import config as env_config
from google.api_core.exceptions import GoogleAPIError
from google.auth.exceptions import GoogleAuthError
from datetime import timedelta
import json
from django.utils.timezone import now
from django.db import models
from django.db.models import Count
from landing.models import Contact,ContactPartner
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from constance import config
from django.core.cache import cache

# Path to your service account JSON key

def get_ga4_last_30_days_metrics():
    credentials_path = env_config("GOOGLE_APPLICATION_CREDENTIALS", default="g4.json")  # Path to your service account JSON key
    empty_metrics = dict(last_30_days_visitors=0, last_30_days_clicks=0, last_30_days_events=0)
    if not config.G4_GOOGLE_ANAYTICS_PROPERTY_ID:
        return empty_metrics
    property_id = f"properties/{config.G4_GOOGLE_ANAYTICS_PROPERTY_ID}"  # Replace with your GA4 property ID 481394031

    metrics = cache.get(property_id)
    if not metrics :
        try:
            # Initialize the client
            client = BetaAnalyticsDataClient.from_service_account_file(credentials_path)

            # Define the request to fetch all metrics at once
            request = RunReportRequest(
                property=property_id,
                metrics=[
                    Metric(name="activeUsers"),    # Total unique visitors
                    Metric(name="sessions"),       # Total sessions (clicks)
                    Metric(name="eventCount")      # Total events
                ],
                date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
            )

            # Fetch the report
            response = client.run_report(request, timeout=10)
                # Extract metrics (default order: activeUsers, sessions, eventCount)
            if not response.rows:
                return empty_metrics
            metrics = {
                "last_30_days_visitors": int(response.rows[0].metric_values[0].value),
                "last_30_days_clicks": int(response.rows[0].metric_values[1].value),
                "last_30_days_events": int(response.rows[0].metric_values[2].value),
            }
        except (OSError, ValueError, GoogleAPIError, GoogleAuthError):
            logging.getLogger(__name__).warning('Google Analytics unavailable', exc_info=True)
            metrics = empty_metrics
        cache.set(property_id,metrics,60*15)

    return metrics


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for the index template which is used as the dashboard.
    """
    analytics_data = get_ga4_last_30_days_metrics()
    today = now()
    dates = [(today - timedelta(days=x)).date() for x in range(29, -1, -1)]
    date_30_days_ago = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=29)

    # Filter the invoices initiated in the last 30 days
    recent_contacts = Contact.objects.filter(created_at__gte=date_30_days_ago)
    daily_contacts = recent_contacts.annotate(date=models.functions.TruncDate('created_at')).values('date').annotate(count=Count('id'))

    # Gather the payment data from completed invoices
    partner_contacts = ContactPartner.objects.filter(created_at__gte=date_30_days_ago)
    daily_partner_contact = partner_contacts.annotate(date=models.functions.TruncDate('created_at')).values('date').annotate(count=Count('id'))

    # Prepare data for the dashboard
    contact_counts = {row['date']: row['count'] for row in daily_contacts}
    partner_counts = {row['date']: row['count'] for row in daily_partner_contact}
    contactus_data = [contact_counts.get(date, 0) for date in dates]
    contactpartner_data = [partner_counts.get(date, 0) for date in dates]

    context.update({
        "total_contact_last_30_days": recent_contacts.count(),
        "total_partner_contacts_last_30_days": partner_contacts.count(),
        "analytics_data":analytics_data,
        "chart": json.dumps({
            "labels": [date.isoformat() for date in dates],
            "datasets": [
                {
                    "label": "Contact us ",
                    "data": contactus_data,
                    "backgroundColor": "#1e90ff",
                    "borderColor": "#1e90ff",
                    "type": "line",
                    "fill": False,
                },
                {
                    "label": "Partners contacts",
                    "data": contactpartner_data,
                    "backgroundColor": "#f43f5e",
                    "borderColor": "#f43f5e",
                    "type": "bar",
                },
            ]
        }),
            "chart_payment": json.dumps({
            "labels": [date.isoformat() for date in dates],
            "datasets": [
                {
                    "label": "Payments",
                    "data": contactpartner_data,
                    "backgroundColor": "#f43f5e",
                    "borderColor": "#f43f5e",
                    "type": "bar",
                },
            ]
        }),
    })
    return context
