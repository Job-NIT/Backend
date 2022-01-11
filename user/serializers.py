from .models import User, Freelancer, Employer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'user_type', 'password', 'password2'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )

        attrs.pop('password2', None)
        return attrs


class FreelancerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = ('user', 'token')

    def get_token(self, obj):
        return obj.user.auth_token.key

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = User.USER_TYPE.FREELANCER

        user = UserSerializer().create(
            validated_data=user_data
        )

        user.set_password(user_data['password'])
        user.save()

        freelancer = Freelancer.objects.create(
            user=user
        )

        return freelancer


class FreelancerProfileSerializer(FreelancerSerializer):
    class Meta(FreelancerSerializer.Meta):
        fields = ('user',)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            user = UserSerializer().update(
                instance=instance.user,
                validated_data=user_data
            )
            user.save()

        return super().update(instance, validated_data)


class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = Employer
        fields = ('user', 'company', 'token')
        extra_kwargs = {
            'company': {'required': True}
        }

    def get_token(self, obj):
        return obj.user.auth_token.key

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = User.USER_TYPE.EMPLOYER

        user = UserSerializer().create(
            validated_data=user_data
        )

        user.set_password(user_data['password'])
        user.save()

        employer = Employer.objects.create(
            user=user,
            company=validated_data['company']
        )

        return employer


class EmployerProfileSerializer(EmployerSerializer):
    class Meta(EmployerSerializer.Meta):
        fields = ('user', 'company')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            user = UserSerializer().update(
                instance=instance.user,
                validated_data=user_data
            )
            user.save()

        return super().update(instance, validated_data)
