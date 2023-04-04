import unittest
import json
from pybo.database.models import Notice
from pybo import create_app


class PyboTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        """Excute after reach test"""
        pass

    # Notice tests
    """get_notices"""

    def test_get_notices(self):
        res = self.client.get("/notice/list?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["notices"]), 10)

    def test_get_notices_fail(self):
        res = self.client.get("/notice?page=-1")
        self.assertEqual(res.status_code, 404)

    """get_notice_detail"""

    def test_get_notice_detail(self):
        notice_id = 2
        res = self.client.get(f"/notice/detail/{notice_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["notice"])

    def test_get_notice_detail_fail(self):
        # Set a non-existing Notice ID
        non_existing_notice_id = 9999
        res = self.client.get(f"/notice/detail/{non_existing_notice_id}")
        self.assertEqual(res.status_code, 404)

    """test_create_notice """

    def test_create_notice(self):
        new_notice = {
            "author_name": "Test Author",
            "title": "Test Notice Title",
            "content": "This is a test notice content.",
        }
        res = self.client.post("/notice/create", json=new_notice)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["id"])

    def test_create_notice_fail(self):
        invalid_notice = {
            "author_name": "Test Author",
            "title": "",  # Empty title
            "content": "This is a test notice content.",
        }
        res = self.client.post("/notice/create", json=invalid_notice)
        self.assertEqual(res.status_code, 400)

    """modify_notice"""

    def test_modify_notice(self):
        notice_id = 2
        update_notice = {
            "author_name": "Updated Author",
            "title": "Updated Notice Title",
            "content": "This is an updated test notice content.",
        }
        res = self.client.post(f"/notice/modify/{notice_id}", json=update_notice)
        data = json.loads(res.data)
        notice = data["notice"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(notice["title"], "Updated Notice Title")

    def test_modify_notice_fail(self):
        non_existing_notice_id = 9999
        update_notice = {
            "author_name": "Updated Author",
            "title": "Updated Notice Title",
            "content": "This is an updated test notice content.",
        }
        res = self.client.post(
            f"/notice/modify/{non_existing_notice_id}", json=update_notice
        )
        self.assertEqual(res.status_code, 404)

    """ delete_notice """

    def test_delete_notice(self):
        new_notice = {
            "author_name": "Test Author",
            "title": "Test Notice Title",
            "content": "This is a test notice content.",
        }
        res = self.client.post("/notice/create", json=new_notice)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["id"])

        notice_id = data["id"]

        res = self.client.delete(f"/notice/delete/{notice_id}")
        self.assertEqual(res.status_code, 204)

    def test_delete_notice_fail(self):
        non_existing_notice_id = 9999
        res = self.client.delete(f"/notice/delete/{non_existing_notice_id}")
        self.assertEqual(res.status_code, 404)

    # Reply tests
    """get_replies"""

    def test_get_replies(self):
        notice_id = 2
        res = self.client.get(f"/reply/list/{notice_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["replies"])

    def test_get_replies_fail(self):
        non_existing_notice_id = 9999
        res = self.client.get(f"/reply/list/{non_existing_notice_id}")
        self.assertEqual(res.status_code, 404)

    """create_reply"""

    def test_create_reply(self):
        new_reply = {
            "author_name": "Test Reply Author",
            "content": "This is a test reply content.",
            "notice_id": 1,
        }
        res = self.client.post("/reply/create", json=new_reply)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["id"])

    def test_create_reply_fail(self):
        invalid_reply = {
            "author_name": "",  # Empty author_name
            "content": "This is a test reply content.",
            "notice_id": 1,
        }
        res = self.client.post("/reply/create", json=invalid_reply)
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
