from slugify import slugify

import cities
import database
from model import Obligee, NewObligee

if __name__ == '__main__':
    session = database.session
    added = 0

    def get_city(a_city):
        def by_name_like(name):
            return session.query(Obligee).filter(Obligee.name.ilike(name))

        if by_name_like(a_city.name).count() == 0 and \
           by_name_like(a_city.name_with_district).count() == 0:
            return False
        return True

    def create_city(a_city):
        print("Unknown city from JSON data - create new, \n %s" % a_city)
        obj = NewObligee(
            name=a_city.name,
            street=" ".join([
                a_city.adresa_uradu_ulica,
                a_city.adresa_uradu_cislo_domu,
            ]).strip(),
            city=a_city.adresa_uradu_mesto,
            zip=a_city.adresa_uradu_psc,
            emails=a_city.email,
            slug=slugify(a_city.name),
            status=1,
            gender=a_city.gender.value,
            ico='',
            name_accusative=a_city.name_accusative,
            name_dative=a_city.name_dative,
            name_genitive=a_city.name_genitive,
            name_instrumental=a_city.name_instrumental,
            name_locative=a_city.name_locative,
            notes=a_city.notes,
            official_description=a_city.official_description,
            official_name=a_city.official_name,
            simple_description=a_city.simple_description,
            type=a_city.type,
            latitude=a_city.latitude,
            longitude=a_city.longitude,
            iczsj_id=a_city.iczsj_id,
        )
        session.add(obj)
        session.commit()
        print("-" * 70)

    for city in cities.cities():
        if city and city.name and not get_city(city):
            create_city(city)
            added += 1

    print("Added %s new objects" % added)
