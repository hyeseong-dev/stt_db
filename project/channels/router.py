from fastapi import APIRouter

channel_router = APIRouter(
    prefix='/channels',
    tags=['Channels']
)


@channel_router.get('')
async def hello():
    return {'message': 'hello world'}