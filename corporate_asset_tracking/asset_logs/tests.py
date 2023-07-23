from django.test import TestCase
from .models import Company, Employee, Device, DeviceLog, UserProfile
from django.contrib.auth.models import User
from django.urls import reverse

#Test cases for models
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

#Test cases for views 

class DeviceLogListViewTestCase(TestCase):
    def setUp(self):
        # Create a test user, company, and associated DeviceLog
        self.company = Company.objects.create(name='Test Company')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.employee = Employee.objects.create(name='John Doe', company=self.company)
        self.userprofile = UserProfile.objects.create(user=self.user, company=self.company)
        self.device_log = DeviceLog.objects.create(
            employee=self.employee,
            device=Device.objects.create(company=self.company, device_type='Laptop', device_model='DELL 15'),
            checked_out_date='2023-07-22 12:00:00',
            condition_when_checked_out='good',
            condition_when_checked_in='good',
        )
        self.url = reverse('device-log-list')  

    def test_logged_in_user_can_access_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_logged_out_user_cannot_access_view(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect for a logged-out user

    def test_device_logs_are_filtered_by_user_company(self):
        # Create another company and a DeviceLog associated with it
        other_company = Company.objects.create(name='Other Company')
        other_employee = Employee.objects.create(name='Jane Doe', company=other_company)
        DeviceLog.objects.create(
            employee=other_employee,
            device=Device.objects.create(company=other_company, device_type='Phone', device_model='Galaxy S21'),
            checked_out_date='2023-07-23 12:00:00',
            condition_when_checked_out='good',
            condition_when_checked_in='good',
        )

        # Loging in as the test user and access the view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)

        # Ensureing that only the DeviceLog associated with the user's company is displayed
        self.assertEqual(len(response.context['logs']), 1)
        self.assertEqual(response.context['logs'][0], self.device_log)