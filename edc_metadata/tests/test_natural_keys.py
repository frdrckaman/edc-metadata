from faker import Faker
from django.apps import apps as django_apps
from django.test import TestCase, tag

from edc_sync.models import OutgoingTransaction
from edc_sync.tests import SyncTestHelper
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..sync_models import sync_models
from .visit_schedule import visit_schedule
from .models import Enrollment, SubjectVisit
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject
from edc_visit_tracking.constants import SCHEDULED
from edc_constants.constants import MALE
from pprint import pprint

fake = Faker()


@tag('natural_keys')
class TestNaturalKey(TestCase):

    sync_helper = SyncTestHelper()

    exclude_models = [
        'edc_metadata.enrollment',
        'edc_metadata.disenrollment',
        'edc_metadata.subjectrequisition',
        'edc_metadata.subjectvisit',
        'edc_metadata.subjectoffstudy',
        'edc_metadata.crfone',
        'edc_metadata.crftwo',
        'edc_metadata.crfthree',
        'edc_metadata.crffour',
        'edc_metadata.crffive',
    ]

    def setUp(self):

        site_visit_schedules._registry = {}
        site_visit_schedules.loaded = False
        site_visit_schedules.register(visit_schedule)

        # note crfs in visit schedule are all set to REQUIRED by default.
        self.schedule = site_visit_schedules.get_schedule(
            visit_schedule_name='visit_schedule',
            schedule_name='schedule')

    def enroll(self, gender=None):
        subject_identifier = fake.credit_card_number()
        self.registered_subject = RegisteredSubject.objects.create(
            subject_identifier=subject_identifier, gender=gender)
        Enrollment.objects.create(subject_identifier=subject_identifier)
        self.appointment = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code=self.schedule.visits.first.code)
        subject_visit = SubjectVisit.objects.create(
            appointment=self.appointment, reason=SCHEDULED,
            subject_identifier=subject_identifier)
        return subject_visit

    def test_natural_key_attrs(self):
        self.sync_helper.sync_test_natural_key_attr(
            'edc_metadata', exclude_models=self.exclude_models)

    def test_get_by_natural_key_attr(self):
        self.sync_helper.sync_test_get_by_natural_key_attr(
            'edc_metadata', exclude_models=self.exclude_models)

    def test_sync_test_natural_keys(self):
        self.enroll(MALE)
        verbose = False
        model_objs = []
        completed_model_objs = {}
        completed_model_lower = []
        for outgoing_transaction in OutgoingTransaction.objects.all():
            if outgoing_transaction.tx_name in sync_models:
                model_cls = django_apps.get_app_config('edc_metadata').get_model(
                    outgoing_transaction.tx_name.split('.')[1])
                obj = model_cls.objects.get(pk=outgoing_transaction.tx_pk)
                if outgoing_transaction.tx_name in completed_model_lower:
                    continue
                model_objs.append(obj)
                completed_model_lower.append(outgoing_transaction.tx_name)
        completed_model_objs.update({'edc_metadata': model_objs})
        self.sync_helper.sync_test_natural_keys(
            completed_model_objs, verbose=verbose)
