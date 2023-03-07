from pytest import raises, fixture


@fixture
def post_to_delete(api):
    payload_data = dict(title='Best ski resorts in Colorado', content='Check out these awesome ski resorts!',
                        category='travel', published=False, rating=4.5)
    new_post = api.post.create(payload=payload_data)
    return new_post


@fixture
def post_to_update(api):
    payload_data = dict(title='Best camping in Canada', content='Check out these awesome camping!',
                        category='travel', published=False, rating=2.8)
    new_post = api.post.create(payload=payload_data)
    yield new_post
    api.post.delete(uid=new_post['id'])


class TestPosts:

    def test_get_posts_listing(self, api):
        expected_posts_lst = [
            dict(id=0, title='Best beaches in Florida', content='Check out these awesome beaches!',
                 category='travel', published=False, rating=4.5),
            dict(id=1, title='Best restaurants in Florida', content='Check out these awesome restaurants!',
                 category='food', published=True, rating=3.0)
        ]

        posts = api.posts.retrieve()

        assert expected_posts_lst[0] in posts['data']
        assert expected_posts_lst[1] in posts['data']

    def test_get_single_post(self, api):
        expected_post = dict(id=0, title='Best beaches in Florida', content='Check out these awesome beaches!',
                             category='travel', published=False, rating=4.5)

        retrieved_posts = api.post.retrieve(uid=0)

        assert retrieved_posts == expected_post

    def test_get_non_existing_post(self, api):
        post_id = 99999999
        with raises(Exception) as resp:
            api.post.retrieve(uid=post_id)

        assert resp.value.http_code == 404
        assert resp.value.reason == 'Not Found'
        assert resp.value.message == f'{{"detail":"The post with id {post_id} was not found!"}}'

    def test_create_new_post(self, api):
        payload_data = dict(title='Best sunsets in California', content='Check out these awesome sunsets!',
                            category='travel', published=True, rating=5.0)
        new_post = api.post.create(payload=payload_data)
        expected_data = dict(id=new_post['id'], **payload_data)

        assert new_post == expected_data

    def test_create_new_post_with_invalid_category(self, api):
        payload_data = dict(title='Best hospitals in California', content='Check out these hospitals!',
                            category='health', published=True, rating=0.0)
        expected_err_location = '"loc":["body","category"]'
        expected_err_message = "value is not a valid enumeration member; permitted: 'travel', 'food', 'other'"
        with raises(Exception) as resp:
            api.post.create(payload=payload_data)

        assert resp.value.http_code == 422
        assert resp.value.reason == 'Unprocessable Entity'
        assert expected_err_location and expected_err_message in resp.value.message

    def test_update_post(self, api, post_to_update):
        post_to_update.update(dict(published=True, rating=4.7))
        updated_post = api.post.update(uid=post_to_update['id'], payload=post_to_update)

        assert updated_post == post_to_update

    def test_update_non_existing_post(self, api):
        payload_data = dict(id=1, title='Most rated restaurants in Florida',
                            content='"Florida`s Fresh Grill", "The Ravenous Pig", "Highball & Harvest"',
                            category='food', published=False, rating=4.0)
        post_id = 99999999
        with raises(Exception) as resp:
            api.post.update(uid=post_id, payload=payload_data)

        assert resp.value.http_code == 404
        assert resp.value.reason == 'Not Found'
        assert resp.value.message == f'{{"detail":"The post with id {post_id} was not found!"}}'

    def test_delete_post(self, api, post_to_delete):
        delete_resp = api.post.delete(uid=post_to_delete['id'])

        assert delete_resp.status_code == 204
        assert delete_resp.reason == 'No Content'
