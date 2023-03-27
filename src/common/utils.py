from starlette.templating import Jinja2Templates


def templates():
    """
    Jinja2Templates templates 객체 리턴
    :return: Jinja2Templates
    """
    return Jinja2Templates(directory="templates")
