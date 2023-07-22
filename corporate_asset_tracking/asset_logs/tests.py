from django.test import TestCase
from .models import Company, Employee, Device, DeviceLog, UserProfile
from django.contrib.auth.models import User

# Create your tests here.
class CompanyModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')

    def test_company_name(self):
        self.assertEqual(str(self.company), 'Test Company')

class EmployeeModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.employee = Employee.objects.create(name='John Doe', company=self.company)

    def test_employee_name(self):
        self.assertEqual(str(self.employee), 'John Doe')

    def test_employee_company_relationship(self):
        self.assertEqual(self.employee.company, self.company)

class DeviceModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.device = Device.objects.create(company=self.company, device_type='Phone', device_model='iPhone X')

    def test_device_type(self):
        self.assertEqual(self.device.device_type, 'Phone')

    def test_device_model(self):
        self.assertEqual(self.device.device_model, 'iPhone X')

    def test_device_company_relationship(self):
        self.assertEqual(self.device.company, self.company)

class DeviceLogModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.employee = Employee.objects.create(name='John Doe', company=self.company)
        self.device = Device.objects.create(company=self.company, device_type='Phone', device_model='iPhone X')
        self.device_log = DeviceLog.objects.create(employee=self.employee, device=self.device,
                                                   checked_out_date='2023-07-22 12:00:00',
                                                   condition_when_checked_out='good')

    def test_device_log_checked_out_date(self):
        self.assertEqual(str(self.device_log.checked_out_date), '2023-07-22 12:00:00')

    def test_device_log_condition_when_checked_out(self):
        self.assertEqual(self.device_log.condition_when_checked_out, 'good')

    def test_device_log_employee_relationship(self):
        self.assertEqual(self.device_log.employee, self.employee)

    def test_device_log_device_relationship(self):
        self.assertEqual(self.device_log.device, self.device)

    def test_device_log_checked_in_date(self):
        self.assertIsNone(self.device_log.checked_in_date)

    def test_device_log_condition_when_checked_in(self):
        self.assertEqual(self.device_log.condition_when_checked_in, '')

class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, company=self.company)

    def test_user_profile_user_relationship(self):
        self.assertEqual(self.user_profile.user, self.user)

    def test_user_profile_company_relationship(self):
        self.assertEqual(self.user_profile.company, self.company)
