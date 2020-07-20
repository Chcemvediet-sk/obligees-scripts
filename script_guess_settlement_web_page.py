from sqlalchemy import or_

import database
from emails import get_mail_hosting_sites, get_emails_from_obligees, get_domains
from model import Obligee, Webpage

if __name__ == '__main__':
    session = database.session

    def guess_web_page(domain: str, hosting_sites):
        if domain not in hosting_sites:
            return domain
        else:
            return None

    def get_mail_hosting_sites_list(all_obligees):
        return get_mail_hosting_sites(get_emails_from_obligees(all_obligees))


    obligees = session.query(Obligee).filter(
        or_(
            Obligee.slug.like('obec-%'),
            Obligee.slug.like('mestska-cast-%'),
            Obligee.slug.like('mesto-%'),
        )
    )

    mail_hosting_sites = get_mail_hosting_sites_list(obligees.all())

    for obligee in obligees.all():
        not_mail_host_domains = set()
        for domain in get_domains(obligee.emails):
            if domain not in mail_hosting_sites:
                not_mail_host_domains.add(domain)
        if len(not_mail_host_domains) == 1:
            domain = not_mail_host_domains.pop()
            webpage = guess_web_page(domain, mail_hosting_sites)
            if webpage:
                session.add(Webpage(webpage=webpage, obligee=obligee))
                session.commit()
        elif len(not_mail_host_domains) == 0:
            pass
        elif len(not_mail_host_domains) > 1:
            print("Start: ")
            print('multiple domains, skipping')
            print(obligee.emails)
            print("...")
