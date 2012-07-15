from django.test import TestCase
from ..testhelper import TestHelper
from ..models.devilryuserprofile import user_is_admin
from ..models.devilryuserprofile import user_is_admin_or_superadmin

class TestUserIsAdmin(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes="uni:admin(uniadmin)",
                            subjects=["sub:admin(subadmin)"],
                            periods=["p1:admin(p1admin)"],
                            assignments=["a1:admin(a1admin)"])
        self.testhelper.create_superuser('grandma')
        self.testhelper.create_user('notadmin')

    def test_user_is_admin(self):
        self.assertTrue(user_is_admin(self.testhelper.uniadmin))
        self.assertTrue(user_is_admin(self.testhelper.subadmin))
        self.assertTrue(user_is_admin(self.testhelper.p1admin))
        self.assertTrue(user_is_admin(self.testhelper.a1admin))
        self.assertFalse(user_is_admin(self.testhelper.notadmin))
        self.assertFalse(user_is_admin(self.testhelper.grandma))

    def test_user_is_admin_or_superadmin(self):
        self.assertTrue(user_is_admin_or_superadmin(self.testhelper.uniadmin))
        self.assertTrue(user_is_admin_or_superadmin(self.testhelper.subadmin))
        self.assertTrue(user_is_admin_or_superadmin(self.testhelper.p1admin))
        self.assertTrue(user_is_admin_or_superadmin(self.testhelper.a1admin))
        self.assertFalse(user_is_admin_or_superadmin(self.testhelper.notadmin))
        self.assertTrue(user_is_admin_or_superadmin(self.testhelper.grandma))
