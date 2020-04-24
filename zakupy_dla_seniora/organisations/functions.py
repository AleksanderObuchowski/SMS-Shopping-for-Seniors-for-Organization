from zakupy_dla_seniora.organisations.models import Organisations


def get_organisation_name(user):
    # TODO It's temporary solution, find better way to get organisation name based on user id
    try:
        org = Organisations.query.filter_by(id=user.organisation_id).first()
        return org.name
    except Exception:
        return None
