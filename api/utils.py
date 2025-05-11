import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils import timezone
from django.db.models import Count, Sum
import string
import random
from .models import Order, Exam
from .serializers import OrderSerializer, AbbreviationSerializer


def getMostOrdered():
    # Get the current date
    today = timezone.now().date()
    # Filter orders that have been ordered today
    orders_today = Order.objects.filter(ordered_at__date=today)

    # Aggregate the count of each exam in today's orders
    most_ordered_exam = (
        orders_today.values("exam__abbrv")
        .annotate(order_count=Count("exam"))
        .order_by("-order_count")
        .first()
    )

    if most_ordered_exam:
        return {
            "exam": most_ordered_exam["exam__abbrv"],
            "count": most_ordered_exam["order_count"],
        }
    else:
        return {}

    # Return the serialized data


def getTodayRevenue():
    # Get the current date
    today = timezone.now().date()

    # Filter orders that have been ordered today
    orders_today = Order.objects.filter(ordered_at__date=today)

    # Calculate the revenue by summing the prices of all exams for today's orders
    revenue = (
        orders_today.aggregate(total_revenue=Sum("exam__price"))["total_revenue"] or 0
    )

    # Return the revenue
    return revenue


def getSexStats():
    # Get the current date
    today = timezone.now().date()

    # Filter orders that have been ordered today
    orders_today = Order.objects.filter(ordered_at__date=today)

    # Aggregate the count of male and female orders
    sex_statistics = orders_today.values("sex").annotate(order_count=Count("sex"))

    # Initialize counters for male and female orders
    male_count = 0
    female_count = 0

    # Iterate through the sex statistics
    for stat in sex_statistics:
        if stat["sex"] == "male":
            male_count += stat["order_count"]
        elif stat["sex"] == "female":
            female_count += stat["order_count"]

    # Return the sex statistics
    return {"males": male_count, "females": female_count}


def getAgeStats():
    # Get the current date
    today = timezone.now().date()

    # Filter orders that have been ordered today
    orders_today = Order.objects.filter(ordered_at__date=today)

    # Aggregate the count of orders for each age category
    age_statistics = orders_today.values("age").annotate(order_count=Count("age"))

    # Initialize counters for each age category
    kids_count = 0
    adults_count = 0
    old_people_count = 0

    # Iterate through the age statistics
    for stat in age_statistics:
        if stat["age"] == "kid":
            kids_count += stat["order_count"]
        elif stat["age"] == "adult":
            adults_count += stat["order_count"]
        elif stat["age"] == "old":
            old_people_count += stat["order_count"]

    # Return the age statistics
    return {
        "kids": kids_count,
        "adults": adults_count,
        "old_people": old_people_count,
    }


def getFrequentExams():
    # Aggregate the count of orders for each exam
    exam_statistics = Exam.objects.annotate(order_count=Count("orders"))

    # Order the exams by the count of orders in descending order
    top_exams = exam_statistics.order_by("-order_count")[:3]

    # Serialize the top exams
    serializer = AbbreviationSerializer(top_exams, many=True)

    # Return the serialized top exams
    return serializer.data


def getRecentClients():
    latest_orders = Order.objects.order_by("-ordered_at")[:4]
    serializer = OrderSerializer(latest_orders, many=True)
    return serializer.data


# a function to send the newletters
def send_mail(subject, message, to):
    # loading credentials
    email_sender = "saadaouiismailmed@gmail.com"
    email_password = "jyhwznxverzvfadt"
    email_receiver = to

    # message data
    body = f"<html><body>{message}</body></html>"
    msg = MIMEMultipart("alternative")
    msg["From"] = email_sender
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    try:
        # attemting to excute (ssl in mind)
        mail = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail.ehlo()
        mail.login(email_sender, email_password)
        mail.sendmail(email_sender, email_receiver, msg.as_string())
        mail.quit()
    except Exception as e:
        print(f"Error while sending email: {e}")


def generateCode():

    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    while Order.objects.filter(code=code).exists:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
        return code
    return code


def getFinancials(year, month, week, *args, **kwargs):
    # Validate year range
    current_year = timezone.now().year
    if year < current_year - 5 or year > current_year:
        raise ValueError("Year must be between the last 5 years and the current year.")

    # Validate month range
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12.")

    # Calculate the start and end date of the month
    first_day_of_month = timezone.datetime(year, month, 1).date()
    last_day_of_month = timezone.datetime(year, month, 1).date() + timezone.timedelta(
        days=32
    )
    last_day_of_month = timezone.datetime(
        last_day_of_month.year, last_day_of_month.month, 1
    ) - timezone.timedelta(days=1)

    # Calculate the number of weeks in the month
    total_weeks = (last_day_of_month.day + first_day_of_month.weekday()) // 7 + 1

    # Validate week range
    if week < 1 or week > total_weeks:
        raise ValueError(
            "Week must be between 1 and {} for the specified month.".format(total_weeks)
        )

    # Calculate the start and end date of the specified week
    start_date = first_day_of_month + timezone.timedelta(weeks=week - 1)
    end_date = start_date + timezone.timedelta(days=6)

    # Adjust end date if it exceeds the last day of the month
    end_date = min(end_date, last_day_of_month.date())

    # Query orders within the specified time frame
    orders = Order.objects.filter(ordered_at__date__range=[start_date, end_date])

    # Create a dictionary to store revenue for each day
    revenue_per_day = {}

    # Iterate over each day in the specified week
    current_date = start_date
    while current_date <= end_date:
        # Filter orders for the current day
        orders_for_day = orders.filter(ordered_at__date=current_date)

        # Calculate revenue for the current day
        revenue = (
            orders_for_day.aggregate(total_revenue=Sum("exam__price"))["total_revenue"]
            or 0
        )

        # Store revenue for the current day
        revenue_per_day[current_date.day] = revenue

        # Move to the next day
        current_date += timezone.timedelta(days=1)
    return revenue_per_day