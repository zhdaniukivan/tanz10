import unittest
from flask_testing import TestCase
from app import app, db, FormData

class TestBase(TestCase):
    """
    Base class for setting up and tearing down the test environment.
    """
    def create_app(self):
        """
        Create the Flask application with testing configuration.

        Returns:
            Flask: The Flask application instance.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tanz10:tanz10@localhost:5432/testdatabase'
        return app

    def setUp(self):
        """
        Set up the test environment by creating all database tables.
        """
        db.create_all()

    def tearDown(self):
        """
        Tear down the test environment by removing the database session and dropping all tables.
        """
        db.session.remove()
        db.drop_all()

class TestForm(TestBase):
    """
    Test case for the form functionality.
    """
    def test_index_page(self):
        """
        Test that the index page loads correctly.

        Asserts:
            - The response status code is 200.
            - The response contains the expected text.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dynamic Input Form', response.data)

    def test_add_form_data(self):
        """
        Test that form data is added correctly.

        Asserts:
            - The response status code is 302 (redirect).
            - The form data is saved in the database with the correct values.
        """
        response = self.client.post('/', data={'input1': 'value1', 'input2': 'value2'})
        self.assertEqual(response.status_code, 302)  # Redirect to /data

        form_data = FormData.query.first()
        self.assertIsNotNone(form_data)
        print(f"Saved form data: {form_data.data}")  # Отладочное сообщение
        self.assertIn('input1', form_data.data)
        self.assertIn('input2', form_data.data)
        self.assertEqual(form_data.data['input1'], 'value1')
        self.assertEqual(form_data.data['input2'], 'value2')

    def test_display_data(self):
        """
        Test that the submitted form data is displayed correctly.

        Asserts:
            - The response status code is 200.
            - The response contains the expected data.
        """
        form_data = FormData(data={'input1': 'value1', 'input2': 'value2'})
        db.session.add(form_data)
        db.session.commit()

        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value1', response.data)
        self.assertIn(b'value2', response.data)

if __name__ == '__main__':
    unittest.main()
