from fastapi import Depends

from auth.util import get_current_active_user, get_current_user
from db.models import User


async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user.role


async def role_required(*group_names):
    async def in_role(current_user: User = Depends(get_current_user)):
        user = await get_me(current_user)
        return user
    return in_role



#@role_required('Manager', )
#def index2(request):
#    template = 'index2.html'
#    context = {}
#    return render(request, template, context)
