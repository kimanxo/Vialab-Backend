from django.db import models


# stores the data about a specific blood test(exam)
class Exam(models.Model):
    abbrv = models.CharField(
        max_length=100, unique=True, blank=False
    )  # exam abbreviation
    price = models.IntegerField(blank=False, null=False)
    available = models.BooleanField(blank=False, null=False, default=True)
    _type = models.CharField(max_length=64, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    # the representation of the table title in the admin panel
    def __str__(self):
        return self.abbrv


# stores the data about one or more exam ordered by the patient, along some personal details for statistics
class Order(models.Model):
    exam = models.ManyToManyField(Exam, related_name="orders")  # the ordered exam(s)
    patient = models.CharField(max_length=100, blank=False)
    done = models.BooleanField(blank=False, null=False, default=False)  # order status
    email = models.EmailField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=False, null=False, default="")
    age = models.CharField(max_length=10, blank=False, null=False, default="")
    ordered_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(
        unique=True, max_length=12, blank=False, null=False
    )  # is to traceback the order status

    # the representation of the table title in the admin panel
    def __str__(self):
        return self.patient


# stores data about the frequently asked questions and their answers
class FAQ(models.Model):
    question = models.CharField(max_length=100, unique=True, blank=False)
    answer = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # the representation of the table title in the admin panel
    def __str__(self):
        return self.question


# stores data about ads created by the admin
class Announce(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    valid = models.BooleanField(blank=False, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # the representation of the table title in the admin panel
    def __str__(self):
        return self.title


# stores data about the feedback messages sent by the users from the contact form
class Feedback(models.Model):
    email = models.EmailField(max_length=100, blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False)
    message = models.TextField(max_length=1000, blank=False, null=False)
    reply = models.TextField(max_length=1000, blank=True, null=True)
    read = models.BooleanField(blank=False, null=False, default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    # the representation of the table title in the admin panel
    def __str__(self):
        return self.subject


# stores descriptive data about the website which can be edited from the admin panel
class About(models.Model):
    description = models.TextField(max_length=1000, blank=False, null=False)
    doctor_intro = models.TextField(max_length=1000, blank=False, null=False)
    location_guide = models.TextField(max_length=1000, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    cell_phone = models.IntegerField(blank=False, null=False)
    line_phone = models.IntegerField(blank=False, null=False)
    facebook = models.CharField(max_length=100, blank=False)
    instagram = models.CharField(max_length=100, blank=False)
    work_times = models.CharField(max_length=100, blank=False)

    # the representation of the table title in the admin panel
    def __str__(self):
        return "About Information"





# stores the harvested email from the newsletter form
class Newsletter(models.Model):
    email = models.EmailField(max_length=100, blank=False, null=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    # the representation of the table title in the admin panel
    def __str__(self):
        return self.email
