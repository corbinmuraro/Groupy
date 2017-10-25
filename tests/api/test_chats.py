import unittest
from unittest import mock

from groupy.api import chats


class ChatsTests(unittest.TestCase):
    def setUp(self):
        self.m_session = mock.Mock()
        self.chats = chats.Chats(self.m_session)


class ListChatsTests(ChatsTests):
    def setUp(self):
        super().setUp()
        m_chat = {'other_user': {'id': 42}}
        self.m_session.get.return_value = mock.Mock(data=[m_chat])
        self.results = self.chats.list()

    def test_results_is_chats(self):
        self.assertTrue(all(isinstance(c, chats.Chat) for c in self.results))


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.m_manager = mock.Mock()
        other_user = {'id': 42, 'name': 'foo'}
        self.chat = chats.Chat(self.m_manager, other_user=other_user)

    def test_repr(self):
        representation = repr(self.chat)
        self.assertEqual(representation, "<Chat(other_user='foo')>")

    def test_post_uses_create(self):
        self.chat.messages = mock.Mock()
        self.chat.post()
        self.assertTrue(self.chat.messages.create.called)
