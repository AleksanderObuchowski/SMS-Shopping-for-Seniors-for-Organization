from zakupy_dla_seniora import create_app, db, bcrypt
from zakupy_dla_seniora.config import artifai_admin_username, artifai_admin_password
from zakupy_dla_seniora.organisations.models import Organisations
from zakupy_dla_seniora.users.models import User

app = create_app()
port = 80
debug = True


@app.before_first_request
def manage_db():
    db.create_all()
    org = Organisations.query.filter_by(name='Artifai').first()
    if not org:
        org = Organisations(name='Artifai')
        org.save()
    if not User.query.filter_by(username=artifai_admin_username).first():
        user = User(username=artifai_admin_username, email='admin@example.pl', organisation_id=org.id,
                    password_hash=bcrypt.generate_password_hash(artifai_admin_password).decode('utf-8'),
                    is_superuser=True)
        user.save()


if __name__ == '__main__':
    app.run(debug=debug)
