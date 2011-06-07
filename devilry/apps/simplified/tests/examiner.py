from django.test import TestCase
from django.contrib.auth.models import User

from ...core import models
from ..examiner import Subject, Period, Assignment, Group
from ..exceptions import PermissionDenied


class ExaminerTestCase(TestCase):
    fixtures = ["simplified/data.json"]

    def setUp(self):
        self.duck1100_core = models.Subject.objects.get(short_name='duck1100')
        self.duck1080_core = models.Subject.objects.get(short_name='duck1080')

        self.duck1100examiner = User(username='duck1100examiner')
        self.duck1100examiner.save()
        self.duck1100_core.periods.all()[0].assignments.all()[0].assignmentgroups.all()[0].examiners.add(self.duck1100examiner)

        self.duck1080examiner = User(username='duck1080examiner')
        self.duck1080examiner.save()
        self.duck1080_core.periods.all()[0].assignments.all()[0].assignmentgroups.all()[0].examiners.add(self.duck1080examiner)

        self.testexaminerNoPerm = User(username='testuserNoPerm')
        self.testexaminerNoPerm.save()
        self.superadmin = User.objects.get(username='grandma')


class TestExaminerSubject(ExaminerTestCase):

    def test_search(self):
        examiner0 = User.objects.get(username="examiner0")
        subjects = models.Subject.published_where_is_examiner(examiner0).order_by("short_name")
        qryset = Subject.search(examiner0).qryset
        self.assertEquals(len(qryset), len(subjects))
        self.assertEquals(qryset[0].short_name, subjects[0].short_name)

        # query
        qryset = Subject.search(examiner0, query="duck1").qryset
        self.assertEquals(len(qryset), 2)
        qryset = Subject.search(examiner0, query="duck").qryset
        self.assertEquals(len(qryset), len(subjects))
        qryset = Subject.search(examiner0, query="1100").qryset
        self.assertEquals(len(qryset), 1)

    def test_read(self):
        duck1100 = Subject.read(self.duck1100examiner, self.duck1100_core.id)
        self.assertEquals(duck1100, dict(
                short_name = 'duck1100',
                long_name = self.duck1100_core.long_name,
                id = self.duck1100_core.id))

    def test_read_security(self):
        with self.assertRaises(PermissionDenied):
            duck1100 = Subject.read(self.testexaminerNoPerm, self.duck1100_core.id)
        with self.assertRaises(PermissionDenied):
            duck1100 = Subject.read(self.duck1080examiner, self.duck1100_core.id)
        with self.assertRaises(PermissionDenied):
            duck1100 = Subject.read(self.superadmin, self.duck1100_core.id)


class TestExaminerPeriod(ExaminerTestCase):
    def setUp(self):
        super(TestExaminerPeriod, self).setUp()
        self.duck1100_h01_core = self.duck1100_core.periods.get(short_name='h01')

    def test_search(self):
        examiner0 = User.objects.get(username="examiner0")
        periods = models.Period.published_where_is_examiner(examiner0).order_by("short_name")
        qryset = Period.search(examiner0).qryset
        self.assertEquals(len(qryset), len(periods))
        self.assertEquals(qryset[0].short_name, periods[0].short_name)

        # query
        qryset = Period.search(examiner0, query="h01").qryset
        self.assertEquals(len(qryset), 3)
        qryset = Period.search(examiner0, query="duck1").qryset
        self.assertEquals(len(qryset), 2)

    def test_read(self):
        duck1100_h01 = Period.read(self.duck1100examiner, self.duck1100_h01_core.id)
        self.assertEquals(duck1100_h01, dict(
                id = self.duck1100_h01_core.id,
                short_name = 'h01',
                long_name = self.duck1100_h01_core.long_name,
                parentnode__id = self.duck1100_h01_core.parentnode_id))

        duck1100_h01 = Period.read(self.duck1100examiner,
                self.duck1100_h01_core.id,
                result_fieldgroups=['subject'])
        self.assertEquals(duck1100_h01, dict(
                id = self.duck1100_h01_core.id,
                short_name = 'h01',
                long_name = self.duck1100_h01_core.long_name,
                parentnode__id = self.duck1100_h01_core.parentnode_id,
                parentnode__short_name = self.duck1100_h01_core.parentnode.short_name,
                parentnode__long_name = self.duck1100_h01_core.parentnode.long_name))

    def test_read_security(self):
        with self.assertRaises(PermissionDenied):
            duck1100_h01 = Period.read(self.testexaminerNoPerm, self.duck1100_h01_core.id)
        with self.assertRaises(PermissionDenied):
            duck1100_h01 = Period.read(self.duck1080examiner, self.duck1100_h01_core.id)
        with self.assertRaises(PermissionDenied):
            duck1100_h01 = Period.read(self.superadmin, self.duck1100_h01_core.id)


class TestExaminerAssignment(ExaminerTestCase):
    def setUp(self):
        super(TestExaminerAssignment, self).setUp()
        self.duck1100_h01_week1_core = self.duck1100_core.periods.get(
                short_name='h01').assignments.get(short_name='week1')

    def test_search(self):
        examiner0 = User.objects.get(username="examiner0")
        all_assignments = models.Assignment.objects.all().order_by("short_name")
        qryset = Assignment.search(examiner0).qryset
        self.assertEquals(len(qryset), len(all_assignments))
        self.assertEquals(qryset[0].short_name, all_assignments[0].short_name)

        # query
        qryset = Assignment.search(examiner0, query="ek").qryset
        self.assertEquals(len(qryset), 9)
        qryset = Assignment.search(examiner0, query="h0").qryset
        self.assertEquals(len(qryset), len(all_assignments))
        qryset = Assignment.search(examiner0, query="1100").qryset
        self.assertEquals(len(qryset), 4)

    def test_read(self):
        duck1100_h01_week1 = Assignment.read(self.duck1100examiner,
                self.duck1100_h01_week1_core.id)
        self.assertEquals(duck1100_h01_week1, dict(
                id = self.duck1100_h01_week1_core.id,
                short_name = 'week1',
                long_name = self.duck1100_h01_week1_core.long_name,
                parentnode__id=self.duck1100_h01_week1_core.parentnode.id))

        duck1100_h01_week1 = Assignment.read(self.duck1100examiner,
                self.duck1100_h01_week1_core.id,
                result_fieldgroups=['period'])
        self.assertEquals(duck1100_h01_week1, dict(
                id = self.duck1100_h01_week1_core.id,
                short_name = 'week1',
                long_name = self.duck1100_h01_week1_core.long_name,
                parentnode__id=self.duck1100_h01_week1_core.parentnode.id,
                parentnode__short_name=self.duck1100_h01_week1_core.parentnode.short_name,
                parentnode__long_name=self.duck1100_h01_week1_core.parentnode.long_name,
                parentnode__parentnode__id=self.duck1100_h01_week1_core.parentnode.parentnode_id))

        duck1100_h01_week1 = Assignment.read(self.duck1100examiner,
                self.duck1100_h01_week1_core.id,
                result_fieldgroups=['period', 'subject'])
        self.assertEquals(duck1100_h01_week1, dict(
                id = self.duck1100_h01_week1_core.id,
                short_name = 'week1',
                long_name = self.duck1100_h01_week1_core.long_name,
                parentnode__id=self.duck1100_h01_week1_core.parentnode.id,
                parentnode__short_name=self.duck1100_h01_week1_core.parentnode.short_name,
                parentnode__long_name=self.duck1100_h01_week1_core.parentnode.long_name,
                parentnode__parentnode__id=self.duck1100_h01_week1_core.parentnode.parentnode_id,
                parentnode__parentnode__short_name=self.duck1100_h01_week1_core.parentnode.parentnode.short_name,
                parentnode__parentnode__long_name=self.duck1100_h01_week1_core.parentnode.parentnode.long_name))

    def test_read_security(self):
        with self.assertRaises(PermissionDenied):
            duck1100_h01_week1 = Period.read(self.testexaminerNoPerm, self.duck1100_h01_week1_core.id)
        with self.assertRaises(PermissionDenied):
            duck1100_h01_week1 = Period.read(self.duck1080examiner, self.duck1100_h01_week1_core.id)
        with self.assertRaises(PermissionDenied):
            duck1100_h01_week1 = Period.read(self.superadmin, self.duck1100_h01_week1_core.id)



class TestExaminerGroup(ExaminerTestCase):

    def setUp(self):
        super(TestExaminerGroup, self).setUp()
        duck1100_h01_week1_core = self.duck1100_core.periods.get(
                short_name='h01').assignments.get(short_name='week1')
        self.group_core = duck1100_h01_week1_core.assignmentgroups.all()[0]

    def test_search(self):
        examiner0 = User.objects.get(username="examiner0")
        assignment = models.Assignment.published_where_is_examiner(examiner0)[0]

        qryset = Group.search(examiner0, assignment=assignment.id,
                orderby=["-id"], limit=2).qryset
        self.assertEquals(assignment.id, qryset[0].parentnode.id)
        self.assertTrue(qryset[0].id > qryset[1].id)
        self.assertEquals(qryset.count(), 2)

        qryset = Group.search(examiner0, assignment=assignment.id,
                query="student0").qryset
        self.assertEquals(qryset.count(), 1)
        qryset = Group.search(examiner0, assignment=assignment.id,
                query="thisisatest").qryset
        self.assertEquals(qryset.count(), 0)

        g = Group.search(examiner0, assignment=assignment).qryset[0]
        g.name = "thisisatest"
        g.save()
        qryset = Group.search(examiner0, assignment=assignment.id,
                query="thisisatest").qryset
        self.assertEquals(qryset.count(), 1)

    def test_read(self):
        group = Group.read(self.duck1100examiner, self.group_core.id)
        self.assertEquals(group, dict(
                id = self.group_core.id,
                name = None))

    def test_read_security(self):
        with self.assertRaises(PermissionDenied):
            group = Group.read(self.testexaminerNoPerm, self.group_core.id)
        with self.assertRaises(PermissionDenied):
            group = Group.read(self.duck1080examiner, self.group_core.id)
        with self.assertRaises(PermissionDenied):
            group = Group.read(self.superadmin, self.group_core.id)
