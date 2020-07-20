def get_mail_hosting_sites(emails_occurrences_dict):
    sites = []
    for item in emails_occurrences_dict:
        occurrences = emails_occurrences_dict[item]
        if item and occurrences >= 2:
            sites.append(item)

    return tuple(sites)


def get_emails(cities_list):
    emails = {}
    for _city in cities_list:
        domain = get_domain(_city.email)
        current = emails.get(domain, 0)
        emails[domain] = current + 1

    return emails


def get_emails_from_obligees(obligees_list):
    emails = {}
    for obligee in obligees_list:
        domains = get_domains(obligee.emails)
        for domain in domains:
            current = emails.get(domain, 0)
            emails[domain] = current + 1
    return emails


def get_domains(emails):
    return {get_domain(email) for email in emails.decode('utf-8').split(',')}


def get_domain(email: str):
    return email[email.find("@") + 1:]
