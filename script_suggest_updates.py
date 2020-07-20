import cities
import database
from model import Obligee
from zip_code import get_official_zip, zip_equals, diff_severity


if __name__ == '__main__':
    session = database.session
    updates = 0

    for city in cities.cities():
        has_output = False

        try:
            if city.name:
                for obligee in session.query(Obligee).filter(
                        Obligee.name.ilike(city.name)
                ):
                    print(obligee.zip)
                    print(city.adresa_uradu_psc)
                    if not zip_equals(obligee.zip.decode(), city.adresa_uradu_psc):
                        """
                        If ZIP codes differ, we cannot blindly add any email
                        address to the database.
                        """
                        zip_diff_severity = diff_severity(obligee.zip, city.adresa_uradu_psc)
                        print(zip_diff_severity)

                        print("ZIP code of '%s' (DB ID:%s) is (%s) but in input"
                              "file it is (%s)\nName: (%s) (%s)" %
                              (
                                  obligee.name,
                                  obligee.id,
                                  obligee.zip,
                                  city.adresa_uradu_psc,
                                  obligee.name,
                                  city.nazov_obce,
                              ))
                        official_zip = get_official_zip(
                            "%s, %s" % (
                                obligee.street,
                                obligee.city
                            ))
                        if official_zip:
                            print("Official ZIP query result: ", official_zip)
                        has_output = True
                    else:
                        if city.email not in obligee.emails and False:
                            updates += 1
                            print("\t\tAdd email (%s) to %s<ID:%s> (%s)" % (
                                city.email,
                                obligee.name,
                                obligee.id,
                                obligee.emails
                            ))
                            has_output = True

            if has_output:
                print("-" * 72)
        except ValueError as e:
            print(e, city)

    print("Total suggested updates: %s" % updates)
