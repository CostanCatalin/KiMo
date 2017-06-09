from rest_framework import serializers
from django.contrib.auth import get_user_model
from kids.models import Kid, Notification, Location, Encounter, Restriction
from datetime import date

Account = get_user_model()


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = ('url', 'id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True,
                         'style': {
                             'input_type': 'password'
                         }},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        user = Account(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True,
                         'required': False,
                         'style': {'input_type': 'password'}},
            'id': {'read_only': True},
            'username': {'read_only': True},
            'email': {'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name'] if validated_data['first_name'] else instance.first_name
        instance.last_name = validated_data['last_name'] if validated_data['last_name'] else instance.last_name
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class KidSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Kid
        fields = ('url', 'id', 'parent', 'first_name', 'last_name', 'birth_date', 'registered_date')
        extra_kwargs = {
            'id': {'read_only': True},
            'parent': {'read_only': True},
            'last_name': {'read_only': True},
            'registered_date': {'read_only': True}
        }

    def validate_birth_date(self, birth_date):
        if birth_date > date.today():
            raise serializers.ValidationError("Is your kid born into the future?")
        return birth_date

    def create(self, validated_data):
        parent = self.context['request'].user
        kid = Kid(
            parent=parent,
            first_name=validated_data['first_name'],
            last_name=parent.last_name,
            birth_date=validated_data['birth_date']
        )
        kid.save()
        return kid


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'kid', 'text', 'seen', 'date_created')

    def validate_kid(self, kid):
        if kid.parent != self.context['request'].user and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("{} is not your child".format(kid))
        return kid


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'kid', 'latitude', 'longitude', 'date_created')

    def validate_kid(self, kid):
        if kid.parent != self.context['request'].user and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("{} is not your child".format(kid))
        return kid


class RestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restriction
        fields = ('id', 'kid', 'latitude', 'longitude', 'distance', 'date_created')

    def validate_kid(self, kid):
        if kid.parent != self.context['request'].user and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("{} is not your child".format(kid))
        return kid



