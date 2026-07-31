from django.db import models
from django.contrib.auth.models import User


# ==========================
# PROFILE
# ==========================
class Profile(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dosen', 'Dosen'),
        ('mahasiswa', 'Mahasiswa'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


# ==========================
# SEMESTER
# ==========================
class Semester(models.Model):

    nama = models.CharField(max_length=50)

    def __str__(self):
        return self.nama


# ==========================
# KELAS
# ==========================
class Kelas(models.Model):

    nama = models.CharField(max_length=20)

    def __str__(self):
        return self.nama


# ==========================
# DOSEN
# ==========================
class Dosen(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nip = models.CharField(max_length=30)

    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


# ==========================
# MAHASISWA
# ==========================
class Mahasiswa(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nim = models.CharField(max_length=30)

    nama = models.CharField(max_length=100)

    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama


# ==========================
# MATA KULIAH
# ==========================
class MataKuliah(models.Model):

    kode = models.CharField(max_length=20)

    nama = models.CharField(max_length=100)

    sks = models.IntegerField()

    def __str__(self):
        return self.nama


# ==========================
# COURSE
# ==========================
class Course(models.Model):

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)

    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE)

    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('semester', 'kelas', 'mata_kuliah')

    def __str__(self):
        return f"{self.mata_kuliah.nama} - {self.kelas.nama}"


# ==========================
# MATERI
# ==========================
class Materi(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    judul = models.CharField(max_length=200)

    deskripsi = models.TextField()

    file = models.FileField(upload_to='materi/')

    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


# ==========================
# TUGAS
# ==========================
class Tugas(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    judul = models.CharField(max_length=200)

    deskripsi = models.TextField()

    file_tugas = models.FileField(upload_to='tugas/', blank=True, null=True)

    deadline = models.DateTimeField()

    def __str__(self):
        return self.judul


# ==========================
# PENGUMPULAN TUGAS
# ==========================
class PengumpulanTugas(models.Model):

    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE)

    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)

    file_jawaban = models.FileField(upload_to='jawaban/')

    tanggal_kumpul = models.DateTimeField(auto_now_add=True)

    nilai = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.tugas.judul}"