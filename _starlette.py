from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import databases
import orm
import contextlib

database = databases.Database('postgresql://postgres:123456@localhost/blocks', min_size=2, max_size=4)
models = orm.ModelRegistry(database=database)

class User(orm.Model):
    tablename = 'users'
    registry = models
    fields = {
        'id': orm.Integer(primary_key=True),
        'name': orm.String(max_length=255)
    }

@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield

async def homepage(request):
    user = await User.objects.limit(5).all()
    print(user)

    return JSONResponse({'hello': 'world'})

app = Starlette(debug=True, lifespan=lifespan, routes=[
    Route('/', homepage),
])