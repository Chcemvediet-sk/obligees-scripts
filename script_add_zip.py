import cities
import database
from model import Obligee, ZipCodes
from zip_code import zip_equals, get_official_zip

if __name__ == "__main__":
    session = database.session
    updates = 0

    def get_obligee(name):
        return session.query(Obligee).filter(Obligee.name.ilike(name))

    for city in cities.cities():
        has_output = False
        if not city:
            continue

        obligees = get_obligee(city.name)
        count = obligees.count()
        if count == 0:
            # TODO: non existing obligees -- check script 'skript_nove_obce.py'
            continue
        if count == 1:
            obligee = obligees[0]
            official_post_obligee_zip = get_official_zip(
                "{}, {}".format(
                    obligee.street.decode('utf-8'),
                    obligee.city.decode('utf-8')
                )
            )
            official_post_json_zip = get_official_zip(
                "%s %s %s" % (
                    city.adresa_uradu_ulica,
                    city.adresa_uradu_cislo_domu,
                    city.adresa_uradu_mesto,
                )
            )
            zip_code = ZipCodes(
                obligee=obligee,
                json_zip=city.adresa_uradu_psc.replace(" ", ""),
                post_json_zip=official_post_json_zip,
                post_obligee_zip=official_post_obligee_zip,
            )

            session.add(zip_code)
            session.commit()

    print("Total updates: %s" % updates)
