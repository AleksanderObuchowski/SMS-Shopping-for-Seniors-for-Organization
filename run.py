from zakupy_dla_seniora import create_app, db, bcrypt
from zakupy_dla_seniora.config import artifai_admin_username, artifai_user_username, artifai_volunteer_email,\
    artifai_admin_password

from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.volunteers.models import Volunteers
from zakupy_dla_seniora.users.models import User

app = create_app()
port = 80
debug = True


@app.before_first_request
def manage_db():
    db.create_all()
    org = Organisations.query.filter_by(name='Artifai').first()
    if not org:
        org = Organisations(
            name='Artifai', contact_phone='+48666666666', contact_email='contact@artifai.pl',
            town='Gdansk', address='Narutowicza 11/12', website='www.artifai.pl'
        )
        org.save()
    if not User.get_by_username(artifai_admin_username):
        user = User(
            username=artifai_admin_username, email='admin@artifai.pl', organisation_id=org.id,
            password_hash=bcrypt.generate_password_hash(artifai_admin_password).decode('utf-8'),
            first_name='Artifai', last_name='Admin', phone='+48666666666',
            position='Users Manager', town='Gdansk',
            is_superuser=True
        )
        user.save()
    if not User.get_by_username(artifai_user_username):
        user = User(
            username=artifai_user_username, email='user@artifai.pl', organisation_id=org.id,
            password_hash=bcrypt.generate_password_hash(artifai_admin_password).decode('utf-8'),
            first_name='Artifai', last_name='User',
            phone='+48987654321', position='Volunteers Manager', town='Gdansk'
        )
        user.save()
    else:
        user = User.query.filter_by(username=artifai_user_username).first()
    if not Volunteers.query.filter_by(first_name='Artifai').first():
        volunteer = Volunteers(
            first_name='Artifai', last_name='Volunteer', phone='+48123456789',
            email=artifai_volunteer_email, org_id=org.id, town='Gdansk', distr='Wrzeszcz',
            pass_hash=bcrypt.generate_password_hash(artifai_admin_password).decode('utf-8'),
            created_by=user.id
        )
        volunteer.save()


if __name__ == '__main__':
    app.run(debug=debug)
