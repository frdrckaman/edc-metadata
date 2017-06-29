from collections import OrderedDict
from django.test import TestCase, tag

from edc_constants.constants import MALE

from ..constants import REQUIRED, NOT_REQUIRED
from ..rules import CrfRule, P, SiteMetadataRulesAlreadyRegistered
from ..rules import Logic, register, RegisterRuleGroupError, SiteMetadataRulesImportError
from ..rules import site_metadata_rules, RuleGroup, SiteMetadataNoRulesError


class RuleGroupWithoutRules(RuleGroup):
    class Meta:
        app_label = 'edc_metadata'
        source_model = 'edc_metadata.subjectvisit'


class RuleGroupWithRules(RuleGroup):
    rule1 = CrfRule(
        logic=Logic(
            predicate=P('gender', 'eq', MALE),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['crfone', 'crftwo'])

    class Meta:
        app_label = 'edc_metadata'
        source_model = 'edc_metadata.subjectvisit'


class RuleGroupWithRules2(RuleGroup):
    rule1 = CrfRule(
        logic=Logic(
            predicate=P('gender', 'eq', MALE),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED),
        target_models=['crfone', 'crftwo'])

    class Meta:
        app_label = 'edc_metadata'
        source_model = 'edc_metadata.subjectvisit'


class TestSiteMetadataRules(TestCase):

    def setUp(self):
        site_metadata_rules.registry = OrderedDict()

    def test_register_rule_group_no_rules_raises_on_register(self):
        self.assertRaises(
            SiteMetadataNoRulesError,
            site_metadata_rules.register, RuleGroupWithoutRules)

    def test_register_rule_group_with_rule(self):
        try:
            site_metadata_rules.register(RuleGroupWithRules)
        except SiteMetadataNoRulesError:
            self.fail('SiteMetadataNoRulesError unexpectedly raised.')

    def test_register_rule_group_get_rule_groups_for_app_label(self):
        site_metadata_rules.register(RuleGroupWithRules)
        rule_groups = site_metadata_rules.rule_groups.get('edc_metadata')
        self.assertEqual(rule_groups, [RuleGroupWithRules])

    def test_register_rule_group_register_more_than_one_rule_group(self):
        site_metadata_rules.register(RuleGroupWithRules)
        site_metadata_rules.register(RuleGroupWithRules2)
        rule_groups = site_metadata_rules.rule_groups.get('edc_metadata')
        self.assertEqual(
            rule_groups, [RuleGroupWithRules, RuleGroupWithRules2])

    def test_register_twice_raises(self):
        site_metadata_rules.register(rule_group_cls=RuleGroupWithRules)
        self.assertRaises(
            SiteMetadataRulesAlreadyRegistered,
            site_metadata_rules.register, RuleGroupWithRules)

    def test_rule_group_repr(self):
        repr(RuleGroupWithRules())
        str(RuleGroupWithRules())

    def test_register_decorator(self):

        @register()
        class RuleGroupWithRules(RuleGroup):
            rule1 = CrfRule(
                logic=Logic(
                    predicate=P('gender', 'eq', MALE),
                    consequence=REQUIRED,
                    alternative=NOT_REQUIRED),
                target_models=['crfone', 'crftwo'])

            class Meta:
                app_label = 'edc_metadata'
                source_model = 'edc_metadata.subjectvisit'

        self.assertIn('edc_metadata', site_metadata_rules.registry)

    def test_register_decorator_raises(self):

        try:
            @register()
            class RuleGroupWithRules:
                class Meta:
                    app_label = 'edc_metadata'
                    source_model = 'edc_metadata.subjectvisit'
        except RegisterRuleGroupError:
            pass
        else:
            self.fail('RegisterRuleGroupError unexpectedly not raised.')

    def test_autodiscover(self):
        self.assertRaises(
            SiteMetadataRulesImportError,
            site_metadata_rules.autodiscover, 'tests.metadata_rules')
