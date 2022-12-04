from fastapi import Depends
from auth.util import get_current_active_user
from db.models import User


def role_required(*group_names):
    def in_role(current_user: User = Depends(get_current_active_user)):
        for i in group_names:
            if current_user.role == i:
                return True
        return False
    return in_role


@role_required('Manager', )
def index2(request):
    template = 'index2.html'
    context = {}
    return render(request, template, context)
