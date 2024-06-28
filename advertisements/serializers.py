from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True, )

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator',
                  'status', 'created_at', ]
        read_only_fields = ('creator',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию

        user = self.context['request'].user

        # Проверка на количество открытых объявлений у пользователя
        if data.get('status') == 'OPEN':
            open_advertisements_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
            if open_advertisements_count >= 10:
                raise serializers.ValidationError("Вы уже создали максимальное количество открытых объявлений.")

        return data