from django.db import migrations, models


def backfill_closed_at(apps, schema_editor):
    Ticket = apps.get_model('metrics', 'Ticket')
    Ticket.objects.filter(status='closed', closed_at__isnull=True).update(closed_at=models.F('updated_at'))


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0002_alter_historicalticket_options_alter_ticket_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalticket',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de cierre'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de cierre'),
        ),
        migrations.RunPython(backfill_closed_at, migrations.RunPython.noop),
    ]
