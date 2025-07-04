import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_get_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    course_name = courses[0].name

    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == course_id
    assert data['name'] == course_name


@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=50)
    course_id = courses[25].id
    course_name = courses[25].name

    # Act
    response = client.get(f"/api/v1/courses/{course_id}/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == course_id
    assert data['name'] == course_name


@pytest.mark.django_db
def test_filter_course_by_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=50)
    course_name = courses[25].name

    # Act
    response = client.get(f'/api/v1/courses/?name={course_name}/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item['name'] == course_name


@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    data_json = {'name': 'Новый курс', }

    # Act
    response = client.post(f'/api/v1/courses/', data=data_json)
    course_id = response.json()['id']

    # Assert
    assert response.status_code == 201
    response = client.get(f"/api/v1/courses/{course_id}/")
    data = response.json()
    assert data['name'] == data_json['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    data_json = {'name': 'Измененный курс', }

    # Act
    response = client.patch(f'/api/v1/courses/{course_id}/', data=data_json)

    # Assert
    assert response.status_code == 200
    response = client.get(f"/api/v1/courses/{course_id}/")
    data = response.json()
    assert data['name'] == data_json['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    course_id = courses[0].id

    # Act
    response = client.delete(f'/api/v1/courses/{course_id}/')

    # Assert
    assert response.status_code == 204
    response = client.get(f"/api/v1/courses/{course_id}/")
    assert response.status_code == 404
