import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('logout', follow_redirects=True)

    def test_login_out(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        assert 'class=add-entry' not in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_message(self):
        self.login('admin','default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

    '''
    def test_number_increases(self):
        cur = g.db.execute('select id, count from entries order by id desc')
        old_entries = {row[0]:row[1] for row in cur.fetchall()}
        #Visit
        rv = self.app.get("/")
        cur = g.db.execute('select id, count from entries order by id desc')
        new_entries = {row[0]:row[1] for row in cur.fetchall()}
        for entry_id in new_entries.keys():
            assert new_entries[entry_id] == (old_entries[entry_id] + 1)
    '''
        

    
    


if __name__ == '__main__':
    unittest.main()

