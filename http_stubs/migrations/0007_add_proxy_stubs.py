# Generated by Django 3.1.13 on 2021-10-18 22:53

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('http_stubs', '0006_httpstub_is_logging_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyHTTPStub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Enabled')),
                ('path', models.CharField(db_index=True, max_length=2000, verbose_name='Request path')),
                ('regex_path', models.BooleanField(default=False, help_text='Path is a regular expression', verbose_name='REGEX path')),
                ('method', models.CharField(choices=[('GET', 'Get'), ('POST', 'Post'), ('PUT', 'Put'), ('PATCH', 'Patch'), ('DELETE', 'Delete'), ('HEAD', 'Head'), ('OPTIONS', 'Options'), ('TRACE', 'Trace')], db_index=True, max_length=10, verbose_name='Request method')),
                ('request_script', models.TextField(blank=True, help_text='Language: python 3.8. The script will run on each request.', verbose_name='Request script')),
                ('enable_logging', models.BooleanField(default=False, help_text='Enables logging of requests', verbose_name='Logging')),
                ('target_url', models.URLField(verbose_name='Target url')),
                ('allow_forward_query', models.BooleanField(default=False, verbose_name='Forward query params')),
                ('target_ssl_verify', models.BooleanField(default=True, verbose_name='Target SSL verify')),
                ('target_timeout', models.IntegerField(default=15, help_text='In seconds', verbose_name='Target response timeout')),
                ('target_method', models.CharField(choices=[('GET', 'Get'), ('POST', 'Post'), ('PUT', 'Put'), ('PATCH', 'Patch'), ('DELETE', 'Delete'), ('HEAD', 'Head'), ('OPTIONS', 'Options'), ('TRACE', 'Trace')], max_length=10, verbose_name='Target request method')),
                ('target_headers', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict, help_text='In JSON format', verbose_name='Target headers')),
                ('target_body', models.TextField(blank=True, default='', verbose_name='Target body')),
            ],
            options={
                'verbose_name': 'proxy http stub',
                'verbose_name_plural': 'proxy stubs',
            },
        ),
        migrations.CreateModel(
            name='ProxyLogEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.URLField(max_length=2000, verbose_name='Full request path')),
                ('method', models.CharField(choices=[('GET', 'Get'), ('POST', 'Post'), ('PUT', 'Put'), ('PATCH', 'Patch'), ('DELETE', 'Delete'), ('HEAD', 'Head'), ('OPTIONS', 'Options'), ('TRACE', 'Trace')], max_length=10, verbose_name='Request method')),
                ('source_ip', models.GenericIPAddressField(verbose_name='Source IP')),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='Request timestamp')),
                ('request_headers', django.contrib.postgres.fields.hstore.HStoreField(verbose_name='Request headers')),
                ('request_body', models.TextField(verbose_name='Request body')),
                ('result_script', models.CharField(blank=True, max_length=200, verbose_name='Result script')),
                ('target_path', models.URLField(max_length=2000, verbose_name='Full target path')),
                ('response_latency', models.IntegerField(help_text='In milliseconds', verbose_name='Response latency')),
                ('response_body', models.TextField(help_text='From target', verbose_name='Response body')),
                ('response_headers', django.contrib.postgres.fields.hstore.HStoreField(help_text='From target', verbose_name='Response headers')),
            ],
            options={
                'verbose_name': 'proxy log',
                'verbose_name_plural': 'proxy logs',
            },
        ),
        migrations.AlterModelOptions(
            name='httpstub',
            options={'verbose_name': 'request http stub', 'verbose_name_plural': 'request stubs'},
        ),
        migrations.AlterModelOptions(
            name='logentry',
            options={'verbose_name': 'request log', 'verbose_name_plural': 'request logs'},
        ),
        migrations.RemoveConstraint(
            model_name='httpstub',
            name='uniq-path-method',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='body',
            new_name='request_body',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='date',
            new_name='request_date',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='headers',
            new_name='request_headers',
        ),
        migrations.AlterField(
            model_name='httpstub',
            name='method',
            field=models.CharField(choices=[('GET', 'Get'), ('POST', 'Post'), ('PUT', 'Put'), ('PATCH', 'Patch'), ('DELETE', 'Delete'), ('HEAD', 'Head'), ('OPTIONS', 'Options'), ('TRACE', 'Trace')], db_index=True, max_length=10, verbose_name='Request method'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='http_stub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='http_stubs.httpstub', verbose_name='Related stub'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='method',
            field=models.CharField(choices=[('GET', 'Get'), ('POST', 'Post'), ('PUT', 'Put'), ('PATCH', 'Patch'), ('DELETE', 'Delete'), ('HEAD', 'Head'), ('OPTIONS', 'Options'), ('TRACE', 'Trace')], max_length=10, verbose_name='Request method'),
        ),
        migrations.AddField(
            model_name='proxylogentity',
            name='http_stub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='http_stubs.proxyhttpstub', verbose_name='Related proxy stub'),
        ),
    ]
