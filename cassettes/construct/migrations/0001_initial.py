# Generated by Django 4.1.7 on 2023-05-31 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cassette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(choices=[('CEE01', 'CEE01'), ('CEE02', 'CEE02'), ('CEE03', 'CEE03'), ('CEE04', 'CEE04'), ('CEE05', 'CEE05'), ('CEE06', 'CEE06'), ('CEE07', 'CEE07'), ('CEE08', 'CEE08'), ('CEE09', 'CEE09'), ('CEE10', 'CEE10'), ('CEE11', 'CEE11'), ('CEE12', 'CEE12'), ('CEE13', 'CEE13')], max_length=50, null=True)),
                ('started', models.BooleanField(default='False')),
                ('done', models.BooleanField(default='False')),
            ],
        ),
        migrations.CreateModel(
            name='CassetteType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modulemap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plane', models.CharField(max_length=50, null=True)),
                ('u', models.CharField(max_length=50, null=True)),
                ('v', models.CharField(max_length=50, null=True)),
                ('itype', models.CharField(max_length=50, null=True)),
                ('x0', models.CharField(max_length=50, null=True)),
                ('y0', models.CharField(max_length=50, null=True)),
                ('irot', models.CharField(max_length=50, null=True)),
                ('nvertices', models.CharField(max_length=50, null=True)),
                ('vx_0', models.CharField(max_length=50, null=True)),
                ('vy_0', models.CharField(max_length=50, null=True)),
                ('vx_1', models.CharField(max_length=50, null=True)),
                ('vy_1', models.CharField(max_length=50, null=True)),
                ('vx_2', models.CharField(max_length=50, null=True)),
                ('vy_2', models.CharField(max_length=50, null=True)),
                ('vx_3', models.CharField(max_length=50, null=True)),
                ('vy_3', models.CharField(max_length=50, null=True)),
                ('vx_4', models.CharField(max_length=50, null=True)),
                ('vy_4', models.CharField(max_length=50, null=True)),
                ('vx_5', models.CharField(max_length=50, null=True)),
                ('vy_5', models.CharField(max_length=50, null=True)),
                ('vx_6', models.CharField(max_length=50, null=True)),
                ('vy_6', models.CharField(max_length=50, null=True)),
                ('icassette', models.CharField(max_length=50, null=True)),
                ('trigRate', models.CharField(max_length=50, null=True)),
                ('trigLinks', models.CharField(max_length=50, null=True)),
                ('dataRate_ld', models.CharField(max_length=50, null=True)),
                ('dataLinks_ld', models.CharField(max_length=50, null=True)),
                ('dataRate_hd', models.CharField(max_length=50, null=True)),
                ('dataLinks_hd', models.CharField(max_length=50, null=True)),
                ('MB', models.CharField(max_length=50, null=True)),
                ('wagon', models.CharField(max_length=50, null=True)),
                ('isEngine', models.CharField(max_length=50, null=True)),
                ('nROCs', models.CharField(max_length=50, null=True)),
                ('power', models.CharField(max_length=50, null=True)),
                ('mrot', models.CharField(max_length=50, null=True)),
                ('phi', models.CharField(max_length=50, null=True)),
                ('HDorLD', models.CharField(max_length=50, null=True)),
                ('hash', models.CharField(max_length=50, null=True)),
                ('hash_hdld', models.CharField(max_length=50, null=True)),
                ('dataPp0', models.CharField(max_length=50, null=True)),
                ('trigPp0', models.CharField(max_length=50, null=True)),
                ('dataPp0_type', models.CharField(max_length=50, null=True)),
                ('trigPp0_type', models.CharField(max_length=50, null=True)),
                ('dataPp1', models.CharField(max_length=50, null=True)),
                ('trigPp1', models.CharField(max_length=50, null=True)),
                ('dataPp1_type', models.CharField(max_length=50, null=True)),
                ('trigPp1_type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(default=1)),
                ('details', models.CharField(max_length=100, null=True)),
                ('parts', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workstation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('cassette', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='workstation_cassette', to='construct.cassette')),
            ],
        ),
        migrations.CreateModel(
            name='CassetteAssembly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side', models.CharField(default='1', max_length=50)),
                ('layer', models.CharField(default='1', max_length=50)),
                ('step', models.IntegerField(default=1)),
                ('barcode', models.IntegerField(blank=True, null=True)),
                ('placed', models.BooleanField(default=False)),
                ('cassette', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='construct.cassette')),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='construct.modulemap')),
            ],
        ),
        migrations.AddField(
            model_name='cassette',
            name='workstation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cassette_workstation', to='construct.workstation'),
        ),
    ]
