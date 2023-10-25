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

class First:
    async def on_get(self, req, resp):
        user = await User.objects.first()

        resp.media = {
            'name': user.name
        }

class All:
    async def on_get(self, req, resp):
        users = await User.objects.limit(5).all()

        media = [{'name': i.name} for i in users]
        resp.media = media

app = falcon.asgi.App(middleware=[Connection()])

app.add_route('/', First())
app.add_route('/users', All())