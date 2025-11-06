"""
Serializers for QR code management.
"""
from rest_framework import serializers
from .models import QRCode, Tag, QRTemplate


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['id', 'created_at']


class QRCodeListSerializer(serializers.ModelSerializer):
    """Serializer for listing QR codes (minimal fields)."""
    short_url = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    qr_type_display = serializers.CharField(source='get_qr_type_display', read_only=True)

    class Meta:
        model = QRCode
        fields = [
            'id', 'name', 'qr_type', 'qr_type_display', 'short_url',
            'total_scans', 'is_active', 'is_expired', 'created_at',
            'last_scanned_at', 'qr_image'
        ]


class QRCodeDetailSerializer(serializers.ModelSerializer):
    """Serializer for QR code details."""
    short_url = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = QRCode
        fields = [
            'id', 'name', 'qr_type', 'content', 'short_code', 'custom_domain',
            'foreground_color', 'background_color', 'logo', 'size', 'format',
            'error_correction', 'qr_image', 'enable_tracking', 'is_active',
            'expires_at', 'total_scans', 'unique_scans', 'last_scanned_at',
            'tags', 'tag_ids', 'folder', 'short_url', 'is_expired',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'short_code', 'qr_image', 'total_scans', 'unique_scans',
            'last_scanned_at', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        qr_code = QRCode.objects.create(**validated_data)

        if tag_ids:
            qr_code.tags.set(Tag.objects.filter(id__in=tag_ids, user=qr_code.user))

        return qr_code

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids is not None:
            instance.tags.set(Tag.objects.filter(id__in=tag_ids, user=instance.user))

        return instance


class QRCodeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating QR codes."""
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )

    class Meta:
        model = QRCode
        fields = [
            'name', 'qr_type', 'content', 'custom_domain',
            'foreground_color', 'background_color', 'logo', 'size',
            'format', 'error_correction', 'enable_tracking', 'is_active',
            'expires_at', 'tag_ids', 'folder'
        ]

    def validate_content(self, value):
        """Validate content based on QR type."""
        qr_type = self.initial_data.get('qr_type')

        if qr_type == 'url' and 'url' not in value:
            raise serializers.ValidationError("URL is required for URL type QR codes.")

        if qr_type == 'vcard':
            required_fields = ['first_name', 'last_name', 'phone']
            missing = [f for f in required_fields if not value.get(f)]
            if missing:
                raise serializers.ValidationError(
                    f"Missing required vCard fields: {', '.join(missing)}"
                )

        if qr_type == 'wifi':
            if 'ssid' not in value:
                raise serializers.ValidationError("SSID is required for WiFi QR codes.")

        return value

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        user = self.context['request'].user

        # Check if user has reached QR code limit
        if user.has_reached_qr_limit():
            raise serializers.ValidationError(
                "You have reached your QR code limit. Please upgrade your plan."
            )

        qr_code = QRCode.objects.create(user=user, **validated_data)

        if tag_ids:
            qr_code.tags.set(Tag.objects.filter(id__in=tag_ids, user=user))

        return qr_code


class QRTemplateSerializer(serializers.ModelSerializer):
    """Serializer for QR code templates."""
    class Meta:
        model = QRTemplate
        fields = [
            'id', 'name', 'description', 'category', 'qr_type',
            'foreground_color', 'background_color', 'template_image',
            'is_premium', 'usage_count'
        ]


class BulkQRCreateSerializer(serializers.Serializer):
    """Serializer for bulk QR code creation."""
    qr_codes = QRCodeCreateSerializer(many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        qr_codes_data = validated_data['qr_codes']

        # Check if user has enough quota
        count = len(qr_codes_data)
        from qrcodes.models import QRCode
        active_count = QRCode.objects.filter(user=user, is_active=True).count()

        if active_count + count > user.qr_code_limit:
            raise serializers.ValidationError(
                f"Cannot create {count} QR codes. You would exceed your limit."
            )

        # Create QR codes
        qr_codes = []
        for qr_data in qr_codes_data:
            tag_ids = qr_data.pop('tag_ids', [])
            qr_code = QRCode.objects.create(user=user, **qr_data)

            if tag_ids:
                qr_code.tags.set(Tag.objects.filter(id__in=tag_ids, user=user))

            qr_codes.append(qr_code)

        return qr_codes
