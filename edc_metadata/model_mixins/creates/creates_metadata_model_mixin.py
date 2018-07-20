from django.db import models
from edc_metadata_rules import MetadataRuleEvaluator

from ...constants import KEYED, REQUISITION, CRF
from ...metadata import Metadata, Destroyer, DeleteMetadataError
from ...metadata import RequisitionMetadataGetter, CrfMetadataGetter


class CreatesMetadataModelMixin(models.Model):
    """A model mixin for visit models to enable them to
    create metadata on save.
    """

    metadata_cls = Metadata
    metadata_destroyer_cls = Destroyer
    metadata_rule_evaluator_cls = MetadataRuleEvaluator

    def metadata_create(self):
        """Creates metadata, called by post_save signal.
        """
        metadata = self.metadata_cls(visit=self, update_keyed=True)
        metadata.prepare()

    def run_metadata_rules(self):
        """Runs all the metadata rules.

        Initially called by post_save signal.

        Also called by post_save signal after metadata is updated.
        """
        metadata_rule_evaluator = self.metadata_rule_evaluator_cls(
            visit=self)
        metadata_rule_evaluator.evaluate_rules()

    @property
    def metadata_query_options(self):
        """Returns a dictionary of query options needed select
        the visit model instance
        """
        visit = self.visits.get(self.visit_code)
        options = dict(
            visit_schedule_name=self.visit_schedule_name,
            schedule_name=self.schedule_name,
            visit_code=visit.code,
            visit_code_sequence=self.visit_code_sequence)
        return options

    @property
    def metadata(self):
        """Returns a dictionary of metadata querysets for each
        metadata category (CRF or REQUISITION).
        """
        metadata = {}
        for name, getter_cls in [
                (CRF, CrfMetadataGetter), (REQUISITION, RequisitionMetadataGetter)]:
            getter = getter_cls(appointment=self.appointment)
            metadata[name] = getter.metadata_objects
        return metadata

    def metadata_delete_for_visit(self):
        """Deletes metadata for a visit when the visit is deleted.

        See signals.
        """
        for key in [CRF, REQUISITION]:
            if [obj for obj in self.metadata[key] if obj.entry_status == KEYED]:
                raise DeleteMetadataError(
                    f'Metadata cannot be deleted. {key}s have been keyed. Got {repr(self)}.')
        destroyer = self.metadata_destroyer_cls(visit=self)
        destroyer.delete()

    class Meta:
        abstract = True
