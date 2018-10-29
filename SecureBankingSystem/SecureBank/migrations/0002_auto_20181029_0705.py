# Generated by Django 2.0.2 on 2018-10-29 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SecureBank', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankuser',
            options={'permissions': (('is_External_User', 'Customer of bank'), ('is_Internal_User', 'Employee has permissions to access User data'), ('is_Manager', 'Manager has permission to access transactions'))},
        ),
        migrations.AddField(
            model_name='transaction',
            name='Type',
            field=models.CharField(choices=[('C', 'Credit'), ('D', 'Debit'), ('T', 'Transaction')], default='T', editable=False, max_length=1),
        ),
    ]
