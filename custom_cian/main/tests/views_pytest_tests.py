
def test_index_view_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_list_view(client, realty):
    response = client.get('/realty_list/')
    assert response.status_code == 200
    assert bytes(str(realty), encoding='utf-8') in response.content


def test_get_realty_detail(client, realty):
    response = client.get(f'/realty_list/{realty.slug}/')
    assert response.status_code == 200
    assert bytes(str(realty), encoding='utf-8') in response.content


def test_success_get_update_realty_page(client, logged_user, realty):
    client.force_login(logged_user)
    response = client.get(f'/realty_list/{realty.slug}/edit')
    assert response.status_code == 200


def test_redirect_logout(client, realty):
    response = client.get(f'/realty_list/{realty.slug}/edit')
    assert response.status_code == 302
    assert response.url.startswith("/accounts/login/")


def test_logged_in_with_permission_denied(client, user_without_perms, realty):
    client.force_login(user_without_perms)
    response = client.get(f'/realty_list/{realty.slug}/edit')
    assert response.status_code == 403

def test_create_realty(client, logged_user, category, tag):
    form_data = {
        "name": "test Realty",
        "price": 1000,
        "space": 20,
        "tags": tag.pk,
        "description": "test description",
        "category": category.pk,
        "saller": 1,
        "is_mortgage_available": "on",
        "counter": 0
    }
    client.force_login(logged_user)
    response = client.post('/realty/add/', form_data)
    assert response.status_code == 302
    assert response.url == "/realty_list/test-realty/"
