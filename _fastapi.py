import databases
import orm
from fastapi import FastAPI

database = databases.Database('postgresql://postgres:123456@localhost/blocks', min_size=2, max_size=4)
models = orm.ModelRegistry(database=database)

class User(orm.Model):
    tablename = 'users'
    registry = models
    fields = {
        'id': orm.Integer(primary_key=True),
        'name': orm.String(max_length=255)
    }

async def lifespan(app: FastAPI):
    await database.connect()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def users():
    user = await User.objects.first()
    return user

