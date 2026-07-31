from rest_framework import serializers
from .models import Mahasiswa, Dosen, Course, Materi, Tugas


class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = '__all__'


class DosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class MateriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materi
        fields = '__all__'


class TugasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tugas
        fields = '__all__'