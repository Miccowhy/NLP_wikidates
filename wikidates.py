import calendar
from mediawiki import MediaWiki

wikipedia = MediaWiki()

fun_facts = list()


def all_dates_in_year(year=2020):
    for month in range(1, 13): # Month is always 1..12
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            date = f'''{calendar.month_name[month]} {day}'''
            day_page = wikipedia.page(date, auto_suggest=False)
            try:
                event_section = day_page.section("Events").splitlines()[0]
            except IndexError:
                print(f"{date}: IndexError")
                if day_page.section("Events") == "":
                    event_section = day_page.section(
                        day_page.sections[
                            day_page.sections.index("Events") + 1])
            else:
                print(date)
            fun_facts.append(f'''{date}: {event_section}''')


if __name__ == "__main__":
    all_dates_in_year()
    with open("out.txt", "w+") as out:
        for fact in fun_facts:
            out.write(fact + "\n")
