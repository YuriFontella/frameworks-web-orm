import falcon.asgi
import databases
import orm

database = databases.Database('postgresql://postgres:123456@localhost/blocks', min_size=2, max_size=4)
models = orm.ModelRegistry(database=database)

class User(orm.Model):
    tablename = 'users'
    registry = models
    fields = {
        'id': orm.Integer(primary_key=True),
        'name': orm.String(max_length=255)
    }


class Connection:
    async def process_startup(self, scope, event):
        await database.connect()

class Index:
    async def on_get(self, req, resp):
        user = await User.objects.first()

        resp.media = user.__dict__

app = falcon.asgi.App(middleware=[Connection()])

app.add_route('/', Index())