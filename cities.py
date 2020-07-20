import json
from enum import Enum


def as_python():
    with open("input/cities.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def regions(dictionary):
    for region in dictionary.keys():
        yield region


def cities():
    dictionary = as_python()

    for region_name, districts in dictionary.items():
        for district_name, _cities in districts.items():
            for city in _cities.values():
                yield SettlementFactory.create(
                    data=city,
                    district=district_name,
                    region=region_name,
                )


class Gender(Enum):
    MASCULINE = 1
    FEMININE = 2
    NEUTER = 3
    PLURAL = 4


class SettlementType(Enum):
    MESTO = 1
    OBEC = 2
    MESTSKA_CAST = 3
    VOJENSKY = 4


class SettlementFactory(object):
    @staticmethod
    def create(data, **kwargs):
        typ_uradu = data[0].lower()
        if typ_uradu.startswith('mestský úrad'):
            return Mesto(data, **kwargs)
        if typ_uradu.startswith('obecný úrad'):
            return Obec(data, **kwargs)
        if typ_uradu.startswith('miestny úrad'):
            return MestskaCast(data, **kwargs)

        return None


class Settlement(object):
    def __init__(self, data, district=None, region=None):
        self.typ_uradu: str = data[0]
        self.typ_uradu_riadok2 = data[1]
        self.adresa_uradu_ulica = data[2]
        self.adresa_uradu_cislo_domu = data[3]
        self.adresa_uradu_psc = data[4]
        self.adresa_uradu_mesto = data[5]
        self.email = data[6]
        self.tel_predvolba = data[7]
        self.telefon = data[8]
        self.mobil = data[9]
        self.nazov_obce = data[10]
        self.potvrdene_udaje = data[11]
        self.alt_email_pre_preukaz = data[12]
        self.district = district
        self.region = region

    @property
    def name(self):
        return self.nazov_obce

    @property
    def name_with_district(self):
        return "%s (okr. %s)" % (self.name, self.district_short)

    @property
    def district_short(self):
        return self.district.replace("Okres ", "")

    @property
    def name_accusative(self):
        raise NotImplementedError()

    @property
    def name_dative(self):
        raise NotImplementedError()

    @property
    def name_genitive(self):
        raise NotImplementedError()

    @property
    def name_instrumental(self):
        raise NotImplementedError()

    @property
    def name_locative(self):
        raise NotImplementedError()

    @property
    def notes(self):
        return ''

    @property
    def official_description(self):
        raise NotImplementedError()

    @property
    def official_name(self):
        raise NotImplementedError()

    @property
    def simple_description(self):
        raise NotImplementedError()

    @property
    def type(self):
        return '1'

    @property
    def latitude(self):
        # TODO
        return None

    @property
    def longitude(self):
        # TODO
        return None

    @property
    def iczsj_id(self):
        # TODO
        return ''

    def __str__(self) -> str:
        return ", ".join([
            self.typ_uradu,
            self.typ_uradu_riadok2,
            self.adresa_uradu_ulica,
            self.adresa_uradu_cislo_domu,
            self.adresa_uradu_psc,
            self.adresa_uradu_mesto,
            self.email,
            self.tel_predvolba,
            self.telefon,
            self.mobil,
            self.nazov_obce,
            self.potvrdene_udaje,
            self.alt_email_pre_preukaz,
        ])

    def _declension(self, prefix):
        return '%s %s' % (prefix, self.nazov_obce)


class Mesto(Settlement):
    @property
    def name(self):
        return 'Mesto %s' % self.nazov_obce

    @property
    def gender(self):
        # TODO FIXME -- 'to mesto xy', 'ten mestský úrad xy'?
        return Gender.MASCULINE

    @property
    def name_accusative(self):
        return self._declension('Mesto')

    @property
    def name_dative(self):
        return self._declension('Mestu')

    @property
    def name_genitive(self):
        return self._declension('Mesta')

    @property
    def name_instrumental(self):
        return self._declension('Mestom')

    @property
    def name_locative(self):
        return self._declension('Meste')

    @property
    def official_description(self):
        return "Mesto zabezpečuje organizačné a administratívne veci " \
               "mestského zastupiteľstva a primátora, ako aj ďalších " \
               "zriadených orgánov mestského zastupiteľstva a plní úlohy " \
               "v zmysle zákona o obecnom zriadení."

    @property
    def official_name(self):
        return self.name

    @property
    def simple_description(self):
        return ''


class MestskaCast(Settlement):
    @property
    def name(self):
        return 'Mestská časť %s' % self.nazov_obce

    @property
    def gender(self):
        # TODO FIXME -- 'tá mestská časť xy', 'ten miestny úrad xy'?
        return Gender.FEMININE

    @property
    def name_accusative(self):
        return self._declension('Mestskú časť')

    @property
    def name_dative(self):
        return self._declension('Mestskej časti')

    @property
    def name_genitive(self):
        return self._declension('Mestskej časti')

    @property
    def name_instrumental(self):
        return self._declension('Mestskou časťou')

    @property
    def name_locative(self):
        return self._declension('Mestskej časti')

    @property
    def official_description(self):
        """
        TODO Should be updated according the official definition.

        # Bratislava:
        Mestská časť je územným samosprávnym a správnym celkom Bratislavy;
        združuje obyvateľov, ktorí majú na jej území trvalý pobyt. Mestská časť
        vykonáva samosprávu Bratislavy a prenesenú pôsobnosť v rozsahu
        vymedzenom zákonom a štatútom Bratislavy (ďalej len „štatút"); v tomto
        rozsahu má postavenie obce
        (https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/1990/377/20200409)

        # Košice:
        Mestské časti sú právnické osoby, ktoré za podmienok ustanovených
        zákonom a štatútom mesta (ďalej len „štatút”) hospodária so zvereným a
        vlastným majetkom a so zverenými a vlastnými finančnými príjmami.
        Mestské časti vykonávajú samosprávu v rozsahu zverenom týmto zákonom a
        štatútom; vo zverenom rozsahu majú mestské časti postavenie obce.1)
        Mestské časti vykonávajú prenesený výkon štátnej správy v rozsahu
        vymedzenom zákonom;1a) v tomto rozsahu majú mestské časti postavenie
        obce.1)
        (https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/1990/401/20200409

        See also cities.Obec.official_description
        """
        return "Mestská časť je výkonným orgánom Miestneho zastupiteľstva, " \
               "nemá právnu subjektivitu."

    @property
    def official_name(self):
        return self.name

    @property
    def simple_description(self):
        """
        See also cities.Obec.simple_description
        """
        # TODO: update according to cities.MestskaCast.official_description
        return "Mestská časť je výkonným orgánom Miestneho zastupiteľstva, " \
               "nemá právnu subjektivitu."


class Obec(Settlement):
    @property
    def name(self):
        return 'Obec %s' % self.nazov_obce

    @property
    def gender(self):
        # TODO: FIXME -- 'tá obec xy', 'ten obecný úrad xy'?
        return Gender.MASCULINE

    @property
    def name_accusative(self):
        return self._declension('Obec')

    @property
    def name_dative(self):
        return self._declension('Obci')

    @property
    def name_genitive(self):
        return self._declension('Obci')

    @property
    def name_instrumental(self):
        return self._declension('Obcou')

    @property
    def name_locative(self):
        return self._declension('Obci')

    @property
    def official_description(self):
        return "Obec zabezpečuje organizačné a administratívne veci obecného " \
               "zastupiteľstva a starostu, ako aj orgánov " \
               "zriadených obecným zastupiteľstvom."

    @property
    def official_name(self):
        return self.name

    @property
    def simple_description(self):
        return "Obec je podateľňou a výpravňou písomnosti obce, vypracúva " \
               "písomné vyhotovenia rozhodnutí obce a vykonáva nariadenia, " \
               "uznesenia obecného zastupiteľstva a rozhodnutia obce"
