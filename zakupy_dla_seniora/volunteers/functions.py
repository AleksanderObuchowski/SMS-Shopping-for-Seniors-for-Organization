from zakupy_dla_seniora.organisations.models import Organisations


def get_all_organisations():
    return Organisations.query.all()
