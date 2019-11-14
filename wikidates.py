import sys
import io
import calendar
import argparse
from mediawiki import MediaWiki

wikipedia = MediaWiki()


def parse_cli():
    cli_parser = argparse.ArgumentParser(
        prog="wikidates.py",
        description="""Scrape a historical fact from Wikipedia for every date of the year""",
    )
    cli_parser.add_argument("-o", "--output",
                            help="path to the output file")

    cli_parser.add_argument("-q", "--quiet", action="store_true",
                            help="enable quiet mode (no info about scrapped dates)")
    return cli_parser.parse_args()


def all_dates_in_year(year=2020):
    fun_facts = list()

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
    return fun_facts


if __name__ == "__main__":
    args = parse_cli()

    if args.quiet:
        text_trap = io.StringIO()
        sys.stdout = text_trap

    fun_facts = all_dates_in_year()
    sys.stdout = sys.__stdout__

    if args.output:
        with open(args.output, "w+") as out:
            for fact in fun_facts:
                out.write(fact + "\n")
    else:
        for fact in fun_facts:
            print(fact)