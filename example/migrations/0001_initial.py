# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 08:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import django_crypto_fields.fields.encrypted_char_field
import django_crypto_fields.fields.encrypted_text_field
import django_crypto_fields.fields.firstname_field
import django_crypto_fields.fields.identity_field
import django_crypto_fields.fields.lastname_field
import django_crypto_fields.mixins
import django_extensions.db.fields
import django_revision.revision_field
import edc_base.model.fields.custom_fields
import edc_base.model.fields.hostname_modification_field
import edc_base.model.fields.userfield
import edc_base.model.fields.uuid_auto_field
import edc_base.model.validators.date
import edc_consent.models.validators
import edc_meta_data.crf_meta_data_mixin


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='ckgathi', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('close_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Date closed.')),
                ('time_point_status', models.CharField(choices=[('open', 'Open'), ('feedback', 'Feedback'), ('closed', 'Closed')], default='open', max_length=15)),
                ('subject_withdrew', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text='Use ONLY when subject has changed mind and wishes to withdraw consent', max_length=15, null=True, verbose_name='Did the participant withdraw consent?')),
                ('reasons_withdrawn', models.CharField(choices=[('changed_mind', 'Subject changed mind'), ('N/A', 'Not applicable')], default='N/A', max_length=35, null=True, verbose_name='Reason participant withdrew consent')),
                ('withdraw_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Date and time participant withdrew consent')),
                ('visit_schedule_name', models.CharField(max_length=25, null=True)),
                ('schedule_name', models.CharField(max_length=25, null=True)),
                ('visit_code', models.CharField(max_length=25, null=True)),
                ('appointment_identifier', models.CharField(blank=True, editable=False, max_length=50)),
                ('best_appt_datetime', models.DateTimeField(editable=False, null=True)),
                ('appt_close_datetime', models.DateTimeField(editable=False, null=True)),
                ('visit_code_sequence', models.IntegerField(blank=True, default=0, help_text='An integer to represent the sequence of additional appointments relative to the base appointment, 0, needed to complete data collection for the timepoint. (NNNN.0)', null=True, verbose_name='Sequence')),
                ('appt_datetime', models.DateTimeField(db_index=True, verbose_name='Appointment date and time')),
                ('timepoint_datetime', models.DateTimeField(editable=False, help_text='calculated appointment datetime. Do not change', null=True, verbose_name='Timepoint date and time')),
                ('appt_status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In Progress'), ('incomplete', 'Incomplete'), ('done', 'Done'), ('cancelled', 'Cancelled')], db_index=True, default='new', max_length=25, verbose_name='Status')),
                ('appt_reason', models.CharField(blank=True, help_text='Reason for appointment', max_length=25, verbose_name='Reason for appointment')),
                ('comment', models.CharField(blank=True, max_length=250, verbose_name='Comment')),
                ('is_confirmed', models.BooleanField(default=False, editable=False)),
                ('dashboard_type', models.CharField(blank=True, db_index=True, editable=False, help_text='hold dashboard_type variable, set by dashboard', max_length=25, null=True)),
                ('appt_type', models.CharField(choices=[('clinic', 'In clinic'), ('telephone', 'By telephone'), ('home', 'At home')], default='clinic', help_text='Default for subject may be edited Subject Configuration.', max_length=20, verbose_name='Appointment type')),
            ],
        ),
        migrations.CreateModel(
            name='CrfMetaData',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='ckgathi', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('current_entry_title', models.CharField(max_length=250, null=True)),
                ('entry_status', models.CharField(choices=[('NEW', 'New'), ('KEYED', 'Keyed'), ('MISSED', 'Missed'), ('NOT_REQUIRED', 'Not required')], db_index=True, default='NEW', max_length=25)),
                ('due_datetime', models.DateTimeField(blank=True, null=True)),
                ('report_datetime', models.DateTimeField(blank=True, null=True)),
                ('entry_comment', models.TextField(blank=True, max_length=250, null=True)),
                ('close_datetime', models.DateTimeField(blank=True, null=True)),
                ('fill_datetime', models.DateTimeField(blank=True, null=True)),
                ('schedule_name', models.CharField(max_length=25, null=True)),
                ('app_label', models.CharField(max_length=25, null=True)),
                ('model_name', models.CharField(max_length=25, null=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='example.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='CrfOne',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='ckgathi', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('report_datetime', models.DateTimeField(default=django.utils.timezone.now, help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.", validators=[edc_base.model.validators.date.datetime_not_before_study_start, edc_base.model.validators.date.datetime_not_future], verbose_name='Report Date')),
                ('f1', models.CharField(default='erik', max_length=10)),
            ],
            managers=[
                ('entry_meta_data_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredSubject',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='ckgathi', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('subject_identifier', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Subject Identifier as pk')),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('last_name', django_crypto_fields.fields.lastname_field.LastnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='Last name')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(help_text=' (Encryption: RSA local)', max_length=71, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('dob', models.DateField(help_text='Format is YYYY-MM-DD', null=True, verbose_name='Date of birth')),
                ('is_dob_estimated', edc_base.model.fields.custom_fields.IsDateEstimatedField(choices=[('-', 'No'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, null=True, verbose_name='Is date of birth estimated?')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True, verbose_name='Gender')),
                ('subject_type', models.CharField(default='subject', max_length=25)),
                ('subject_consent_id', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_identifier', models.CharField(blank=True, max_length=36, null=True)),
                ('sid', models.CharField(blank=True, max_length=15, null=True, verbose_name='SID')),
                ('study_site', models.CharField(blank=True, max_length=50, null=True)),
                ('relative_identifier', models.CharField(blank=True, help_text="For example, mother's identifier, if available / appropriate", max_length=25, null=True, verbose_name='Identifier of immediate relation')),
                ('identity', django_crypto_fields.fields.identity_field.IdentityField(blank=True, help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('identity_type', edc_base.model.fields.custom_fields.IdentityTypeField(blank=True, choices=[('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other')], max_length=15, null=True, verbose_name='What type of identity number is this?')),
                ('may_store_samples', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('?', 'Unknown')], default='?', help_text='Does the subject agree to have samples stored after the study has ended', max_length=3, verbose_name='Sample storage')),
                ('hiv_status', models.CharField(blank=True, choices=[('POS', 'Positive'), ('NEG', 'Negative'), ('unknown', 'Unknown')], max_length=15, null=True, verbose_name='Hiv status')),
                ('survival_status', models.CharField(blank=True, choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], max_length=15, null=True, verbose_name='Survival status')),
                ('screening_identifier', models.CharField(blank=True, max_length=36, null=True)),
                ('screening_datetime', models.DateTimeField(blank=True, null=True)),
                ('screening_age_in_years', models.IntegerField(blank=True, null=True)),
                ('registration_datetime', models.DateTimeField(blank=True, null=True)),
                ('randomization_datetime', models.DateTimeField(blank=True, null=True)),
                ('registration_status', models.CharField(blank=True, max_length=25, null=True, verbose_name='Registration status')),
                ('comment', models.TextField(blank=True, max_length=250, null=True, verbose_name='Comment')),
                ('additional_key', models.CharField(default=None, editable=False, help_text='A uuid (or some other text value) to be added to bypass the unique constraint of just firstname, initials, and dob.The default constraint proves limiting since the source model usually has some otherattribute in additional to first_name, initials and dob which is not captured in this model', max_length=36, null=True, verbose_name='-')),
                ('dm_comment', models.CharField(editable=False, max_length=150, null=True, verbose_name='Data Management comment')),
            ],
        ),
        migrations.CreateModel(
            name='RequisitionMetaData',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='ckgathi', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('current_entry_title', models.CharField(max_length=250, null=True)),
                ('entry_status', models.CharField(choices=[('NEW', 'New'), ('KEYED', 'Keyed'), ('MISSED', 'Missed'), ('NOT_REQUIRED', 'Not required')], db_index=True, default='NEW', max_length=25)),
                ('due_datetime', models.DateTimeField(blank=True, null=True)),
                ('report_datetime', models.DateTimeField(blank=True, null=True)),
                ('entry_comment', models.TextField(blank=True, max_length=250, null=True)),
                ('close_datetime', models.DateTimeField(blank=True, null=True)),
                ('fill_datetime', models.DateTimeField(blank=True, null=True)),
                ('schedule_name', models.CharField(max_length=25, null=True)),
                ('app_label', models.CharField(max_length=25, null=True)),
                ('model_name', models.CharField(max_length=25, null=True)),
                ('panel_name', models.CharField(max_length=50, null=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='example.Appointment')),
                ('registered_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.RegisteredSubject')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectConsent',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='ckgathi', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('citizen', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, verbose_name='Are you a Botswana citizen? ')),
                ('legal_marriage', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text="If 'NO' participant will not be enrolled.", max_length=3, null=True, verbose_name='If not a citizen, are you legally married to a Botswana Citizen?')),
                ('marriage_certificate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text="If 'NO' participant will not be enrolled.", max_length=3, null=True, verbose_name='[Interviewer] Has the participant produced the marriage certificate, as proof? ')),
                ('marriage_certificate_no', models.CharField(blank=True, help_text='e.g. 000/YYYY', max_length=9, null=True, verbose_name='What is the marriage certificate number?')),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('last_name', django_crypto_fields.fields.lastname_field.LastnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='Last name')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(help_text=' (Encryption: RSA local)', max_length=71, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('dob', models.DateField(help_text='Format is YYYY-MM-DD', null=True, verbose_name='Date of birth')),
                ('is_dob_estimated', edc_base.model.fields.custom_fields.IsDateEstimatedField(choices=[('-', 'No'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, null=True, verbose_name='Is date of birth estimated?')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Undetermined')], max_length=1, null=True, verbose_name='Gender')),
                ('guardian_name', django_crypto_fields.fields.lastname_field.LastnameField(blank=True, help_text="Required only if subject is a minor. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma then followe by a space. (Encryption: RSA local)", max_length=71, null=True, validators=[edc_consent.models.validators.FullNameValidator()], verbose_name="Guardian's Last and first name (minors only)")),
                ('subject_type', models.CharField(max_length=25)),
                ('consent_reviewed', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have reviewed the consent with the client')),
                ('study_questions', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have answered all questions the client had about the study')),
                ('assessment_score', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have asked the client questions about this study and they have demonstrated understanding')),
                ('consent_signature', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='The client has signed the consent form?')),
                ('consent_copy', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Declined', 'Yes, but subject declined copy')], help_text='If declined, return copy to the clinic with the consent', max_length=20, null=True, validators=[edc_consent.models.validators.eligible_if_yes_or_declined], verbose_name='I have provided the client with a copy of their signed informed consent')),
                ('is_incarcerated', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='-', help_text="( if 'Yes' STOP patient cannot be consented )", max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_no], verbose_name='Is the participant under involuntary incarceration?')),
                ('is_literate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default=None, help_text="( if 'No' provide witness's name on this form and signature on the paper document.)", max_length=3, verbose_name='Is the participant LITERATE?')),
                ('witness_name', django_crypto_fields.fields.lastname_field.LastnameField(blank=True, help_text="Required only if subject is illiterate. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma. (Encryption: RSA local)", max_length=71, null=True, validators=[edc_consent.models.validators.FullNameValidator()], verbose_name="Witness's Last and first name (illiterates only)")),
                ('language', models.CharField(choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-co', 'Colombian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese')], default='not specified', help_text='The language used for the edc_consent process will also be used during data collection.', max_length=25, verbose_name='Language of consent')),
                ('is_verified', models.BooleanField(default=False, editable=False)),
                ('is_verified_datetime', models.DateTimeField(editable=False, null=True)),
                ('verified_by', models.CharField(editable=False, max_length=25, null=True)),
                ('subject_identifier', models.CharField(blank=True, max_length=50, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.CharField(default=None, editable=False, max_length=50, verbose_name='Subject Identifier as pk')),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('consent_datetime', models.DateTimeField(validators=[edc_base.model.validators.date.datetime_not_before_study_start, edc_base.model.validators.date.datetime_not_future], verbose_name='Consent date and time')),
                ('version', models.CharField(default='?', editable=False, help_text="See 'Consent Type' for consent versions by period.", max_length=10, verbose_name='Consent version')),
                ('study_site', models.CharField(max_length=15, null=True)),
                ('sid', models.CharField(blank=True, help_text='Used for randomization against a prepared rando-list.', max_length=15, null=True, verbose_name='SID')),
                ('comment', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=250, null=True, verbose_name='Comment')),
                ('dm_comment', models.CharField(editable=False, help_text='see also edc.data manager.', max_length=150, null=True, verbose_name='Data Management comment')),
                ('identity', django_crypto_fields.fields.identity_field.IdentityField(help_text="Use Omang, Passport number, driver's license number or Omang receipt number (Encryption: RSA local)", max_length=71, verbose_name='Identity number (OMANG, etc)')),
                ('identity_type', edc_base.model.fields.custom_fields.IdentityTypeField(choices=[('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other')], max_length=15, verbose_name='What type of identity number is this?')),
                ('confirm_identity', django_crypto_fields.fields.identity_field.IdentityField(help_text='Retype the identity number from the identity card (Encryption: RSA local)', max_length=71, null=True)),
            ],
            bases=(django_crypto_fields.mixins.CryptoMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SubjectVisit',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='ckgathi', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('report_datetime', models.DateTimeField(help_text='Date and time of this report', validators=[edc_base.model.validators.date.datetime_not_before_study_start, edc_base.model.validators.date.datetime_not_future], verbose_name='Visit Date and Time')),
                ('reason', models.CharField(help_text='<Override the field class for this model field attribute in ModelForm>', max_length=25, verbose_name='What is the reason for this visit?')),
                ('study_status', models.CharField(help_text='<Override the field class for this model field attribute in ModelForm>', max_length=50, verbose_name="What is the participant's current study status")),
                ('require_crfs', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=10, verbose_name='Are scheduled data being submitted with this visit?')),
                ('reason_missed', models.CharField(blank=True, max_length=35, null=True, verbose_name="If 'missed' above, Reason scheduled visit was missed")),
                ('info_source', models.CharField(max_length=25, verbose_name='What is the main source of this information?')),
                ('info_source_other', edc_base.model.fields.custom_fields.OtherCharField(blank=True, editable=True, verbose_name='...if "Other", specify')),
                ('survival_status', models.CharField(choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], default='alive', max_length=10, null=True, verbose_name="Participant's survival status")),
                ('last_alive_date', models.DateField(blank=True, null=True, validators=[edc_base.model.validators.date.date_not_before_study_start, edc_base.model.validators.date.date_not_future], verbose_name='Date participant last known alive')),
                ('comments', models.TextField(blank=True, max_length=250, null=True, verbose_name='Comment if any additional pertinent information about the participant')),
                ('subject_identifier', models.CharField(editable=False, help_text='updated automatically as a convenience to avoid sql joins', max_length=50, verbose_name='subject_identifier')),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='example.Appointment')),
            ],
            bases=(edc_meta_data.crf_meta_data_mixin.CrfMetaDataMixin, models.Model),
        ),
        migrations.AddField(
            model_name='crfone',
            name='subject_visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.SubjectVisit'),
        ),
        migrations.AddField(
            model_name='crfmetadata',
            name='registered_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.RegisteredSubject'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='registered_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.RegisteredSubject'),
        ),
    ]
