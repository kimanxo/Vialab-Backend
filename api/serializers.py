from .models import Exam, Feedback, Announce, FAQ, About, Order, Newsletter
from rest_framework import serializers


# Serializer for the Announce model.
class AnnounceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announce
        fields = "__all__"


# Serializer for the Feedback model.
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")

        # If this is a POST request from an unauthenticated user
        if request and request.method == "POST" and not request.user.is_authenticated:
            self.fields.pop("read", None)
            self.fields.pop("reply", None)

    def create(self, validated_data):
        request = self.context.get("request")
        if request and not request.user.is_authenticated:
            validated_data.pop("read", None)
            validated_data.pop("reply", None)
        return super().create(validated_data)


# Serializer for the Exam model.
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


# Serializer for the Order model.
class AbbreviationField(serializers.RelatedField):
    def to_representation(self, value):
        return value.abbrv

    def get_queryset(self):
        return Exam.objects.all()


class OrderCleanSerializer(serializers.ModelSerializer):

    exam = serializers.SerializerMethodField()

    def get_exam(self, obj):
        return [{"id": exam.id, "abbrv": exam.abbrv} for exam in obj.exam.all()]

    total_price = serializers.SerializerMethodField()  # Custom field for total price

    class Meta:
        model = Order
        fields = "__all__"

    def get_total_price(self, obj):
        # Calculate total price by summing prices of related exams
        return sum(exam.price for exam in obj.exam.all())


class OrderSerializer(serializers.ModelSerializer):
    exam = serializers.SlugRelatedField(
        slug_field="id", queryset=Exam.objects.all(), many=True
    )
    total_price = serializers.SerializerMethodField()  # Custom field for total price

    class Meta:
        model = Order
        fields = "__all__"

    def get_total_price(self, obj):
        # Calculate total price by summing prices of related exams
        return sum(exam.price for exam in obj.exam.all())


# Serializer for the FAQ model.
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


# Serializer for the Newsletter model.
class Newsletterserializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = "__all__"


# Serializer for the About model.
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"


class AbbreviationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ["abbrv"]
