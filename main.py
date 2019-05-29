import click
import text_conditioner
import os

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    db = text_conditioner.TextConditionDatabase()
    db.initdb()
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    os.remove('conditions.db')
    click.echo('Dropped the database')

@cli.command()
def selftest():
    db = text_conditioner.TextConditionDatabase()
    cons = db.get_all_conditions()
    for con in cons:
        if con.eval({}):
            print(con.repText)

if __name__ == '__main__':
    cli()
