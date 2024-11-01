# Generated by Django 5.1.2 on 2024-10-27 18:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField()),
                ('cpf', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='CPF must be in the format XXX.XXX.XXX-XX', regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$')])),
                ('is_published', models.BooleanField(default=False)),
                ('marital_status', models.CharField(choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('DIVORCED', 'Divorced'), ('WIDOWED', 'Widowed')], max_length=20)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
                ('degree', models.CharField(choices=[('TECHNICAL', 'Technical'), ('BACHELOR', 'Bachelor'), ('SPECIALIZATION', 'Specialization'), ('MASTERS', 'Masters'), ('DOCTORATE', 'Doctorate')], max_length=30)),
                ('start_date', models.DateField()),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('in_progress', models.BooleanField(default=False)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='curriculums.personaldata')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Phone must be in the format (XX) XXXXX-XXXX', regex='^\\(\\d{2}\\) \\d{4,5}-\\d{4}$')])),
                ('address', models.CharField(max_length=200)),
                ('neighborhood', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='ZIP code must be in the format XXXXX-XXX', regex='^\\d{5}-\\d{3}$')])),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='curriculums.personaldata')),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('current', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='curriculums.personaldata')),
            ],
        ),
    ]
