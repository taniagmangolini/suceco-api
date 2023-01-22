"""Serializers for Register API."""
from rest_framework import serializers

from core.models import Register, Forest, Species, Reference

from utils import fields
from utils.constants import StateType, StageType

from reference.serializers import ReferenceSerializer
from species.serializers import SpeciesSerializer
from forest.serializers import ForestSerializer
from register_picture.serializers import RegisterPictureSerializer


class RegisterSerializer(serializers.ModelSerializer):
    stage = fields.EnumField(enum=StageType)
    state = fields.EnumField(enum=StateType)
    reference = ReferenceSerializer(required=True)
    species = SpeciesSerializer(required=True)
    forest = ForestSerializer(required=True)
    pictures = RegisterPictureSerializer(many=True, required=False)

    class Meta:
        model = Register
        fields = ['species',
                  'forest',
                  'reference',
                  'latitude',
                  'longitude',
                  'stage',
                  'state',
                  'pictures']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Overriding the default create method of the Model
        Register serializer to create dependencies forest, species
        and reference if necessary.
        :param validated_data: data containing all the details of a
        register.
        :return: returns a successfully created register record."""
        reference_data = validated_data.pop('reference')
        reference, created = Reference.objects.get_or_create(**reference_data)

        species_data = validated_data.pop('species')
        species, created = Species.objects.get_or_create(**species_data)

        forest_data = validated_data.pop('forest')
        forest, created = Forest.objects.get_or_create(**forest_data)

        register = Register.objects.create(
            reference=reference,
            species=species,
            forest=forest,
            stage=validated_data.pop('stage'),
            state=validated_data.pop('state'),
            latitude=validated_data.pop('latitude', None),
            longitude=validated_data.pop('longitude', None))

        return register

    def update(self, instance, validated_data):
        """Overriding the default update method of the Model Register.
        :param validated_data: data containing all the details of a
        register.
        :return: returns a successfully created register record."""
        ref_data = validated_data.pop('reference', None)
        if ref_data:
            reference, created = Reference.objects.get_or_create(**ref_data)
            instance.reference = reference

        species_data = validated_data.pop('species', None)
        if species_data:
            species, created = Species.objects.get_or_create(**species_data)
            instance.species = species

        forest_data = validated_data.pop('forest', None)
        if forest_data:
            forest, created = Forest.objects.get_or_create(**forest_data)
            instance.forest = forest

        instance.save()
        return instance


class RegisterDetailSerializer(RegisterSerializer):

    class Meta(RegisterSerializer.Meta):
        fields = RegisterSerializer.Meta.fields + ['is_active',
                                                   'created_at',
                                                   'updated_at']
