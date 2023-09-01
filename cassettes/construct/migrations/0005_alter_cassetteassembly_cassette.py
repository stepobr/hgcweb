# Generated by Django 4.1.7 on 2023-06-01 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construct', '0004_alter_cassetteassembly_workstation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cassetteassembly',
            name='cassette',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assembly', to='construct.cassette'),
        ),
    ]
