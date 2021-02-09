class TestUser:

    def test_get_users_list(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/users' page is requested (GET)
        THEN check that the response is valid
        THEN check that the response is not empty
        """
        response = test_client.get(base_url + '/users')

        assert response.status_code == 200
        assert len(response.json) != 0

    def test_get_user(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/users/id' page is requested (GET)
        THEN check that the response is valid
        THEN check that the response is not empty
        """
        response = test_client.get(base_url + '/users/1')

        assert response.status_code == 200
        assert len(response.json) != 0

    def test_add_user(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        GIVEN user
        WHEN the '/users' page is requested (POST)
        WHEN got id of the added user
        WHEN the '/users/id' page is requested (GET)
        THEN check that the response is valid
        THEN check that the user is created
        """
        user = {
            "name": "John",
            "surname": "Wick"
        }

        response_post = test_client.post(base_url + '/users', json=user)
        added_user_id = response_post.json["id"]
        response_get = test_client.get(base_url + '/users/' + str(added_user_id))

        assert response_post.status_code == 200
        assert user["name"] == response_get.json["name"]
        assert user["surname"] == response_get.json["surname"]

    def test_edit_user(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        GIVEN user
        WHEN the '/users/1' page is requested (PUT)
        THEN check that the response is valid
        THEN check that the user is edited
        """
        user = {
            "name": "Tony",
            "surname": "Stark"
        }

        response_put = test_client.put(base_url + '/users/1', json=user)
        response_get = test_client.get(base_url + '/users/1')

        assert response_put.status_code == 200
        assert user["name"] == response_get.json["name"]
        assert user["surname"] == response_get.json["surname"]

    def test_delete_user(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/users/1' page is requested (DELETE)
        WHEN the '/users/1' page is requested (GET)
        THEN check that the response is valid
        THEN check that the user is deleted
        """
        response_delete = test_client.delete(base_url + '/users/1')
        response_get = test_client.get(base_url + '/users/1')

        assert response_delete.status_code == 200
        assert response_get.status_code == 404

    def test_add_user_validation(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        GIVEN user with integers in the fields
        GIVEN user without field "surname"
        GIVEN user without field "name"
        GIVEN user without fields at all
        WHEN the '/users' page is requested (POST) for each case
        THEN check that the response is not valid for each case
        """
        user_with_int_in_field = {
            "name": 1,
            "surname": 1
        }
        user_without_surname = {
            "name": "Jon"
        }
        user_without_name = {
            "surname": "Doe"
        }
        user_empty = {}

        response_user_with_int_in_field = test_client.post(base_url + '/users', json=user_with_int_in_field)
        response_user_without_name = test_client.post(base_url + '/users', json=user_without_name)
        response_user_without_surname = test_client.post(base_url + '/users', json=user_without_surname)
        response_user_empty = test_client.post(base_url + '/users', json=user_empty)

        assert response_user_with_int_in_field.status_code == 400
        assert response_user_without_name.status_code == 400
        assert response_user_without_surname.status_code == 400
        assert response_user_empty.status_code == 400

    def test_get_user_404(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/users/id' page is requested (GET)
        THEN check that the response is equals to 404
        """
        response = test_client.get(base_url + '/users/897233')

        assert response.status_code == 404

    def test_edit_user_404(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/users/id' page is requested (GET)
        THEN check that the response is equals to 404
        """
        response = test_client.put(base_url + '/users/897233')

        assert response.status_code == 404

    def test_delete_user_404(self, base_url, test_client, init_database):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/users/id' page is requested (GET)
        THEN check that the response is equals to 404
        """
        response = test_client.delete(base_url + '/users/897233')

        assert response.status_code == 404
